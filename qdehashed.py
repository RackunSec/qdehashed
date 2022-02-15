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
from sys import exit # for Exit
from texttable import Texttable # for TUBULAR TABLES, DOOD!!
import os # for terminal width
from re import search

version="0.5.20.0b"
## Enter your API token and email address below:
## Get it from: https://www.dehashed.com/profile
full_query={
    "api_auth":("(EMAIL ADDRESS)","(API TOKEN)"),
    "params":{"query":"","size":"10000"}, # what will the user query? (10k is the limit)
    "headers":{"Accept":"application/json"}, # headers required to get "JSON" in the response
    "dehashed_api_url":"https://api.dehashed.com/search", # This might chnage one day, so I put it up here.
    # These are the different types of queries that you can do:
    "query_types_available":["email", "ip_address", "username", "password", "hashed_password", "name"]
}

full_query=SimpleNamespace(**full_query) # make this dot notation (this might not work with requests, maybe with .__dict__ ?)


## INTRODUCTION
print(f"""
   . ___ * .  __    . *     __  .       __   *
    / _ \___ / /  *__  __*_/ /  ___*___/ /     .
*  / // / -_) _ \/ _ `(_-</ _ \/ -_) _  /
  /____/\__/_//_/\_,_/___/_//_/\__/\_,_/ *
 . API QUERY TOOL version: {version}
""")

parser = argparse.ArgumentParser()
parser.add_argument("--query", help="Specify the string to query the Dehashed.com API.", required=True, metavar='(domain|user|name)')
parser.add_argument("--type", help="The type of data to query.", required=True, metavar='(email|ip_address|username|password|hashed_password|name)')
parser.add_argument("--output", help="Output results to a file.", type=argparse.FileType('a'), metavar="OUTPUT_FILE")
parser.add_argument("--tables", help="Output results to a table.", action="store_true")
args = parser.parse_args()

## Ensure that the user chose a correct method to consume:
if args.type not in full_query.query_types_available:
    print(f"\"{args.type}\" is NOT a valid method for the Dehashed API.")
    print(f" Here are the available mehthods: {full_query.query_types_available}\n")
    exit()

## Create a query object:
class APIQuery:
    @staticmethod
    def query(qtype,qstring):
        full_query.__dict__['params']['query']=f"{args.type}:{args.query}"
        ## Make our Request:
        try:
            response = requests.get(
                full_query.dehashed_api_url,
                params=full_query.params,
                headers=full_query.headers,
                auth=full_query.api_auth
            )
            json_response = response.json()
            json_response = SimpleNamespace(**json_response) # dot notation.
            ## print(json_response)  ## DEBUG
            if json_response.success == False:
                if json_response.message=="Invalid API credentials.":
                    print("Invalid API credentials. Please check them in the \"full_query\" variable at the top of this script.")
                    exit()
                else:
                    print(f"Something is wrong with the API query: {json_response.message}")
                    exit()
            # Sun Microsystems.
            if json_response.balance: # does it exist?
                print(f" Dehashed API token balance: {str(json_response.balance)}")
                print(f" Total entries discovered: {str(json_response.total)}")
                print(f" API server sesponse time: {str(json_response.took)}")
            if args.output:
                print(f" Outputting to file: {args.output.name}\n")
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
            else: # NO FILE OUTPUT, JUST SCREEN OUTPUT
                if json_response.entries:
                    if args.tables:
                        tubular_table = Texttable((os.get_terminal_size().columns)-5)
                        tubular_table.add_row(["email","name","username","password","hashed_password"])
                        for entry in json_response.entries:
                            entry = SimpleNamespace(**entry)
                            #print([entry.email,entry.name,entry.username,entry.password,entry.hashed_password])
                            tubular_table.add_row([entry.email,entry.name,entry.username,entry.password,entry.hashed_password])
                        print(tubular_table.draw()) # draw it
                    else:
                        print(f"\nid,email,ip_address,username,password,hashed_password,name,vin,address,phone,database_name") # CSV first line.
                        for entry in json_response.entries:
                            entry = SimpleNamespace(**entry)
                            print(f"{entry.id},",end="")
                            print(f"{entry.email},",end="")
                            print(f"{entry.ip_address},",end="")
                            print(f"{entry.username},",end="")
                            print(f"{entry.password},",end="")
                            print(f"{entry.hashed_password},",end="")
                            print(f"{entry.vin},",end="")
                            print(f"{entry.address},",end="")
                            print(f"{entry.phone},",end="")
                            print(f"{entry.database_name}") # newline OK here.
                        #print(json_response) DEBUG
                    print("")

        except Exception as e:
            print("Something went wrong with the API query")
            print(e)


api = APIQuery()
api.query(args.type,args.query)
