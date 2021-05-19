#!/usr/bin/env python3
#
# Query dehashed with your API key
# Useful during Reconnaissance of penetration tests
# to abuse password reuse
#
import argparse # for arguments
from types import SimpleNamespace # for dot notation
import json # to interpret results
import requests # for API query
import sys # for Exit

version="0.5.19.0a"
## Enter your API token and email address below:
## Get it from: https://www.dehashed.com/profile
full_query={
    "api_auth":("<EMAIL>","<API TOKEN>"),
    "params":{"query":""}, # what will the user query?
    "headers":{"Accept":"application/json"},
    "dehashed_api_url":"https://api.dehashed.com/search",
    "query_types_available":["email", "ip_address", "username", "password", "hashed_password", "name"]
}

full_query=SimpleNamespace(**full_query) # make this dot notation (this might not work with requests, maybe with .__dict__ ?)

## UI Colors:
class prompt_color:
    bcolors = {
        'OKGREEN' : '\033[3m\033[92m ✔ ',
        'FAIL' : '\033[3m\033[91m ✖ ',
        'GREEN' : '\033[92m',
        'RED' : '\033[91m',
        'ENDC' : '\033[0m',
        'BOLD' : '\033[1m',
        'YELL' : '\033[33m\033[3m',
        'ITAL' : '\033[3m',
        'UNDER' : '\033[4m',
        'BLUE' : '\033[34m',
        'BUNDER': '\033[1m\033[4m',
        'WARN': '\033[33m   ',
        'COMMENT': '\033[37m\033[3m',
        'QUESTION': '\033[3m ',
        'INFO': ' ',
        'BLINK': '\033[5m',
        'GREY':'\033[37m'
    }
color = SimpleNamespace(** prompt_color.bcolors) # create color object to use throughout.

## INTRODUCTION
print(f"""{color.BLUE}
   . ___ * .  __    . *     __  .       __   *
    / _ \___ / /  *__  __*_/ /  ___*___/ /     .
*  / // / -_) _ \/ _ `(_-</ _ \/ -_) _  /
  /____/\__/_//_/\_,_/___/_//_/\__/\_,_/ *
 . {color.ITAL}API QUERY TOOL version: {color.ENDC}{color.ITAL}{color.BOLD}{color.GREEN}{version}{color.ENDC}
""")

## END GRACEFULLY
def quit_me():
    print(f"{color.ENDC}",end="")
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument("--query", help="Specify the string to query the Dehashed.com API.", required=True, metavar='(domain|user|name)')
parser.add_argument("--type", help="The type of data to query.", required=True, metavar='(email|ip_address|username|password|hashed_password|name)')
parser.add_argument("--output", help="Output results to a file.", type=argparse.FileType('a'), metavar="OUTPUT_FILE")
args = parser.parse_args()

## Ensure that the user chose a correct method to consume:
if args.type not in full_query.query_types_available:
    print(f"{color.FAIL}\"{args.type}\" is NOT a valid method for the Dehashed API.")
    print(f"    Please check the Deshashed API and try again.{color.ENDC}\n")
    quit_me()

## Create a query object:
class APIQuery:
    @staticmethod
    def query(qtype,qstring):
        full_query.__dict__['params']['query']=f"{args.type}:{args.query}"
        #print(full_query.__dict__) # DEBUG
        ## Make our Request:
        response = requests.get(
            full_query.dehashed_api_url,
            params=full_query.params,
            headers=full_query.headers,
            auth=full_query.api_auth
        )
        json_response = response.json()
        json_response = SimpleNamespace(**json_response) # dot notation. Sun Microsystems.
        if json_response.balance: # does it exist?
            print(f"{color.OKGREEN}{color.ENDC}{color.ITAL} Dehashed API token balance: {color.BLUE}{str(json_response.balance)}{color.ENDC}")
            print(f"{color.OKGREEN}{color.ENDC}{color.ITAL} Total entries discovered: {color.BLUE}{str(json_response.total)}{color.ENDC}")
            print(f"{color.OKGREEN}{color.ENDC}{color.ITAL} API server sesponse time: {color.BLUE}{str(json_response.took)}{color.ENDC}")
        if args.output:
            print(f"{color.OKGREEN}{color.ENDC} Outputting to file: {color.BLUE}{args.output.name}{color.ENDC}\n")
            print(f"id,email,ip_address,username,password,hashed_password,name,vin,address,phone,database_name",file=args.output) # CSV first line.
            if json_response.entries:
                for entry in json_response.entries:
                    entry = SimpleNamespace(**entry)
                    print(f"{entry.id},",end="",file=args.output)
                    print(f"{entry.email},",end="",file=args.output)
                    print(f"{entry.ip_address},",end="",file=args.output)
                    print(f"{entry.username},",end="",file=args.output)
                    print(f"{entry.password},",end="",file=args.output)
                    print(f"{entry.hashed_password},",end="",file=args.output)
                    print(f"{entry.vin},",end="",file=args.output)
                    print(f"{entry.address},",end="",file=args.output)
                    print(f"{entry.phone},",end="",file=args.output)
                    print(f"{entry.database_name}",file=args.output) # newline OK here.
        else:
            if json_response.entries:
                print(f"\n{color.BOLD}id,email,ip_address,username,password,hashed_password,name,vin,address,phone,database_name{color.ENDC}") # CSV first line.
                for entry in json_response.entries:
                    entry = SimpleNamespace(**entry)
                    print(f"{color.GREY}{entry.id}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.email}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.ip_address}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.username}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.password}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.hashed_password}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.vin}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.address}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.phone}{color.ENDC},",end="")
                    print(f"{color.GREY}{entry.database_name}{color.ENDC}") # newline OK here.
                #print(json_response) DEBUG
                print("")

api = APIQuery()
api.query(args.type,args.query)

quit_me()
