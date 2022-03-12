"""
 
    PyFuscation.py
    This python3 script obfuscates powershell function, variable and parameters in an attempt to bypass AV blacklists

    original by  CBHue

    refactored by dotPY
        I only refactored it don't judge me

"""

import ast
import configparser
import re
import random
import string

import files


class Obfuscator:
    def __init__(self, script_in):
        self.verbose = True

        self.original_script = script_in
        self.script = script_in
        self.wordlist = None
        self.lower_reserved = self.get_reserved()

    def replacer(self, replace_dictionary):
        for replace, replacer in replace_dictionary.items():
            base_name = replace
            base_name_replacer = replacer
            if replacer.startswith("$"):
                base_name_replacer = base_name_replacer[1:]
            if replace.startswith("$"):
                base_name = base_name[1:]
                replace = replace.replace("$", "\$")

            self.script = re.sub(r"{}\b".format(replace), replacer, self.script)
            self.script = re.sub(r"@{}\b".format(base_name), "@" + base_name_replacer, self.script)
            self.script = re.sub(r"\$PSBoundParameters\['{}'\]".format(base_name), "$PSBoundParameters['{}']".format(base_name_replacer), self.script)
            self.script = re.sub(r"\$Arguments\['{}'\]".format(base_name), "$Arguments['{}']".format(base_name_replacer), self.script)



    def find_custom_parameters(self, variables):
        parameters = {}
        read = False
        start = 0
        end = 0
        regex = r'([\$-]\w{4,})'

        for line in self.original_script.split("\n"):
            line += "\n"
            line = line.strip()

            if re.search(r'\bparam\b', line, re.I):
                # Ok we are at the beginning of a custom parameter

                read = True

                # The open bracket is on another line so move until we find it
                start = start + line.count('(')
                if start == 0:
                    continue
                end = end + line.count(')')

                v = re.findall(regex, line)
                for i in v:
                    if i.lower() not in self.lower_reserved and i not in parameters:
                        # Lets check to see if this has been replaced already
                        new = variables.get(i)
                        if not new:
                            continue
                        new = " -" + new[1:]
                        old = " -" + i[1:]
                        parameters[old] = new
                        self.print_replace(old, new)

                # If the params are all on one line were done here
                if start != 0 and start == end:
                    start = 0
                    end = 0
                    read = False
                    continue

            # These are the custom parameters
            elif read:
                v = re.findall(regex, line)
                for i in v:
                    if i.lower() not in self.lower_reserved and i not in parameters:
                        new = variables.get(i)
                        if not new:
                            continue
                        new = " -" + new[1:]
                        old = " -" + i[1:]
                        parameters[old] = new
                        self.print_replace(old, new)

                start = start + line.count('(')
                end = end + line.count(')')
                if start != 0 and start == end:
                    start = 0
                    end = 0
                    read = False

            # Keep moving until we have work
            else:
                continue

        if self.verbose:
            print("Parameters Replaced : " + str(len(parameters)))

        return parameters

    def find_variables(self):
        variables = {}
        regex = r'(\$\w{6,})'

        for line in self.script.split("\n"):
            line += "\n"
            v = re.findall(regex, line)
            for i in v:
                if i in variables:
                    continue
                elif i.lower() not in self.lower_reserved:
                    # Powershell vars are case insensitive
                    lower_vars = {k.lower(): v for k, v in variables.items()}
                    if i.lower() in lower_vars:
                        new = lower_vars.get(i.lower())
                        self.print_replace(i, new)
                        variables[i] = new
                    else:
                        v_num = 99
                        new = "$" + self.random_string()
                        variables[i] = new + str(v_num)
                        self.print_replace(i, new)
                        v_num += 1

        # return dict of variable and their replacements
        if self.verbose:
            print("Variables Replaced  : " + str(len(variables)))
        return variables

    def find_functions(self):
        functions = {}

        for line in self.script.split("\n"):
            line += "\n"
            function_match = re.search(r'^\s*Function ([a-zA-Z0-9_-]{6,})[\s{]+$', line, re.IGNORECASE)
            if function_match and function_match.group(1) not in functions:
                if function_match.group(1) == "main":
                    continue
                v_num = 9999
                new = self.random_word()
                functions[function_match.group(1)] = new
                self.print_replace(function_match.group(1), new)
                v_num += 1
        if self.verbose:
            print("Functions Replaced  : " + str(len(functions)))
        return functions

    def random_word(self):
        if not self.wordlist:
            self.wordlist = []
            with open(files.wordlist_file) as file:
                for line in file.readlines():
                    line = line.strip()
                    self.wordlist.append(line)
        return random.choice(self.wordlist)

    def random_string(self, length=8):
        return "".join(random.choices(string.ascii_letters, k=length))

    def get_reserved(self):
        config = configparser.ConfigParser()
        config.read(files.ps_config_file)
        reserved = ast.literal_eval(config.get("PS_Reserverd", "f"))
        return list(map(lambda x: x.lower(), reserved))

    def print_replace(self, old, new):
        if self.verbose:
            print("Replacing: {} with: {}".format(str(old), str(new)))

    def main(self):
        print("Obfuscating")

        variables = self.find_variables()
        self.replacer(variables)

        parameters = self.find_custom_parameters(variables)
        self.replacer(parameters)

        functions = self.find_functions()
        self.replacer(functions)

        return self.script
