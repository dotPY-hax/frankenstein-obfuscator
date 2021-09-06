import argparse

import build


def run():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", metavar="EXE", help="exe file you want to obfuscate", required=True)
    parser.add_argument("-o", metavar="OUTPUT", help="file you want to write to", default="/tmp/totally_legitimate_powershell_file.ps1")
    args = parser.parse_args()

    script = build.build_final_script(args.e)
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
