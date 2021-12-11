''' A simple tkinter application
which let you to see how much you erned and how 
much you spend.
'''

#! /usr/bin/python

import sqlite3
import datetime
import os

from tkinter import *
from tkinter import ttk

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'img')

class Daxl:

    def __init__(self, master):
        self.master = master
        self.main_frame = ttk.Frame(self.master)
        self.today = datetime.date.today()
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.master.title("Daxl")
        self.master.geometry("600x400")
        self.master.resizable(width=False, height=False)
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # connect to the db
        self.conn = sqlite3.connect('daxl.db')
        self.c = self.conn.cursor()

        self.main_frame.grid(row=0, column=0, sticky=(W, E, S, N))
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.side_frame = ttk.Frame(self.main_frame, relief='solid', padding=5)

        self.header_ui()
        self.side_ui()

        # body frames
        self.wallet_frame = ttk.Frame(self.main_frame)
        self.spend_frame = ttk.Frame(self.main_frame)
        self.chart_frame = ttk.Frame(self.main_frame)
        self.report_frame = ttk.Frame(self.main_frame)
        self.wallet_report_frame = ttk.Frame(self.report_frame, padding=5)
        self.spends_report_frame = ttk.Frame(self.report_frame, padding=5)

        self.chart_ui()  # initial first seen
        self.balance()   # calculate and display balance

    def header_ui(self):
        color = '#3498db'
        f_color = '#ecf0f1'

        header_frame = ttk.Frame(self.main_frame, padding=(500, 0, 0, 0))

        balance_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'Coins.png'))
        self.balance_label = ttk.Label(header_frame, text='Money', image=balance_image, compound='left')
        self.balance_label.img = balance_image

        self.balance_label.grid(row=0, column=0)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(E, N))

        # style configuration
        self.style.configure('header.TFrame', background=color)
        self.style.configure('main.TFrame', background='#ffffff')
        self.style.configure('header.TLabel', background=color, foreground=f_color, font=('Ubuntu', 14))
        # applying the style
        header_frame.config(style='header.TFrame')
        self.balance_label.config(style='header.TLabel')
        self.main_frame.config(style='main.TFrame')

    def side_ui(self):
        color = '#2c3e50'
        f_color = '#cccccc'
        h_color = '#243342'

        # init wallet icon
        wallet_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'wallet1.png'))
        self.wallet_label = ttk.Label(self.side_frame, text="Wallet", image=wallet_image, compound='left')
        self.wallet_label.img = wallet_image
        # call wallet_ui when click on its icon
        self.wallet_label.grid(row=0, column=0)
        self.wallet_label.bind("<Button-1>", self.wallet)

        # spend
        spend_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'spend1.png'))
        self.spend_label = ttk.Label(self.side_frame, text="Spend", image=spend_image, compound='left')
        self.spend_label.img = spend_image
        self.spend_label.grid(row=1, column=0)
        self.spend_label.bind("<Button-1>", self.spend_ui)

        # chart
        chart_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'chart1.png'))
        self.chart_label = ttk.Label(self.side_frame, text='Chart', image=chart_image, compound='left')
        self.chart_label.img = chart_image
        self.chart_label.grid(row=2, column=0)
        self.chart_label.bind("<Button-1>", self.chart_ui)

        report_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'report1.png'))
        self.report_label = ttk.Label(self.side_frame, text='Report', image=report_image, compound='left')
        self.report_label.img = report_image
        self.report_label.grid(row=3, column=0)
        self.report_label.bind("<Button-1>", self.report)

        # grid side frame
        self.side_frame.grid(row=1, column=0, sticky=(W, N, S))
        # self.side_frame.grid_columnconfigure(0, weight=1)

        # Adding some configuration for all sidebar widgets
        for child in self.side_frame.winfo_children():
            if child.widgetName == 'ttk::label':
                child.grid_configure(pady=5, ipady=5, ipadx=10, sticky='we')

        # style configuration
        self.style.configure('side.TFrame', background=color)
        self.style.configure('side.TLabel', background=color, foreground=f_color, font='Ubuntu')
        # applying the style
        self.side_frame.config(style='side.TFrame')
        self.wallet_label.config(style='side.TLabel')
        self.spend_label.config(style='side.TLabel')
        self.chart_label.config(style='side.TLabel')
        self.report_label.config(style='side.TLabel')
        # changing background color of side bar pictures on hover
        self.style.map('side.TLabel', 
                        background=[('hover', '#78909C')], 
                        foreground=[('hover', '#212121')])

        # Hover event for sidebar pictures.
        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.spend_label.bind('<Enter>', lambda e: self.on_hover(e, 'spend'))
        self.chart_label.bind('<Enter>', lambda e: self.on_hover(e, 'chart'))
        self.report_label.bind('<Enter>', lambda e: self.on_hover(e, 'report'))

        # Leave event for sidebar pictures
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        self.spend_label.bind('<Leave>', lambda e: self.on_leave(e, 'spend'))
        self.chart_label.bind('<Leave>', lambda e: self.on_leave(e, 'chart'))
        self.report_label.bind('<Leave>', lambda e: self.on_leave(e, 'report'))

    def on_hover(self, event, image):
        ''' Change sidebar picture(label) backround when 
            mouse point hover on it. 
        '''
        print(image)
        img2 = PhotoImage(file=os.path.join(IMAGE_DIR, f'{image}2.png'))
        event.widget.configure(image=img2)
        event.widget.img2 = img2

    def on_leave(self, event, image):
        ''' Change sidebar picture(label) backround when 
            mouse leave the widget area. 
        '''
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'{image}1.png'))
        event.widget.configure(image=img1)
        event.widget.img1 = img1

    def sidebar_enhence(self, widget):
        color1 = '#CFD8DC'
        color2 = '#212121'
        back_color = '#2c3e50'
        front_color = '#cccccc'
        widgets = {
            'wallet':self.wallet_label, 
            'spend': self.spend_label,
            'chart': self.chart_label, 
            'report': self.report_label
        }
        images = ['wallet', 'spend', 'chart', 'report']

        widgets[widget].configure(background=color1, foreground=color2)
        widgets[widget].unbind('<Enter>')
        widgets[widget].unbind('<Leave>')
        # del widgets[widget]

        for w in widgets.values():
            w.configure(background=back_color, foreground=front_color)

        images.remove(widget)

        print(widgets)

        for image in images:
            print(image)
            img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'{image}1.png'))
            widgets[image].configure(image=img1)
            widgets[image].img1 = img1
            widgets[image].bind('<Enter>', lambda e: self.on_hover(e, image))
            widgets[image].bind('<Leave>', lambda e: self.on_leave(e, image))
            
       

    def wallet(self, event):
        # self.sidebar_enhence('wallet')
        # self.sidebar_enhence(self.wallet)
        self.wallet_label.configure(background='#CFD8DC', foreground='#212121')
        self.spend_label.configure(background='#2c3e50', foreground='#cccccc')
        self.chart_label.configure(background='#2c3e50', foreground='#cccccc')
        self.report_label.configure(background='#2c3e50', foreground='#cccccc')

        self.wallet_label.unbind('<Enter>')
        self.wallet_label.unbind('<Leave>')

        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'spend1.png'))
        self.spend_label.configure(image=img1)
        self.spend_label.img1 = img1
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'chart1.png'))
        self.chart_label.configure(image=img1)
        self.chart_label.img1 = img1
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'report1.png'))
        self.report_label.configure(image=img1)
        self.report_label.img1 = img1

        self.spend_label.bind('<Enter>', lambda e: self.on_hover(e, 'spend'))
        self.spend_label.bind('<Leave>', lambda e: self.on_leave(e, 'spend'))
        self.chart_label.bind('<Enter>', lambda e: self.on_hover(e, 'chart'))
        self.chart_label.bind('<Leave>', lambda e: self.on_leave(e, 'chart'))
        self.report_label.bind('<Enter>', lambda e: self.on_hover(e, 'report'))
        self.report_label.bind('<Leave>', lambda e: self.on_leave(e, 'report'))

        jobs = self.c.execute("SELECT (JobName) FROM Jobs").fetchall()

        self.spend_frame.grid_forget()
        self.chart_frame.grid_forget()
        self.report_frame.grid_forget()

        title_label = ttk.Label(self.wallet_frame, text="Refill Your Wallet")

        ttk.Label(self.wallet_frame, text="Categories: ").grid(row=1, column=0)
        self.jobs_var = StringVar()
        jobs_group = ttk.Combobox(self.wallet_frame, values=jobs, textvariable=self.jobs_var)
        jobs_group.insert(0, jobs[0])
        plus_button = ttk.Button(self.wallet_frame, text="+", command=lambda: self.add_category_ui('wallet'))

        ttk.Label(self.wallet_frame, text="Amount").grid(row=2, column=0)
        ttk.Label(self.wallet_frame, text="Description").grid(row=3, column=0)
        self.money = ttk.Entry(self.wallet_frame)
        save_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'Save.png'))
        save = ttk.Button(self.wallet_frame, text="Save", compound='left',
                          image=save_image, command=self.wallet_save)
        save.img = save_image
        self.desc = ttk.Entry(self.wallet_frame)

        title_label.grid(row=0, column=1)
        jobs_group.grid(row=1, column=1)
        self.money.grid(row=2, column=1)
        self.desc.grid(row=3, column=1)
        save.grid(row=4, column=1)
        plus_button.grid(row=1, column=2)
        # grid wallet frame
        self.wallet_frame.grid(row=1, column=1)

        for child in self.wallet_frame.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky=(W, E))

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff', font=('Open Sans', 10))
        self.style.configure('title.TLabel', font=('Open Sans', 14, 'bold'))
        self.style.configure('save.TButton', justify='left')
        # applying style
        self.wallet_frame.config(style='wallet.TFrame')
        title_label.config(style='title.TLabel')
        save.config(style='save.TButton')

    def spend_ui(self, event):
        # self.sidebar_enhence('spend')
        self.wallet_label.configure(background='#2c3e50', foreground='#cccccc')
        self.spend_label.configure(background='#CFD8DC', foreground='#212121')
        self.chart_label.configure(background='#2c3e50', foreground='#cccccc')
        self.report_label.configure(background='#2c3e50', foreground='#cccccc')

        self.spend_label.unbind('<Enter>')
        self.spend_label.unbind('<Leave>')

        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'wallet1.png'))
        self.wallet_label.configure(image=img1)
        self.wallet_label.img1 = img1
        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'chart1.png'))
        self.chart_label.configure(image=img1)
        self.chart_label.img1 = img1
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'report1.png'))
        self.report_label.configure(image=img1)
        self.report_label.img1 = img1

        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        self.chart_label.bind('<Enter>', lambda e: self.on_hover(e, 'chart'))
        self.chart_label.bind('<Leave>', lambda e: self.on_leave(e, 'chart'))
        self.report_label.bind('<Enter>', lambda e: self.on_hover(e, 'report'))
        self.report_label.bind('<Leave>', lambda e: self.on_leave(e, 'report'))


        title = self.c.execute("SELECT (SpendTitle) FROM SpendGroup").fetchall()

        self.wallet_frame.grid_forget()
        self.chart_frame.grid_forget()
        self.report_frame.grid_forget()

        self.style.configure('ts.TLabel', font=('Open Sans', 14, 'bold'))

        ttk.Label(self.spend_frame, text='For what & how much?', style='ts.TLabel').grid(row=0, column=1)
        ttk.Label(self.spend_frame, text='Title').grid(row=1, column=0)
        ttk.Label(self.spend_frame, text="Amount").grid(row=2, column=0)
        ttk.Label(self.spend_frame, text="Description").grid(row=3, column=0)

        self.spend_title_var = StringVar()
        spend_title = ttk.Combobox(self.spend_frame, textvariable=self.spend_title_var, values=title)
        spend_title.insert(0, title[0])
        category = ttk.Button(self.spend_frame, text='+', command=lambda: self.add_category_ui('spend'))

        self.spend_money = ttk.Entry(self.spend_frame)

        save_image = PhotoImage(file=os.path.join(IMAGE_DIR, 'Save.png'))
        spend_save = ttk.Button(self.spend_frame, text="Save", image=save_image, compound='left',
                                command=self.spend_save)
        spend_save.img = save_image

        self.spend_desc = ttk.Entry(self.spend_frame)

        spend_title.grid(row=1, column=1)
        category.grid(row=1, column=2)
        self.spend_money.grid(row=2, column=1)
        self.spend_desc.grid(row=3, column=1)
        spend_save.grid(row=4, column=1)
        self.spend_frame.grid(row=1, column=1)

        for child in self.spend_frame.winfo_children():
            child.grid_configure(padx=5, pady=5, sticky=(W, E))

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff')
        # applying style
        self.spend_frame.config(style='wallet.TFrame')

    def chart_ui(self, *event):
        # self.sidebar_enhence('chart')
        self.chart_label.configure(background='#CFD8DC', foreground='#212121')
        self.wallet_label.configure(background='#2c3e50', foreground='#cccccc')
        self.spend_label.configure(background='#2c3e50', foreground='#cccccc')
        self.report_label.configure(background='#2c3e50', foreground='#cccccc')

        self.chart_label.unbind('<Enter>')
        self.chart_label.unbind('<Leave>')

        img2 = PhotoImage(file=os.path.join(IMAGE_DIR, f'chart2.png'))
        self.chart_label.configure(image=img2)
        self.chart_label.img2 = img2

        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'wallet1.png'))
        self.wallet_label.configure(image=img1)
        self.wallet_label.img1 = img1
        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'spend1.png'))
        self.spend_label.configure(image=img1)
        self.spend_label.img1 = img1
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'report1.png'))
        self.report_label.configure(image=img1)
        self.report_label.img1 = img1

        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        self.spend_label.bind('<Enter>', lambda e: self.on_hover(e, 'spend'))
        self.spend_label.bind('<Leave>', lambda e: self.on_leave(e, 'spend'))
        self.report_label.bind('<Enter>', lambda e: self.on_hover(e, 'report'))
        self.report_label.bind('<Leave>', lambda e: self.on_leave(e, 'report'))

        self.wallet_frame.grid_forget()
        self.spend_frame.grid_forget()
        self.report_frame.grid_forget()

        canvas = Canvas(self.chart_frame, bg='white', highlightthickness=0)
        spend_value, spend_percent = self.calculate_percent()

        h_line = canvas.create_line(50, 30, 50, 230)
        v_line = canvas.create_line(50, 230, 350, 230)

        h_x1 = 45
        h_y1 = 30
        h_x2 = 50
        h_y2 = 30
        percent_text = '100'
        for i in range(10):
            text = canvas.create_text(h_x1-10, h_y1, text=percent_text)
            line = canvas.create_line(h_x1, h_y1, h_x2, h_y2)
            h_y1 += 20
            h_y2 += 20
            percent_text = int(percent_text)-10

        v_x1 = 110
        v_y1 = 230
        v_x2 = 110
        v_y2 = 235
        spends_text = ['Food', 'Tech', 'Family', 'Clothes', 'Edu']
        for i in range(5):
            text = canvas.create_text(v_x1, v_y1+10, text=spends_text[i])
            line = canvas.create_line(v_x1, v_y1, v_x2, v_y2)
            chart_line = canvas.create_line(v_x1, v_y1, v_x2, v_y2-spend_percent[spends_text[i]]*2,
                                            fill='blue', width=3)
            v_x1 += 50
            v_x2 += 50

        canvas.grid(row=0, column=0)
        self.chart_frame.grid(row=1, column=1)

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff')
        # applying style
        self.chart_frame.config(style='wallet.TFrame')

    def report(self, event):
        # self.sidebar_enhence('report')
        self.report_label.configure(background='#CFD8DC', foreground='#212121')
        self.spend_label.configure(background='#2c3e50', foreground='#cccccc')
        self.chart_label.configure(background='#2c3e50', foreground='#cccccc')
        self.wallet_label.configure(background='#2c3e50', foreground='#cccccc')

        self.report_label.unbind('<Enter>')
        self.report_label.unbind('<Leave>')

        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'wallet1.png'))
        self.wallet_label.configure(image=img1)
        self.wallet_label.img1 = img1
        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'spend1.png'))
        self.spend_label.configure(image=img1)
        self.spend_label.img1 = img1
        img1 = PhotoImage(file=os.path.join(IMAGE_DIR, f'chart1.png'))
        self.chart_label.configure(image=img1)
        self.chart_label.img1 = img1

        self.wallet_label.bind('<Enter>', lambda e: self.on_hover(e, 'wallet'))
        self.wallet_label.bind('<Leave>', lambda e: self.on_leave(e, 'wallet'))
        self.spend_label.bind('<Enter>', lambda e: self.on_hover(e, 'spend'))
        self.spend_label.bind('<Leave>', lambda e: self.on_leave(e, 'spend'))
        self.chart_label.bind('<Enter>', lambda e: self.on_hover(e, 'chart'))
        self.chart_label.bind('<Leave>', lambda e: self.on_leave(e, 'chart'))

        self.wallet_frame.grid_forget()
        self.spend_frame.grid_forget()
        self.chart_frame.grid_forget()

        var = StringVar()
        r1 = ttk.Radiobutton(self.report_frame, text="Wallet Report",
                             variable=var, value='wallet', command=self.wallet_report)
        r2 = ttk.Radiobutton(self.report_frame, text="Spends Report",
                             variable=var, value='spends', command=self.spends_report)

        r1.grid(row=0, column=0, sticky=W)
        r2.grid(row=0, column=0, sticky=E)
        self.report_frame.grid(row=1, column=1)

        # run r1 event
        r1.invoke()

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff')
        # applying style
        self.report_frame.config(style='wallet.TFrame')

    def wallet_report(self):
        self.wallet_report_frame.grid_forget()
        self.spends_report_frame.grid_forget()

        data = self.c.execute("SELECT Date, JobName, Amount, Description FROM Wallet").fetchall()

        tree = ttk.Treeview(self.wallet_report_frame, columns=('title', 'amount', 'desc'))
        tree.column('title', width=50, anchor='w')
        tree.column('amount', width=100, anchor='center')
        tree.column('desc', width=200, anchor='w')
        tree.column('#0', width=100, anchor='w')

        tree.heading('#0', text='Date')
        tree.heading('title', text='Title')
        tree.heading('amount', text='Amount')
        tree.heading('desc', text='Description')
        # inserting data to tree.
        for i in data:
            tree.insert('', 'end', text=i[0], values=(i[1], i[2], i[3]))

        tree.grid(row=0, column=0)
        self.wallet_report_frame.grid(row=1, column=0)

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff')
        # applying style
        self.wallet_report_frame.config(style='wallet.TFrame')

    def spends_report(self):
        self.wallet_report_frame.grid_forget()

        data = self.c.execute("SELECT Date, SpendTitle, Amount, Description FROM Spend").fetchall()

        tree = ttk.Treeview(self.spends_report_frame, columns=('title', 'amount', 'desc'))
        tree.column('title', width=50, anchor='w')
        tree.column('amount', width=100, anchor='center')
        tree.column('desc', width=200, anchor='w')
        tree.column('#0', width=100, anchor='w')

        tree.heading('#0', text='Date')
        tree.heading('title', text='Title')
        tree.heading('amount', text='Amount')
        tree.heading('desc', text='Description')
        # inserting data to tree.
        for i in data:
            tree.insert('', 'end', text=i[0], values=(i[1], i[2], i[3]))

        tree.grid(row=0, column=0)
        self.spends_report_frame.grid(row=1, column=0)

        # style config
        self.style.configure('wallet.TFrame', background='#ffffff')
        self.style.configure('TLabel', background='#ffffff')
        # applying style
        self.spends_report_frame.config(style='wallet.TFrame')

    def calculate_percent(self):
        data = self.c.execute("SELECT SpendTitle, Amount FROM Spend").fetchall()
        total_spend = 0
        spends_title = [item[0] for item in data]
        spends_title_value = {title: 0 for title in spends_title}

        for item in data:
            total_spend += item[1]
            for title in spends_title_value:
                if item[0] == title:
                    spends_title_value[title] += item[1]

        spends_percent = {}
        for title in spends_title:
            percent = round(spends_title_value[title] * 100 / total_spend)
            spends_percent[title] = percent

        return spends_title_value, spends_percent

    def wallet_save(self):

        self.c.execute(
            """INSERT INTO Wallet(Date, JobName, Amount, Description)
                VALUES (?, ?, ?, ?)
            """, (self.today, self.jobs_var.get(), self.money.get(), self.desc.get())
        )
        self.conn.commit()

        self.money.delete(0, END)
        self.desc.delete(0, END)
        self.balance()

    def spend_save(self):
        self.c.execute(
            """INSERT INTO Spend(Date, SpendTitle, Amount, Description)
                VALUES (?, ?, ?, ?)
            """, (self.today, self.spend_title_var.get(), self.spend_money.get(), self.spend_desc.get())
        )
        self.conn.commit()
        self.spend_money.delete(0, END)
        self.spend_desc.delete(0, END)
        self.balance()

    def balance(self):
        wallet = 0
        spend = 0

        wallet_money = self.c.execute("SELECT (Amount) FROM Wallet").fetchall()
        spend_money = self.c.execute("SELECT (Amount) FROM Spend").fetchall()

        for w in wallet_money:
            wallet += w[0]

        for s in spend_money:
            spend += s[0]

        balance = wallet - spend
        print(balance)
        self.balance_label.config(text=str(balance))

    def add_category_ui(self, flag):
        window = Toplevel()
        frame = ttk.Frame(window)
        window.title("New Category")
        ttk.Label(frame, text='Category Name: ').grid(row=0, column=0)
        entry = ttk.Entry(frame)
        button = ttk.Button(frame, text='Add', command=lambda: self.add_category(entry, flag))

        entry.grid(row=0, column=1)
        button.grid(row=1, column=1)
        frame.grid(row=0, column=0)

        for child in frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
            

    def add_category(self, entry, flag):
        v = str(entry.get())

        if flag == 'wallet':
            self.c.execute("INSERT INTO Jobs (JobName, blob) VALUES (?, ?);", (v, 'blob'))
            self.conn.commit()
            entry.delete(0, END)

        if flag == 'spend':
            self.c.execute("INSERT INTO SpendGroup(SpendTitle, blob) VALUES (?, ?)", (v, 'blob'))
            self.conn.commit()
            entry.delete(0, END)
            self.conn.close()



root = Tk()
app = Daxl(root)
root.mainloop()
