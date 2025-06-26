from codecs import charmap_decode
import tkinter as tk
from tkinter import messagebox
import datetime
import pyperclip
import subprocess
# importing datetime module for now()
from datetime import datetime
import pyautogui
import time
import os
import pandas as pd
import qrcode
from PIL import ImageTk, Image
import textwrap
import xml.etree.ElementTree as ET
import pynput
import requests
import xmltodict
import json
os.environ['PYTHONIOENCODING'] = 'utf-8'

class AlwaysOnTopGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        
        # Create input box
        self.input_box = tk.Entry(self)
        self.input_box.pack(fill=tk.X)
        
        # Bind input to run command
        self.input_box.bind("<Return>", self.run_command)
        
        # Create label to display results
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        #Create QRCODE
        
        # Focus on input box
        self.input_box.focus()
        self.title("Support app!")
        self.result_label.config(text="Command: ? | in | log | bt | cls | vn | rep | q")

        #Load file config
        if self.load_xmlfile():
            self.result_label.config(text="Load config file ok!")
            self.call_update()
        else:
            self.result_label.config(text="Can not find file config!!!")
            self.call_update()

    def on_key_press(self, key):
        try:
            if key == pynput.keyboard.Key.esc:
                self.listener.stop()
        except Exception as e:
            print(f"Co loi: {e}")
            print("Loi!")

    listener = None
    tree = None
    wwidth = wheight = pheight = pwidth = qrwidth = ontop = None
    blur = extension = ""
    listtest = []

    def chk_child_window(self):
        try:
            test = self.dialog
            return True
        except:
            return False

    def load_variable(self):
        try:
            self.wwidth = self.tree.find("windows").attrib.get("width")
            self.wheight = self.tree.find("windows").attrib.get("height")
            self.pwidth = self.tree.find("position").attrib.get("width")
            self.pheight = self.tree.find("position").attrib.get("height")
            self.blur = self.tree.find("blur").attrib.get("value")
            self.qrwidth = self.tree.find("qrcode").attrib.get("width")
            self.ontop = self.tree.find("alwaysontop").attrib.get("enable")
            self.extension = self.tree.find("backupfile").attrib.get("extension")
            if self.blur == "":
                self.blur = 0.5
        except:
            self.wwidth = 300
            self.wheight = 50
            self.pwidth = 1612
            self.pheight = 959
            self.blur = 0.5
            self.ontop = 0
            self.qrwidth = 300
            self.extension = "txt"

    def load_geometry(self):
        # Set window size and position
        self.geometry("{}x{}+{}+{}".format(self.wwidth, self.wheight, self.pwidth, self.pheight))

    def load_ontop(self):
        # Set window always on top
        self.wm_attributes("-topmost", self.ontop)

    def load_blurform(self):
        self.attributes("-alpha", self.blur)
        self.result_label.config(wraplength = (int(self.wwidth) - 10))

    def load_xmlfile(self):
        try:
            path = os.path.realpath("a.config")
            self.tree = ET.parse(path)
            self.load_variable()
            self.load_geometry()
            self.load_blurform()
            self.load_ontop()
            return True
        except Exception as e:
            print(f"Co loi: {e}")
            print("Khong thay file config")
            self.load_variable()
            self.load_geometry()
            self.load_blurform()
            self.load_ontop()
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            return False
    
    def read_clipboard(self):
        try:
            clipboard_contents = pyperclip.paste()
            self.result_label.config(text=clipboard_contents)
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def prepare_in2(self):
        try:
            listIn = []
            data = pyperclip.paste()
            # print(data)
            
            count = 0
            
            dataar = data.split("\r\n")
            for f in dataar:
                if count == 0:
                    intxt = "IN\n("
                # print (f)
                count += 1
                if f == '':
                    break
                if count == 100 or count == 200 or count == 300 or count == 400 or count == 500 or count == 600 or count == 700 or count == 800 or count == 900:
                    intxt += f"'{f.strip()}',\n"
                else:
                    intxt += f"'{f.strip()}',"
                if count == 1000:
                    intxt = intxt.rstrip(',')
                    intxt = intxt.rstrip(",\n")
                    intxt = intxt+")"
                    count = 0
                    listIn.append(intxt)
                
            intxt = intxt.rstrip(',')
            intxt = intxt.rstrip(",\n")
            intxt = intxt+")"
            listIn.append(intxt)
            intxt = "WITH temp AS (\n"
            count = 0
            for i in listIn:
                count += 1
            for i in listIn:
                intxt += f"\tSELECT isn from ISN WHERE ISN {i}\n"
                count -= 1
                if count != 0:
                    intxt += "\tUNION\n"
            intxt += ")"
            print(intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the IN command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()
    
    def prepare_in(self):
        try:
            data = pyperclip.paste()
            # print(data)
            
            countlen = 0
            intxt = "IN\n("
            dataar = data.split("\r\n")
            for f in dataar:
                # print (f)
                countlen = countlen + len(f) 
                if f == '':
                    break
                if countlen < 120 :
                    intxt = intxt + "'"+f.strip()+"',"
                else:
                    intxt = intxt + "'"+f.strip()+"',\n"
                    countlen = 0
                
            intxt = intxt.rstrip(',')
            intxt = intxt.rstrip(",\n")
            intxt = intxt+")"
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the IN command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def prepare_table(self):
        try:
            data = pyperclip.paste()
            # print(data)
            
            countlen = 0
            intxt = ""
            dataar = data.split("\t")
            for f in dataar:
                # print (f)
                intxt = intxt + f.strip() + "\t"
                
            intxt = intxt.rstrip('\t')
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the table command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def prepare_update(self):
        data = pyperclip.paste()
        uptxt = "UPDATE "
        dem = 0
        data1 = data.split(" ")
        for i in data1:
            if dem == 1:
                uptxt += "SET  = '' "
            uptxt += i + " "
            dem += 1
        
        uptxt = uptxt.rstrip()
        print(f"Da chuan bi xong cau lenh: {uptxt}")
        pyperclip.copy(uptxt)
        self.result_label.config(text="Done! Prepare update code complete!")
        self.call_update()

    def prepare_between(self):
        try:
            dem1 = dem2 = 0
            data = pyperclip.paste()
            #print(data)
            
            data = str(data)
            first_time = second_time = intxt = ""
            if "-" in data and "/" in data :
                dataa = data.split('-')
                for i in dataa:
                    dem1 = dem1 + 1
                datab = data.split('/')
                for i in datab:
                    dem2 = dem2 + 1
                if dem1 == 2:
                    if '/' in dataa[0]:
                        temp = dataa[0].split('/')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'YYYY/MM/DD HH24:MI:SS')"
                            else:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'DD/MM/YYYY HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'DD/MM/YYYY HH24:MI:SS')"
                    elif '-' in dataa[0]:
                        temp = dataa[0].split('-')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'YYYY-MM-DD HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'YYYY-MM-DD HH24:MI:SS')"
                            else:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'DD-MM-YYYY HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'DD-MM-YYYY HH24:MI:SS')"
                elif dem2 == 2:
                    if '/' in datab[0]:
                        temp = datab[0].split('/')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'YYYY/MM/DD HH24:MI:SS')"
                            else:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'DD/MM/YYYY HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'DD/MM/YYYY HH24:MI:SS')"
                    elif '-' in datab[0]:
                        temp = datab[0].split('-')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'YYYY-MM-DD HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'YYYY-MM-DD HH24:MI:SS')"
                            else:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + " 00:00:00', 'DD-MM-YYYY HH24:MI:SS') AND TO_DATE('" + second_time + " 23:59:59', 'DD-MM-YYYY HH24:MI:SS')"
            else :
                intxt = """BETWEEN TO_DATE('2022/01/01 00:00:00', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('2022/12/31 23:59:59', 'YYYY/MM/DD HH24:MI:SS')"""
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the between command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def prepare_between2(self):
        try:
            dem1 = dem2 = 0
            data = pyperclip.paste()
            #print(data)
            
            data = str(data)
            first_time = second_time = intxt = ""
            if "-" in data and "/" in data :
                dataa = data.split('-')
                for i in dataa:
                    dem1 = dem1 + 1
                datab = data.split('/')
                for i in datab:
                    dem2 = dem2 + 1
                if dem1 == 2:
                    if '/' in dataa[0]:
                        temp = dataa[0].split('/')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('" + second_time + "', 'YYYY/MM/DD HH24:MI:SS')"
                            else:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'DD/MM/YYYY HH24:MI:SS') AND TO_DATE('" + second_time + "', 'DD/MM/YYYY HH24:MI:SS')"
                    elif '-' in dataa[0]:
                        temp = dataa[0].split('-')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'YYYY-MM-DD HH24:MI:SS') AND TO_DATE('" + second_time + "', 'YYYY-MM-DD HH24:MI:SS')"
                            else:
                                first_time = dataa[0].strip()
                                second_time = dataa[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'DD-MM-YYYY HH24:MI:SS') AND TO_DATE('" + second_time + "', 'DD-MM-YYYY HH24:MI:SS')"
                elif dem2 == 2:
                    if '/' in datab[0]:
                        temp = datab[0].split('/')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('" + second_time + "', 'YYYY/MM/DD HH24:MI:SS')"
                            else:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'DD/MM/YYYY HH24:MI:SS') AND TO_DATE('" + second_time + "', 'DD/MM/YYYY HH24:MI:SS')"
                    elif '-' in datab[0]:
                        temp = datab[0].split('-')
                        for i in temp[0]:
                            if len(temp[0]) == 4:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'YYYY-MM-DD HH24:MI:SS') AND TO_DATE('" + second_time + "', 'YYYY-MM-DD HH24:MI:SS')"
                            else:
                                first_time = datab[0].strip()
                                second_time = datab[1].strip()
                                intxt = "BETWEEN TO_DATE('" + first_time + "', 'DD-MM-YYYY HH24:MI:SS') AND TO_DATE('" + second_time + "', 'DD-MM-YYYY HH24:MI:SS')"
            else :
                intxt = """BETWEEN TO_DATE('2022/01/01 00:00:00', 'YYYY/MM/DD HH24:MI:SS') AND TO_DATE('2022/12/31 23:59:59', 'YYYY/MM/DD HH24:MI:SS')"""
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the between command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def prepare_log(self):
        try:
            data = pyperclip.paste()
            
            if data.isdecimal() and len(data) == 6 :
                intxt = """SELECT * FROM log_stpc WHERE stp = 'CENTRIC:""" + data + """' AND track LIKE '%%' AND message LIKE '%%' AND logtime >= SYSDATE - 2 ORDER BY logtime DESC;"""
            else :
                intxt = """SELECT * FROM log_stpc WHERE stp = 'CENTRIC:' AND track LIKE '%%' AND message LIKE '%%' AND logtime >= SYSDATE - 2 ORDER BY logtime DESC;"""

            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the Check Log command complete.")
            self.call_update()
        except:
            intxt = """SELECT * FROM log_stpc WHERE stp = 'CENTRIC:' AND track LIKE '%%' AND message LIKE '%%' AND logtime >= SYSDATE - 2 ORDER BY logtime DESC;"""
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the Check Log command complete.")
            self.call_update()
            

    def prepare_dt(self):

        intxt = datetime.now.strftime("%Y-%m-%d %H:%M:%S")

        print (intxt)
        # set clipboard data
        pyperclip.copy(intxt)
        self.result_label.config(text=intxt)
    
    def autofillbyexcel(self):
        # Đợi 5 giây để mở phần mềm và point 
        # print ('chờ 5s để bắt đầu thực thi')
        # time.sleep(5)
        try:
            print ('bắt đầu ')
            excelname = ""
            special_cmd = "0"
            t1 = ""
            try:
                root = self.tree.getroot()
                t1 = root.find("timeautofill").attrib.get("time")
            except:
                t1 = ""
            if t1 == "":
                t1 = 0.5
            t1 = float(t1)
            try: 
                excelname = self.tree.find("file_excel_at").attrib.get("link")
                special_cmd = self.tree.find("special_command_loc_0").attrib.get("enable")
            except:
                excelname = 'D:/test.xlsx'
                special_cmd = "0"
            excelname = os.path.realpath(path=excelname)
            # read by default 1st sheet of an excel file
            dataframe1 = pd.read_excel(excelname)
            count=chk=0
            for i in dataframe1.iterrows():
                count += 1
            self.listener = pynput.keyboard.Listener(on_press=self.on_key_press)
            print(self.listener)
            if not self.listener.is_alive():
                self.listener.start()
            print("Bat dau nghe ban phim")
            for index, row in dataframe1.iterrows():
                row1 = dataframe1.loc[index]
                if not self.listener.is_alive():
                    print("Khong thay tin hieu nghe")
                    chk = 1
                    break
                if special_cmd == "1":
                    pyautogui.typewrite("ef-aoiloc-0")    
                    pyautogui.press("enter")
                    time.sleep(t1)
                pyautogui.typewrite(str(row1[0]))    
                pyautogui.press("enter")
                print (str(row1[0]))
                self.result_label.config(text=f"ITEM remaining: {str(count)}")
                self.update()
                count -= 1
                # thời gian chờ giữa 2 lần 
                time.sleep(t1)
            print("Ket thuc nghe ban phim")
            self.listener.stop()
            if chk == 0:
                self.result_label.config(text="Auto fill complete!")
            else:
                self.result_label.config(text=f"Auto fill complete! {count} didn't run yet.")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            print("File not found or empty!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="File not found or empty!")
            self.call_update()

    def autofillex(self):
        try:
            t1 = ""
            try:
                root = self.tree.getroot()
                t1 = root.find("timewait").attrib.get("time")
            except:
                t1 = ""
            if t1 == "":
                t1 = 5
            t1 = round(float(t1))
            while t1 > 0:
                self.result_label.config(text=f"Auto fill will run after {t1}s!!!")
                self.update()
                t1 -= 1;
                time.sleep(1)
            self.after(100, self.runautofillex)
        except Exception as e:
            print(f"Co loi: {e}")
            print("Khong the chay autofill")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")

    def runautofillex(self):
        self.result_label.config(text="Autofill is running....")
        self.after(100, self.autofillbyexcel)

    def autofillbyclipboard(self):
        try:
            self.attributes("-alpha", 1)
            t1 = ""
            special_cmd = "0"
            try:
                root = self.tree.getroot()
                t1 = root.find("timeautofill").attrib.get("time")
                special_cmd = self.tree.find("special_command_loc_0").attrib.get("enable")
            except:
                t1 = ""
                special_cmd = "0"
            if t1 == "":
                t1 = 0.5
            t1 = float(t1)
            data = pyperclip.paste()
            a = data.split("\r\n")
            datatxt = ""
            dem = chk = 0;
            print(a)
            for i in a:
                dem += 1
            self.listener = pynput.keyboard.Listener(on_press=self.on_key_press)
            print(self.listener)
            if not self.listener.is_alive():
                self.listener.start()
            print("Bat dau nghe ban phim")
            for i in a:
                if i == '':
                    continue
                datatxt = i.strip()
                print(datatxt)
                if not self.listener.is_alive():
                    print("Khong thay tin hieu nghe")
                    chk = 1
                    break
                self.result_label.config(text=f"ITEM remaining: {str(dem)}")
                self.update()
                dem -= 1
                if special_cmd == "1":
                    pyautogui.typewrite("ef-aoiloc-0")    
                    pyautogui.press("enter")
                    time.sleep(t1)
                pyautogui.typewrite(datatxt)
                pyautogui.press("enter")
                time.sleep(t1)
            print("Ket thuc nghe ban phim")
            self.listener.stop()
            if chk == 0:
                self.result_label.config(text="Auto fill complete!")
            else:
                self.result_label.config(text=f"Auto fill complete! {dem} didn't run yet.")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error!")
            self.call_update()

    def autofillcb(self):
        try:
            t1 = ""
            try:
                root = self.tree.getroot()
                t1 = root.find("timewait").attrib.get("time")
            except:
                t1 = ""
            if t1 == "":
                t1 = 5
            t1 = round(float(t1))
            while t1 > 0:
                self.result_label.config(text=f"Auto fill will run after {t1}s!!!")
                self.update()
                t1 -= 1;
                time.sleep(1)
            self.after(100, self.runautofillcb)
        except Exception as e:
            print(f"Co loi: {e}")
            print("Khong the chay autofill")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")

    def runautofillcb(self):
        self.result_label.config(text="Autofill is running....")
        self.after(100, self.autofillbyclipboard)

    def help(self):
        print("? \t show all action")
        print("in \t prepare in - read clipboard and prepare and record to clip board")
        print("bt \t prepare between")
        print("log \t prepare log sql")
        print("dt \t get current datetime")
        print("autofill \t auto fill from excel file")
        print("q \t quit")
    
    def generate_qr_code(self):
        try:
            self.open_dialog_showQRCODE()
            self.result_label.config(text="Done! Generate the QR Code complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.") 
            self.call_update()

    def open_dialog_showQRCODE(self):
        try:
            if self.chk_child_window():
                self.windows_destroy()
            width = int(self.qrwidth)+50
            height = int(self.qrwidth)+100
            pw = 960 - (width/2)
            ph = 540 - (height/2)
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Result")
            self.dialog.geometry("{}x{}+{}+{}".format(width, height,int(pw),int(ph)))
            self.label = tk.Label(self.dialog, text="QR CODE")
            self.label.pack()
            self.input_box_qr = tk.Entry(self.dialog)
            self.input_box_qr.pack(fill=tk.X)
            self.qr_code_image = tk.Label(self.dialog)
            self.qr_code_image.pack()
            self.label_qr = tk.Label(self.dialog, text="", wraplength=(width-20))
            self.label_qr.pack()
            self.input_box_qr.bind("<Return>", self.showQRCODE)
            # win32clipboard.OpenClipboard()
            # clipboard_contents = win32clipboard.GetClipboardData()
            # win32clipboard.CloseClipboard()
            clipboard_contents = pyperclip.paste()
            # value = self.entry.get()
            clipboard_contents = clipboard_contents.strip().rstrip("\n")
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(clipboard_contents)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((int(self.qrwidth), int(self.qrwidth)), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.qr_code_image.config(image = img)
            self.qr_code_image.image = img
            self.label_qr.config(text=clipboard_contents)
            print(clipboard_contents)
        except Exception as e:
            print(f"Co loi: {e}")
            print("Error!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")

    def showQRCODE(self, event):
        try:
            # value = self.entry.get()
            clipboard_contents = self.input_box_qr.get()
            self.input_box_qr.delete(0, tk.END)
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(clipboard_contents)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((int(self.qrwidth), int(self.qrwidth)), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)
            self.qr_code_image.config(image = img)
            self.qr_code_image.image = img
            text_long = textwrap.wrap(clipboard_contents, width=50)
            self.label_qr.config(text='\n'.join(text_long))
            print(text_long)
        except Exception as e:
            print(f"Co loi: {e}")
            print("Error!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
   
    def prepare_sn_unknit(self):
        try:
            data = pyperclip.paste()
            
            intxt = """INSERT INTO sn_unknit(TYPE,SNTYPE,SN,LINE,GRP,CDATE,COP,LASTUPD,LASTOP,SNDESC,FLAG,ID,IND_SNTYPE,IND_SN) \r\nVALUES('DEVOUTPUT','ISN','""" + data + """','LINE','GRP',SYSDATE,'V22003527',SYSDATE,'V22003527','REPRINT ISN',NULL,4162389,NULL,NULL);"""
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare the SN_UNKNIT command complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()

    def clear_cb(self):
        pyperclip.copy("")
        print("Clear clipboard ok!")
        self.result_label.config(text="Done! Clear clipboard successful!")
        self.call_update()

    def prepare_translate(self):
        try:
            data = pyperclip.paste()
            
            intxt = """Xin chào! Dịch câu sau sang tiếng Việt giúp tôi: \n\"""" + data + "\"\nCảm ơn bạn!"
            print (intxt)
            # set clipboard data
            pyperclip.copy(intxt)
            self.result_label.config(text="Done! Prepare to translate complete.")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            print("The clipboard is contain special data, You can't use this function!")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error! Clipboard has some special data.")

    def update_label(self):
        self.result_label.config(text="Command: ? | in | log | bt | cls | vn | rep | q")

    def call_update(self):
        self.after(10000, self.update_label)

    def open_dialog_showHelp(self):
        try:
            if self.chk_child_window():
                self.windows_destroy()
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Help!")
            self.dialog.geometry("400x300+760+390")
            self.label = tk.Label(self.dialog, text="All commands can be used")
            self.label.pack()
            intxt = """
?: Show this windows
in: Prepare 'in' command SQL
in2: Prepare 'in' command SQL with over 1000 line
log: Prepare 'log' command SQL
bt: Prepare 'between' command
cls: CLear clipboard
vn: Prepare command to translate with chatGPT
rep: Prepare the command SN_UNKNIT
atc: Run auto paste data from clipboard
at: Run auto paste data from excel
op <command>: Open file was configed in the config file.
<command>: Open folder was configed in the config file
gws: Get webservice string
rws: Run webservice with webservice string in the clipboard.
c: Prepare copy data
qw: Close sub window.
tb: Prepare data to create device
q: Quit
            """
            self.label2 = tk.Label(self.dialog, text=intxt, wraplength=480, justify=tk.LEFT)
            self.label2.pack()
            print("Show Help")
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")

    def copy(self):
        try:
            data = pyperclip.paste()
            a = data.split("\r\n")
            datatxt = ""
            dem = 0;
            print(a)
            for i in a:
                dem += 1
            for i in a:
                datatxt = i.strip()
                print(datatxt)
                pyperclip.copy(datatxt)
                time.sleep(0.5)
            self.result_label.config(text="Prepare copy complete!")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Error!")
            self.call_update()

    def prepare_copy(self):
        self.after(100, self.copy)

    def prepare_copy2(self):
        data = pyperclip.paste()
        pyperclip.copy(data)
        self.result_label.config(text="Done! Prepare copy data complete!")
        self.call_update()

    def windows_destroy(self):
        window_children = self.winfo_children()
        for child in window_children:
            if isinstance(child, tk.Toplevel):
                child.destroy()

    def create_folder(self):
        try:
            root = self.tree.getroot()
            folders = root.findall("folder")
            name = path = ""
            for folder in folders:
                name = folder.attrib.get("name")
                path = folder.attrib.get("path")
                if name == "temp":
                    break
            if path != "":
                today = datetime.now()
                if today.day < 10:
                    strdate = "0" + str(today.day)
                else:
                    strdate = str(today.day)
                path = path + "\\" + strdate
                path = os.path.realpath(path)
                if os.path.exists(path):
                    print("Thu muc da ton tai")
                    self.result_label.config(text="Folder has existed!!!")
                    self.call_update()
                else:
                    os.mkdir(path)
                    print("Tao Thu muc thanh cong!")
                    self.result_label.config(text="Create folder successful!!!")
                    self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot create new folder!!!")
            self.call_update()

    def save_Backup(self):
        try:
            root = self.tree.getroot()
            folders = root.findall("folder")
            name = path = path2 = ""
            chk = 0
            for folder in folders:
                name = folder.attrib.get("name")
                path = folder.attrib.get("path")
                if name == "temp":
                    break
            if path != "":
                today = datetime.now()
                if today.day < 10:
                    strdate = "0" + str(today.day)
                else:
                    strdate = str(today.day)
                path = path + "\\" + strdate
                path2 = path
                path = os.path.realpath(path)
                if os.path.exists(path):
                    dttxt = today.strftime("%Y%m%d %H%M%S")
                    txt = pyperclip.paste()
                    dt = txt.split("\r\n")
                    b = data = ""
                    for i in dt:
                        b = i
                        break
                    for i in dt:
                        data += i + "\n"
                    txt = data
                    path2 += "\\" + dttxt + " " + b + "." + self.extension
                    with open(path2, "w") as file:
                        file.write(txt)
                    chk = 1
                    print(f"Luu file backup {path2} ok!")
            if chk == 1:
                self.result_label.config(text="Save backup file OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot Backup file!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot backup this ffile!!!")
            self.call_update()
    
    def get_link_folder_today(self):
        try:
            root = self.tree.getroot()
            folders = root.findall("folder")
            name = path = ""
            chk = 0
            for folder in folders:
                name = folder.attrib.get("name")
                path = folder.attrib.get("path")
                if name == "temp":
                    break
            if path != "":
                today = datetime.now()
                if today.day < 10:
                    strdate = "0" + str(today.day)
                else:
                    strdate = str(today.day)
                path = path + "\\" + strdate
                path = os.path.realpath(path)
                if os.path.exists(path):
                    print(f"Sao chep link thu muc {path} ok!")
                    pyperclip.copy(path)
                    chk = 1
            if chk == 1:
                self.result_label.config(text="Copy link folder OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot find this folder!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot copy this link folder!!!")
            self.call_update()
    
    def open_folder_temp_today(self):
        try:
            root = self.tree.getroot()
            folders = root.findall("folder")
            name = path = ""
            chk = 0
            for folder in folders:
                name = folder.attrib.get("name")
                path = folder.attrib.get("path")
                if name == "temp":
                    break
            if path != "":
                today = datetime.now()
                if today.day < 10:
                    strdate = "0" + str(today.day)
                else:
                    strdate = str(today.day)
                path = path + "\\" + strdate
                path = os.path.realpath(path)
                if os.path.exists(path):
                    print(f"Mo thu muc {path} ok!")
                    subprocess.call(["explorer.exe", path])
                    chk = 1
            if chk == 1:
                self.result_label.config(text="Open folder temp OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot find this folder!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot open this folder!!!")
            self.call_update()

    def RunRuleMail(self):
        try:
            self.attributes("-alpha", 1)
            t1 = ""
            try:
                root = self.tree.getroot()
                t1 = root.find("timerunrulemail").attrib.get("time")
            except:
                t1 = ""
            print(t1)
            if t1 == "":
                t1 = 5
            t1 = round(float(t1))
            print("Rule Mail function is running...")
            self.result_label.config(text=f"Rule Mail is running.... Auto click is running!!!")
            self.update()
            pyautogui.moveTo(-1030, 6, duration=0.5)
            pyautogui.click(clicks=2)
            pyautogui.moveTo(-1656, 50, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-1550, 93, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(-1115, 398, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-1115, 413, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-915, 716, duration=0.5)
            pyautogui.click()
            while(t1 > 0):
                self.result_label.config(text=f"Rule Mail is running.... Please wait {t1}s!!!")
                self.update()
                time.sleep(1)
                t1 -= 1
            pyautogui.moveTo(-815, 593, duration=0.5)
            pyautogui.click()
            pyautogui.hotkey('esc')
            pyautogui.moveTo(-1030, 6, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-1835, 46, duration=0.5)
            pyautogui.click()
            pyautogui.hotkey('esc')
            print("Run rule thanh cong!")
            self.result_label.config(text="Run rule complete!")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot run rule!!!")
            self.call_update()

    def prepare_runrule(self):
        t1 = ""
        try:
            root = self.tree.getroot()
            t1 = root.find("timewait").attrib.get("time")
        except:
            t1 = ""
        if t1 == "":
            t1 = 5
        t1 = round(float(t1))
        while t1 > 0:
            self.result_label.config(text=f"Rule mail will run after {t1}s!!!")
            self.update()
            t1 -= 1
            time.sleep(1)

        self.after(100, self.runrulenow)

    def runrulenow(self):
        self.result_label.config(text="Rule Mail is running....")
        self.after(100, self.RunRuleMail)
    
    def RunRuleMail2(self):
        try:
            self.attributes("-alpha", 1)
            t1 = ""
            try:
                root = self.tree.getroot()
                t1 = root.find("timerunrulemail").attrib.get("time")
            except:
                t1 = ""
            print(t1)
            if t1 == "":
                t1 = 5
            t1 = round(float(t1))
            print("Rule Mail function is running...")
            self.result_label.config(text=f"Rule Mail is running.... Auto click is running!!!")
            self.update()
            pyautogui.moveTo(890, 6)
            pyautogui.click(clicks=2)
            time.sleep(0.2)
            pyautogui.moveTo(264, 50)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.moveTo(370, 93)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(805, 376)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.moveTo(805, 391)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.moveTo(1005, 695)
            pyautogui.click()
            while(t1 > 0):
                self.result_label.config(text=f"Rule Mail is running.... Please wait {t1}s!!!")
                self.update()
                time.sleep(1)
                t1 -= 1
            pyautogui.moveTo(1105, 573)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.hotkey('esc')
            pyautogui.moveTo(890, 6)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.moveTo(85, 46)
            pyautogui.click()
            time.sleep(0.2)
            pyautogui.hotkey('esc')
            print("Run rule thanh cong!")
            self.result_label.config(text="Run rule complete!")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
            self.result_label.config(text="Cannot run rule!!!")
            self.call_update()
    
    def prepare_runrule2(self):
        t1 = ""
        try:
            root = self.tree.getroot()
            t1 = root.find("timewait").attrib.get("time")
        except:
            t1 = ""
        if t1 == "":
            t1 = 5
        t1 = round(float(t1))
        while t1 > 0:
            self.result_label.config(text=f"Rule mail will run after {t1}s!!!")
            self.update()
            t1 -= 1
            time.sleep(1)

        self.after(100, self.runrulenow)

    def runrulenow2(self):
        self.result_label.config(text="Rule Mail is running....")
        self.after(100, self.RunRuleMail2)

    def get_stringWeb(self):
        txt = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <WTSP_GETVERSION xmlns="http://www.pegatroncorp.com/SFISWebService/">
      <programId>TSP_RAYVND</programId>
      <programPassword>=?3f9Q</programPassword>
      <ISN>A829AC38JS7D</ISN>
      <device>820099</device>
      <type>ITEMINFO</type>
      <ChkData></ChkData>
      <ChkData2></ChkData2>
    </WTSP_GETVERSION>
  </soap:Body>
</soap:Envelope>"""
        pyperclip.copy(txt)
        self.result_label.config(text="Get stringWeb ok!")
        self.call_update()

    def Run_Webservice(self):
        try:
            if self.chk_child_window():
                self.windows_destroy()
            root = self.tree.getroot()
            link = root.find("webservice").attrib.get("link")
            url=link
            # headers = {'content-type': 'application/soap+xml'}
            headers = {'content-type': 'text/xml'}
            body = pyperclip.paste()
            response = requests.post(url,data=body,headers=headers)
            data = response.content
            xml = xmltodict.parse(data)
            txt2 = json.dumps(xml, indent=4)
            print(f"{txt2}")
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Result")
            self.dialog.geometry("900x640+{}+{}".format(510, 280))
            self.label = tk.Label(self.dialog, text="Data got from WEBSERVICE")
            self.label.pack()
            self.label_data = tk.Label(self.dialog, text="", wraplength=880)
            self.label_data.pack()
            self.button = tk.Button(self.dialog, text="Copy data", command=lambda: pyperclip.copy(txt2))
            self.button.pack()
            self.button.config(justify=tk.RIGHT)
            self.label_data.config(justify=tk.LEFT)
            self.label_data.config(text=txt2)
            self.label.config(text="Get data ok")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")

    def copy_button(self, data):
        try:
            pyperclip.copy(data)
        except Exception as e:
            print(f"Co loi: {e}")
            pyautogui.alert(text = f"{e}", title = "Error!", button = "Ok")
    
    def run_command(self, event):
        # Get user input
        command = self.input_box.get().lower()
        
        # Clear input box
        self.input_box.delete(0, tk.END)

             
        # Determine command to run
        if command == "?":
            self.open_dialog_showHelp()
        elif command == "config":
            if self.load_xmlfile():
                self.result_label.config(text="Load config file successful")
                self.call_update()
            else:
                self.result_label.config(text="Cannot load config file")
                self.call_update()
        elif command == "q":
            self.destroy()
        elif command == "cb":
            self.read_clipboard()
        elif command == "in":
            self.prepare_in()
        elif command == "in2":
            self.prepare_in2()
        elif command == "up":
            self.prepare_update()
        elif command == "test":
            messagebox.showinfo("Information!",self.dialog)
        elif command == "bt":
            self.prepare_between()
        elif command == "bt2":
            self.prepare_between2()
        elif command == "log":
            self.prepare_log()
        elif command == "bu":
            self.save_Backup()
        elif command == "save":
            self.get_link_folder_today()
        elif command == "qr":
            self.generate_qr_code()
        elif command == "gws":
            self.get_stringWeb()
        elif command == "rws":
            self.Run_Webservice()
        elif command == "n":
            self.open_dialog()
        elif command == "rep":
            self.prepare_sn_unknit()
        elif command == "tb":
            self.prepare_table()
        elif command == "cls":
            self.clear_cb()
        elif command == "vn":
            self.prepare_translate()
        elif command == "c":
            self.result_label.config(text="This function take few second. Please wait!!!")
            self.prepare_copy()
        elif command == "qw":
            self.windows_destroy()
            self.result_label.config(text="Close form complete!")
            self.call_update()
        elif command == "at":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use autofill by excel file function?")
            if chk:
                self.autofillex()
        elif command == "atc":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use autofill by clipboard file function?")
            if chk:
                self.autofillcb()
        elif command == "copy":
            self.prepare_copy2()
        elif command == "create":
            self.create_folder()
        elif command == "mail":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use run rule mail function?")
            if chk:
                self.prepare_runrule()
        elif command == "mail2":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use run rule mail function?")
            if chk:
                self.prepare_runrule2()
        elif command == "today":
            self.open_folder_temp_today()
        elif command[0:2] == "op":
            try:
                op = command[3:20]
                root = self.tree.getroot()
                files = root.findall("file")
                chk = 0
                for file in files:
                    name = file.attrib.get("name")
                    path = file.attrib.get("path")
                    if name == op:
                        path = os.path.realpath(path)
                        print(f"Mo file {path} thanh cong!")
                        os.startfile(path)
                        chk = 1
                if chk == 1:
                    self.result_label.config(text=f"Open {command[3:20].upper()} file ok!")
                    self.call_update()
                else:
                    self.result_label.config(text="Invalid command!")
                    self.call_update()
            except:
                self.result_label.config(text="Invalid command")
                self.call_update()
        else:
            try:
                root = self.tree.getroot()
                folders = root.findall("folder")
                chk = 0
                for folder in folders:
                    name = folder.attrib.get("name")
                    path = folder.attrib.get("path")
                    if name == command:
                        path = os.path.realpath(path)
                        subprocess.call(["explorer.exe", path])
                        chk = 1
                    elif name == command[0:4] and len(command) > 4:
                        chkyear = command[5:7]
                        chkmonth = "\\" + command[7:9] + command[5:7]
                        chkday = "\\" + command[9:11]
                        chkyear = "20" + chkyear
                        strpath = root.find("temp").attrib.get("path")
                        if os.path.exists(os.path.realpath(strpath + chkyear + chkmonth + chkday)):
                            lk = os.path.realpath(strpath + chkyear + chkmonth + chkday)
                            print(f"Mo folder: {lk} thanh cong!")
                            subprocess.call(["explorer.exe", lk])
                            print(lk)
                            chk = 1
                        elif os.path.exists(os.path.realpath(strpath + chkyear + chkmonth)):
                            lk = os.path.realpath(strpath + chkyear + chkmonth)
                            print(f"Mo folder: {lk} thanh cong!")
                            subprocess.call(["explorer.exe", lk])
                            print(strpath + chkyear + chkmonth)
                            chk = 1
                        elif os.path.exists(os.path.realpath(strpath + chkyear)):
                            lk = os.path.realpath(strpath + chkyear)
                            print(f"Mo folder: {lk} thanh cong!")
                            subprocess.call(["explorer.exe", lk])
                            print(strpath + chkyear)
                            chk = 1
                if chk == 1:
                    self.result_label.config(text=f"Open {command.upper()} folder ok!")
                    self.call_update()
                else:
                    self.result_label.config(text="Invalid command")
                    self.call_update()
            except:
                self.result_label.config(text="Invalid command")
                self.call_update()
        
if __name__ == "__main__":
    print("The program has been started successfully!!!\n\nProgram is running....")
    app = AlwaysOnTopGUI()
    app.mainloop()

