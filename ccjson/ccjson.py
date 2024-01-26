import os, sys, pprint

delimiter_set = set(["[", "]", ",", "{", "}", ":"])

space_set = set({"\n", " ", "\t"})
default_values_dict = {"true": True, "false": False, "null": None}
stack = []
token_index = 0

def tokenize(string_input: str) -> list[str]:
    pointer1 = 0
    tokens = []
    while pointer1 < len(string_input):
        if string_input[pointer1] in delimiter_set:
            tokens.append(string_input[pointer1])
            pointer1 += 1
        elif string_input[pointer1] == '"':
            temp = string_input[pointer1]
            pointer1 += 1
            while pointer1 < len(string_input):
                if string_input[pointer1] == "\\":
                    # Escape sequence started so we should take this and the next character along with us
                    temp += string_input[pointer1 : pointer1 + 2]
                    pointer1 += 2
                    continue
                else:
                    temp += string_input[pointer1]
                if string_input[pointer1] == '"':
                    break
                pointer1 += 1
            pointer1 += 1
            tokens.append(temp)
        elif string_input[pointer1] == "\n" or string_input[pointer1] == " ":
            pointer1 += 1
            continue
        else:
            temp = string_input[pointer1]
            pointer1 += 1
            while pointer1 < len(string_input):
                if (
                    string_input[pointer1] in delimiter_set
                    or string_input[pointer1] in space_set
                ):
                    break
                temp += string_input[pointer1]
                pointer1 += 1
            tokens.append(temp)
    return tokens


def isFloat(s: str) -> bool:
    if len(s.split(".")) == 2:
        [a,b] = s.split(".")
        if len(a) > 1 and a.startswith("0"):
            return False
        if "E" in b or "e" in b:
            b = b.upper()
            [upper,lower] = b.split("E")
            if not upper.isnumeric():
                return False
            if not(lower.isnumeric() or (
                (lower.startswith("+") or lower.startswith("-"))
                and lower[1:].isnumeric()
            )):
                return False
        return True
    if "E" in s or "e" in s:
        print(s)
        [upper,lower] = s.upper().split("E")
        if len(upper) == 1 and not upper.isnumeric():
            return False
        if upper.startswith("0"):
            return False
        if not upper.isnumeric():
            return False
        if not (lower.isnumeric() or (
            (lower.startswith("+") or lower.startswith("-")) and 
            lower[1:].isnumeric() 
        )):
            return False
    return True

def isInt(s:str)->bool:
    if len(s) == 1 and s.isdigit():
        return True
    if s.startswith("0"):
        return False
    return True
            

def parse_array(tokens: list[str]):
    global token_index
    array = []
    while tokens[token_index] != "]" and token_index < len(tokens):
        if tokens[token_index] == ",":
            if (
                token_index + 1 < len(tokens)
                and (
                    tokens[token_index + 1] in "{["
                    or tokens[token_index + 1] in default_values_dict
                    or parse_value(tokens[token_index + 1])
                )
                and (
                    tokens[token_index - 1] in "}]"
                    or tokens[token_index - 1] in default_values_dict
                    or parse_value(tokens[token_index - 1])
                )
            ):
                token_index += 1
            else:
                # print(tokens[token_index + 1])
                # print(tokens[token_index - 1])
                # print(tokens[token_index])
                raise ValueError("Invalid delimiter found")
        elif tokens[token_index] == "[":
            token_index += 1
            array.append(parse_array(tokens))
        elif tokens[token_index] == "{":
            token_index += 1
            array.append(parse_object(tokens))
        elif tokens[token_index] == ":":
            raise ValueError(": found in array function")
        elif tokens[token_index] == "}":
            raise ValueError("} found in array: Invalid JSON")
        else:
            array.append(parse_value(tokens[token_index]))
            token_index += 1
    if tokens[token_index] == "]":
        token_index += 1
        return array
    else:
        raise ValueError("Invalid JSON structure")


def parse_value(s: str):
    if s.startswith('"') and s.endswith('"'):
        # String type
        return s[1:-1]
    elif s in default_values_dict:
        return default_values_dict[s]
    elif isFloat(s):
        return float(s)
    elif isInt(s):
        return int(s)
    elif "\\" in s:
        # we need to ensure that there are no illegal values - this will also throw an exception so we need to catch it
        return s.encode().decode("unicode_escape")
    else:
        raise ValueError(f"Something went wrong while parsing the value {s}")


def parse_key(s: str):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    elif s.startswith("'") or s.endswith("'"):
        raise ValueError(f"{s} cannot start or end with ' single quotes")
    elif s in delimiter_set:
        raise ValueError(f"Found an invalid expression")
    else:
        raise ValueError(f"String was not closed correctly for {s}")


def parse_object(tokens: list[str]):
    global token_index
    processing_key = True
    obj = {}
    while tokens[token_index] != "}" and token_index < len(tokens):
        if tokens[token_index] == ":":
            key = parse_key(tokens[token_index - 1])
            token_index += 1
            if tokens[token_index] == "{":
                token_index += 1
                obj[key] = parse_object(tokens)
                continue
            elif tokens[token_index] == "[":
                token_index += 1
                obj[key] = parse_array(tokens)
                continue
            else:
                obj[key] = parse_value(tokens[token_index])
        elif tokens[token_index] == ",":
            # Check if the next token is a key value combination
            # If tokenization was correctly done then
            # the next value will be a key and the value
            # two places from it will be a value or an object
            if token_index + 2 < len(tokens) and tokens[token_index + 2] == ":":
                if tokens[token_index + 1] in delimiter_set:
                    raise ValueError(
                        "We have an invalid delimiter at a where a key was expected"
                    )
                if tokens[token_index + 3] in ",}]:":
                    raise ValueError("Expected a value got invalid delimiter")
            else:
                raise ValueError(
                    "Invalid JSON due to missing key value combination or extra comma"
                )
        token_index += 1
    if tokens[token_index] == "}":
        token_index += 1
        return obj
    else:
        raise ValueError("invalid object")


def parse(tokens):
    global token_index
    output = None
    if len(tokens) == 0:
        raise ValueError("Empty file")
    if tokens[0] not in "[{":
        raise ValueError("JSON needs to be an object or array")
    if tokens[0] == "[":
        token_index += 1
        output = parse_array(tokens)
    elif tokens[0] == "{":
        token_index += 1
        output = parse_object(tokens)
    return output


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        if not os.path.exists(os.path.join(os.getcwd(), filename)):
            print("File does not exist")
            sys.exit(1)
        file = open(filename)
        tokens = tokenize(file.read())
        # print(tokens)
        pprint.pprint(parse(tokens))
        print(token_index)
        if token_index < len(tokens):
            raise ValueError("Invalid JSON, found extra token at end")
        if not file.closed:
            file.close()
