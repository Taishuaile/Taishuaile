from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import filedialog
hot = []
filepath = 'C:/Users/李朋泰/Desktop/happy/hot.txt'
f = open(filepath, 'r')
for i in f:
    hot.append(i.replace('\n', ''))
ori_hot = []
for i in hot:
    ori_hot.append(i)

board = ''
target = ''
nums = ''
select = ''
result = []
url = []
driver = ''
PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chromedriver'

#點選上一頁
def presslastpage():
    global driver
    s = driver.find_elements(By.CLASS_NAME, 'btn')
    for i in s:
        if '上頁' in i.text:
            i.click()
            break


def search():
    global board
    global target
    global nums
    global select
    board = boardtk.get()
    target = targettk.get()
    target = target.split()
    nums = numstk.get()
    if len(selecttk.get()) != 0:
        select = selecttk.get().split()[0]
    #win.destroy()
    #print(board, target, nums, select)
    work()


def searchbyenter(event):
    global board
    global target
    global nums
    global select
    board = boardtk.get()
    target = targettk.get()
    target = target.split()
    nums = numstk.get()
    select = selecttk.get()
    if len(selecttk.get()) != 0:
        select = selecttk.get().split()[0]
    #win.destroy()
    #print(board, target, nums, select)
    work()

def check(event):
    a = boardtk.get()
    global hot
    #print(a)
    #print(len(hot))
    if len(a) > 0:
        for i in range(len(hot)):
            if a.casefold() not in hot[i].casefold():
                hot[i] = ''
        while '' in hot:
            hot.remove('')
        comboExample = ttk.Combobox(win, values=hot, textvariable=selecttk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=3, sticky="W", padx=10)
    else:
        #print(ori_hot)
        hot = []
        for i in ori_hot:
            hot.append(i)
        #print(hot)
        comboExample = ttk.Combobox(win, values=ori_hot, textvariable=selecttk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=3, sticky="W", padx=10)


def gourl():
    print(paask1['text'])


def work():
    global nums
    time_start = time.time() #開始計時
    #判斷輸入值
    if nums == '全部' or nums == 'all' or nums == 'All' or nums == 'ALL':
        nums = 9999
        real_nums = int(nums)
    elif len(target) > 1:
        real_nums = int(nums)
        nums = 9999
    else:
        real_nums = int(nums)
        nums = int(nums)

    #路徑和造訪網站
    global PATH
    if select != '':
        dist = 'https://www.ptt.cc/bbs/'+select+'/index.html'
    else:
        dist = 'https://www.ptt.cc/bbs/'+board+'/index.html'
    global driver
    driver = webdriver.Chrome(PATH)
    driver.get(dist)

    #若18歲看板
    if 'ask/over18?' in driver.current_url:
        s = driver.find_element(By.CLASS_NAME, "over18-button-container")
        s.click()

    #搜尋
    s = driver.find_element(By.CLASS_NAME, "query")
    s.clear()
    s.send_keys(target[0])
    s.send_keys(Keys.RETURN)
    # Xpath =//tagname[@Attribute=’value’]
    a = [] #儲存網址
    b = [] #儲存標題文字
    num = 0 #已存到幾筆資料
    while num < nums:
        s = driver.find_elements(By.XPATH, "//a[@href]")
        for i in s:
            if ".html" in i.get_attribute('href') and "/M." in i.get_attribute('href'):
                for j in target:
                    if j not in i.text:
                        if i in s:
                            s.remove(i)
        for i in s:
            if ".html" in i.get_attribute('href') and "/M." in i.get_attribute('href'):
                a.append(i.get_attribute('href'))
                b.append(i.text)
                num += 1
                if num == real_nums:
                    break
        if num >= real_nums:
            break
        m = driver.find_elements(By.CLASS_NAME, 'disabled')
        for i in m:
            if '上頁' in i.text:
                num = 99999
        if num < nums:
            presslastpage()
    driver.quit()

    filepath = 'C:/Users/李朋泰/Desktop/happy/txt.txt'
    f = open(filepath, 'w')
    global result
    for i in range(len(a)):
        result.append(b[i])
        result.append(a[i])
        print(b[i], file=f)
        print(a[i], file=f)
    print(len(result))
    count = '有'+str(len(a))+'筆資料'
    print(count)

    # 計時
    time_end = time.time()    #結束計時
    time_c = round(time_end - time_start, 3)   #執行所花時間
    t_cost = '共花費'+str(time_c)+'秒'
    print('time cost', time_c, 's')
    print('time cost', time_c, 's', file=f)
    f.close()
    passk = tk.Label(win, width=20, text=count, font=tkFont.Font(family='consolas', size=20), bg='red').grid(column=0, row=10, sticky="W", padx=10)#使用者輸入框
    passk = tk.Label(win, width=20, text=t_cost, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=11, sticky="W", padx=10)#使用者輸入框
    #time.sleep(3)
    #win.destroy()
    return 0


win=tk.Tk()
win.title("登入")
win.geometry('550x550')
#win.resizable(width=0, height=0)

boardtk = tk.StringVar()
targettk = tk.StringVar()
numstk = tk.StringVar()
selecttk = tk.StringVar()

userlabel = tk.Label(win,text="要搜尋的看板:", font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=0, sticky="W", padx=10)
userkeyin = tk.Entry(win, width=20,textvariable=boardtk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=1, sticky="W", padx=10)#使用者輸入框
win.bind("<Motion>", check)

combolabel = tk.Label(win,text="或使用選單:", font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=2, sticky="W", padx=10)
comboExample = ttk.Combobox(win, values=hot, textvariable=selecttk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=3, sticky="W", padx=10)

passlabel = tk.Label(win,text="要搜尋的關鍵字:", font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=4, sticky="w", padx=10)
passkeyin = tk.Entry(win, width=20, textvariable=targettk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=5, sticky="W", padx=10)#使用者輸入框

passlabel = tk.Label(win,text="要搜尋幾筆資料?(全部請打全部或all):", font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=6, sticky="w", padx=10)
passkeyin = tk.Entry(win, width=20, textvariable=numstk, font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=7, sticky="W", padx=10)#使用者輸入框


login = tk.Button(win, text="搜尋", font=tkFont.Font(family='consolas', size=20), width=15, height=2, command=search)
login.grid(column=0, row=8, sticky="w", padx=10, pady=10)
win.bind("<Return>", searchbyenter)


passla = tk.Label(win,text="搜尋結果:", font=tkFont.Font(family='consolas', size=20)).grid(column=0, row=9, sticky="w", padx=10)
passk = tk.Label(win, width=20, text=result, font=tkFont.Font(family='consolas', size=15)).grid(column=0, row=10, sticky="W", padx=10)#使用者輸入框

# image = Image.open('C:/Users/李朋泰/Desktop/happy/123.gif')
# image = image.resize((600, 750), Image.ANTIALIAS)
# image1 = ImageTk.PhotoImage(image)
# gif = tk.Label(win, text='AV女優', image=image1).grid(column=1, row=15, sticky='W', padx=10)
file_path = filedialog.askdirectory()
print(file_path)


win.mainloop()


