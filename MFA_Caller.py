# Importing required module
import subprocess
import os

# Using system() method to
# execute shell commands
command = "cd; cd Desktop"
#os.chdir("Users/albarh22/")
#subprocess.Popen("conda init ", shell=True)
subprocess.Popen(['conda', 'activate', 'aligner'], shell=True)
# wd = os.getcwd()
# os.chdir("/")
# subprocess.Popen("ls")
# os.chdir(wd)