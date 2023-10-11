import asyncio
import os
import sys
from typing import List


async def tokenizer(string: str) -> List[str]:
    output = []
    i = 0
    while i < len(string):
        if string[i] == "{" or string[i] == "}":
            output.append(string[i])
        i += 1
    return output


async def main():
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
            print(await tokenizer(stringval))


asyncio.run(main())
