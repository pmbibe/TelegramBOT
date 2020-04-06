import subprocess
from telegram.ext import Updater, CommandHandler

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
    if owner == 817269876:
        user_says = " ".join(context.args)
        update.message.reply_text(output_command(user_says))
    else:
        update.message.reply_text('You are not my owner')

def check_all_service_running(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        command = """netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Services are running: {} " .format(result))
    else:
        update.message.reply_text('You are not my owner')

def check_all_port_opening(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        command = """netstat -lntp | awk '$4 ~ /:/ {print$4}' | sort | uniq"""
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Ports are opening: {} " .format(result))
    else:
        update.message.reply_text('You are not my owner')

def restart_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service restart " + service
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def start_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service start " + service
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def stop_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service stop " + service
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def status_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service status " + service
        if check_is_root == False:
            command = "sudo " + command
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('You are not my owner')

def authentication_bot(token):
    return Updater(token, use_context=True)

def main():
    updater = authentication_bot("1111280886:AAFhKDDyRxIOGuBvogpedMuoEM7t8kWiLhI")
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
