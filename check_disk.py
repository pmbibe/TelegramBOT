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


def check_all_service_running(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
            if not check_is_success(ssh_to_server(context.args[0]) + " && exit"):
                #                update.message.reply_text('Check your host or IP address')
                print("1")
            else:
                #                update.message.reply_text("Services are running: {} ".format(output_command(command)))
                print("2")
            print(command)
        else:
            update.message.reply_text("Services are running: {} ".format(output_command(command)))
    else:
        update.message.reply_text('You are not my owner')


def main():
    updater = Updater(get_token_bot(), use_context=True)
    updater.dispatcher.add_handler(CommandHandler("service_running", check_all_service_running))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
