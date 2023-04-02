import argparse

import build


def run():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", metavar="EXE", help="exe file you want to obfuscate")
    parser.add_argument("-p", metavar="POWERSHELL", help="powershell file you want to obfuscate")
    parser.add_argument("-m", help="if you want to use the file as a module i.e. use Import-Module use this flag. This sets aliases for obfuscated functions and leaves argument names intact!", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("-o", metavar="OUTPUT", help="file you want to write to", default="/tmp/totally_legitimate_powershell_file.ps1")
    args = parser.parse_args()
    if (args.e and args.p) or (not args.e and not args.p):
        parser.print_help()
        parser.exit()

    if args.e:
        do_exe(args)
    elif args.p:
        do_powershell(args)


def do_exe(args):
    script = build.build_final_script(args.e)
    build.write_final_file(script, args.o)

def do_powershell(args):
    script = build.pure_powershell_obfuscation(args.p, args.m)
    build.write_final_file(script, args.o)

def banner():
    print("=" * 25)
    print("Frankenstein Obfuscator by dotPY")
    print("=" * 25)
    print("NOO you cant multiply strings...")
    print("HAHA python go b" + "r"*5)
    print("-"*25)
    print("uses parts of PyFuscation by CBHue - refactored by dotPY")
    print("uses Invoke-ReflectivePEInjection by PowershellMafia - fixed by dotPY")
    print("-" * 25)
    print("\n")
