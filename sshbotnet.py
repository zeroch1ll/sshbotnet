#!/usr/bin/python3

from pexpect import pxssh 
from sshbot import Client

class BotNet(object):
    def __init__(self, name):
        """initializes botnet object
        Has:
            1. a name
            2. a list of bots (Client objects)"""
        self.name = name
        self.net = []

    def botnet_command(self, command):
        """Issue a command to all bots in net"""
        for bot in self.net:
            output = bot.send_command(command)
            print(f"[>] Output from {bot.host}\n[>] {output.decode()}")

    def add_client(self, host, user, password):
        """Instantiate new client and append to botnet list"""
        new_client = Client(host, user, password)
        self.net.append(new_client)

    def kill_client(self, host):
        """Closes a bot connection and removes it from the list"""
        for bot in self.net:
            if bot.host == host:
                bot.disconnect()
                self.net.remove(bot)

    def get_bot_count(self):
        """Returns number of bots in the net list"""
        return len(self.net)