import PyQt5.QtGui as qt
from PyQt5 import QtCore
from PyQt5 import QtGui 
import os
import numpy as np
import subprocess
import utils
import os
from PyQt5.QtWidgets import QWidget, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtWidgets as qt
   
def fill_QTableWidget(datatable, df_tmp):
    
    df = df_tmp
    header_labels = df.columns
    datatable.setColumnCount(len(df.columns))
    
    datatable.setRowCount(len(df.index))
    datatable.setHorizontalHeaderLabels(header_labels)
    for i in range(len(df.index)):
        for j in range(len(df.columns)):
            datatable.setItem(i,j, QTableWidgetItem(str(df.iat[i, j])))

class mainClass(QWidget):
    def __init__(self, data_csv, args, sheetName, subName, asst_name, qList):

        self.subName = subName
        self.sheetName = sheetName
        QWidget. __init__(self)
        self.qList = qList
        self.asst_name = asst_name
        self.excel = data_csv

        #self.grades = np.array(excel[self.asst])
        self.setWindowTitle("Grading %s" % asst_name)
        self.cols = self.excel.columns
        self.col_dict = {}
        for i, col in enumerate(self.cols):
          self.col_dict[col] = i

        #excel#data_csv = data_csv.sort(['category'], ascending=[1])
        self.datatable = QTableWidget()
        self.datatable.setSortingEnabled(True)
        fill_QTableWidget(self.datatable, data_csv)

        ### CREATE LAYOUT
        self.dlayout = qt.QVBoxLayout()
        self.button_layout = qt.QHBoxLayout()
        
       
        ### CREATE LABELS
        self.info = qt.QLabel("TBD")

        ### CREATE BUTTONS
        self.folder = qt.QPushButton("Open Folder")
        self.folder.clicked.connect(self.open_folder)

        # self.insert_btn = qt.QPushButton("Open PDF")
        # self.insert_btn.clicked.connect(self.open_pdf)
        #self.save_btn.clicked.connect(self.save_table)
        
        self.button_layout.addWidget(self.info)
        self.button_layout.addWidget(self.folder)
        # self.button_layout.addWidget(self.insert_btn)
        #self.button_layout.addWidget(self.save_btn)

        ### Create DATA layout
        self.datatable.resizeColumnsToContents()
        self.dlayout.addWidget(self.datatable)
        self.dlayout.addLayout(self.button_layout)
        self.view_table()
        
        #self.datatable.itemChanged.connect(self.view_table)
        self.datatable.itemChanged.connect(self.update_table) 

        ### Plot table
        # figure, self.ax = plt.subplots()
        # self.canvas = FigureCanvas(figure)
        # #self.PlotFunc(data_csv)

        ### CREATE MAIN layout
        mainLayout = qt.QVBoxLayout(self)
        #mainLayout.addWidget(self.canvas)
        mainLayout.addLayout(self.dlayout)

        ### MODIFY LAYOUT
        self.setLayout(mainLayout)       
        self.setGeometry(200, 200, 1000, 600)
        
        self.show()

    def view_table(self):
      dt = self.datatable

      n_students = len(self.excel)

      # GET EXISTING ACCOUNTS      
      stu_id = self.col_dict["snum"]
      acct_id = self.col_dict["acct"]

      grades = np.array(self.excel[self.qList]).min(axis=1)
      for row in range(n_students):
          if grades[row] < 0:
            item = dt.item(row, stu_id)
            item.setBackground(QtGui.QColor(255, 128, 128))
            #dt.setItem(row, stu_id, item)

            item = dt.item(row, acct_id)
            item.setBackground(QtGui.QColor(255, 128, 128))
            #dt.setItem(row, acct_id, item)
          else:
            item = dt.item(row, stu_id)
            item.setBackground(QtGui.QColor(128, 255, 128))
            #dt.setItem(row, stu_id, item)

            item = dt.item(row, acct_id)
            item.setBackground(QtGui.QColor(128, 255, 128))
            #dt.setItem(row, acct_id, item)
      


      # REAMINING to GRADE STUDENTS
      n_remaining = (grades < 0).sum()
      self.info.setText("%s - Remaining Students: %d" % (self.asst_name,
                                                         n_remaining))
      

      
    def update_table(self):
     dt = self.datatable

     rows = sorted(set(index.row() for index in
                   dt.selectedIndexes()))

     assert len(rows) == 1     
     grade_id = dt.currentColumn()  
     grade_column = self.excel.columns[grade_id]
     
     stu_id = self.col_dict["snum"]
     acct_id = self.col_dict["acct"]
     self.grades = self.excel[self.excel.columns[grade_id]]
     grade = float(dt.item(dt.currentRow(), grade_id).text())
     stu = dt.item(dt.currentRow(), stu_id).text()

     row = dt.currentRow()
     self.grades[row] = float(grade)
     self.excel[grade_column] = self.grades
     print "stu: %s, %s: %s" % (stu, grade_column, grade)

       
     self.excel.to_csv(self.sheetName, index=False)
     print "Grade sheet saved in %s" % self.sheetName
     grades = np.array(self.excel[self.qList]).min(axis=1)

     if grades[row] >= 0:
      color = QtGui.QColor(128, 255, 128)

     else:
      color = QtGui.QColor(255, 128, 128)

     item = dt.item(row, stu_id)
     item.setBackground(color)

     item = dt.item(row, acct_id)
     item.setBackground(color)

     
     n_remaining = (grades < 0).sum()
     self.info.setText("%s - Remaining Students: %d" % (self.asst_name,
                                                         n_remaining))

    def open_folder(self):
     dt = self.datatable
     acct_id = self.col_dict["acct"]
     acct = dt.item(dt.currentRow(), acct_id).text()

     path = "%s/%s/" % (self.subName, acct)

     subprocess.Popen(["thunar", path])

    def open_pdf(self):
     print "Removed"