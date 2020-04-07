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
    result = subprocess.check_output(command, shell=True)
    result = result.decode("utf-8")
    print(result)
    return result


def other_command(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        user_says = " ".join(context.args)
        update.message.reply_text(output_command(user_says))
    else:
        update.message.reply_text('You are not my owner')


def check_all_service_running(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text("Services are running: {} ".format(output_command(command)))
    else:
        update.message.reply_text('You are not my owner')


def check_all_port_opening(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """netstat -lntp | awk '$4 ~ /:/ {print$4}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text("Ports are opening: {} ".format(output_command(command)))
    else:
        update.message.reply_text('You are not my owner')


def restart_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service restart " + service
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')


def start_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service " + service + " start"
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')


def stop_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service " + service + " stop"
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')


def status_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = " ".join(context.args)
        command = "service " + service + " status"
        if not check_is_root:
            command = "sudo " + command
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')


def check_mem(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """cat /proc/meminfo | awk '$1 ~ /Mem/ {print $2/1024/1024}'"""
        if not check_is_root:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        mem_total = float(result.split("\n")[0])
        mem_free = float(result.split("\n")[1])
        mem_available = float(result.split("\n")[2])
        mem_used_rate = 1 - mem_free / mem_total
        mem_total = float("{:.2f}".format(mem_total))
        mem_free = float("{:.2f}".format(mem_free))
        mem_available = float("{:.2f}".format(mem_available))
        mem_used_rate = float("{:.4f}".format(mem_used_rate)) * 100
        result = "Total: " + str(mem_total) + "GB \n" + "Free: " + str(mem_free) + 'GB \n' + "Avaiable: " + str(
            mem_available) + "GB \n" + "Used Rate: " + str(mem_used_rate) + "%"
        print(result)
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')


def main():
    updater = Updater(get_token_bot(), use_context=True)
    updater.dispatcher.add_handler(CommandHandler("run", other_command))
    updater.dispatcher.add_handler(CommandHandler("service_running", check_all_service_running))
    updater.dispatcher.add_handler(CommandHandler("port_opening", check_all_port_opening))
    updater.dispatcher.add_handler(CommandHandler("start_service", start_service))
    updater.dispatcher.add_handler(CommandHandler("restart_service", restart_service))
    updater.dispatcher.add_handler(CommandHandler("stop_service", stop_service))
    updater.dispatcher.add_handler(CommandHandler("status_service", status_service))
    updater.dispatcher.add_handler(CommandHandler("check_mem", check_mem))
    updater.start_polling()
    updater.idle()


main()
