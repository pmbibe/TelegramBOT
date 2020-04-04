import subprocess
from telegram.ext import Updater, CommandHandler

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
        update.message.reply_text('Bad')

def check_all_service_running(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        command = """netstat -lntp 
                    | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' 
                    | sort 
                    | uniq """
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Services are running: {} ", result)
    else:
        update.message.reply_text('Bad')

def check_all_port_opening(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        command = """netstat -lntp 
                        | awk '$4 ~ /:/ {print$4}' 
                        | sort 
                        | uniq """
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text("Ports are opening: {} ", result)
    else:
        update.message.reply_text('Bad')

def restart_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service " + service + "restart"
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('Bad')

def start_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service " + service + "start"
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('Bad')

def stop_service(update, context):
    owner = update.message.from_user.id
    if owner == 817269876:
        service = " ".join(context.args)
        command = "service " + service + "stop"
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        update.message.reply_text(result)
    else:
        update.message.reply_text('Bad')
updater = Updater('1111280886:AAFhKDDyRxIOGuBvogpedMuoEM7t8kWiLhI', use_context=True)

updater.dispatcher.add_handler(CommandHandler("run", other_command))
updater.dispatcher.add_handler(CommandHandler("service_running",check_all_service_running))
updater.dispatcher.add_handler(CommandHandler("port_opening",check_all_port_opening))
updater.dispatcher.add_handler(CommandHandler("start_service",start_service))
updater.dispatcher.add_handler(CommandHandler("restart_service",restart_service))
updater.dispatcher.add_handler(CommandHandler("stop_service",stop_service))
updater.start_polling()
updater.idle()
