import subprocess
from telegram.ext import Updater, CommandHandler
import json

def get_owner():
    with open('Authentication.json') as Authen:
        read_data = json.load(Authen)
    return read_data["ID_Owner"]
def get_token_bot():
    with open('Authentication.json') as Authen:
        read_data = json.load(Authen)
    return read_data["Token_TelegramBot"]
def check_is_root():
    check_root = "whoami"
    if output_command(check_root) == "root":
        return True
    else:
        return False
def output_command(command):
    result = subprocess.check_output(command, shell = True)
    result = result.decode("utf-8")
    print(result)
    return result

def other_command(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        user_says = " ".join(context.args)
        update.message.reply_text(output_command(user_says))
    else:
        update.message.reply_text('You are not my owner')

def check_all_service_running(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        command = """netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Services are running: {} " .format(result))
    else:
        update.message.reply_text('You are not my owner')

def check_all_port_opening(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        command = """netstat -lntp | awk '$4 ~ /:/ {print$4}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Ports are opening: {} " .format(result))
    else:
        update.message.reply_text('You are not my owner')

def restart_service(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service restart " + service
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def start_service(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service start " + service
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def stop_service(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service stop " + service
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def status_service(update, context):
    owner = update.message.from_user.id
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service status " + service
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def main():
    updater = Updater(get_token_bot(), use_context=True)
    updater.dispatcher.add_handler(CommandHandler("run", other_command))
    updater.dispatcher.add_handler(CommandHandler("service_running",check_all_service_running))
    updater.dispatcher.add_handler(CommandHandler("port_opening",check_all_port_opening))
    updater.dispatcher.add_handler(CommandHandler("start_service",start_service))
    updater.dispatcher.add_handler(CommandHandler("restart_service",restart_service))
    updater.dispatcher.add_handler(CommandHandler("stop_service",stop_service))
    updater.dispatcher.add_handler(CommandHandler("status_service",status_service))
    updater.start_polling()
    updater.idle()

main()
