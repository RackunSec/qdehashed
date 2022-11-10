#!/usr/bin/env python3
## Password analytics for qdehashed results
## 2022 @RackunSec
##
from sys import argv,exit
from os import path

def usage():
    print("[i] Usage: python3 analysis.py (/path/to/qdehashed/output.csv)")
    exit()

def error(msg):
    print(f"[!] {msg}")
    exit()

def banner():
    print(f"\n *** QDehashed Password Analysis Tool ***\n")

def main(args):
    banner()
    if len(args)!=2:
        usage()
    else:
        file = args[1]
        if path.exists(file):
            print(f"[i] Analysis for file: {file}")
            passwds = {}
            users = []
            with open(file,"r") as qd_results:
                for line in qd_results.readlines():
                    line_array=line.split(",")
                    if len(line_array)>4: ## This is a good line for reading
                        if line_array[4]!="": ## disregard blank entries
                            passwd=line_array[4]
                            user=line_array[1]
                            if user not in users: ## deduplicate
                                users.append(user)
                                if passwd not in passwds: ## No there yet. add it.
                                    passwds[passwd]=0
                                else: ## Already there
                                    passwds[passwd]=passwds[passwd]+1 ## increment it                            
            if len(passwds)>0: ## If we got results, let's look at them
                sorted_passwds=sorted(passwds, key=lambda i: int(passwds[i]), reverse=True)
                print("[i] Top Ten passwords used: \n+=====================================+")
                for i in range(0,10):
                    print(f"[{passwds[sorted_passwds[i]]}] {sorted_passwds[i]}")
            else:
                print(f"[!] No passwords identified in file: {file}")
        else: ## Could not find file specified
            error(f"Could not open file for reading: {file}")

if __name__ == "__main__":
    main(argv)
