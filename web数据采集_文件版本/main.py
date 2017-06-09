from Tkinter import *
import log
import config
import browser
import url
import save
import subprocess
import threading
import Queue
import dns

class Main():
    def __init__(self):
        self.root = None
        self.text_frame = None
        self.list_frame = None
        self.next_botton = None
        self.scrollbar = None
        self.score_entry = None
        self.listbox = None
        self.label = None
        self.logger = log.get_logger()
        self.confger = config.Config()
        self.url = url.URL(self.confger.url_file)
        self.index = 0
        self.saver = save.Save(self.confger.result_file)
        self.cur_url = None
        self.save_button = None
        self.queue = Queue.Queue()
        self.running = False
        self.prefix = "..."

    def main(self):
        self.root = Tk()
        self.root.title("web performance collection")
        w = 600
        h = 400
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.root.geometry('%dx%d+%d+%d' %(w, h, x, y))

        self.text_frame = Frame(self.root)
        self.list_frame = Frame(self.root)

        self.next_button = Button(self.text_frame, text="run test", command = self.run_test, width = 10, height = 1)
        self.save_button = Button(self.text_frame, text="save score", command = self.save_score, width = 10, height = 1)
        self.score_entry = Entry(self.text_frame, width = 30)
        self.score_entry.bind("<Return>", self.return_event)
        self.scrollbar = Scrollbar(self.list_frame, orient = VERTICAL)
        self.listbox = Listbox(self.list_frame, yscrollcommand = self.scrollbar.set, height = 16)
        self.scrollbar.configure(command = self.listbox.yview)
        self.label = Label(self.text_frame, text = "input score:", height = 3, width = 30)

        
        self.list_frame.pack(side = TOP, fill = X)
        self.text_frame.pack(side = BOTTOM, fill = X)


        self.label.grid(row = 0, column = 0)
        self.score_entry.grid(row = 0, column = 1)
        self.next_button.grid(row = 1, column = 1, pady = 5)
        self.save_button.grid(row = 1, column = 0)
        self.save_button.config(state = "disabled")

        self.listbox.pack(side = LEFT, fill = BOTH, expand = 1)
        self.scrollbar.pack(side = RIGHT, fill = Y)

        self.index += 1
        url_flag, url = self.url.get_next()
        if url_flag == False:
            self.list_insert(self.prefix + "get url fail!")
        elif url == None:
            self.list_insert(self.prefix + "no next url, test done!")

        self.list_insert(str(self.index) + ".test:" + url)
        self.list_insert(self.prefix + "click run, run test!")
        self.cur_url = url

        self.root.mainloop()

    def save_score(self):
        score = 0
        try:
            score = int(self.score_entry.get())
        except Exception, reason:
            self.list_insert(reason)
            self.list_insert(self.prefix + "score not legal, input again!")
            return
        else:
            if score > 100 or score < 0:
                self.list_insert(self.prefix + "score must in 0-100, input again!")
                return
            else:
                self.save_button.config(state = "disabled")

        save_flag = self.saver.save(self.cur_url, self.res, score)
        if save_flag:
            self.list_insert(self.prefix + "save success!")
        else:
            self.list_insert(self.prefix + "save fail!")

        self.list_insert(self.prefix + "click run, run test!")

        self.index += 1
        url_flag, url = self.url.get_next()
        if url_flag == False:
            self.list_insert(self.prefix + "get url fail!")
        elif url == None:
            self.list_insert(self.prefix + "no next url, test done!")
            return
        self.list_insert(str(self.index) + ".test:" + url)
        self.cur_url = url

        self.next_button.config(state = "normal")

    def run_test(self):
        #self.listbox.insert(END, "button pressed")
        browser.close_browser()
        if self.cur_url == None:
            self.next_botton.config(state = "disabled")
            return
        
        self.list_insert(self.prefix + "clear dns caches...")
        res = dns.clear_dns()
        if res:
            self.list_insert(self.prefix + "dns clear success")
        else:
            self.list_insert(self.prefix + "dns clear fail, click test")
            return


        self.score_entry.delete(0, END)
        self.period_call()
        self.root.iconify()
        self.next_button.config(state = "disabled")
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
                    end_flag = True
                else:
                    com = msg.split("=")
                    if com[0] == "list":
                        self.list_insert(com[1])
                    elif com[0] == "button":
                        if com[1] == "test":
                            self.next_botton.config(state = "normal")
                        else:
                            self.save_button.config(state = "normal")
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
        test_flag, self.res = browser.test(self.cur_url, self.listbox)
        if test_flag == False:
            self.queue.put("list " + self.prefix + "test " + self.cur_url + " fail!")
            self.queue.put("button test")
            self.queue.put("end")
            #self.next_botton.config(state = "normal")
            return
        else:
            self.queue.put("list=" + self.prefix + "test " + self.cur_url + " success!")
        self.queue.put("list=" + self.prefix + "please input the score according to your own feeling(0-100)!")    
        self.queue.put("button=save")
        #self.save_button.config(state = "normal")
        #self.root.wm_attributes('-topmost',1)
        #self.root.deiconify()
        #self.root.lift()
        self.queue.put("root")
        self.queue.put("end")

    def list_insert(self, txt):
        self.listbox.insert(END, txt)
        self.listbox.see(END)

    def return_event(self, event):
        self.next()
      

if __name__ == '__main__':
    m = Main()
    m.main()