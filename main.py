import numpy as np
import  pandas as pd
import sys
import argparse
from PyQt5.QtWidgets import QApplication
import utils
import os
     
import gui
import json
if __name__ == "__main__": 
  argv = sys.argv[1:]

  parser = argparse.ArgumentParser()
  parser.add_argument('-c','--config', default="")
  parser.add_argument('-cl','--classlist')
  parser.add_argument('-n','--assignment_name')
  parser.add_argument('-q','--questions', nargs="+")
  args = parser.parse_args()

  # 1. LOAD DATA
  with open("configs.json") as conf: 
    configs = json.load(conf)
  args = utils.parse_args(configs[args.config], parser)  

  classlist = pd.read_csv("classlists/" + args.classlist)
  classlist.columns = [col.lower() for col in classlist.columns]
  name = args.assignment_name + "_" + args.classlist
  # 2. CREATE or LOAD GRADE SHEET
  sheetName = "grade_sheets/" + name
  if os.path.exists(sheetName):
    gradeSheet = pd.read_csv(sheetName)
  else:
    gradeSheet = classlist.copy()
    for quest in args.questions:
      q, p = quest.replace(")","").replace("(","").split(",")
      gradeSheet["%s (Max %s points)" % (q, p)] = -1

  # 3. Submissions
  name = name.replace(".csv", "")
  subName = "submissions/" + name
  if not os.path.exists(subName):
    os.makedirs(subName)
    for c in gradeSheet["acct"]: 
      os.makedirs(subName + "/%s" % c)
  
  # 3. Launch App
  app = QApplication(sys.argv)

  qList = [col for col in gradeSheet.columns if "Max" in col]
  mc = gui.mainClass(gradeSheet, args, sheetName, subName, args.assignment_name, qList)
  sys.exit(app.exec_())


