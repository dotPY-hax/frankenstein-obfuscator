# frankenstein-obfuscator
Obfuscate and run .exe files in a powershell script

This is my humble try to evade antivirus and specifically Defender on HackTheBox and run well known .exe files without having to mess with them and recompile.

It takes the .exe, base64s it, chops up the base64 and then tries to use obfuscated `Invoke-ReflectivePEInjection` from PowerSploit to run it.

Its built upon `Invoke-ReflectivePEInjection` from [PowerSploit](https://github.com/PowerShellMafia/PowerSploit) and
a very heavily refactored version of  [PyFuscate](https://github.com/CBHue/PyFuscation)

This could become arbitrarily sophisticated by adding more layers of obfuscation and/or encryption but for now I try to keep it simple and stupid


This might break when there are # signs inside strings because the obfuscator thinks its an inline comment.
If that happens replace line 35 in comment_remover.py <code> line = cut_inline_comment(line) </code> with <code>pass</code>

## update for arguments
Obfuscation is great but too good obfuscation means that you cant use the powershell script as a module! Now there is the -m flag which preserves arguments and sets aliases so you can effectively use an obfuscated powershell script as a module!

```
usage: frankenstein.py [-h] -e EXE [-o OUTPUT]

optional arguments:
  -h, --help     show this help message and exit
  -e EXE         exe file you want to obfuscate
  -p POWERSHELL  powershell file you want to obfuscate
  -m             if you want to use the file as a module i.e. use Import-Module use this flag. This sets aliases for obfuscated functions and leaves argument names intact! (default: False)
  -o OUTPUT      file you want to write to

  ```
  # HOWTO:
  - `python frankenstein.py -e /tmp/juicypotato.exe` OR `python frankenstein.py -p /tmp/absolutely_not_covenant_i_promisse.ps1`
  - upload `/tmp/totally_legitimate_powershell_file.ps1` to your target
  - on target: `powershell ./totally_legitimate_powershell_file.ps1 -arguments 'arguments for the exe here'`
