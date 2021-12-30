# SSH Botnet

Implementing and extending the SSH botnet from Chapter 2 of Violent Python by TJ O'Connor. This is not meant to be useful in any real situation; I'm just playing around with building a botnet to get a better idea of basic C2 and implant concepts.

There are two components to this:
    1. An SSH Botnet with clients
    2. A python implant that communicates with an HTTP server

The general idea is that one could use the SSH botnet and clients to do password spraying or something similar (this could even be extended to FTP, SMB, etc), and then when an SSH bot client is successfully able to authenticate to a target host, it could then use the SSH session to pull down the implant file from the HTTP server and then either run it as a backgrounded process, or it could attach the process to a cronjob or something similar for better persistence. There's a lot that could happen!

Once the implant is running on the target host, after 60 seconds it will reach out to the HTTP server for an initial check-in. A lot of things could be done during the initial check-in phase. For example, this initial check-in request could include information about the target host that would be stored locally on the HTTP server host. This could then be used to maintain continuity/command history if the implant process is killed and then restarted later, or an entirely new implant is executed on a previously compromised host.

After check-in, the implant waits another 60 seconds before checking in again. All check-ins after the initial one will be to return any command output and/or check for new tasks to execute. It waits 60 seconds in between each task.

You'll notice that most of the above is not implented. Currently, the bot net clients require known, valid credentials. There is also no HTTP server and I'm not even sure yet if the implant will work (need to have the server running first). The main file doesn't even do anything with the HTTP server stuff just yet, and there is really only the ability to interact with one SSH client bot.

TO DOs:

[] Build out HTTP Server
    [] Add TLS
    [] Create routes for different actions
    [] Create logic to handle JSON
    [] Create local DB to store info from target machines
[] Add logic to include a compiled version of implant containing only needed modules
[] Obfuscation and/or encryption of command output