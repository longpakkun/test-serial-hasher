from codecs import charmap_decode
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox, simpledialog
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
import webbrowser
import shutil
import sys
import gamettt
import feedback
import view_data
import tetris
import hashlib
# import pia
os.environ['PYTHONIOENCODING'] = 'utf-8'

class SupportApp(tk.Tk):
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

        self.osname = os.getlogin()

        if(self.osname == ""):
            messagebox.showerror(title="Warning", message="You don't have a permission to use this software!")
            self.destroy()
        

        #Load file config
        if self.load_xmlfile():
            self.result_label.config(text=f"Loading config file ok!\nWelcome back {self.osname}")
            self.call_update()
        else:
            self.result_label.config(text="Can not find file config!!!\nWelcome back {self.osname}")
            self.call_update()

        # Create progress bar
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=int(self.wwidth) - 10)
        self.progress_bar.pack()
        self.progress_bar.pack_forget()

        # self.iconify()
        self.welcomeFrm()
        # self.after(2000, lambda: self.deiconify())
        self.after(2020, lambda: self.input_box.focus_set())

        style = ttk.Style()
        style.theme_use("clam")
        # self.bind("<Configure>", self.update_position)

    def welcomeFrm(self):
        dialog = tk.Toplevel(self)
        dialog.geometry("600x150+{}+{}".format(int(self.w/2-300), int(self.h/2-150/2)))
        dialog.attributes("-topmost", 1)
        dialog.overrideredirect(True)

        welcomelbl = tk.Label(dialog, text=f"New version:\nAdd: New function checkISN. Use the comman: isn\nADD: Convect Hex to Dec and Dec to hex. Use the command: h2d, d2h", font=("Arial", 15), wraplength=550, fg="#004040", background="#80ffff")
        welcomelbl.pack(fill="both", ipady=50)
        self.after(6000, lambda: (dialog.destroy()))

    def feedbackFrm(self):
        dialog = tk.Toplevel(self)
        feedback.feedback(dialog, int(self.w/2), int(self.h/2), self.osname)

    def view_dataFrm(self):
        dialog = tk.Toplevel(self)
        view_data.view_data(dialog, int(self.w/2), int(self.h/2))

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
    osname = blur = extension = ""
    moverule = False
    listtest = []

    def chk_child_window(self):
        try:
            test = self.dialog
            return True
        except:
            return False

    def load_variable(self):
        self.w, self.h = pyautogui.size()
        try:
            self.wwidth = self.tree.find("windows").attrib.get("width")
        except:
            self.wwidth = 250
        try:
            self.wheight = self.tree.find("windows").attrib.get("height")
        except:
            self.wheight = 60
        try:
            self.pwidth = self.tree.find("position").attrib.get("width")
        except:
            self.pwidth = self.w - 260
        try:
            self.pheight = self.tree.find("position").attrib.get("height")
        except:
            self.pheight = self.h - 132
        try:
            self.blur = self.tree.find("blur").attrib.get("value")
        except:
            self.blur = 0.5
        try:
            self.qrwidth = self.tree.find("qrcode").attrib.get("width")
        except:
            self.qrwidth = 300
        try:
            self.ontop = self.tree.find("alwaysontop").attrib.get("enable")
        except:
            self.ontop = 0
        try:
            self.extension = self.tree.find("backupfile").attrib.get("extension")
        except:
            self.extension = "txt"
        try:
            self.password = self.tree.find("password").attrib.get("pass")
        except:
            self.password = "173113ca9a612f9dd70b238042d87c0654cf3bab52d7049b82ad677cc151aeb4"

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
            messagebox.showwarning(message = f"{e}", title = "Error!")
            return False
            
    def read_clipboard(self):
        try:
            clipboard_contents = pyperclip.paste()
            self.result_label.config(text=clipboard_contents)
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Error! Clipboard has some special data.")
            self.call_update()
    
    def prepare_in1(self):
        try:
            data = pyperclip.paste()
            # print(data)
            
            countlen = 0
            intxt = "IN\n("
            dataar = data.split("\t")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
                if f.find("\n") != -1:
                    datai = f.split("\n")
                    f = ""
                    for i in datai:
                        f += i.strip() + "\n"
                    f = f.rstrip("\n")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            

    def prepare_log1(self):
        try:
            data = pyperclip.paste()

            intxt = """WITH temp AS ( 	SELECT '{}' dev, '{}' grp, '' track, '200' loglimit, '' sdate, '' edate FROM dual ), devt AS ( 	SELECT a.device, devicenm, line, section, grp, wktype, outdevid, devflag, paramno, CASE WHEN b.device IS NOT NULL AND d.device IS NOT NULL THEN 'Working' WHEN c.local_addr IS NOT NULL AND d.device IS NOT NULL THEN 'Working' END status, '' FROM device a LEFT JOIN device_cfg b ON a.device = b.device LEFT JOIN ap_status_check c ON to_char(a.device) = c.local_addr LEFT JOIN devinfo d ON a.device = d.device and d.class = 1 WHERE grp = (SELECT grp FROM temp) OR a.device = (SELECT dev FROM temp) ORDER BY status, device ), wkt AS ( 	SELECT wktype, actidx, action, control, ptyp, pfield, pflag, pclass, nname, actflag, ctrltyp FROM wk_act WHERE wktype IN (SELECT wktype FROM devt) ORDER BY wktype, actidx ), logct AS ( 	SELECT logtime, stp, track, message,'','','','','','','' FROM (SELECT logtime, stp, track, message,'','','','','','','' FROM log_stpc WHERE stp LIKE '%'||(SELECT dev FROM temp) AND track LIKE '%' || (SELECT track FROM temp) ||'%' AND message LIKE '%%' AND logtime BETWEEN to_date((SELECT nvl((SELECT sdate FROM temp), to_char(SYSDATE - 2,'yyyy/mm/dd hh24:mi:ss')) FROM dual),'yyyy/mm/dd hh24:mi:ss') AND to_date((SELECT nvl((SELECT edate FROM temp), to_char(SYSDATE,'yyyy/mm/dd hh24:mi:ss')) FROM dual),'yyyy/mm/dd hh24:mi:ss') ORDER BY logtime DESC) WHERE ROWNUM <= (SELECT CASE WHEN (SELECT sdate FROM temp) <> '' THEN '10000' ELSE (SELECT loglimit FROM temp) END FROM dual) ), logt AS ( 	SELECT logtime, stp, track, message,'','','','','','','' FROM (SELECT logtime, stp, track, message,'','','','','','','' FROM log_stp WHERE stp = 'CENTRIC:'||(SELECT dev FROM temp) AND track LIKE '%%' AND message LIKE '%%' AND logtime BETWEEN to_date((SELECT nvl((SELECT sdate FROM temp), to_char(SYSDATE - 2,'yyyy/mm/dd hh24:mi:ss')) FROM dual),'yyyy/mm/dd hh24:mi:ss') AND to_date((SELECT nvl((SELECT edate FROM temp), to_char(SYSDATE,'yyyy/mm/dd hh24:mi:ss')) FROM dual),'yyyy/mm/dd hh24:mi:ss') ORDER BY logtime DESC) WHERE ROWNUM <= (SELECT CASE WHEN (SELECT sdate FROM temp) <> '' THEN '10000' ELSE (SELECT loglimit FROM temp) END FROM dual) ), devinfot AS ( 	SELECT device, seq, class, info, logtime, infocase, info_nm, '', '', '', '' FROM devinfo WHERE device = (SELECT dev FROM temp) ORDER BY seq ), devcfg AS ( 	SELECT devtype, device, devid, sid, ip, apid, pageid, op, lastupd, flag, memo FROM device_cfg WHERE device IN (SELECT device FROM devt) ), apstatust AS ( 	SELECT apid, apver, HOST, afar_addr, local_addr, ip, op, lastupd, '', '', '' FROM AP_STATUS_CHECK WHERE local_addr IN (SELECT to_char(device) FROM devt) ), iotype AS ( 	SELECT device, outdevid, outtype, outtypedesc, labtype FROM devoutput WHERE device IN (SELECT dev FROM temp) ) SELECT 'DEVICE table' col1,'----DEVICE NAME----' col2,'----LINE----' col3,'----SECTION----' col4,'----GRP----' col5,'----WKTYPE----' col6,'----OUTDEVID----' col7,'----DEVFLAG----' col8,'----PARAMNO----' col9,'----STATUS----' col10,'--------' col11 FROM dual UNION ALL SELECT to_char(device), devicenm, line, section, grp, wktype, outdevid, devflag, to_char(paramno), status,'' FROM devt UNION ALL SELECT '----DEVOUTPUT table----' col1,'----OUTDEVID----' col2,'----OUTTYPE----' col3,'----OUTTYPEDESC----' col4,'----LABTYPE----' col5,'--------' col6,'--------' col7,'--------' col8,'--------' col9,'--------' col10,'--------' col11 FROM dual UNION ALL SELECT to_char(device), to_char(outdevid), to_char(outtype), outtypedesc, labtype, '', '', '', '', '', '' FROM iotype UNION ALL SELECT '----DEVINFO table----' col1,'----SEQ----' col2,'----CLASS----' col3,'----INFO----' col4,'----LOGTIME----' col5,'----INFOCASE----' col6,'----INFO_NM----' col7,'--------' col8,'--------' col9,'--------' col10,'--------' col11 FROM dual UNION ALL SELECT to_char(device), to_char(seq), to_char(class), info, to_char(logtime, 'yyyy/mm/dd hh24:mi:ss'), infocase, info_nm, '', '', '', '' FROM devinfot UNION ALL SELECT '----WKTYPE table----' col1,'----ACTIDX----' col2,'----ACTION----' col3,'----CONTROL----' col4,'----PTYP----' col5,'----PFIELD----' col6,'----PFLAG----' col7,'----PCLASS----' col8,'----NNAME----' col9,'----ACTFLAG----' col10,'----CTRLTYP----' col11 FROM dual UNION ALL SELECT wktype, to_char(actidx), action, control, ptyp, pfield, pflag, to_char(pclass), nname, actflag, ctrltyp FROM wkt UNION ALL SELECT '----DEVICE_CFG table----' col1,'----DEVICE----' col2,'----DEVID----' col3,'----SID----' col4,'----IP----' col5,'----APIP----' col6,'----PAGEID----' col7,'----OP----' col8,'----LAST UPDATE----' col9,'----FLAG----' col10,'----MEMO----' col11 FROM dual UNION ALL SELECT devtype, to_char(device), devid, sid, ip, apid, pageid, op, to_char(lastupd, 'yyyy/mm/dd hh24:mi:ss'), flag, memo FROM devcfg UNION ALL SELECT '----AP_STATUS_CHECK table----' col1,'----APVER----' col2,'----HOST----' col3,'----AFAR_ADDR----' col4,'----LOCAL_ADDR----' col5,'----IP----' col6,'----OP----' col7,'----LAST UPDATE----' col8,'--------' col9,'--------' col10,'--------' col11 FROM dual UNION ALL SELECT apid, apver, HOST, afar_addr, local_addr, ip, op, to_char(lastupd, 'yyyy/mm/dd hh24:mi:ss'), '', '', '' FROM APSTATUST UNION ALL SELECT '----LOG table----' col1,'----STP----' col2,'----TRACK----' col3,'----MESSAGE----' col4,'--------' col5,'--------' col6,'--------' col7,'--------' col8,'--------' col9,'--------' col10,'--------' col11 FROM dual UNION ALL SELECT to_char(logtime, 'yyyy/mm/dd hh24:mi:ss'), stp, track, message,'','','','','','','' FROM logct UNION ALL SELECT to_char(logtime, 'yyyy/mm/dd hh24:mi:ss'), stp, track, message,'','','','','','','' FROM logt;"""
            device = ""
            grp = ""
            if data.isdecimal() and len(data) == 6 :
                device = data
                grp = ""
            else :
                device = ""
                grp = data

            intxt = intxt.format(device, grp)

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
            self.attributes("-alpha", 1)
            print ('bắt đầu ')
            excelname = ""
            special_cmd = "0"
            t1 = ""
            fdata = ""
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
                excelname = 'D:/test.txt'
                special_cmd = "0"
            excelname = os.path.realpath(path=excelname)
            # read by default 1st sheet of an excel file
            with open(excelname, "r") as file:
                fdata = file.read()
            # dataframe1 = pd.read_excel(excelname)
            count=chk=0
            fdata = fdata.split("\n")
            for i in fdata:
                count += 1
            self.progress_bar.config(maximum=count)
            self.progress_bar.pack()
            self.listener = pynput.keyboard.Listener(on_press=self.on_key_press)
            print(self.listener)
            if not self.listener.is_alive():
                self.listener.start()
            print("Bat dau nghe ban phim")
            for index in fdata:
                if not self.listener.is_alive():
                    print("Khong thay tin hieu nghe")
                    chk = 1
                    break
                if special_cmd == "1":
                    pyautogui.typewrite("ef-aoiloc-0")    
                    pyautogui.press("enter")
                    time.sleep(t1)
                pyautogui.typewrite(index.strip())    
                pyautogui.press("enter")
                print (index.strip())
                self.progress_bar['value'] += 1
                self.result_label.config(text=f"ITEM remaining: {str(count)}")
                self.update()
                count -= 1
                # thời gian chờ giữa 2 lần 
                time.sleep(t1)
            print("Ket thuc nghe ban phim")
            self.listener.stop()
            self.progress_bar.pack_forget()
            self.progress_bar['value'] = 0
            if chk == 0:
                self.result_label.config(text="Auto fill complete!")
            else:
                self.result_label.config(text=f"Auto fill complete! {count} didn't run yet.")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            print("File not found or empty!")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")

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
            self.progress_bar.config(maximum=dem)
            self.progress_bar.pack()
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
                self.progress_bar['value'] += 1
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
            self.progress_bar.pack_forget()
            self.progress_bar['value'] = 0
            if chk == 0:
                self.result_label.config(text="Auto fill complete!")
            else:
                self.result_label.config(text=f"Auto fill complete! {dem} didn't run yet.")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")

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
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Error! Clipboard has some special data.") 
            self.call_update()

    def open_dialog_showQRCODE(self):
        try:
            if self.chk_child_window():
                self.windows_destroy()
            width = int(self.qrwidth)+50
            height = int(self.qrwidth)+100
            pw = self.w/2 - (width/2)
            ph = self.h/2 - (height/2)
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Result")
            self.dialog.geometry("{}x{}+{}+{}".format(width, height,int(pw),int(ph)))
            self.dialog.resizable(False, False)
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
            messagebox.showwarning(message = f"{e}", title = "Error!")

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
            messagebox.showwarning(message = f"{e}", title = "Error!")
   
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            self.dialog.geometry("400x408+{}+{}".format(int(self.w/2-200), int(self.h/2-408/2)))
            self.dialog.resizable(False, False)
            self.label = tk.Label(self.dialog, text="All commands can be used", font=("Arial", 10, "bold"))
            self.label.pack()
            self.label1 = tk.Label(self.dialog, text="Copyright by Nick_Pham & Happy_Luu", font=("Arial", 8))
            self.label1.pack()
            intxt = """
?: Show this windows
in: Preparing 'in' command SQL
in2: Preparing 'in' command SQL with over 1000 line
log or log1: Preparing 'log' command SQL
isn: Preparing check ISN command SQL
bt: Preparing 'between' command
cls: CLear clipboard
vn: Preparing command to translate with chatGPT
rep: Preparing the command SN_UNKNIT
atc: Run auto paste data from clipboard
at: Run auto paste data from excel
up: Preparing the UPDATE command SQL
w <command>: Open website's link was configed in the config file
op <command>: Open file was configed in the config file.
<command>: Open folder was configed in the config file
c: Preparing copy data
qw: Close sub window.
tb: Preparing data to create device
game: Running game
feedback: Send request for Author.
logout <namedb> <device>: Logout device namedb like vnkr.
h2d: Convert Hex to Dec
d2h: Conver Dec to Hec
q: Quit
            """
            self.label2 = tk.Label(self.dialog, text=intxt, wraplength=480, justify=tk.LEFT)
            self.label2.pack(fill="both", padx=5)
            print("Show Help")
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")

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
            self.result_label.config(text="Preparing copy complete!")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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

    def create_Sharefolder(self):
        try:
            chk = "";
            sharefolder = r"\\PVN-LANFS-01.PVN.CORP.PEGATRON\PVN_admin$\GBA-00228915\ITS\SOP\Nick\NOTE"
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%Y%m")
            monpath = r"{0}\{1}".format(sharefolder, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if not os.path.exists(daypath):
                os.mkdir(daypath)
            dem = 1
            while True:
                subpath = r"{}\{:003d}".format(daypath, dem)
                if os.path.exists(subpath):
                    userpath = r"{}\__{}.txt".format(subpath, self.osname)
                    if os.path.exists(userpath):
                        dem += 1
                    else:
                        dem += 1
                else:
                    os.mkdir(subpath)
                    open(r"{}\__{}.txt".format(subpath, self.osname), "x")
                    subprocess.call(["explorer.exe", subpath])
                    chk = "new"
                    break
            if chk == "new":
                self.result_label.config(text="Create share folder ok!!!")
                self.call_update()
            elif chk == "exist":
                self.result_label.config(text="Open share folder ok!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot create new folder!!!")
            self.call_update()

    def open_Sharefolder(self, note):
        try:
            chk = False
            sharefolder = r"\\PVN-LANFS-01.PVN.CORP.PEGATRON\PVN_admin$\GBA-00228915\ITS\SOP\Nick\NOTE"
            if len(note) == 3:
                sub = note
                today = datetime.now()
                daystr = today.strftime("%d")
                monstr = today.strftime("%Y%m")
                sub = "";
                
                monpath = r"{0}\{1}".format(sharefolder, monstr)
                daypath = r"{0}\{1}".format(monpath, daystr)
                subpath = r"{}\{}".format(daypath, note)
                if os.path.exists(subpath):
                    subprocess.call(["explorer.exe", subpath])
                    chk = True
            elif len(note) == 11:
                monstr = note[0:6]
                daystr = note[6:8]
                sub = note[8:11]

                monpath = r"{0}\{1}".format(sharefolder, monstr)
                daypath = r"{0}\{1}".format(monpath, daystr)
                subpath = r"{}\{}".format(daypath, sub)
                if os.path.exists(subpath):
                    subprocess.call(["explorer.exe", subpath])
                    chk = True
            elif len(note) == 8:
                monstr = note[0:6]
                daystr = note[6:8]

                monpath = r"{0}\{1}".format(sharefolder, monstr)
                daypath = r"{0}\{1}".format(monpath, daystr)
                if os.path.exists(daypath):
                    subprocess.call(["explorer.exe", daypath])
                    chk = True
            elif len(note) == 6:
                monstr = note[0:6]

                monpath = r"{0}\{1}".format(sharefolder, monstr)
                if os.path.exists(monpath):
                    subprocess.call(["explorer.exe", monpath])
                    chk = True

            if chk:
                self.result_label.config(text="Open share folder ok!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot Open share folder ok!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot open folder!!!")
            self.call_update()

    def create_folder(self):
        try:
            chk = False
            sharefolder = self.tree.find("temp").attrib.get("path")
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%m%y")
            yearstr = today.strftime("%Y")
            yearpath = r"{0}\{1}".format(sharefolder, yearstr)
            if not os.path.exists(yearpath):
                os.mkdir(yearpath)
            monpath = r"{0}\{1}".format(yearpath, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if not os.path.exists(daypath):
                os.mkdir(daypath)
                chk = True
            if chk:
                self.result_label.config(text="Create folder ok!!!")
                self.call_update()
            else:
                self.result_label.config(text="Folder has existed ok!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot create new folder!!!")
            self.call_update()

    def save_Backup(self):
        try:
            chk = False
            sharefolder = self.tree.find("temp").attrib.get("path")
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%m%y")
            yearstr = today.strftime("%Y")
            yearpath = r"{0}\{1}".format(sharefolder, yearstr)
            if not os.path.exists(yearpath):
                os.mkdir(yearpath)
            monpath = r"{0}\{1}".format(yearpath, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if os.path.exists(daypath):
                chk = True
                if os.path.exists(daypath):
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
                    daypath += "\\" + dttxt + " " + b + "." + self.extension
                    with open(daypath, "w") as file:
                        file.write(txt)
                    chk = True
                    print(f"Luu file backup {daypath} ok!")
            if chk:
                self.result_label.config(text="Save backup file OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot Backup file!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot backup this ffile!!!")
            self.call_update()
    
    def get_link_folder_today(self):
        try:
            chk = False
            sharefolder = self.tree.find("temp").attrib.get("path")
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%m%y")
            yearstr = today.strftime("%Y")
            yearpath = r"{0}\{1}".format(sharefolder, yearstr)
            if not os.path.exists(yearpath):
                os.mkdir(yearpath)
            monpath = r"{0}\{1}".format(yearpath, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if os.path.exists(daypath):
                print(f"Sao chep link thu muc {daypath} ok!")
                pyperclip.copy(daypath)
                chk = True
            if chk:
                self.result_label.config(text="Copy link folder OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot find this folder!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot copy this link folder!!!")
            self.call_update()

    def uploadFile(self, name):
        try:
            if name != "":
                sourcePath = r"D:\python\{}.py".format(name)
                desPath = r"\\10.177.113.250\data$\Happy\python\{}.py".format(name)
            else:
                sourcePath = r"D:\python\SupportApp.py"
                desPath = r"\\10.177.113.250\data$\Happy\python\SupportApp.py"
            shutil.copy(sourcePath, desPath)
            self.result_label.config(text="Upload file ok!!!")
            self.call_update()
        except Exception as e:
            print("Co loi: {}".format(e))
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot upload file!!!")
            self.call_update()

    def create_PPTFILE(self, namefile):
        try:
            sourcePath = "C:\\Users\\happy_luu\\OneDrive - PEGATRON CORPORATION\\Working data\\MR Happy\\Document\\Support for work\\SOP TEMP.pptx"
            sourcePath = os.path.realpath(sourcePath)

            chk = False
            sharefolder = self.tree.find("temp").attrib.get("path")
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%m%y")
            yearstr = today.strftime("%Y")
            yearpath = r"{0}\{1}".format(sharefolder, yearstr)
            if not os.path.exists(yearpath):
                os.mkdir(yearpath)
            monpath = r"{0}\{1}".format(yearpath, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if os.path.exists(daypath):
                print(f"Sao chep link thu muc {daypath} ok!")
                shutil.copy(src = sourcePath, dst= daypath)
                if namefile != "":
                    os.rename(daypath + "\\SOP TEMP.pptx", daypath + "\\{}.pptx".format(namefile))
                    daypath += "\\{}.pptx".format(namefile);
                else:
                    os.rename(daypath + "\\SOP TEMP.pptx", daypath + "\\Test .pptx")
                    daypath += "\\Test .pptx";
                os.startfile(daypath)
                chk = True

            if chk:
                self.result_label.config(text="Create file Power point ok!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot create file!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot copy file!!!")
            self.call_update()
    
    def open_folder_temp_today(self):
        try:
            chk = False
            sharefolder = self.tree.find("temp").attrib.get("path")
            today = datetime.now()
            daystr = today.strftime("%d")
            monstr = today.strftime("%m%y")
            yearstr = today.strftime("%Y")
            yearpath = r"{0}\{1}".format(sharefolder, yearstr)
            if not os.path.exists(yearpath):
                os.mkdir(yearpath)
            monpath = r"{0}\{1}".format(yearpath, monstr)
            if not os.path.exists(monpath):
                os.mkdir(monpath)
            daypath = r"{0}\{1}".format(monpath, daystr)
            if os.path.exists(daypath):
                chk = True
                print(f"Mo thu muc {daypath} ok!")
                subprocess.call(["explorer.exe", os.path.realpath(daypath)])
            if chk:
                self.result_label.config(text="Open folder temp OK!!!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot find this folder!!!")
                self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
            self.progress_bar.config(maximum=t1)
            print("Rule Mail function is running...")
            self.result_label.config(text=f"Rule Mail is running.... Auto click is running!!!")
            self.update()
            if not self.moverule:
                pyautogui.moveTo(176, 1060, duration=0.2)
                pyautogui.click()
            pyautogui.moveTo(-1856, 192, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-1030, 6, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-1656, 50, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-1550, 93, duration=0.2)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.moveTo(-1115, 398, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-1115, 413, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-915, 716, duration=0.2)
            pyautogui.click()
            time.sleep(1)
            while(t1 > 0):
                self.progress_bar.pack()
                self.progress_bar['value'] += 1
                self.result_label.config(text=f"Rule Mail is running.... Please wait {t1}s!!!")
                self.update()
                time.sleep(1)
                t1 -= 1
            self.progress_bar.pack_forget()
            self.progress_bar['value'] = 0
            self.result_label.config(text=f"Rule Mail is running.... Auto click is running!!!")
            self.update()
            pyautogui.moveTo(-815, 593, duration=0.2)
            pyautogui.click()
            pyautogui.hotkey('esc')
            pyautogui.moveTo(-1030, 6, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-1835, 46, duration=0.2)
            pyautogui.click()
            pyautogui.hotkey('esc')
            print("Run rule thanh cong!")
            self.result_label.config(text="Run rule complete!")
            self.call_update()
            self.load_blurform()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
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
    
    def RunMoveMail(self):
        try:
            self.attributes("-alpha", 1)
            print("Moving Mail function is running...")
            self.result_label.config(text=f"Moving Mail is running.... Auto click is running!!!")
            self.update()
            pyautogui.moveTo(176, 1060, duration=0.2)
            pyautogui.click()
            pyautogui.moveTo(-1850, 136, duration=0.5)
            pyautogui.click()
            pyautogui.moveTo(-1459, 100, duration=1)
            pyautogui.mouseDown(button='left')
            pyautogui.dragTo(-1851, 206, duration=1, button='left')
            pyautogui.mouseUp(-1851, 206, button='left', duration=1)
            time.sleep(1)
            pyautogui.click()
            print("Chuyen mail thanh cong!")
            self.result_label.config(text="Moving mail to inbox complete!")
            self.call_update()
            self.load_blurform()
            if self.moverule:
                self.RunRuleMail()
            self.moverule = False
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
            self.result_label.config(text="Cannot moving mail!!!")
            self.call_update()
    
    def prepare_movemail(self):
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

        self.after(100, self.MoveMail)

    def MoveMail(self):
        self.result_label.config(text="Rule Mail is running....")
        self.after(100, self.RunMoveMail)

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
            webservice = self.get_link_Webservice(root.find("webservice").attrib.get("link"))
            link = webservice[0]
            userid = webservice[1]
            password = webservice[2]
            isn = root.find("webservice").attrib.get("isn")
            device = root.find("webservice").attrib.get("device")
            type = root.find("webservice").attrib.get("type")
            temp = root.find("webservice").attrib.get("temp")
            temp2 = root.find("webservice").attrib.get("temp2")
            url=link
            
            # headers = {'content-type': 'application/soap+xml'}
            headers = {'content-type': 'text/xml'}
            body = pyperclip.paste()
            body = body.format(userid, password, isn, device, type, temp, temp2)
            response = requests.post(url,data=body,headers=headers)
            data = response.content.decode("utf-8")
            # xml = xmltodict.parse(data)
            # txt2 = json.dumps(xml, indent=4)
            # txt2 = txt2.replace("\\u007f", "\n\t")
            xml = ET.fromstring(data)
            txt2 = xml[0][0][0].text
            txt2 = txt2.replace('\x7F', "\n")
            print(f"{txt2}")
            self.dialog = tk.Toplevel(self)
            self.dialog.title("Result")
            self.dialog.geometry("750x300+{}+{}".format(int(self.w/2-750/2), int(self.h/2-150)))
            framelbl = tk.Frame(self.dialog)
            framelbl.pack(side="top",fill="x")
            lblfont = font.Font(family="Arial", size=20, weight="bold")
            self.label_data = tk.Label(framelbl, text="Data from WEBSERVICE", font=lblfont)
            self.label_data.pack(pady=10)
            frametxt = tk.Frame(self.dialog)
            frametxt.pack(fill="both", expand=True)
            self.text_data = tk.Text(frametxt, font=("Arial", 10))
            self.text_data.pack(pady=10, padx=10, side="top",fill="both", expand=True)
            self.text_data.insert(tk.END, txt2)
            self.text_data.config(state="disabled")
            self.result_label.config(text="Get data ok")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")

    def Run_Webservice2(self):
        try:
            dem = 0
            fdata = ""
            today = datetime.now()
            data = "Log\n"
            datas = pyperclip.paste()
            datas = datas.split("\r\n")
            if self.chk_child_window():
                self.windows_destroy()
            root = self.tree.getroot()
            webservice = self.get_link_Webservice(root.find("webservice").attrib.get("link"))
            link = webservice[0]
            userid = webservice[1]
            password = webservice[2]
            device = root.find("webservice").attrib.get("device")
            type = root.find("webservice").attrib.get("type")
            temp = root.find("webservice").attrib.get("temp")
            temp2 = root.find("webservice").attrib.get("temp2")
            linkfile = root.find("webservice").attrib.get("linkfile")
            if linkfile == "":
                linkfile = "test.txt"
            path = os.path.realpath(linkfile)
            with open(path, "r") as file:
                fdata = file.read()
            url=link
            # headers = {'content-type': 'application/soap+xml'}
            for i in datas:
                dem += 1
            self.progress_bar.config(maximum=dem)
            self.progress_bar.pack()
            for i in datas:
                if i == "":
                    break
                headers = {'content-type': 'text/xml'}
                body = fdata.format(userid, password, i.strip(), device, type, temp, temp2)
                response = requests.post(url,data=body,headers=headers)
                result = response.content
                xml = xmltodict.parse(result)
                data += today.strftime("%Y/%m/%d %H:%M:%S") + "\n______________________________________________\n" + json.dumps(xml, indent=4).replace("\\u007f", "\n\t") + "\n" 
                dem -= 1
                time.sleep(0.5)
                self.progress_bar['value'] += 1
                self.result_label.config(text=f"ITEM remaining: {str(dem)}")
                self.update()
            with open("log-{}.txt".format(today.strftime("%Y%m%d")), "a", encoding="utf-8") as file:
                file.write(data)
            self.progress_bar['value'] = 0
            self.progress_bar.pack_forget()
            self.result_label.config(text="Run WEBSERVICE ok")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
    
    def Run_Webservice3(self):
        try:
            dem = 0
            fdata = ""
            today = datetime.now()
            data = "Log\n"
            datas = pyperclip.paste()
            datas = datas.split("\r\n")
            if self.chk_child_window():
                self.windows_destroy()
            root = self.tree.getroot()
            webservice = self.get_link_Webservice(root.find("webservice").attrib.get("link"))
            link = webservice[0]
            userid = webservice[1]
            password = webservice[2]
            device = root.find("webservice").attrib.get("device")
            type = root.find("webservice").attrib.get("type")
            temp = root.find("webservice").attrib.get("temp")
            temp2 = root.find("webservice").attrib.get("temp2")
            linkfile = "webservicestring_smt.xml"
            special_cmd = "0"
            special_code = "ef-aoiloc-0"
            self.result_label.config(text=f"database: {str(webservice)}")
            try: 
                special_cmd = self.tree.find("special_command_loc_0").attrib.get("enable")
            except:
                special_cmd = "0"
            if linkfile == "":
                linkfile = "test.txt"
            path = os.path.realpath(linkfile)
            with open(path, "r") as file:
                fdata = file.read()
            url=link
            # headers = {'content-type': 'application/soap+xml'}
            for i in datas:
                dem += 1
            self.progress_bar.config(maximum=dem)
            self.progress_bar.pack()
            for i in datas:
                if special_cmd == "1":
                    headers = {'content-type': 'text/xml'}
                    body = fdata.format(userid, password, special_code, device, type)
                    response = requests.post(url,data=body,headers=headers)
                    result = response.content
                if i == "":
                    break
                headers = {'content-type': 'text/xml'}
                body = fdata.format(userid, password, i.strip(), device, type)
                response = requests.post(url,data=body,headers=headers)
                result = response.content
                xml = xmltodict.parse(result)
                data += today.strftime("%Y/%m/%d %H:%M:%S") + "\n______________________________________________\n" + json.dumps(xml, indent=4).replace("\\u007f", "\n\t") + "\n" 
                dem -= 1
                time.sleep(0.0005)
                self.progress_bar['value'] += 1
                self.result_label.config(text=f"ITEM remaining: {str(dem)}")
                self.update()
            with open("log-{}.txt".format(today.strftime("%Y%m%d")), "a", encoding="utf-8") as file:
                file.write(data)
            self.progress_bar['value'] = 0
            self.progress_bar.pack_forget()
            self.result_label.config(text="Run WEBSERVICE ok")
            self.call_update()
        except Exception as e:
            print(f"Co loi: {e}")
            messagebox.showwarning(message = f"{e}", title = "Error!")
    
    def get_link_Webservice(self, dbname):
        data = []
        if dbname == "vnkr":
            data = ["http://pvn-sftsp-n1.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnnc":
            data = ["http://pvn-sftsp-n5.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vntz":
            data = ["http://pvn-sftsp-n2.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnjl":
            data = ["http://pvn-sftsp-n4.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnfb":
            data = ["http://pvn-sftsp-n6.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]
        elif dbname == "vhgu":
            data = ["http://10.177.33.16/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnso":
            data = ["http://pvn-sftsp-n3.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]
        elif dbname == "vnkrdb0":
            data = ["http://pvn-sftsp-n1.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnncdb0":
            data = ["http://pvn-sftsp-n5.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vntzdb0":
            data = ["http://pvn-sftsp-n2.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnjldb0":
            data = ["http://pvn-sftsp-n4.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnfbdb0":
            data = ["http://pvn-sftsp-n6.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]
        elif dbname == "vhgudb0":
            data = ["http://10.177.33.16/SFISWebService/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnsodb0":
            data = ["http://pvn-sftsp-n3.sfis.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]
        elif dbname == "vnkrdb0qa":
            data = ["http://pvn-sftsp-n1.sfis.pegatroncorp.com/SFISWebService_VNKRDB0QA/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnncdb0qa":
            data = ["http://pvn-sftsp-n5.sfis.pegatroncorp.com/SFISWebService_VNNCDB0QA/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vntzdb0qa":
            data = ["http://pvn-sftsp-n2.sfis.pegatroncorp.com/SFISWebService_VNTZDB0QA/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnjldb0qa":
            data = ["http://pvn-sftsp-n4.sfis.pegatroncorp.com/SFISWebService_VNJLDB0QA/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnfbdb0qa":
            data = ["http://pvn-sftsp-n6.sfis.pegatroncorp.com/SFISWebService_VNFBDB0QA/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]
        elif dbname == "vhgudb0qa":
            data = ["http://172.24.255.10/SFISWebService_VHGUDB0QA/SFISTSPWebService.asmx","TSP_SYSENG","pas0g#rl"]
        elif dbname == "vnsodb0qa":
            data = ["http://pvn-sftsp-n3.sfis.pegatroncorp.com/SFISWebService_VNSOFS0QA/SFISTSPWebService.asmx","TSP_ATSHH","pap_ahga"]

        return data
    
    def logoutDevice(self, dbname, device):
        datadb = self.get_link_Webservice(dbname=dbname)
        xml = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <WTSP_LOGINOUT xmlns="http://www.pegatroncorp.com/SFISWebService/">
      <programId>{}</programId>
      <programPassword>{}</programPassword>
      <op>V20000012</op>
      <password>string</password>
      <device>{}</device>
      <TSP>string</TSP>
      <status>2</status>
    </WTSP_LOGINOUT>
  </soap:Body>
</soap:Envelope>"""
        try:
            headers = {'content-type': 'text/xml'}
            body = xml.format(datadb[1], datadb[2], device)
            url = datadb[0]
            response = requests.post(url=url, data=body, headers=headers)
            data = response.content.decode("utf-8")
            xmlstr = ET.fromstring(data)
            txt2 = xmlstr[0][0][0].text
            txt2 = txt2.replace('\x7F', "\n")
            print(f"{txt2}")
            messagebox.showinfo(title="Result", message=txt2)
            self.result_label.config(text="Running function ok!")
            self.call_update()
        except Exception as e:
            print("Co loi: {}".format(e))
            messagebox.showerror(title="Error!!!", message=e)
    
    def prepare_isnkp(self):
        try:
            txt = ""
            data = pyperclip.paste()
            data = data.split("\r\n")
            for i in data:
                if i == "":
                    break
                txt += f"UPDATE isn_kp SET outtime = outtime + INTERVAL '1' MINUTE WHERE isn = '{i.strip()}' AND mo_route_seq IN (SELECT seq FROM (SELECT isn, erridx, MAX (mo_route_seq) seq FROM isn_kp WHERE isn = '{i.strip()}' AND kpbc = 'CU' GROUP BY isn, erridx));"
                txt += "\n\n"
            for i in data:
                if i == "":
                    break
                txt += "select * from isn_kp where isn = '{}';\n".format(i)
            txt = txt.strip("\n")
            pyperclip.copy(txt)
            print(f"repare update testtime in the ISN_KP complete!!!\n{txt}")
            self.result_label.config(text="Prepare update outtime in the ISN_KP complete!!!")
            self.call_update()
        except Exception as e:
            print(f"Co loi {e}")
            messagebox.showwarning("Warnning!", f"Please check the error: {e}")

    def prepare_snerr(self):
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
            data = f"UPDATE snerr SET testtime = testtime + INTERVAL '1' MINUTE WHERE sn {intxt} AND mo_route_seq IN (SELECT mo_route_seq FROM (SELECT sn, MAX (mo_route_seq) mo_route_seq FROM snerr WHERE sn {intxt} GROUP BY sn));\n\n"
            for i in dataar:
                if i == "":
                    break
                data += "select * from snerr where sn = '{}';\n".format(i)
            data = data.strip("\n")
            pyperclip.copy(data)
            print(f"repare update testtime in the SNERR complete!!!\n{data}")
            self.result_label.config(text="Prepare update testtime in the SNERR complete!!!")
            self.call_update()
        except Exception as e:
            print(f"Co loi {e}.")
            messagebox.showwarning("Warnning!", f"Please check the error: {e}")
    
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def run_game(self, id):
        self.windows_destroy()
        self.dialog = tk.Toplevel(self)
        if id == 0:
            gamettt.gamettt(self.dialog)
        elif id == 1:
            game = tetris.Tetris(self.dialog, True)
            game.start()
        # elif id == 2:
        #     try:
        #         pia.start()
        #     except:
        #         pass
        self.result_label.config(text="Run game ok!!!")
        self.call_update()

    def update_config(self, element, name, path):
        try:
            root = self.tree.getroot()
            data = root.findall(element)
            for i in data:
                if i.attrib.get("name") == name:
                    i.attrib["path"] = path
            self.tree.write(os.path.realpath("a.config"), encoding="utf-8", xml_declaration=True, method="xml")
            self.result_label.config(text="Updating config successful!")
            self.call_update()
        except Exception as e:
            print("Co loi: {}".format(e))
            messagebox.showerror(title="Error", message=e)

    def update_position(self, event):
        try:
            x = event.x
            y = event.y
            root = self.tree.getroot()
            root.find("position").attrib["width"] = str(x)
            root.find("position").attrib["height"] = str(y)
            self.tree.write(os.path.realpath("a.config"), encoding="utf-8", xml_declaration=True, method="xml")
        except Exception as e:
            pass
    
    def check_ISN(self):
        try:
            data = pyperclip.paste()
            intxt = """WITH temp AS ( 	SELECT '{}' isn, '1' chk2isn, '' searchitem FROM dual ), chkisnmac AS ( 	SELECT CASE WHEN (SELECT chk2isn FROM temp) != 0 and exists(select isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn_sn_mac WHERE mac = (SELECT isn FROM temp))) AND (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn_sn_mac WHERE mac = (SELECT isn FROM temp))) IS NOT NULL THEN (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn_sn_mac WHERE mac = (SELECT isn FROM temp))) ELSE (SELECT isn FROM isn_sn_mac WHERE mac = (SELECT isn FROM temp)) END isn FROM dual ), chkisninfo AS (     SELECT CASE WHEN (SELECT chk2isn FROM temp) != 0 and EXISTS(SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isninfo WHERE imei = (SELECT isn FROM temp) OR sn2 = (SELECT isn FROM temp) OR mac1 = (SELECT isn FROM temp))) OR (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isninfo WHERE imei = (SELECT isn FROM temp) OR sn2 = (SELECT isn FROM temp) OR mac1 = (SELECT isn FROM temp))) IS NOT NULL THEN (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isninfo WHERE imei = (SELECT isn FROM temp) OR sn2 = (SELECT isn FROM temp) OR mac1 = (SELECT isn FROM temp))) ELSE (SELECT isn FROM isninfo WHERE imei = (SELECT isn FROM temp) OR sn2 = (SELECT isn FROM temp) OR mac1 = (SELECT isn FROM temp)) END isn FROM dual ), chkssn AS ( 	SELECT CASE WHEN (SELECT chk2isn FROM temp) != 0 AND EXISTS(SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn WHERE ssn = (SELECT isn FROM temp))) AND (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn WHERE ssn = (SELECT isn FROM temp))) IS NOT NULL THEN (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn WHERE ssn = (SELECT isn FROM temp))) ELSE (SELECT isn FROM isn WHERE ssn = (SELECT isn FROM temp)) END isn FROM dual ), chkisn AS ( 	SELECT CASE WHEN (SELECT chk2isn FROM temp) != 0 and exists(SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM temp)) AND (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM temp)) IS NOT NULL THEN (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM temp)) WHEN exists(SELECT isn FROM chkisninfo) AND (SELECT isn FROM chkisninfo) IS NOT NULL THEN (SELECT isn FROM chkisninfo) WHEN EXISTS(SELECT isn FROM chkisnmac) AND (SELECT isn FROM chkisnmac) IS NOT NULL THEN (SELECT isn FROM chkisnmac) WHEN EXISTS(SELECT isn FROM chkssn) AND (SELECT isn FROM chkssn) IS NOT NULL THEN (SELECT isn FROM chkssn) ELSE (SELECT isn FROM temp) END isn FROM dual ), isn1t AS ( 	SELECT CASE WHEN exists(SELECT isn FROM chkisn) AND (SELECT isn FROM chkisn) IS NOT NULL THEN (SELECT isn FROM chkisn) WHEN exists(SELECT isn FROM chkisninfo) AND (SELECT isn FROM chkisninfo) IS NOT NULL THEN (SELECT isn FROM chkisninfo) ELSE (SELECT isn FROM temp) END isn FROM dual ), isn2t AS ( 	SELECT CASE WHEN exists(SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn1t)) AND (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn1t)) IS NOT NULL AND (SELECT chk2isn FROM temp) = 2 THEN (SELECT isn FROM mokp_d WHERE kpsn = (SELECT isn FROM isn1t)) ELSE (SELECT isn FROM isn1t) END isn FROM dual ), isnt AS ( 	SELECT b.mo, a.isn, a.item, b.device, b.intime, b.grp, b.status, b.ngrp, b.nstep, b.route, a.scarno, a.pallet, a.so FROM isn a, mo_d b WHERE a.isn = b.isn AND a.isn = (SELECT isn FROM isn2t)
), route_stept AS ( 	SELECT route, ridx, step, SECTION, grp, kp1, kp2, stepnm, stepflag, stepflag1, stepflag3, '', '' FROM route_step WHERE route = (SELECT route FROM isnt) AND step LIKE '%' || (SELECT CASE WHEN nstep <> '0' THEN nstep WHEN ngrp IS NOT NULL AND nstep = '0' THEN ngrp WHEN ngrp = 'NONE' OR ngrp IS NULL THEN grp END FROM isnt) ), mokpt AS ( 	SELECT mo, kpitem, itemnm, kpbc, kpcount, a.crstamp, a.lastupd,b.custitem,a.sisn,a.eisn,'', '', '' FROM mokp a, item b WHERE mo = (SELECT mo FROM isnt) AND a.kpitem = b.item AND kpitem LIKE '%' || (SELECT searchitem FROM temp) || '%' ORDER BY kpitem ), mokp_dt AS ( 	SELECT mo, isn, kpsn, kpitem, device, step, intime, op, kpbc, '', '', '', '' FROM mokp_d WHERE isn = (SELECT isn FROM isn2t) ORDER BY kpsn ), mokp_dt2 AS ( 	SELECT mo, isn, kpsn, kpitem, device, step, intime, op, kpbc, '', '', '', '' FROM mokp_d WHERE isn IN (SELECT kpsn FROM mokp_dt) ORDER BY isn ), rulet AS ( 	SELECT ruletype, ruleitem, rulestr, rulestatus, op, a.lastupd, ruleflag, ruledesc, item, b.kpbc, '', '', '' FROM chkrule_d a, mokpt b WHERE a.ruleitem = b.kpitem ORDER BY ruleitem, lastupd DESC ), reworkt AS ( 	SELECT a.rwno, rqty, op, a.rwtime, route, step, rwdesc, rwmo, rwkp, isn, status, statusdesc, b.rwtime rwtime_isn FROM rework a, rework_d b WHERE a.rwno = b.rwno AND b.isn = (SELECT isn FROM isn2t) ORDER BY a.rwtime DESC ), moroutet AS ( 	SELECT mo, isn, item, seq, device, step, intime, status, premo, nstep, line, b_intime, stepflag FROM mo_route WHERE isn = (SELECT isn FROM isn2t) ORDER BY seq ) SELECT '---ISN Table---' col1,'---ISN---' col2,'---ITEM---' col3,'---DEVICE---' col4, '---IN TIME---' col5,'---GRP---' col6,'---STATUS---' col7,'---NEXT GRP---' col8,'---NEXT STEP---' col9,'---ROUTE---' col10,'---SCARNO---' col11,'---PALLET---' col12,'---SO---' col13 FROM dual
UNION ALL SELECT isnt.mo, isnt.isn, isnt.item, to_char(isnt.device), to_char(intime, 'yyyy/mm/dd hh24:mi:ss'), isnt.grp, to_char(isnt.status), isnt.ngrp, nstep, isnt.route, isnt.scarno, isnt.pallet, isnt.so FROM isnt UNION ALL SELECT '---ROUTE Table---' col1,'---RIDX---' col2,'---STEP---' col3,'---SECTION---' col4,'---GRP---' col5,'---KP1---' col6,'---KP2---' col7,'---STEPMN---' col8,'---STEPFLAG---' col9,'---STEPFLAG1---' col10,'---STEPFLAG3---' col11, '--------' col12, '--------' col13 FROM dual UNION ALL SELECT route, to_char(ridx), step, SECTION, grp, kp1, kp2, stepnm, stepflag, stepflag1, stepflag3, '', '' FROM route_stept UNION ALL SELECT '---MOKP_D Table---' col1,'---ISN---' col2,'---KPSN---' col3,'---ITEM---' col4,'---DEVICE---' col5,'---STEP---' col6,'---INTIME---' col7,'---OP---' col8,'---KPBC---' col9,'------' col10,'------' col11, '--------' col12, '--------' col13 FROM dual UNION ALL SELECT mo, isn, kpsn, kpitem, to_char(device), step, to_char(intime, 'yyyy/mm/dd hh24:mi:ss'), op, kpbc, '', '', '', '' FROM mokp_dt UNION ALL SELECT '---MOKP_D2 Table---' col1,'---ISN---' col2,'---KPSN---' col3,'---ITEM---' col4,'---DEVICE---' col5,'---STEP---' col6,'---INTIME---' col7,'---OP---' col8,'---KPBC---' col9,'------' col10,'------' col11, '--------' col12, '--------' col13 FROM dual UNION ALL SELECT mo, isn, kpsn, kpitem, to_char(device), step, to_char(intime, 'yyyy/mm/dd hh24:mi:ss'), op, kpbc, '', '', '', '' FROM mokp_dt2 UNION ALL SELECT '---MOKP table---' col1,'---KP ITEM---' col2,'---ITEM NAME---' col3,'---KPBC---' col4,'---KP COUNT---' col5,'---CRSTAMP---' col6,'---LASTUP DATE---' col7,'---CUSTITEM---' col8,'---SISN---' col9,'---EISN---' col10,'------' col11, '--------' col12, '--------' col13 FROM dual UNION ALL SELECT mokpt.mo, mokpt.kpitem, itemnm, mokpt.kpbc, to_char(mokpt.kpcount), to_char(mokpt.crstamp, 'yyyy/mm/dd hh24:mi:ss'), to_char(mokpt.lastupd, 'yyyy/mm/dd hh24:mi:ss'),custitem,sisn,eisn,'', '', '' FROM mokpt
UNION ALL SELECT '---RULE table---' col1,'---RULEITEM---' col2,'---RULESTR---' col3,'---KPBC---' col4,'---OP---' col5,'---LAST UPDDATE---' col6,'---RULEFLAG---' col7,'---RULEDESC---' col8,'---ITEM---' col9,'---RULESTATUS---' col10,'------' col11, '--------' col12, '--------' col13 FROM dual UNION ALL SELECT ruletype, ruleitem, rulestr, kpbc, op, to_char(lastupd, 'yyyy/mm/dd hh24:mi:ss'), ruleflag, ruledesc, item, rulestatus, '', '', '' FROM rulet UNION ALL SELECT '---REWORK table---' col1,'---RQTY---' col2,'---OP---' col3,'---RWTIME---' col4,'---ROUTE---' col5,'---STEP---' col6,'---RWDESC---' col7,'---RWMO---' col8,'---RWKP---' col9,'---ISN---' col10,'---STATUS---' col11, '----STATUS DESC----' col12, '----RWTIME_ISN----' col13 FROM dual UNION ALL SELECT rwno, to_char(rqty), op, to_char(rwtime, 'yyyy/mm/dd hh24:mi:ss'), route, step, rwdesc, rwmo, rwkp, isn, to_char(status), statusdesc, to_char(rwtime_isn, 'yyyy/mm/dd hh24:mi:ss') FROM reworkt UNION ALL SELECT '---MO_ROUTE table---' col1,'---ISN---' col2, '----ITEM----' col3,'---SEQ---' col4,'---DEVICE---' col5,'---STEP---' col6,'---INTIME---' col7,'---STATUS---' col8,'---PREMO---' col9,'---NSTEP---' col10,'---LINE---' col11,'---B_INTIME---' col12, '----STEPFLAG----' col13 FROM dual UNION ALL SELECT mo, isn, item, to_char(seq), to_char(device), step, to_char(intime, 'yyyy/mm/dd hh24:mi:ss'), to_char(status), premo, nstep, line, to_char(b_intime, 'yyyy/mm/dd hh24:mi:ss'), stepflag FROM moroutet;"""

            intxt = intxt.format(data)
            pyperclip.copy(intxt)
            self.result_label.config(text="Preparing check ISN command ok!!")
            self.call_update()
        except Exception as e:
            print("Co loi {}".format(e))
            messagebox.showerror(title="Error", message=e)
    
    def Hex2Dec(self):
        try:
            data = pyperclip.paste()
            a = int(data, 16)
            pyperclip.copy(a)
            self.result_label.config(text="Converting Hex to Dec successfull!")
            self.call_update()
        except Exception as e:
            print("Co loi {}".format(e))
            messagebox.showerror(title="Error", message=e)
    
    def Dec2Hex(self):
        try:
            data = pyperclip.paste()
            a = hex(int(data))
            a = a.replace("0x", "")
            pyperclip.copy(a.upper())
            self.result_label.config(text="Converting Hex to Dec successfull!")
            self.call_update()
        except Exception as e:
            print("Co loi {}".format(e))
            messagebox.showerror(title="Error", message=e)
    
    def generate_sha256_hash(self, input_string):
        # Tạo đối tượng hash SHA-256
        sha256_hash = hashlib.sha256()

        # Cập nhật đối tượng hash với dữ liệu đầu vào (chuyển đổi thành bytes trước)
        sha256_hash.update(input_string.encode('utf-8'))

        # Lấy mã băm SHA-256 dưới dạng chuỗi hex
        sha256_hash_string = sha256_hash.hexdigest()

        return sha256_hash_string
    
    def changPass(self, old, new):
        try:
            oldPass = self.generate_sha256_hash(old)
            newPass = self.generate_sha256_hash(new)
            if oldPass == self.password:
                root = self.tree.getroot()
                root.find("password").attrib["pass"] = newPass
                self.tree.write(os.path.realpath("a.config"), encoding="utf-8", xml_declaration=True, method="xml")
                self.result_label.config(text="Change passwork ok!")
                self.call_update()
                self.load_xmlfile()
            else:
                self.result_label.config(text="Old password is wrong!")
                self.call_update()
        except Exception as e:
            print("Co loi {}".format(e))
            messagebox.showerror(title="Error", message=e)
    
    def run_command(self, event):
        # Get user input
        command = self.input_box.get()
        
        # Clear input box
        self.input_box.delete(0, tk.END)

             
        # Determine command to run
        if command == "?":
            self.open_dialog_showHelp()
        elif command == "config":
            if self.load_xmlfile():
                self.result_label.config(text="Load config file successful!")
                self.call_update()
            else:
                self.result_label.config(text="Cannot load config file")
                self.call_update()
        elif command[0:6] == "config" and len(command) > 6:
            name = command.split()
            path = pyperclip.paste()
            if len(name) == 4:
                path = "{}\\{}".format(path, name[3])
            self.update_config(element=name[1], name=name[2], path=path)
        elif command == "q":
            self.destroy()
        elif command == "cb":
            self.read_clipboard()
        elif command == "feedback":
            self.feedbackFrm()
        elif command == "viewfb":
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.view_dataFrm()
            else:
                self.view_dataFrm()
        elif command == "in" or command == "IN":
            self.prepare_in()
        elif command == "in1" or command == "IN1":
            self.prepare_in1()
        elif command == "in2" or command == "IN2":
            self.prepare_in2()
        elif command == "up" or command == "UP":
            self.prepare_update()
        elif command == "snerr" or command == "SNERR":
            self.prepare_snerr()
        elif command == "bt" or command == "BT":
            self.prepare_between()
        elif command == "bt2" or command == "BT2":
            self.prepare_between2()
        elif command == "log" or command == "LOG":
            self.prepare_log()
        elif command == "log1" or command == "LOG1":
            self.prepare_log1()
        elif command == "isn" or command == "ISN":
            self.check_ISN()
        elif command == "bu" or command == "BU":
            self.save_Backup()
        elif command == "save" or command == "SAVE":
            self.get_link_folder_today()
        elif command == "qr" or command == "QR":
            self.generate_qr_code()
        elif command[0:6] == "logout" and len(command) > 7:
            webbrowser.open_new_tab(url="https://pvn-sfweb-01.sfis.pegatroncorp.com/HermesWeb/SFISAPPSETTING/AP_STATUS_CHECK/AP_STATUS_CHECK.aspx")
            chk = simpledialog.askstring("Confirm to use", "Are you sure use this function?\n If yes, type yes")
            if chk == 'yes' or chk == 'YES':
                name = command.split(" ")
                try:
                    self.logoutDevice(name[1], name[2])
                except:
                    pass
        elif command == "gws" or command == "GWS":
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.get_stringWeb()
            else:
                self.get_stringWeb()
        elif command == "rws" or command == "RWS":
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.Run_Webservice()
            else:
                self.Run_Webservice()
        elif command == "rws2"  or command == "RWS2":
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.Run_Webservice2()
        elif command == "rws_smt"  or command == "RWS_SMT":
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.Run_Webservice3()
            else:
                self.Run_Webservice2()
        elif command == "rep" or command == "REP":
            self.prepare_sn_unknit()
        elif command == "tb" or command == "TB":
            self.prepare_table()
        elif command == "cls" or command == "CLS":
            self.clear_cb()
        elif command == "rs" or command == "RS":
            self.restart_program()
        elif command == "h2d" or command == "H2D":
            self.Hex2Dec()
        elif command == "d2h" or command == "D2H":
            self.Dec2Hex()
        elif command == "vn" or command == "VN":
            self.prepare_translate()
        elif command[0:10] == "changepass" and len(command) > 10:
            txt = command.split(" ")
            if len(txt) > 2:
                self.changPass(txt[1], txt[2])
        elif command[0:4] == "game" or command == "GAME":
            if command[4:5] == "":
                game = 0
            elif command [4:5].isdecimal():
                game = int(command[4:5])
            else:
                game = 0
            self.run_game(game)
        elif command == "c" or command == "C":
            self.result_label.config(text="This function take few second. Please wait!!!")
            self.prepare_copy()
        elif command == "qw" or command == "QW":
            self.windows_destroy()
            self.result_label.config(text="Close form complete!")
            self.call_update()
        elif command == "at" or command == "AT":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use autofill by excel file function?")
            if chk:
                self.autofillex()
        elif command == "atc" or command == "ATC":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use autofill by clipboard file function?")
            if chk:
                self.autofillcb()
        elif command == "copy" or command == "COPY":
            self.prepare_copy2()
        elif command == "create" or command == "CREATE":
            self.create_folder()
        elif command == "share" or command == "SHARE":
            self.create_Sharefolder()
        elif command[0:5] == "share" and len(command) > 5:
            self.open_Sharefolder(command[6:20])
        elif command == "isnkp" or command == "ISNKP":
            self.prepare_isnkp()
        elif command[0:6] == "upload":
            namefile = command[7:50]
            if self.osname != "Happy_Luu":
                chk = self.generate_sha256_hash(simpledialog.askstring("Password", "Please input the password to use this function:", show="*"))
                if chk == self.password:
                    self.uploadFile(namefile)
            else:
                self.uploadFile(namefile)
        elif command[0:3] == "new" or command == "NEW":
            self.create_PPTFILE(command[4:50])
        elif command == "mail":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use run rule mail function?")
            if chk:
                self.prepare_runrule()
        elif command[0:4] == "move" or command == "MOVE":
            chk = messagebox.askyesno("Confirm to use!","Are you sure to use Moving mail function?")
            if chk:
                try:
                    if command[4:5] == '1':
                        self.moverule = True
                    else:
                        self.moverule = False
                    self.prepare_movemail()
                except:
                    self.result_label.config(text="Invalid command")
                    self.call_update()
        elif command == "today" or command == "TODAY":
            self.open_folder_temp_today()
        elif command[0:2] == "w ":
            try:
                weblink = command[2:20]
                root = self.tree.getroot()
                webs = root.findall("web")
                chk = 0
                for web in webs:
                    name = web.attrib.get("name")
                    path = web.attrib.get("link")
                    if name == weblink:
                        print(f"Mo trang WEB {path} thanh cong!")
                        webbrowser.open_new_tab(url=path)
                        chk = 1
                if chk == 1:
                    self.result_label.config(text=f"Open {command[2:20].upper()} web ok!")
                    self.call_update()
                else:
                    self.result_label.config(text="Invalid command!")
                    self.call_update()
            except:
                self.result_label.config(text="Invalid command")
                self.call_update()
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
                        strpath = root.find("temp").attrib.get("path") + "\\"
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
        
