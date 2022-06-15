# Imported libraries and other py files
from tkinter import *
from tkinter import ttk, filedialog
from PIL import ImageTk, Image
from pathlib import Path
from data_import import *
from readers import *
import pandas as pd
import warnings
import datetime
import shutil
import qrcode
import csv
import os

warnings.filterwarnings('ignore')

# Tkinter GUI window settings
root = Tk()
root.title("APS System app")
root.iconbitmap("Media/APS favicon.ico")
root.geometry("800x500")
root.resizable(width=False, height=False)

# Global variables
APScolor = "#9AD8AF"
APSbold = 'Verdana 14 bold'
APSfont = 'Verdana 12'
APSlight = 'Verdana 10'
today = datetime.date.today()
order_id = 1
order_num = ""
qr_name = ""
qr_orid = ""
qr_data = ""
i = 1
data = []
last = []
exp_list = []

# Different view frames settings and function
frame0 = Frame(root)
frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
frame4 = Frame(root)
frame5 = Frame(root)


# ***************************************** FUNCTION SECTION ***********************************************************

# Enabling to have multiple "windows" in GUI
def show_frame(frame):
    frame.tkraise()


for frame in (frame0, frame1, frame2, frame3, frame4, frame5):
    frame.grid(row=0, column=0, sticky="NESW")

show_frame(frame0)


# Obtaining data from the db to display in combobox (dropdown list)
def fetch_name():
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    cursor.execute('select Part_Name from PARTS')
    global sql_name
    sql_name = cursor.fetchall()
    connection.close()


# Onclick: Views Frame 1, creates new order id and clears previous order data from the treeview
def new_order():
    global order_num
    order_num = "APS-" + str(today) + "-OR-" + str(order_id)
    show_frame(frame1)
    print(order_num)
    for item in tree.get_children():
        tree.delete(item)


# Obtaining remaining data about selected item in combobox
def fetch_remaining(x):
    connection = sqlite3.connect("Data/ItemListData.db")
    cursor = connection.cursor()
    name = (x, )
    qry = "select SKU, Category, Storing, LOT from PARTS where Part_Name=?"
    cursor.execute(qry, name)
    global data
    data = cursor.fetchall()
    connection.close()


# Onclick: Fits selected item to the Treeview as a preview for the order
def add_order():
    global i
    qty = quantity.get()
    selected = combo.get()

    if qty == "" or selected == "":
        messagebox.showerror(title='Error', message='Please select the item and quantity')
    elif qty.isdigit() == False:
        messagebox.showerror(title='Error', message='Enter integer as a quantity!')
        quantity.delete(0, END)
    elif qty != "" and selected != "":
        cleared = selected.strip('{}')
        fetch_remaining(cleared)
        tree.insert(parent='', index='end', iid=str(i), text=str(i),
                    values=(cleared, qty, order_num, data[0][0], data[0][3],  data[0][1], data[0][2]))
        quantity.delete(0, END)
        combo.delete(0, END)
        i += 1
    else:
        messagebox.showerror(title='Error', message='Unexpected error xD:')


# Onclick: Deletes selected items in Treeview from the order preview
def remove_selected():
    r = tree.selection()
    for record in r:
        tree.delete(record)


# Creates folder in Export directory for particular order. Overwrites if one already exists
def create_folder():
    global order_num
    dirpath = os.path.join('./Export/', order_num)
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
    os.makedirs(dirpath)
    print('Folder {} created'.format(dirpath))


# Onclick: Finishes the order, exports the csv file and generates the QR symbols for each item in the order
def finish_order():

    create_folder()
    global order_num
    global exp_list
    file_name = "./Export/%s/CSV-%s.csv" % (order_num, order_num)
    if len(tree.get_children()) < 1:
        messagebox.showerror(title='Error', message='No items selected for ordering')
        return False

    # Exports the treeview data to csv and adds the header
    with open(file_name, newline='', mode='x') as exp_file:
        exp_writer = csv.writer(exp_file, delimiter=',')
        exp_writer.writerow([h for h in tree['columns']])
        for g in tree.get_children():
            row = tree.item(g)['values']
            exp_writer.writerow(row)
            exp_list.append(row)

    # QR Codes generating and label pasting
    def create_qr(label):
        global qr_orid, qr_name
        ss = Image.open('Media/{}.png'.format(label))
        side = 333
        wpc = (side/float(ss.size[0]))
        hsz = int((float(ss.size[1])*float(wpc)))
        ss = ss.resize((side, hsz), Image.ANTIALIAS)    # PIL.Image.ANTIALIAS= Resampling.LANCZOS
        path_name = "./Export/%s/QR-%s-%s.png" % (order_num, qr_orid, qr_name)
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=15, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_image = qr.make_image()
        pos = ((qr_image.size[0] - ss.size[0]) // 2, (qr_image.size[1] - ss.size[1]) // 2)
        qr_image.paste(ss, pos)
        qr_image.save(path_name)

    # Iterate and gather data for generating QRs, paste labels based on storing spot
    def iterate_qr():
        read_csv = pd.read_csv(file_name)
        for index, values in read_csv.iterrows():
            global qr_data, qr_orid, qr_name
            qr_name = values['Item Name']
            qr_qty = values['Quantity']
            qr_orid = values['Order ID']
            qr_sku = values['SKU']
            qr_lot = values['Supplier lot#']
            spot = values['Storing spot']
            qr_data = f'''
                Item:  {qr_name}
                Quantity:  {qr_qty}
                Order ID:  {qr_orid}
                SKU:  {qr_sku}
                Lot #:  {qr_lot}
                '''
            if spot == 'in-A1':
                create_qr('SS A1 b')
            elif spot == 'in-A2':
                create_qr('SS A2 b')
            elif spot == 'in-WS':
                create_qr('SS WS b')
            elif spot == 'in-CG':
                create_qr('SS CG b')
            elif spot == 'in-ST':
                create_qr('SS ST b')
            else:
                messagebox.showerror(title='Error', message='Iterating went wrong :( ')

    iterate_qr()

    export_message = "Order has been exported to the folder: \n./Export/%s/ \n Go back to Menu." % order_num
    messagebox.showinfo(title='Message', message=export_message)
    global order_id
    order_id = order_id + 1
    show_frame(frame0)


# Browse files for new data import
def browse_file():
    select_file = filedialog.askopenfilename(initialdir='C:/Users/Stepan VENCL/Desktop',
                                             title='Select .xlsx file:',
                                             filetypes=(('xlsx Files', '*.xlsx'), ))
    browse_label['text'] = select_file


# Onclick: calls functions from data_import.py
def import_data():
    file_path = browse_label['text']

    def delete_old():
        [f.unlink() for f in Path("./Data/").glob("*") if f.is_file()]

    if browse_label['text'] != "No file selected:":
        delete_old()
        messagebox.showinfo(title='Message', message='Old data deleted')
        convert_to_csv(file_path)
        messagebox.showinfo(title='Message', message='Excel was converted to CSV')
        create_new_db()
        messagebox.showinfo(title='Message', message='New local Database created')
        fill_db()
        messagebox.showinfo(title='Message', message='Database filled with a new data')
        messagebox.showinfo(title='Message', message='Please restart the program')

    else:
        messagebox.showerror(title='Error', message='Please select valid file for import')


# unrealized AR part
def nothing():
    global sml
    messagebox.showinfo(title='Message', message='Nothing here, sorry!')
    ar_lbl.set("So sorry, really! Nothing is here...")
    sml.set(":-(")
    f4_btn_back = Button(frame4, textvariable=sml, command=lambda: smile())
    f4_btn_back.place(x=400, y=245)
    f4_btn1.place_forget()
    f4_btn2.place_forget()


def smile():
    messagebox.showinfo(title='Message', message='Usm2j se 4ur8ku! :-)')
    sml.set(":-)")


# Generating 1 time warehouse sorting QRs:
def warehouse_qr(spot):
    wqr_path = './Export/%s.png' % spot
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=15, border=5)
    qr.add_data(spot)
    qr.make(fit=True)
    qr_image = qr.make_image()
    qr_image.save(wqr_path)

# warehouse_qr('APS-W-in-A1')
# warehouse_qr('APS-W-in-A2')
# warehouse_qr('APS-W-in-WS')
# warehouse_qr('APS-W-in-CG')
# warehouse_qr('APS-W-in-ST')


# Fetches last record uploaded to WSS database
def show_wss_last():
    connection = sqlite3.connect("WSS.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WSS ORDER BY ROWID DESC LIMIT 1;")
    global last
    last = cursor.fetchall()
    connection.close()
    dis_title.set('(Item Name, Quantity, Order ID, SKU, LOT#, WSS)')
    display.set(str(last))


# Deletes all rows in WSS database after confirming
def delete_wss():
    response = messagebox.askyesno('Warning', 'Do you really want to delete all data in WSS.db?')
    if response == 1:
        connection = sqlite3.connect("WSS.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM WSS;")
        connection.commit()
        connection.close()
        messagebox.showwarning('Message', 'All data deleted!')
    else:
        messagebox.showinfo('Message', 'No purge happening!')


# ***************************************** GUI SECTION ****************************************************************

# =================================== Frame 0 code = Menu Screen

# Label
f0_spacer = Label(frame0, text="")
f0_spacer.pack()
f0_title = Label(frame0, text="APS System App Menu:", font=APSfont)
f0_title.pack(pady=10)

# MENU Buttons
f0_btn1 = Button(frame0, text="New Order", command=lambda: new_order(),
                 width=16, height=2, bd=6, bg=APScolor, font=APSbold, relief=GROOVE)
f0_btn1.pack(pady=5)
f0_btn2 = Button(frame0, text="Import New Data", command=lambda: show_frame(frame2),
                 width=16, height=2, bd=6, bg=APScolor, font=APSbold, relief=GROOVE)
f0_btn2.pack(pady=5)
f0_btn3 = Button(frame0, text="Read QR Codes", command=lambda: show_frame(frame3),
                 width=16, height=2, bd=6, bg=APScolor, font=APSbold, relief=GROOVE)
f0_btn3.pack(pady=5)
f0_btn4 = Button(frame0, text="AR Demo", command=lambda: show_frame(frame4),
                 width=16, height=2, bd=6, bg=APScolor, font=APSbold, relief=GROOVE)
f0_btn4.pack(pady=5)
f0_btn5 = Button(frame0, text="About", command=lambda: show_frame(frame5),
                 width=16, height=2, bd=6, bg=APScolor, font=APSbold, relief=GROOVE)
f0_btn5.pack(pady=5)

# =================================== Frame 1 code = Ordering system

# Title Label
f1_space = Label(frame1, height=1)
f1_space.grid(row=0, column=2, columnspan=2)
f1_title = Label(frame1, text="APS Item Ordering System:", font=APSbold)
f1_title.grid(row=1, column=2, columnspan=2, pady=15)
# Label 1.1
f1_label1 = Label(frame1, text="Search items to be ordered by name:", font=APSlight)
f1_label1.grid(row=2, column=0, columnspan=2, padx=15, pady=5)

# Combobox
sql_name = ()
fetch_name()
combo = ttk.Combobox(frame1, values=sql_name, width=30, height=15, font=APSlight)
combo.grid(row=3, column=0, columnspan=2, padx=15, pady=10)

# Label 1.2
f1_label2 = Label(frame1, text="Enter quantity to be ordered:", font=APSlight)
f1_label2.grid(row=2, column=2, columnspan=2, padx=15, pady=5)

# Quantity entry field
quantity = Entry(frame1, width=15, font=APSlight)
quantity.grid(row=3, column=2, columnspan=2, padx=15, pady=10)

# Button 1.1
f1_btn1 = Button(frame1, text="Add to the order list", command=lambda: add_order(), font=APSlight, bg=APScolor)
f1_btn1.grid(row=3, column=4, pady=10)

# TreeView of the order
tree = ttk.Treeview(frame1)
tree['columns'] = ('Item Name', 'Quantity', 'Order ID', 'SKU', 'Supplier lot#', 'Category', 'Storing spot')
tree.column('#0', width=35, minwidth=30, anchor=CENTER)
tree.column('Item Name', width=150, minwidth=100, anchor=W)
tree.column('Quantity', width=70, minwidth=50, anchor=CENTER)
tree.column('Order ID', width=150, minwidth=50, anchor=CENTER)
tree.column('SKU', width=80, minwidth=50, anchor=CENTER)
tree.column('Supplier lot#', width=120, minwidth=100, anchor=CENTER)
tree.column('Category', width=80, minwidth=50, anchor=CENTER)
tree.column('Storing spot', width=80, minwidth=50, anchor=CENTER)

tree.heading('#0', text='#', anchor=CENTER)
tree.heading('Item Name', text='Item Name', anchor=CENTER)
tree.heading('Quantity', text='Quantity', anchor=CENTER)
tree.heading('Order ID', text='Order ID', anchor=CENTER)
tree.heading('SKU', text='SKU', anchor=CENTER)
tree.heading('Supplier lot#', text='Supplier lot#', anchor=CENTER)
tree.heading('Category', text='Category', anchor=CENTER)
tree.heading('Storing spot', text='Storing spot', anchor=CENTER)
tree.grid(row=4, column=0, rowspan=5, columnspan=5, padx=15, pady=15)

# Button 1.3
f1_btn3 = Button(frame1, text="Remove selected from the order", command=lambda: remove_selected(),
                 font='Verdana, 8', bg='#F73939')
f1_btn3.grid(row=9, column=0, columnspan=2)

# Button 1.2
f1_btn2 = Button(frame1, text="Finish the order", command=lambda: finish_order(), font=APSfont, bg=APScolor)
f1_btn2.grid(row=9, column=2)

# Back button
f1_btn_back = Button(frame1, text="Back to Menu", command=lambda: show_frame(frame0), bg='#9fa8d6', font=APSfont)
f1_btn_back.grid(row=9, column=4)

# =================================== Frame 2 code = IMPORT

# Labels
f2_title = Label(frame2, text="Import new data to Ordered Parts Database:", font=APSbold)
f2_title.place(x=170, y=30)
f2_label2 = Label(frame2, text="Please select xlsx file that has no headers and the columns are: \n"
                               "SKU | Name | Category | WSS | LOT#",
                  font=APSfont, justify=CENTER)
f2_label2.place(x=140, y=70)
f2_label1 = Label(frame2, text="Data inside should not contain any of the following characters:",
                  font=APSfont, justify=CENTER)
f2_label1.place(x=140, y=120)

# Image - forbidden special characters
specchar = Image.open('Media/Specials.png')
specchar = ImageTk.PhotoImage(specchar)
logo_label3 = Label(frame2, image=specchar)
logo_label3.image = specchar
logo_label3.place(x=200, y=150)

browse_label = Label(frame2, text="No file selected:", font=APSfont, justify=CENTER)
browse_label.place(x=300, y=240)

# Buttons
f2_btn1 = Button(frame2, text="Browse files", command=lambda: browse_file(), font=APSfont, bg=APScolor)
f2_btn1.place(x=250, y=300)
f2_btn2 = Button(frame2, text="Import data", command=lambda: import_data(), font=APSfont, bg=APScolor)
f2_btn2.place(x=450, y=300)

f2_btn_back = Button(frame2, text="Back to Menu", command=lambda: show_frame(frame0), bg='#9fa8d6', font=APSfont)
f2_btn_back.place(x=345, y=400)

# ====== Frame 3 code = READ QR

f3_title = Label(frame3, text="Scan & save QR Codes", font=APSbold, justify=CENTER)
f3_title.place(x=280, y=30)
f3_label = Label(frame3, text="Press S key to stop the video capture.", font=APSfont, justify=CENTER)
f3_label.place(x=255, y=80)

f3_btn1 = Button(frame3, text="Start Scanning", command=lambda: read_qr(),
                 width=16, height=2, font=APSbold, bg=APScolor)
f3_btn1.place(x=300, y=130)

f3_btn2 = Button(frame3, text="Show the last WSS.db entry:", command=lambda: show_wss_last(), font=APSfont)
f3_btn2.place(x=280, y=210)

dis_title = StringVar()
dis_title.set('Click the button!')
display_title = Label(frame3, textvariable=dis_title, font=APSlight, justify=CENTER)
display_title.place(x=240, y=250)

display = StringVar()
display_lbl = Label(frame3, textvariable=display, font=APSlight, justify=CENTER)
display_lbl.place(x=150, y=270)

f3_btn3 = Button(frame3, text="Delete all WSS data", command=lambda: delete_wss(),
                 font=APSlight, bg='#F73939')
f3_btn3.place(x=335, y=330)

f3_btn_back = Button(frame3, text="Back to Menu", command=lambda: show_frame(frame0), bg='#9fa8d6', font=APSfont)
f3_btn_back.place(x=345, y=400)

# =================================== Frame 4 code = READ AR

f4_title = Label(frame4, text="Enter the Augmented Reality!", font=APSbold)
f4_title.place(x=245, y=60)

ar_lbl = StringVar()
ar_lbl.set("Select the camera for AR preview. \n \n Press S key to stop.")
f4_label = Label(frame4, textvariable=ar_lbl, font=APSfont, justify=CENTER)
f4_label.place(x=260, y=130)

sml = StringVar()
f4_btn1 = Button(frame4, text="Use Webcam", command=lambda: nothing(),
                 width=16, height=2, font=APSbold, bg=APScolor)
f4_btn1.place(x=150, y=230)
f4_btn2 = Button(frame4, text="Use IP camera", command=lambda: nothing(),
                 width=16, height=2, font=APSbold, bg=APScolor)
f4_btn2.place(x=450, y=230)

f4_btn_back = Button(frame4, text="Back to Menu", command=lambda: show_frame(frame0), bg='#9fa8d6', font=APSfont)
f4_btn_back.place(x=345, y=400)

# =================================== Frame 5 code = ABOUT

# Title
f5_title = Label(frame5, text="MASTER'S THESIS PROJECT \n 2022 (c) by \n Štěpán Vencl", pady=4, font=APSfont)
f5_title.place(x=290, y=70)

# Logos
APSlogo = Image.open('Media/APS logo small.png')
APSlogo = ImageTk.PhotoImage(APSlogo)
logo_label = Label(frame5, image=APSlogo)
logo_label.image = APSlogo
logo_label.place(x=140, y=200)
CTUlogo = Image.open('Media/CTU lion.png')
CTUlogo = ImageTk.PhotoImage(CTUlogo)
logo_label2 = Label(frame5, image=CTUlogo)
logo_label2.image = CTUlogo
logo_label2.place(x=420, y=160)

f5_btn_back = Button(frame5, text="Back to Menu", command=lambda: show_frame(frame0), bg='#9fa8d6', font=APSfont)
f5_btn_back.place(x=345, y=400)


# ***************************************** MAIN LOOP ******************************************************************

if __name__ == '__main__':

    root.mainloop()
    print("\n Master's thesis project of Štěpán Vencl")
