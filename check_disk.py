import subprocess
from telegram.ext import Updater, CommandHandler
import json




def check_is_success(command):
    return_code = subprocess.call(command, shell=True)
    if return_code.split("\n")[0] == "0":
        print("1")
    else:
        print("2")

check_is_success("ls")
