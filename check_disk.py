import subprocess
from telegram.ext import Updater, CommandHandler
import json
import re

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


def other_command(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        print(context.args[0])
        if re.match('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',context.args[0]):
            for i in range(1, len(context.args)):
                command = "".join(context.args[i])
            command = ssh_to_server(context.args[0]) + " " +command
            if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        else:
            command = " ".join(context.args)
        print(command)
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')



def main():
    updater = Updater(get_token_bot(), use_context=True)

    updater.dispatcher.add_handler(CommandHandler("run", other_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
