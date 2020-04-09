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


def restart_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = context.args[0]
        command = "service " + service + " restart"
        if not check_is_root:
            command = "sudo " + command
        if context.args[1] is not None:
            print("1")
        else:
             print("2")
    #               command = ssh_to_server(context.args[1]) + " " + command
    #               if not check_is_success(ssh_to_server(context.args[1]) + " exit"):
    #                   print("1")
    #               else:
    #                   print("2")
    #       command = ssh_to_server(context.args[1]) + " " + command
    print(command)
    print(type(context.args[1]))
    print(context.args[1])
    print(check_is_success(ssh_to_server(context.args[1]) + " exit"))


#    if check_is_success(command):
#        update.message.reply_text("Service {} has been restarted".format(service))

def main():
    updater = Updater(get_token_bot(), use_context=True)
    updater.dispatcher.add_handler(CommandHandler("restart_service", restart_service))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
