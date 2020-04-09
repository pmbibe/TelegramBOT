import subprocess
from telegram.ext import Updater, CommandHandler
import json


def get_token_bot():
    with open('Authentication.json') as Authen:
        read_data = json.load(Authen)
    return read_data["Token_TelegramBot"]


def check_is_success(command):
    return_code = subprocess.call(command, shell=True)
    if return_code == 0:
        return True
    return False


def get_owner():
    with open('Authentication.json') as Authen:
        read_data = json.load(Authen)
    return read_data["ID_Owner"]


def ssh_to_server(server):
    command = "ssh root@" + server
    return command


def check_is_root():
    check_root = "whoami"
    if output_command(check_root) == "root":
        return True
    else:
        return False


def output_command(command):
    result = subprocess.check_output(command, shell=True)
    result = result.decode("utf-8")
    return result


def check_mem(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """cat /proc/meminfo | awk '$1 ~ /Mem/ {print $2/1024/1024}'"""
        if not check_is_root:
            command = "sudo " + command
        try:
            command = ssh_to_server(context.args[0]) + " " + command
        except NameError:
            pass
        if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
            update.message.reply_text('Check your host or IP address')
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
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')


def main():
    updater = Updater(get_token_bot(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler("check_mem", check_mem))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
