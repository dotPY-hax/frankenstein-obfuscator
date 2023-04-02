import base64


def add_alias(function_name, obfuscated_funtion_name):
    unbased_variable = "$unbased"
    based_function_name = base64.b64encode(function_name.encode()).decode()
    unbaser = f"{unbased_variable} = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{based_function_name}'))"
    alias_command = f"Set-Alias -Name {unbased_variable} -Value {obfuscated_funtion_name}"
    command = ";".join((unbaser, alias_command))
    return command

def add_all_aliases(function_dictionary):
    aliases = []
    for function_name, obfuscated_function_name in function_dictionary.items():
        new_alias = add_alias(function_name, obfuscated_function_name)
        aliases.append(new_alias)
    return aliases
