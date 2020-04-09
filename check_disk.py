import subprocess
from telegram.ext import Updater, CommandHandler
import json
import re


def ssh_to_server(server):
    command = "ssh root@" + server
    return command

def output_command(command):
    result = subprocess.check_output(command, shell=True)
    result = result.decode("utf-8")
    return result

def check_all_service_running(update, context):
    command = """ netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
    if context.args:
        #        server = re.match('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$', context.args[0])
        #        if not server:
        #            update.message.reply_text('Check your host or IP address')
        #        else:
        command = ssh_to_server(context.args[0]) + command
    print(command)
    print(output_command(ssh_to_server(context.args[0])))

def main():
    updater = Updater(get_token_bot(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler("service_running", check_all_service_running))

    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()


def get_token_bot():
    with open('Authentication.json') as Authen:
        read_data = json.load(Authen)
    return read_data["Token_TelegramBot"]


if __name__ == '__main__':
    main()
