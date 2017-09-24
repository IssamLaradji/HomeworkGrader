import os
import json
import pandas as pd

from scipy.io import savemat
from subprocess import Popen, PIPE
from subprocess import call 
import shlex 

def parse_args(argString, parser):
    if isinstance(argString, list):
      argString = " ".join(argString)

    io_args = parser.parse_args(shlex.split(argString))

    return io_args

def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    command = cmd.split(" ")
    args = [x.strip() for x in command if x.strip()]

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    #
    return exitcode, out, err


def bash(cmd):
    code = call(cmd, shell=True)
    return code

def create_dirs(fname):
    if "/" not in fname:
        return
        
    if not os.path.exists(os.path.dirname(fname)):
        try:
            os.makedirs(os.path.dirname(fname))
        except OSError:
            pass  

def save_json(path, dictionary):
    create_dirs(path)
    with open(path + ".json" , 'w') as fp:
        json.dump(dictionary, fp, sort_keys=True, indent=4)
    print "JSON saved in %s" % path

def save_mat(path, dictionary):
    create_dirs(path)
    savemat(path +".mat", dictionary)
    print "MAT saved in %s" % path

def read_json(path):
    with open(path + '.json') as data_file:    
        dictionary = json.load(data_file)
    
    return dictionary

def read_csv(path):
    csv = pd.read_csv(path + ".csv")
    return csv

def read_txt(path):
  f = open(path + ".txt", 'r')
  lines = f.readlines()
  f.close()

  return lines

def dict_equal(d1, d2):
    flag = True
    for key in d1:
        if key in ["p", "s", "u"]:
            continue
        if key not in d2:
            return False
        v1 = d1[key] 
        v2 = d2[key]

        if v1 != v2:
            print "Diff (%s): %s != %s" % (key, v1, v2)
            flag = False
    print "Both are equal..."
    return flag

def save_fig(path, fig):
    create_dirs(path)
    fig.savefig(path + ".png")
    print "Figure saved in %s" % (path)

def save_csv(path, csv_file):
    create_dirs(path)
    csv_file.to_csv(path + ".csv", index=False) 

    print "csv file saved in %s" % (path)

def print_dict(dictionary):
    for key in dictionary:
        print "%s: %s" % (key, dictionary[key])



