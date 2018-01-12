import os
from platform import system as system_name  
from os import system as system_call  
import logging
from datetime import date
import time
import smtplib  
import urllib
import paramiko
import socket


def ping(host): 
    ping_param = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return system_call("ping " + ping_param + " " + host) == 0
def is_website_online(url):  
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    socket.setdefaulttimeout(5)
    try:
        code = urllib.urlopen(url).getcode()
    except Exception as e:
        code = 404
    return code == 200


def write_log(log_msg):
    
    debug = False
    today = date.today()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)
    if not os.path.isdir('logs'):
        os.mkdir('logs')
    if debug:
        print ("[DEBUG] %s" % log_msg)
    else:
        logging.basicConfig(filename=dir_path + '/logs/vmm_log_' + str(today) + '.log', level=logging.DEBUG)
        logging.info(log_msg)


def send_email(to_address, subject, body):
    fromaddr = 'educloud.monitor@gmail.com'
    toaddrs = to_address
    msg = "\r\n".join([
        "From: %s" % fromaddr,
        "To: %s" % toaddrs,
        "Subject: %s" % subject,
        "",
        "%s" % body
    ])
    username = fromaddr
    password = 'educloud2018'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

def main(vm_name, vm_ip, cmd_command):
    admin_email = 'elyes.ch0@gmail.com'
    log_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if not is_website_online(vm_ip):
        time.sleep(30)
        if not is_website_online(vm_ip):
            write_log("%s :: Connect to VM name [%s], IP/URL [%s] failed" % (log_time, vm_name, vm_ip))
            send_email(admin_email, '[VMM] Educloud : %s down' % vm_name,
                       'Connect to %s failed, will try to reboot VM\r\nTime: %s' % (vm_ip, log_time))           
            #system_call(cmd_command)
            ssh = paramiko.SSHClient()
            ssh.connect('192.168.153.33', username='root', password='21256193')
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('vim-cmd vmsvc/power.reset vim-cmd vmsvc/getallvms | grep '+ server_name +' | cut -c1,2')
            time.sleep(180)
            log_time = time.strftime("%Y-%m-%d %H:%M:%S")
            if not is_website_online(vm_ip):
                write_log("%s :: Try to reboot VM name [%s], IP/URL [%s] failed" % (log_time, vm_name, vm_ip))
                send_email(admin_email, '[VMM] Educloud : %s reboot failed' % vm_name,
                           'Try to reboot VM name [%s], IP/URL [%s] failed, please check.\r\nTime: %s'
                           % (vm_name, vm_ip, log_time))
            else:
                write_log("%s :: Reboot VM name [%s], IP/URL [%s] success, host is online" % (log_time, vm_name, vm_ip))
                send_email(admin_email, '[VMM] Educloud: %s reboot success' % vm_name,
                           'Reboot [%s], IP/URL [%s] success, host is online.\r\nTime: %s' % (vm_name, vm_ip, log_time))
        else:
            write_log("%s :: Connect to VM name [%s], IP/URL [%s] success (retry 2)" % (log_time, vm_name, vm_ip))
    else:
        write_log("%s :: Connect to VM name [%s], IP/URL [%s] success" % (log_time, vm_name, vm_ip))


server_name = 'mail server'

server_ip = '192.168.159.129'

cmd =' '
main(server_name, server_ip, cmd)
