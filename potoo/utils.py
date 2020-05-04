from flask import request
from subprocess import check_output
from ansi2html import Ansi2HTMLConverter
from os import path
import ipaddress
import configparser


def get_config():
    if path.exists('config.ini'):
        config = configparser.ConfigParser()
        config.read('config.ini')
    else:
        config = configparser.ConfigParser()
        config.read('/etc/potoo/config.ini')
    return config


def authorized_ip():
    config = get_config()
    network_whitelist = config['default']['network_whitelist'].split(',')
    client = request.remote_addr
    for network in network_whitelist:
        if ipaddress.ip_address(client) in \
                          ipaddress.ip_network(network, strict=False):
            return True
    return False


def get_param(param):
    if request.args.get(param) is not None:
        param = request.args.get(param)
    else:
        param = eval(param)
    return param


def run_originate(dest_context, dest_exten, src_context, src_exten):
    stdout = check_output(['/usr/sbin/rasterisk -rx "channel originate Local/'
                          + dest_exten + '@' + dest_context + ' extension '
                          + src_exten + '@' + src_context + '"'],
                          shell=True).decode('utf-8')
    return stdout


def run_shell(cmd):
    stdout = check_output([cmd], shell=True).decode('utf-8')
    return stdout


def stdout2html(stdout):
    conv = Ansi2HTMLConverter()
    return conv.convert(stdout)
