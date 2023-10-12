import asyncio
import os
import sys
from pprint import pprint
from typing import List


async def tokenizer(string: str) -> List[str]:
    output = []
    i = 0
    if len(string) == 0:
        return ""
    while i < len(string):
        # print(i)
        if string[i] == "{" or string[i] == "}" or  string[i] == ":" or string[i]==",":
            output.append(string[i])
            i+=1
            continue
        elif string[i] == '"':
            temp = '"'
            i+=1
            while string[i] != '"':
                temp += string[i]
                i+=1
            temp += string[i]
            i+=1
            output.append(temp)
            continue
        elif string[i] == "\n" or string[i] == " ":
            i+=1
            continue
        else:
            temp=""
            while string[i] != "}" and string[i] != "," and string[i] != "\n" and string!=" ":
                temp += string[i]
                i+=1
            output.append(temp)
            continue
    # print(output)
    return output

async def determine_value_type(string:str)-> int | bool | str | float | None :
    if '"' in string:
        return string.replace('"','')
    if string == "true":
        return True
    if string == "false":
        return False
    if string == "null":
        return None
    if string.isnumeric():
        return int(string)
    if string.isdecimal():
        return float(string)
    
    print("Invalid value {}".format(string))
    sys.exit(1)

async def analyse_syntax(tokens:List):
    current_object = None
    token_stack = []
    i = 0
    # print(tokens)
    while i < len(tokens):
        # print(token_stack)
        if tokens[i] == "{":
            token_stack.append(tokens[i])
            current_object = {}
        elif tokens[i] == ":":
            i+=1
            if tokens[i] == ",":
                print("Invalid JSON format, expected key value got empty")
                sys.exit(1)
            if token_stack[-1] == ",":
                print("Missing key for value")
                sys.exit(1)
            if tokens[i]:
                current_object[token_stack.pop(-1)] = await determine_value_type(tokens[i])
                # If a key value gets added then we should also see that the token stack will probably have a comma value
                if token_stack[-1] == ",":
                    #If so we can safely pop this
                    token_stack.pop(-1)
        elif tokens[i] == "}":
            # We should ideally be left with only 1 value here
            if token_stack[-1] == "{":
                token_stack.pop(-1)
            else:
                if token_stack[-1] == ",":
                    print("Extra comma before object ending")
                if len(token_stack) == 0:
                    print("missing parenthesis")
                sys.exit(1)
        elif tokens[i] == ",":
            token_stack.append(tokens[i])
        else:
            if tokens[i][0] == '"' and tokens[i][-1] == '"' and len(tokens[i]) > 2:
                token_stack.append(tokens[i].replace('"',''))
            else:
                print("Invalid key value")
                sys.exit(1)
        i+=1
    return current_object if current_object else ""
            

async def main():
    # print(os.getcwd())
    files = []
    for index, arg in enumerate(
        sys.argv
    ):  # We choose to ignore the first argument as we know it's going to be the program name
        # Simpler check if file mentioned exists
        if index == 0:
            continue
        if not os.path.exists(arg):
            sys.exit(1)
        else:
            if not os.path.isdir(arg) and arg.endswith(".json"):
                files.append(arg)
    for file in files:
        with open(file, "r") as f:
            stringval = f.read()
            pprint(await analyse_syntax(await tokenizer(stringval)))


asyncio.run(main())
