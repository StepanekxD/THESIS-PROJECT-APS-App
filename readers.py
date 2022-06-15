# Imported libraries
from tkinter import messagebox
from pyzbar.pyzbar import decode
import sqlite3
import cv2


def read_qr():

    print('Press S key to close the camera window.')
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    w_list = ['APS-W-in-A1', 'APS-W-in-A2', 'APS-W-in-WS', 'APS-W-in-CG', 'APS-W-in-ST']
    w_state = 0
    wss = ""
    connection = sqlite3.connect("WSS.db")
    cursor = connection.cursor()

    while True:
        ret, image = cap.read()
        cv2.imshow('APS QR Reader', image)
        # cv2.setWindowProperty('APS QR Reader', cv2.WND_PROP_TOPMOST, 1)

        for barcode in decode(image):
            decoded = barcode.data.decode('utf-8')
            # raw_data = barcode.data

            # *************** State 0 (ZERO) => reads QR of a WSS (Warehouse Storing Spot) *****************************
            if w_state == 0 and decoded not in w_list:
                messagebox.showerror(title='Error', message='This is not any of the Warehouse Storing Spot QR')

            elif w_state == 0 and decoded == w_list[0]:
                messagebox.showinfo(title='Message',
                                    message=f"You chose {w_list[0]} \n Please scan the items to be stored")
                w_state = 1
                wss = w_list[0]
                print(wss)
                print(w_state)

            elif w_state == 0 and decoded == w_list[1]:
                messagebox.showinfo(title='Message',
                                    message=f"You chose {w_list[1]} \n Please scan the items to be stored")
                w_state = 1
                wss = w_list[1]
                print(wss)
                print(w_state)

            elif w_state == 0 and decoded == w_list[2]:
                messagebox.showinfo(title='Message',
                                    message=f"You chose {w_list[2]} \n Please scan the items to be stored")
                w_state = 1
                wss = w_list[2]
                print(wss)
                print(w_state)

            elif w_state == 0 and decoded == w_list[3]:
                messagebox.showinfo(title='Message',
                                    message=f"You chose {w_list[3]} \n Please scan the items to be stored")
                w_state = 1
                wss = w_list[3]
                print(wss)
                print(w_state)

            elif w_state == 0 and decoded == w_list[4]:
                messagebox.showinfo(title='Message',
                                    message=f"You chose {w_list[4]} \n Please scan the items to be stored")
                w_state = 1
                wss = w_list[4]
                print(wss)
                print(w_state)

            # *************** State 1 (ONE) => assigns Item QR dat to the WWS in database ******************************

            elif w_state == 1 and wss == w_list[0]:
                decoded = decoded.lstrip('\n')
                decoded = decoded.replace('\n', ',')
                decoded = ''.join(decoded.split())
                list_decoded = decoded.split(',')
                list_decoded.pop()
                cl_item = list_decoded[0].lstrip('Item:')
                cl_qty = list_decoded[1].lstrip('Quantity:')
                cl_ordid = list_decoded[2].lstrip('Order ID:')
                cl_sku = list_decoded[3].lstrip('SKU:')
                cl_lot = list_decoded[4].lstrip('Lot #:')

                cursor.execute("""insert into WSS (Item_Name, Quantity, Order_ID, SKU, LOT, WSS) values 
                ('{}', '{}', '{}', '{}', '{}', 'WSS-A1');""".format(cl_item, cl_qty, cl_ordid, cl_sku, cl_lot))
                connection.commit()

                w_state = 0
                print(w_state)
                messagebox.showinfo(title='Message',
                                    message="Item was scanned and saved."
                                            "\n Please scan the Warehouse Storing Spot QR "
                                            "\n for storing the next Item")

            elif w_state == 1 and wss == w_list[1]:
                decoded = decoded.lstrip('\n')
                decoded = decoded.replace('\n', ',')
                decoded = ''.join(decoded.split())
                list_decoded = decoded.split(',')
                list_decoded.pop()
                cl_item = list_decoded[0].lstrip('Item:')
                cl_qty = list_decoded[1].lstrip('Quantity:')
                cl_ordid = list_decoded[2].lstrip('Order ID:')
                cl_sku = list_decoded[3].lstrip('SKU:')
                cl_lot = list_decoded[4].lstrip('Lot #:')

                cursor.execute("""insert into WSS (Item_Name, Quantity, Order_ID, SKU, LOT, WSS) values 
                ('{}', '{}', '{}', '{}', '{}', 'WSS-A2');""".format(cl_item, cl_qty, cl_ordid, cl_sku, cl_lot))
                connection.commit()

                w_state = 0
                print(w_state)
                messagebox.showinfo(title='Message',
                                    message="Item was scanned and saved."
                                            "\n Please scan the Warehouse Storing Spot QR "
                                            "\n for storing the next Item")

            elif w_state == 1 and wss == w_list[2]:
                decoded = decoded.lstrip('\n')
                decoded = decoded.replace('\n', ',')
                decoded = ''.join(decoded.split())
                list_decoded = decoded.split(',')
                list_decoded.pop()
                cl_item = list_decoded[0].lstrip('Item:')
                cl_qty = list_decoded[1].lstrip('Quantity:')
                cl_ordid = list_decoded[2].lstrip('Order ID:')
                cl_sku = list_decoded[3].lstrip('SKU:')
                cl_lot = list_decoded[4].lstrip('Lot #:')

                cursor.execute("""insert into WSS (Item_Name, Quantity, Order_ID, SKU, LOT, WSS) values 
                ('{}', '{}', '{}', '{}', '{}', 'WSS-WS');""".format(cl_item, cl_qty, cl_ordid, cl_sku, cl_lot))
                connection.commit()

                w_state = 0
                print(w_state)
                messagebox.showinfo(title='Message',
                                    message="Item was scanned and saved."
                                            "\n Please scan the Warehouse Storing Spot QR "
                                            "\n for storing the next Item")

            elif w_state == 1 and wss == w_list[3]:
                decoded = decoded.lstrip('\n')
                decoded = decoded.replace('\n', ',')
                decoded = ''.join(decoded.split())
                list_decoded = decoded.split(',')
                list_decoded.pop()
                cl_item = list_decoded[0].lstrip('Item:')
                cl_qty = list_decoded[1].lstrip('Quantity:')
                cl_ordid = list_decoded[2].lstrip('Order ID:')
                cl_sku = list_decoded[3].lstrip('SKU:')
                cl_lot = list_decoded[4].lstrip('Lot #:')

                cursor.execute("""insert into WSS (Item_Name, Quantity, Order_ID, SKU, LOT, WSS) values 
                ('{}', '{}', '{}', '{}', '{}', 'WSS-CG');""".format(cl_item, cl_qty, cl_ordid, cl_sku, cl_lot))
                connection.commit()

                w_state = 0
                print(w_state)
                messagebox.showinfo(title='Message',
                                    message="Item was scanned and saved."
                                            "\n Please scan the Warehouse Storing Spot QR "
                                            "\n for storing the next Item")

            elif w_state == 1 and wss == w_list[4]:
                decoded = decoded.lstrip('\n')
                decoded = decoded.replace('\n', ',')
                decoded = ''.join(decoded.split())
                list_decoded = decoded.split(',')
                list_decoded.pop()
                cl_item = list_decoded[0].lstrip('Item:')
                cl_qty = list_decoded[1].lstrip('Quantity:')
                cl_ordid = list_decoded[2].lstrip('Order ID:')
                cl_sku = list_decoded[3].lstrip('SKU:')
                cl_lot = list_decoded[4].lstrip('Lot #:')

                cursor.execute("""insert into WSS (Item_Name, Quantity, Order_ID, SKU, LOT, WSS) values 
                ('{}', '{}', '{}', '{}', '{}', 'WSS-ST');""".format(cl_item, cl_qty, cl_ordid, cl_sku, cl_lot))
                connection.commit()

                w_state = 0
                print(w_state)
                messagebox.showinfo(title='Message',
                                    message="Item was scanned and saved."
                                            "\n Please scan the Warehouse Storing Spot QR "
                                            "\n for storing the next Item")

            else:
                messagebox.showerror(title='Error', message='Something went wrong :-/')

        if cv2.waitKey(10) == ord('s'):
            print('Scanning finished')
            break

    connection.close()
    cap.release()
    cv2.destroyAllWindows()


# ***************************************** NOT WORKING CODE ***********************************************************

# # Showing borderline and text for QR does not work but it would look nice
# pts = np.array([barcode.polygon], np.int32)
# pts = pts.reshape((-1, 1, 2))
# cv2.polylines(image, [pts], True, (255, 0, 255), thickness=5)
# anchor = barcode.rect
# cv2.putText(image, decoded, anchor[0], anchor[1], cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 2)
# (x, y, w, h) = barcode.rect
# cv2.rectangle(image, (x - 10, y - 10),
#               (x + w + 10, y + h + 10),
#               (255, 0, 0), 2)
