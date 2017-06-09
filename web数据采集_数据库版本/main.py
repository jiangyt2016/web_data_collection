# -*- coding: utf-8 -*- 
from Tkinter import *
from ttk import *
import log
import config
import browser
import url
import save
import subprocess
import threading
import Queue
import dns
import db
import path

class Main():
    def __init__(self):
        path.add_path()
        self.root = None
        self.text_frame = None
        self.list_frame = None
        self.scrollbar = None
        self.listbox = None
        self.logger = log.get_logger()
        self.confger = config.Config()
        
        self.saver = save.Save(self.confger.result_file)
        self.cur_url = None
        self.kill_flag = False

        self.queue = Queue.Queue()
        self.running = False
        self.pausing = False
        self.prefix = "   "
        self.db_saver = db.DBSaver(self.confger.host, self.confger.user, self.confger.passwd,
            self.confger.db)

    def main(self):
        self.root = Tk()
        self.root.withdraw()
        self.root.title("web performance collection")
        self.root.iconbitmap('logo.ico')
        self.root.resizable(True, False)
        self.root.protocol("WM_DELETE_WINDOW", self.kill)
        self.root.wm_attributes('-topmost',1)
        w = 600
        h = 400
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry('%dx%d+%d+%d' %(w, h, x, y))

        self.text_frame = Frame(self.root, height = 100)
        self.list_frame = Frame(self.root, height = 300)

        self.run_button = Button(self.text_frame, text="run", command = self.run_test)#, width = 10, height = 1)
        self.pause_button = Button(self.text_frame, text="pause", command = self.pause_test)#, width = 10, height = 1)
        txt = "total:%d" %0
        self.url_total_label = Label(self.text_frame, text = txt)
        txt = "now:%d" %0
        self.url_left_label = Label(self.text_frame, text = txt)

        self.scrollbar = Scrollbar(self.list_frame, orient = VERTICAL)
        self.listbox = Listbox(self.list_frame, yscrollcommand = self.scrollbar.set
            ,height = 15, font = ("courier new", 12, ""))
        self.scrollbar.configure(command = self.listbox.yview)
        
        self.list_frame.pack(side = TOP, fill = X)
        self.text_frame.pack(side = BOTTOM, fill = X)
        self.list_frame.pack_propagate(0)
        self.text_frame.pack_propagate(0)
        
        #self.run_button.grid(row = 0, column = 0)
        self.run_button.place(in_ = self.text_frame, x= 100, y = 20)#, width = 50 , height = 50)
        self.pause_button.place(in_ = self.text_frame, x= 400, y = 20)#, width = 50 , height = 50)
        self.url_total_label.place(in_ = self.text_frame,x= 350,y = 75)#, width = 50 , height = 50)
        self.url_left_label.place(in_ = self.text_frame,x= 500,y = 75)#, width = 50 , height = 50)

        self.listbox.pack(side = LEFT, fill = BOTH, expand = 1)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.list_insert("tip:" + "click run button to run test!")
        self.pause_button.config(state = "disabled")

        self.root.update()
        self.root.deiconify()
        self.root.mainloop()

    def kill(self):
        #print "kill"

        self.kill_flag = True
        if self.running == False:
            self.root.destroy()
        elif self.pausing == True:
            self.list_insert("***process will be killed after the one test down!***")
            self.mutex.release()
            
            #self.root.destroy()
        else:
            self.list_insert("***process will be killed after the one test down!***")
            
        #self.root.destroy()

    def save_score(self):
        
        save_flag = self.saver.save(self.cur_url, self.res, 1)
        db_flag, e = self.db_saver.save(self.cur_url, self.res[0], self.res[1])
        
        if db_flag:
            self.list_insert(self.prefix + "save to database success!")
        else:
            self.list_insert(self.prefix + "save to database fail!")
            self.list_insert(self.prefix + str(e))

        if save_flag:
            self.list_insert(self.prefix + "save to file success!")
        else:
            self.list_insert(self.prefix + "save to file fail!")

    def pause_test(self):
        if self.pausing:
            self.pause_button.config(text = "pause")
            self.list_insert("   continue")
            self.pausing = False
            try:
                self.mutex.release()
            except:
                pass
        else:
            self.pause_button.config(text = "continue")
            self.list_insert("***pause after the current one down!***")
            self.pausing = True # pausing == true pause
            self.mutex.acquire()

    def run_test(self):
        # init
        self.mutex = threading.Lock()

        self.listbox.delete(0, END)
        self.url = url.URL(self.confger.url_file)
        count = self.url.get_count()
        txt = "total:%d" %count
        self.url_total_label.config(text = txt)

        self.running = True
        self.pausing = False
        self.index = 0
        txt = "now:%d" %0
        self.url_left_label.config(text = txt)

        browser.close_browser()
        
        self.run_button.config(state = "disabled")
        self.pause_button.config(state = "normal")
        self.pause_button.config(text = "pause")

        self.period_call()
        #self.root.iconify()
        # start work thread
        handle = threading.Thread(target = Main.run_thread, args=(self,))
        handle.setDaemon(True)
        handle.start()
    
    def period_call(self):
        msg = None
        end_flag = False
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                #print msg
                if msg == "end":
                    self.run_button.config(state = "normal")
                    self.pause_button.config(state = "disabled")
                    end_flag = True
                    self.running = False
                else:
                    com = msg.split("=")
                    if com[0] == "list":
                        self.list_insert(com[1])
                    elif com[0] == "label":
                        txt = "now:" + com[1]
                        self.url_left_label.config(text = txt)
                    else:
                        #print "topmost"
                        self.root.deiconify()
                        #self.root.lift()
                        #self.root.wm_attributes('-topmost',1)
            except Queue.Empty:
                pass
        if end_flag == False:
            self.root.after(200, self.period_call)

    def run_thread(self):
        while True:
            if self.kill_flag == True:
                self.running == False
                self.root.destroy()
                return
            self.mutex.acquire()
            self.mutex.release()
            if self.kill_flag == True:
                self.running == False
                self.root.destroy()
                return

            self.get_next_url()
            if self.cur_url == None:
                break
            clear_flag = self.clear_dns()
            if clear_flag == False:
                self.queue.put("list=" + "stop!")
                self.queue.put("end")
                return

            test_flag, self.res = browser.test(self.cur_url, self.listbox)
            browser.close_browser()

            if test_flag == False:
                self.queue.put("list=" + self.prefix + "test " + self.cur_url + " fail!")
                self.queue.put("list=" + "not close browser when testing or webdriver not in PATH")
                self.queue.put("list=" + "rerun or close")
                self.queue.put("end")
                
                #self.next_botton.config(state = "normal")
                return
            else:
                self.queue.put("list=" + self.prefix + "test " + self.cur_url + " success!")
                self.save_score()
                
                
        #self.save_button.config(state = "normal")
        #self.root.wm_attributes('-topmost',1)
        #self.root.deiconify()
        #self.root.lift()
        self.queue.put("end")
    
    def get_next_url(self):
        self.index += 1
        url_flag, url = self.url.get_next()
        if url_flag == False:
            self.queue.put("list=" + self.prefix + "get next url fail!")
            self.cur_url = None
            return
        elif url == None:
            self.queue.put("list=" + "***no next url, test completed!***")
            self.cur_url = None
            return
        self.queue.put("list=" + str(self.index) + ".test:" + url)
        self.queue.put("label=" + str(self.index))
        self.cur_url = url

    def clear_dns(self):
        self.queue.put("list=" + self.prefix + "clear dns caches")
        res = dns.clear_dns()
        if res:
            self.queue.put("list=" + self.prefix + "clear dns caches success!")
            return True
        else:
            self.queue.put("list=" + self.prefix + "clear dns caches fail!")
            return False

    def list_insert(self, txt):
        self.listbox.insert(END, txt)
        self.listbox.see(END)


if __name__ == '__main__':
    m = Main()
    m.main()