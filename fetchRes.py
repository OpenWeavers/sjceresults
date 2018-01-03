from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
try:
    from Tkinter import *
    from ttk import *
except ImportError:  # Python 3
    from tkinter import *
    from tkinter.ttk import *


class App(Frame):

    def __init__(self, parent, temp):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable(temp)
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('subname', 'grade')

        tv.heading('#0', text='Subject Code', anchor='center')
        tv.column('#0', anchor='center', width=100)
        tv.heading('subname', text='Subject Name')
        tv.column('subname', anchor='center', width=100)
        tv.heading('grade', text='Grade')
        tv.column('grade', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self, temp):

        for i in temp:

            row = i.split(' ')
            self.treeview.insert('', 'end', text=row[0], values=(row[1:-1], row[-1]))


def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome("./chromedriver", chrome_options=options)
    '''
    try:
        #browser.client = webdriver.Chrome(chrome_options=options)
    except:
        pass
    '''
    try:
        while True:
            browser.get('http://sjce.ac.in/results/')
            delay = 5 # seconds
            usnField = browser.find_element_by_css_selector('#USN')
            usnField.click()
            print("Enter Your USN:")
            USN = input()
            usnRegex = re.compile('(4[jJ][cC][1][1-9]){1}([cC][sS]|[eE][cC]|[iI][sS]|[eE][eE]|[mM][eE]|[cC][vV]){1}([0-9]){3}')
            if usnRegex.match(USN):
                usnField.send_keys(usnRegex.match(USN).group())
                fetchBtn = browser.find_element_by_css_selector('body > div.container.container_12 > div > div > div > form > input[type="submit"]:nth-child(5)')
                fetchBtn.click()
                try:
                    test = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.container.container_12 > div > div > div > table')))
                    name = browser.find_element_by_css_selector('body > div.container.container_12 > div > div > div > center > h1')
                    table = browser.find_element_by_css_selector('body > div.container.container_12 > div > div > div > table')
                    tableList = table.text.split('\n')
                    root = Tk()
                    root.title(name.text.split(":")[1])
                    App(root, tableList[1:])
                    root.mainloop()
                except TimeoutException:
                    print("Busy!")
            else:
                print('Invalid USN!')

    except KeyboardInterrupt:
        print("Bye!")
        pass


if __name__ == '__main__':
    main()
