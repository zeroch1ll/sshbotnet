#!/usr/bin/python3

import optparse
from pexpect import pxssh 
from sshbot import Client

class BotNet(object):
    def __init__(self, name):
        """initializes botnet object
        Should have:
            1. a name
            2. a list of bots (Client objects)"""
        self.name = name
        self.net = []

    def botnet_command(self, command):
        """Issue a command to al bots in net"""
        for client in self.net:
            output = client.send_command(command)
            print(f"[+] Output from {client.host}\n[+] {output}")

    def add_client(self, host, user, password):
        """Instantiate new client and append to botnet list"""
        new_client = Client(host, user, password)
        self.net.append(new_client)