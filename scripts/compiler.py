import os
import shutil


# remove unnecessary files that created after simulation from "sim" folder
if os.path.exists("..\\sim\\vsim_stacktrace.vstf"):
    os.remove("..\\sim\\vsim_stacktrace.vstf")

if os.path.exists("..\\sim\\work"):
    shutil.rmtree("..\\sim\\work")

if os.path.exists("..\\sim\\transcript"):
    os.remove("..\\sim\\transcript")

os.chdir("..\\sim")
os.system('cmd /c "vsim -do sim_Arbiter_req_grant_check.do"')
