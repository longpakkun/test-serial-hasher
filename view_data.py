from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

class view_data:
    def __init__(self, root, pw, ph):
        self.root = root
        root.geometry("1200x500+{}+{}".format(pw-600, ph-250))
        root.title("View Record")

        self.titleFRM = Frame(root)
        self.titleFRM.pack(fill="x")
        self.lblTitle = Label(self.titleFRM, text="DATA FEEDBACK", font=("Arial", 20, "bold"))
        self.lblTitle.pack(pady=10)
        
        self.ContentFRM = Frame(root)
        self.ContentFRM.pack(side="top", fill="both", expand=True)

        self.datagrvFRM = Frame(self.ContentFRM)
        self.datagrvFRM.pack(side="left", fill="both", expand=True)
        self.dataTree = ttk.Treeview(self.datagrvFRM, columns=("DATETIME", "NAME", "CONTENT"))

        self.dataTree.heading("#0", text="", anchor=W)
        self.dataTree.heading("DATETIME", text="Date time", anchor=W)
        self.dataTree.heading("NAME", text="Name", anchor=W)
        self.dataTree.heading("CONTENT", text="Content", anchor=W)

        self.dataTree.column("#0", width=0, stretch=NO)
        self.dataTree.column("DATETIME", width=150, stretch=NO)
        self.dataTree.column("NAME", width=100, stretch=NO)
        self.dataTree.column("CONTENT", width=800, stretch=NO)
        
        
        self.dataTree.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.scrollbarVerFRM = Frame(self.ContentFRM)
        self.scrollbarVerFRM.pack(side="right", fill="y")
        self.vsb = Scrollbar(self.scrollbarVerFRM, orient="vertical")
        self.vsb.pack(side="left", fill="y", pady=5)

        self.dataTree.config(yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.dataTree.yview)

        self.dataTreescrollFRM = Frame(root)
        self.dataTreescrollFRM.pack(fill="x", side="bottom")
        self.hsb = Scrollbar(self.dataTreescrollFRM, orient="horizontal")
        self.hsb.pack(side="top", fill="x", pady=5)

        self.dataTree.config(xscrollcommand=self.hsb.set)
        self.hsb.config(command=self.dataTree.xview)

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")

        self.view_data_load()

    def view_data_load(self):
        data = []
        with open(r"\\10.177.113.250\data$\Happy\python\Feedback\feedback.csv", mode="r", encoding = "utf-8") as file:
            data_csv = csv.reader(file)

            for i in data_csv:
                data.append(i)

        for i in data:
            i[2] = i[2].replace("\n", "| ")
            self.dataTree.insert("", "end", values=i)

if __name__ == "__main__":
    root = Tk()
    view_data(root, -1200, 300)
    root.mainloop()