import subprocess
from telegram.ext import Updater, CommandHandler
import json
import re


def output_command(command):
    result = subprocess.check_output(command, shell=True)
    result = result.decode("utf-8")
    return result


def check_is_success(command):
    return_code = subprocess.call(command, shell=True)
    if return_code == 0:
        return True
    return False


def ssh_to_server(server):
    command = "ssh root@" + server
    return command


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


def other_command(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        ip = context.args[0]
        if re.match('^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$',ip):
            context.args.pop(0)
            command = " ".join(context.args)
            command = ssh_to_server(ip) + " " + command
            print(command)
            if not check_is_success(ssh_to_server(ip) + " exit"):
                update.message.reply_text('Check your host or IP address')
        else:
            command = " ".join(context.args)
        print(command)
        print(context.args)
        print(context.args.pop(0))
        update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')



def check_all_service_running(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """netstat -lntp | awk '{split($7,a,"/"); split(a[2],b,":"); print(b[1])}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
            if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        update.message.reply_text("Services are running: {} ".format(output_command(command)))
    else:
        update.message.reply_text('You are not my owner')


def check_all_port_opening(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """netstat -lntp | awk '$4 ~ /:/ {print$4}' | sort | uniq"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
            if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        update.message.reply_text("Ports are opening: {} ".format(output_command(command)))
    else:
        update.message.reply_text('You are not my owner')


def restart_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = context.args[0]
        command = "service " + service + " restart"
        if not check_is_root:
            command = "sudo " + command
        try:
            command = ssh_to_server(context.args[1]) + " " + command
            if not check_is_success(ssh_to_server(context.args[1]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        except IndexError:
            pass
        if check_is_success(command):
            update.message.reply_text("Service {} has been restarted".format(service))
    else:
        update.message.reply_text('You are not my owner')


def start_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = context.args[0]
        command = "service " + service + " start"
        if not check_is_root:
            command = "sudo " + command
        try:
            command = ssh_to_server(context.args[1]) + " " + command
            if not check_is_success(ssh_to_server(context.args[1]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        except IndexError:
            pass
        if check_is_success(command):
            update.message.reply_text("Service {} has been started".format(service))
    else:
        update.message.reply_text('You are not my owner')


def stop_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = context.args[0]
        command = "service " + service + " stop"
        if not check_is_root:
            command = "sudo " + command
        try:
            command = ssh_to_server(context.args[1]) + " " + command
            if not check_is_success(ssh_to_server(context.args[1]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        except IndexError:
            pass
        if check_is_success(command):
            update.message.reply_text("Service {} has been stoped".format(service))
    else:
        update.message.reply_text('You are not my owner')


def status_service(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        service = context.args[0]
        command = "service " + service + " status"
        if not check_is_root:
            command = "sudo " + command
        try:
            command = ssh_to_server(context.args[1]) + " " + command
            if not check_is_success(ssh_to_server(context.args[1]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        except IndexError:
            pass
        if check_is_success(command):
            update.message.reply_text(output_command(command))
    else:
        update.message.reply_text('You are not my owner')


def check_mem(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """cat /proc/meminfo | awk '$1 ~ /Mem/ {print $2/1024/1024}'"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
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


def check_load_cpu(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """cat /proc/loadavg | awk '{print $1}'"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
            if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        update.message.reply_text("CPU Load: {}/{} ".format(output_command(command).split("\n")[0],
                                                            output_command("grep -c ^processor /proc/cpuinfo")))
    else:
        update.message.reply_text('You are not my owner')


def check_disk_usage(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        command = """df | awk 'NR > 1 {print $6,$5, $4}'"""
        if not check_is_root:
            command = "sudo " + command
        if context.args:
            command = ssh_to_server(context.args[0]) + " " + command
            if not check_is_success(ssh_to_server(context.args[0]) + " exit"):
                update.message.reply_text('Check your host or IP address')
        result = subprocess.check_output(command, shell=True)
        result = result.decode("utf-8")
        d = result.count('\n')
        for i in range(d):
            line = result.split("\n")[i]
            a = line.split()
            update.message.reply_text("Location: {} \nUsed: {} \nAvailable: {}".format(a[0], a[1], a[2]))
    else:
        update.message.reply_text('You are not my owner')


def help(update, context):
    owner = str(update.message.from_user.id)
    if owner == get_owner():
        help = "To start service: /start_service + service_name \n" \
               "To stop service: /stop_service + service_name \n" \
               "To restart service: /restart_service + service_name \n" \
               "To see status service: /status_service + service_name \n" \
               "To check ports are openning: /port_opening \n" \
               "To check service are running: /service_running \n" \
               "To check memory: /check_mem \n" \
               "To check load cpu: /check_load_cpu \n" \
               "To check disk usage: /check_disk_usage \n " \
               "To use other command: /run + [IP] + command"
        update.message.reply_text(help)
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
    updater.dispatcher.add_handler(CommandHandler("check_load_cpu", check_load_cpu))
    updater.dispatcher.add_handler(CommandHandler("check_disk_usage", check_disk_usage))
    updater.dispatcher.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
