import subprocess
from telegram.ext import Updater, CommandHandler
import json



def check_is_success(command):
    return_code = subprocess.call(command, shell=True)
    if return_code.split == 0:
        return True
    return False

if not check_is_success("ls"):
    print("1")
else:
    print("2")
