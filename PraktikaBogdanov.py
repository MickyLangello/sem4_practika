import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.otobrazit_zapisi()

    def init_main(self):

        self.mainmenu = tk.Menu(root)
        root.config(menu=self.mainmenu)

        self.searchmenu = tk.Menu(self.mainmenu, tearoff=0)
        self.searchmenu.add_command(label="Параметризированный запрос", command=self.open_search_dialog)
        self.searchmenu.add_command(label="Парам. запрос с группировкой", command=self.poisk_zapisi_Group)
        self.searchmenu.add_command(label="Запрос по двум таблицам", command=self.Search_Two_Table)
        self.searchmenu.add_command(label="Вернуть первую таблицу", command=self.otobrazit_zapisi)
        self.mainmenu.add_cascade(label="Запрос", menu=self.searchmenu)

        self.mb = tk.Menubutton(text="Режимы работы")
        self.mb.menu = tk.Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        self.mb.place(x=1, y=1)
        self.mb.menu.add_command(label="Добавить", command=self.open_dialog_winow)
        self.mb.menu.add_command(label="Редактировать", command=self.proverka_vibora_update)
        self.mb.menu.add_command(label="Удалить", command=self.proverka_vibora_delete)


        # show=headings скрывает нулевую колонку
        self.tree = ttk.Treeview(columns=('ID', 'instrument_name', 'instrument_Company', 'Instrument_Price', 'date_privoza'),
                                 height=17, show='headings')
        # anchor=tk.CENTER выравнивает по центру заголовок
        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('instrument_name', width=122, anchor=tk.CENTER)
        self.tree.column('instrument_Company', width=150, anchor=tk.CENTER)
        self.tree.column('Instrument_Price', width=120, anchor=tk.CENTER)
        self.tree.column('date_privoza', width=110, anchor=tk.CENTER)
        self.tree.heading('ID', text='ID')
        self.tree.heading('instrument_name', text='Инструмент')
        self.tree.heading('instrument_Company', text='Производитель')
        self.tree.heading('Instrument_Price', text='Цена')
        self.tree.heading('date_privoza', text='Дата привоза')
        self.tree.place(x=10, y=130)

        self.tree2 = ttk.Treeview(columns=('Company_Name', 'Company_Strana', 'Date_Founded'), height=3, show='headings')
        self.tree2.column('Company_Name', width=200, anchor=tk.CENTER)
        self.tree2.column('Company_Strana', width=105, anchor=tk.CENTER)
        self.tree2.column('Date_Founded', width=200, anchor=tk.CENTER)
        self.tree2.heading('Company_Name', text='Производитель')
        self.tree2.heading('Company_Strana', text='Страна')
        self.tree2.heading('Date_Founded', text='Дата основания')
        self.tree2.place(x=270, y=30)

        self.tree3 = ttk.Treeview(columns=('instrument_name', 'instrument_Price', 'Company_Name', 'Company_Strana'), height=17,
                                  show='headings')
        self.tree3.column('instrument_name', width=120, anchor=tk.CENTER)
        self.tree3.column('instrument_Price', width=150, anchor=tk.CENTER)
        self.tree3.column('Company_Name', width=115, anchor=tk.CENTER)
        self.tree3.column('Company_Strana', width=135, anchor=tk.CENTER)
        self.tree3.heading('instrument_name', text='Инструмент')
        self.tree3.heading('instrument_Price', text='Cтоимость')
        self.tree3.heading('Company_Name', text='Производитель')
        self.tree3.heading('Company_Strana', text='Страна производителя')
        self.tree3.place(x=570, y=130)

        self.Vibran_Zapis = []

    def proverka_vibora_update(self):
        try:
            self.Vibran_Zapis = self.tree.item(self.tree.selection()[0], option="values")
            self.Vibran_Zapis = self.Vibran_Zapis[1:]
            Redaktirovanie_Okno(app.Vibran_Zapis)
        except:
            mb.showerror("Ошибка", "Не выбрана запись!")

    def proverka_vibora_delete(self):
        try:
            self.Vibran_Zapis = self.tree.item(self.tree.selection()[0], option="values")
            self.Vibran_Zapis = self.Vibran_Zapis[1:]
            self.Open_Ask_Delete()
        except:
            mb.showerror("Ошибка", "Не выбрана запись!")


    def open_dialog_winow(*args):
        Vtoroe_Okno()

    def open_search_dialog(*args):
        Search()

    def otobrazit_zapisi(self):
        self.db.c.execute('''SELECT * FROM Instrument''')
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.c.fetchall():
            self.tree.insert('', 'end', values=row)

        self.db.c.execute('''SELECT * FROM CompanyTable''')
        for i in self.tree2.get_children():
            self.tree2.delete(i)
        for row in self.db.c.fetchall():
            self.tree2.insert('', 'end', values=row)

    def zapisi(self, instrument_name, instrument_Company, Instrument_Price, date_privoza):
        self.db.insert_data(instrument_name, instrument_Company, Instrument_Price, date_privoza)
        self.otobrazit_zapisi()

    def update_record(self, instrument_name, instrument_Company, Instrument_Price, date_privoza):
        self.db.c.execute(
            '''UPDATE Instrument SET instrument_name=?, instrument_Company=?, Instrument_Price=?, date_privoza=? WHERE ID=?''',
            (instrument_name, instrument_Company, Instrument_Price, date_privoza, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.otobrazit_zapisi()

    def ydalit_zapisi(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM Instrument WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.otobrazit_zapisi()

    def poisk_zapisi(self, instrument_Company):
        instrument_Company = ('%' + instrument_Company + '%',)
        self.db.c.execute('''SELECT * FROM Instrument WHERE instrument_Company LIKE ?''', instrument_Company)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.c.fetchall():
            self.tree.insert('', 'end', values=row)

    def poisk_zapisi_Group(self):
        self.db.c.execute('''SELECT * FROM Instrument ORDER BY instrument_Name''')
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.c.fetchall():
            self.tree.insert('', 'end', values=row)

    def Search_Two_Table(self):
        self.db.c.execute(
            '''SELECT Instrument.instrument_name, Instrument.instrument_Price, CompanyTable.Company_Name, CompanyTable.Company_Strana FROM Instrument INNER JOIN CompanyTable ON Instrument.instrument_Company=CompanyTable.Company_Name ''')
        for i in self.tree3.get_children():
            self.tree3.delete(i)
        for row in self.db.c.fetchall():
            self.tree3.insert('', 'end', values=row)


    def Open_Ask_Delete(self):
        answer = mb.askyesno(title="Вопрос", message="Вы действительно хотите удалить запись?")
        if answer:
            self.ydalit_zapisi()


class Vtoroe_Okno(tk.Toplevel):  # Класс создания вспомогательного окна для добавления записей
    def __init__(self):
        super().__init__(root)
        self.init_Vtoroe_Okno()
        self.view = app

    def init_Vtoroe_Okno(self):
        self.title('Добавить позицию')
        self.geometry('400x220+600+400')
        self.resizable(False, False)

        label_instrument_name = tk.Label(self, text='Инструмент:')
        label_instrument_name.place(x=50, y=10)
        label_instrument_Company = tk.Label(self, text='Производитель:')
        label_instrument_Company.place(x=50, y=70)
        label_Instrument_Price = tk.Label(self, text='Стоимость:')
        label_Instrument_Price.place(x=50, y=40)
        label_data = tk.Label(self, text='Дата привоза')
        label_data.place(x=50, y=100)

        self.entry_instrument_price = ttk.Entry(self)
        self.entry_instrument_price.place(x=200, y=40)

        self.entry_instrument_name = ttk.Entry(self)
        self.entry_instrument_name.place(x=200, y=10)

        self.conn = sqlite3.connect('InstrumentDB.db')
        self.c = self.conn.cursor()
        self.CompanyList = []
        self.CompanyList = [Company_Name[0] for Company_Name in self.c.execute("SELECT Company_Name FROM CompanyTable")]
        self.companyComboBox = ttk.Combobox(self, state="readonly")
        self.companyComboBox["values"] = self.CompanyList
        self.companyComboBox.place(x=200, y=70)
        self.numberAction = 1

        self.entry_data = ttk.Entry(self)
        self.entry_data.place(x=200, y=100)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=100, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.Check_Empty(self.entry_instrument_name.get(),
                                                                           self.companyComboBox.get(),
                                                                           self.entry_instrument_price.get(),
                                                                           self.entry_data.get(),
                                                                           self.numberAction))

        self.grab_set()  # перехватывает все события происходящих в приложении
        self.focus_set()  # захватывает и удерживает фокус

    def Check_Empty(self, instrument_name, instrument_Company, Instrument_Price, date_privoza, numberAction):
        date = date_privoza.split("-")
        dateStr = "".join(date)
        if len(instrument_name) > 20 or len(instrument_Company) > 20:
            mb.showerror("Ошибка", "Превышен лимит символов!")
        else:
            try:
                sym = float(Instrument_Price)
            except:
                mb.showerror("Ошибка", "Неправильна введена цена!")
            if not instrument_name or not instrument_Company or not Instrument_Price or not date_privoza:
                mb.showerror("Ошибка", "Не все поля заполнены!")
            else:
                if sym > 0:
                    try:
                        int(dateStr)
                        if len(date) == 3:
                            for i in range(3):
                                date[i] = int(date[i])
                        else:
                            mb.showerror("Ошибка", "Неправильная введена дата!")
                    except:
                        mb.showerror("Ошибка", "Неправильна введена дата!")

                    if date[0] < 32 and date[1] < 13 and date[2] < 2022 and date[2] > 1980:
                        if numberAction == 1:
                            self.view.zapisi(instrument_name, instrument_Company, Instrument_Price, date_privoza)
                            mb.showinfo("Успех", "Запись добавлена!")
                            self.Destroy()
                        else:
                            self.view.update_record(instrument_name, instrument_Company, Instrument_Price, date_privoza)
                            mb.showinfo("Успех", "Запись обновлена!")
                            self.Destroy()
                    else:
                        mb.showerror("Ошибка", "Неправильно введена дата!")
                else:
                    mb.showerror("Ошибка", "Неправильна введена цена!")

    def Destroy(self, *args):
        Vtoroe_Okno.destroy(self)



class Redaktirovanie_Okno(
    Vtoroe_Okno):  # Класс создания окна для редактирования записей(наследует свойства от окна добавления)
    def __init__(self, Vibran_Zapis):
        super().__init__()
        self.init_edit(Vibran_Zapis)
        self.view = app

    def init_edit(self, Vibran_Zapis):
        self.numberAction = 2
        self.Vibran_Zapis = Vibran_Zapis
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        self.entry_instrument_name.insert(0, Vibran_Zapis[0])
        self.entry_instrument_price.insert(0, Vibran_Zapis[2])
        self.companyComboBox.set(Vibran_Zapis[1])
        self.entry_data.insert(0, Vibran_Zapis[3])
        btn_edit.place(x=100, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.Check_Empty(self.entry_instrument_name.get(),
                                                                           self.companyComboBox.get(),
                                                                           self.entry_instrument_price.get(),
                                                                           self.entry_data.get(),
                                                                           self.numberAction))
        self.btn_ok.destroy()


class Search(tk.Toplevel):  # Окно для поиска записей
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+600+400')
        self.resizable(False, False)

        self.conn = sqlite3.connect('InstrumentDB.db')
        self.c = self.conn.cursor()
        self.CompanyList = []
        self.CompanyList = [Company_Name[0] for Company_Name in self.c.execute("SELECT Company_Name FROM CompanyTable")]
        self.companyComboBox = ttk.Combobox(self, state="readonly")
        self.companyComboBox["values"] = self.CompanyList
        self.companyComboBox.place(x=115, y=20)

        labelSearch = tk.Label(self, text='Компания')
        labelSearch.place(x=15, y=20)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.poisk_zapisi(self.companyComboBox.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('InstrumentDB.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS Instrument (
                        id integer primary key, 
                        instrument_name text,
                        instrument_Company text,
                        Instrument_Price real, 
                        date_privoza timestamp,  
                        FOREIGN KEY (instrument_Company) REFERENCES CompanyTable(Company_Name))
                        ''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS CompanyTable(
                        Company_Name text primary key, 
                        Company_Strana text, 
                        Date_Founded text) 
                        ''')
        self.conn.commit()

    def insert_data(self, instrument_name, instrument_Company, Instrument_Price, date_privoza):
        self.c.execute(
            '''INSERT INTO Instrument(instrument_name, instrument_Company, Instrument_Price, date_privoza) VALUES (?, ?, ?, ?)''',
            (instrument_name, instrument_Company, Instrument_Price, date_privoza))
        self.conn.commit()


root = tk.Tk()
root.geometry("1100x620")
root.resizable(False, False)
db = DB()
Main(root)
app = Main(root)
root.mainloop()