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
        if (
            string[i] == "{"
            or string[i] == "}"
            or string[i] == ":"
            or string[i] == ","
            or string[i] == "["
            or string[i] == "]"
        ):
            #This is our generic token addition.
            output.append(string[i])
            i += 1
            continue
        elif string[i] == '"':
            # This is the area that processes a value.
            temp = '"'
            i += 1
            while string[i]!="," and string[i]!=":": # We should really probably expect a comma here
                temp += string[i]
                i += 1
            output.append(temp)
            continue
        elif string[i] == "\n" or string[i] == " ":
            # This is our whitespace and line break ignore section
            i += 1
            continue
        else:
            # This is the are that processes keys
            temp = ""
            while (
                string[i] != "}"
                and string[i] != "]"
                and string[i] != ","
                and string[i] != "\n"
                and string != " "
            ):
                if (
                    string[i] == "'" and temp[0] !='"'
                ):  # We cannot allow single quotes in if it's a string type
                    print("Invalid token")
                    sys.exit(1)
                temp += string[i]
                i += 1
            output.append(temp)
            continue
    # print(output)
    return output


async def determine_value_type(string: str) -> int | bool | str | float | None:
    if '"' in string:
        return string.replace('"', "")
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


async def analyse_syntax(tokens: List):
    current_object = None
    token_stack = []
    # print(tokens)
    # We do an intermediate check to ensure that the first part of JSON is actually an { or a [
    if tokens[0] != "{" and tokens[0] !="[":
        print("Invalid JSON: should always begin with a { or a [")
        sys.exit(1)
    while tokens:
        token = tokens.pop(0)
        # print(token_stack)
        if token == "[":
            token_stack.append(token)
            current_object = []
        elif token == "{":
            token_stack.append(token)
            current_object = {}
        elif token == ":":
            if isinstance(current_object,list):
                print("Colon cannot be inserted in array")
                sys.exit(1)
            token = tokens.pop(0)
            if token == ",":
                print("Invalid JSON: Invalid JSON format, expected key value got empty")
                sys.exit(1)
            if token_stack and token_stack[-1] == ",":
                print("Invalid JSON: Missing key for value")
                sys.exit(1)
            if token == "{":
                temp_array = []
                while not token == "}":
                    temp_array.append(token)
                    token = tokens.pop(0)
                # double check the value of the token ender is indeed the } bracket
                if token == "}":
                    temp_array.append(token)
                    if isinstance(current_object, dict):
                        current_object[token_stack.pop(-1)] = await analyse_syntax(
                            temp_array
                        )
                    elif isinstance(current_object, list):
                        current_object.append(await analyse_syntax(temp_array))
                    if token_stack and token_stack[-1] == ",":
                        token_stack.pop(-1)
            elif token == "[":
                temp_array = []
                while not token == "]":
                    temp_array.append(token)
                    token = tokens.pop(0)
                # double check the value of the token ender is indeed the ] bracket
                if token == "]":
                    temp_array.append(token)
                    if isinstance(current_object, dict):
                        current_object[token_stack.pop(-1)] = await analyse_syntax(
                            temp_array
                        )
                    elif isinstance(current_object, list):
                        current_object.append(await analyse_syntax(temp_array))
                    if token_stack and token_stack[-1] == ",":
                        token_stack.pop(-1)
            elif token:
                if isinstance(current_object, dict):
                    current_object[token_stack.pop(-1)] = await determine_value_type(
                        token
                    )
                elif isinstance(current_object, list):
                    current_object.append(
                        await determine_value_type(token_stack.pop(-1))
                    )
                # If a key value gets added then we should also see that the token stack will probably have a comma value
                if token_stack and token_stack[-1] == ",":
                    # If so we can safely pop this
                    token_stack.pop(-1)
        elif token == "}":
            # We should ideally be left with only 1 value here
            if token_stack and token_stack[-1] == "{":
                token_stack.pop(-1)
            if token_stack and token_stack[-1] == ",":
                print("Invalid JSON: Extra comma before object ending")
                sys.exit(1)
            if len(token_stack) == 0:
                print("Invalid JSON: Extra content or } seems to be added in the end")
                sys.exit(1)
        elif token == ",":
            token_stack.append(token)
        elif token == "]":
            # we need to ensure that there's no trailing comma
            if token_stack and token_stack[-1] == "[":
                token_stack.pop(-1)
            if token_stack and token_stack[-1] == ",":
                print("Extra comma before array entry")
                sys.exit(1)
            if len(token_stack) == 0:
                print("Invalid JSON: Extra ] or content at the end")
                sys.exit(1)
        else:
            if token[0] == '"' and token[-1] == '"' and len(token) > 2:
                if isinstance(current_object, list):
                    current_object.append(token.replace('"', ""))
                elif isinstance(current_object, dict):
                    token_stack.append(token.replace('"', ""))
            else:
                print("Invalid JSON: Invalid key value")
                sys.exit(1)
    if len(token_stack) > 0:
        print("Invalid JSON: unknown error")
        sys.exit(1)
    print(tokens)
    if len(tokens) > 0:
        print("Invalid JSON format: extra content that does not fit.")
        sys.exit()
    return current_object


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
        print(file)
        with open(file, "r") as f:
            stringval = f.read()
            pprint(await analyse_syntax(await tokenizer(stringval)))


asyncio.run(main())
