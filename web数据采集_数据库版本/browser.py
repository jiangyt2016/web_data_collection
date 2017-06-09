from selenium import webdriver
import log
from Tkinter import END

g_driver = None

def open_browser(browser, listbox):
    res = True
    driver = None
    
    if browser == "Chrome":
        driver = webdriver.Chrome()
    elif browser == "Firefox":
        driver = webdriver.Firefox()
    else:
        res = False
    
    return res, driver
    

def test(url, listbox):
    browser = [ "Chrome"]#, "Firefox"]
    res = False
    driver = None
    try:
        for i in browser:
            res, driver = open_browser(i, listbox)
            if res:
                break
        if res == False:
            return False, None
        driver.get(url)
        perf_time = driver.execute_script("return window.performance.timing")
        entry_time = driver.execute_script("return window.performance.getEntries()")
    except Exception, e:
        listbox.insert(END,"error:" + str(e))
        listbox.see(END)
        return False, None

    global g_driver
    g_driver = driver
    #driver.close()
    #driver.quit()
    return True, (perf_time, entry_time)


def close_browser():
    global g_driver
    if g_driver == None:
        pass
    else:
        try:
            g_driver.close()
            g_driver.quit()
            g_driver = None
        except Exception, reason:
            print reason
            g_driver = None


    
