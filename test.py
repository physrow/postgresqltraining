import psycopg2
from psycopg2 import OperationalError
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import Menu
from tkinter import messagebox
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PortgreSQL succesful")
    except OperationalError as e:
        print(f"The error '{e}' occured")
    return connection


connection = create_connection(
    "postgres",
    "postgres",
    "kekw",
    "127.0.0.1",
    "5432"
)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------=======================================================

window = Tk()
window.title("DROM V2.0 GODMODE")
window.geometry('500x500')


def search():
    query = "SELECT car_announcement.id,id_user,id_car,price,documents,description,name_brand FROM car_announcement JOIN car c on c.id = car_announcement.id_car JOIN car_model cm on c.id_car_model = cm.id JOIN car_brand cb on cm.id_car_brand = cb.id WHERE id_car_brand=='{choose_marks}'"
    stack = execute_read_query(connection, query)
    info = Label(text=stack)
    info.grid()


def delete():
    destroy_object = [log]
    for i in destroy_object:
        i.destroy()


def add_announcement():
    delete()

    def add_an():
        usid = int(first_label_entry.get())
        caid = int(second_label_entry.get())
        price = int(price_label_entry.get())
        doc = docs.get()
        description = description_label_entry.get()
        if doc == "Yes":
            doc = True
        else:
            doc = False

        if first_label_entry.get() != None:
            sad = f"insert into car_announcement (id_user, id_car, price, documents, description) values ({usid},{caid},{price},{doc},'{description}')"
            execute_query(connection, sad)

    number = IntVar
    first_label = Label(text="Write ur user ID")
    first_label.grid(row=0, column=3, sticky="w")
    first_label_entry = Entry(textvariable=number)
    first_label_entry.grid(row=1, column=3, sticky="w")

    second_label = Label(text="Write ur car ID")
    second_label.grid(row=0, column=4, sticky="w")
    second_label_entry = Entry(textvariable=number)
    second_label_entry.grid(row=1, column=4, sticky="w")

    price_label = Label(text='Write ur price')
    price_label.grid(row=0, column=5, sticky="w")
    price_label_entry = Entry(textvariable=number)
    price_label_entry.grid(row=1, column=5, sticky="w")

    documents_label = Label(text="Do u have documents?")
    documents_label.grid(row=0, column=6, sticky="w")
    docs = Combobox(window)
    docs['values'] = ("Yes", "No")
    docs.grid(row=1, column=6, sticky="w")

    description_label = Label(text="Write description")
    description_label.grid(row=0, column=7, sticky="w")
    description_label_entry = Entry(textvariable=number)
    description_label_entry.grid(row=1, column=7, sticky="w")

    message_button = Button(text="ADD ANNOUNCEMENT")
    message_button.grid(row=4, column=5, padx=5, pady=5, sticky="e")
    message_button.config(command=add_an)


def add_car():
    delete()

    def add():
        if (mileage_entry.get() != None):
            global id_car
            a = mileage_entry.get()
            b = model.get()
            c = color.get()
            if b == 'M3 perfomance':
                b = 1
            if b == 'R8':
                b = 2
            if b == 'LAND CRUISER':
                b = 4
            if b == 'ATENZA':
                b = 5
            if b == 'M5 perfomance':
                b = 6
        query = f"insert into car (id_car_model,mileage,color) values ('{b}',{a},'{c}')"
        execute_query(connection, query)
        if int(mileage_entry.get()) >= 0:
            query = "SELECT id,id_car_model,color,mileage FROM car"
            stack = execute_read_query(connection, query)
            for z, i, j, k in stack:
                print(z, i, j, k)
                if str(j) == str(c) and int(k) == int(a) and int(i) == int(b):
                    id_car = z

    def add_an():
        add()

        usid = user_id
        caid = id_car
        price = int(price_label_entry.get())
        doc = docs.get()
        description = description_label_entry.get()
        if doc == "Yes":
            doc = True
        else:
            doc = False

        if price_label_entry.get() != None:
            sad = f"insert into car_announcement (id_user, id_car, price, documents, description) values ({usid},{caid},{price},{doc},'{description}')"
            execute_query(connection, sad)

    car_label = Label(text="Choose ur model")
    car_label.grid(row=0, column=2, sticky="w")
    marks = Combobox(window)
    model = Combobox(window)
    color = Combobox(window)
    marks['values'] = ('BMW', 'AUDI', 'MAZDA', 'TOYOTA', 'HONDA', 'TESLA', 'SUZUKI', 'LEXUS', 'SUBARU')
    model.grid(row=1, column=2, sticky="w")
    model['values'] = ('M3 perfomance', 'R8', 'LAND CRUISER', 'ATENZA', 'M5 perfomance')
    color['values'] = ('WHITE', 'BLACK', 'BLUE', 'YELLOW', 'GRAY', 'GREEN')
    color_label = Label(text="Choose color")
    color_label.grid(row=2, column=2, sticky="w")
    color.grid(row=3, column=2, sticky="w")
    mileage = IntVar
    mileage_label = Label(text="Write mileage")
    mileage_label.grid(row=4, column=2, sticky="w")
    mileage_entry = Entry(textvariable=mileage)
    mileage_entry.grid(row=6, column=2, sticky="w")

    number = IntVar

    price_label = Label(text='Write ur price')
    price_label.grid(row=0, column=5, sticky="w")
    price_label_entry = Entry(textvariable=number)
    price_label_entry.grid(row=1, column=5, sticky="w")

    documents_label = Label(text="Do u have documents?")
    documents_label.grid(row=0, column=6, sticky="w")
    docs = Combobox(window)
    docs['values'] = ("Yes", "No")
    docs.grid(row=1, column=6, sticky="w")

    description_label = Label(text="Write description")
    description_label.grid(row=0, column=7, sticky="w")
    description_label_entry = Entry(textvariable=number)
    description_label_entry.grid(row=1, column=7, sticky="w")

    message_button = Button(text="ADD ANNOUNCEMENT")
    message_button.grid(row=4, column=5, padx=5, pady=5, sticky="e")
    message_button.config(command=add_an)

    marks_1 = Combobox()
    marks_1['values'] = ('BMW', 'AUDI', 'MAZDA', 'TOYOTA', 'HONDA', 'TESLA', 'SUZUKI', 'LEXUS', 'SUBARU')
    marks_1.grid(row=1, column=8)

    def search():
        a = marks_1.get()
        if a == "BMW":
            a = 1
        if a == "AUDI":
            a = 2
        if a == "TOYOTA":
            a = 3
        if a == "MAZDA":
            a = 4
        test = f"SELECT car_announcement.id,id_user,id_car,price,documents,description,name_brand FROM car_announcement JOIN car c on c.id = car_announcement.id_car JOIN car_model cm on c.id_car_model = cm.id JOIN car_brand cb on cm.id_car_brand = cb.id WHERE id_car_brand={a}"
        stack = execute_read_query(connection, test)

        def add_search():
            for i in range(len(stack)):
                test = f"ID : {stack[i][0]} USER_ID : {stack[i][1]} CAR ID : {stack[i][2]} PRICE : {stack[i][3]} DOCUMENTS : {stack[i][4]} DESCRIPTION : {stack[i][5]} MARK : {stack[i][6]}"
                x = Label(text=test)
                x.grid(row=i + 1, column=9)



        add_search()
        info = Label()
        info.grid(row=4, column=8)

    message_button = Button(text="SEARCH ANNOUNCEMENTS")
    message_button.grid(row=2, column=8, padx=5, pady=5, sticky="e")
    message_button.config(command=search)


def enter():
    delete()

    def kk():
        global user_id
        if int(login_entry.get()) != None:
            now = "SELECT phone_number,id from users where users.phone_number != 0"
            stack = execute_read_query(connection, now)
            for i in stack:
                if i[0] == int(login_entry.get()):
                    messagebox.showinfo('User find', 'Good! u are logged')
                    user_id = i[1]
                    if messagebox.OK:
                        add_car()
                        break
                if i[0] == 8432139:
                    messagebox.showerror('Not found', "This phone not registered")
                    break
                delete()

    login = StringVar()
    login_label = Label(text="Input phone number")
    login_label.grid(row=0, column=1, sticky="w")
    login_entry = Entry(textvariable=login)
    login_entry.grid(row=1, column=1, padx=5, pady=5)
    message_button = Button(text="LOGIN")
    message_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
    message_button.config(command=kk)


log = Button(text="LOGIN", background="#555", foreground="#ccc", padx="15", pady="7", font="13")
log.config(command=enter)
log.pack()

log.mainloop()
