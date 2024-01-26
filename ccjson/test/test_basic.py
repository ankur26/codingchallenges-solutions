import pytest,os
from ccjson import tokenize,clean_up

basic_test_path = os.path.join(os.getcwd(),'test/basic')




def test_tokenizer_for_empty_object():
    '''Object used for test is {}'''
    with open(f"{basic_test_path}/step1/valid.json") as f:
        tokens = tokenize(f.read())
        assert len(tokens) == 2
        assert tokens[0] == '{' and tokens[1] == '}'

def test_tokenizer_for_empty_file():
    '''Invalid file is empty in step 1 but should not impact tokenization'''
    with open(f"{basic_test_path}/step1/invalid.json") as f:
        tokens = tokenize(f.read())
        assert len(tokens) == 0


def test_tokenizer_for_single_object():
    #Refer to file attached in the tests folder
    with open(f"{basic_test_path}/step2/valid.json") as f:
        tokens = tokenize(f.read())
        # print(tokens)
        assert len(tokens) == 5 
        assert tokens[0] == '{'
        assert tokens[-1] == '}'
        assert tokens[1] == '"key"' and tokens[2] == ":" and tokens[3] == '"value"'

def test_tokenizer_for_multiple_keys():
    #Refer to file attached in the tests folder
    with open(f"{basic_test_path}/step2/valid2.json") as f:
        tokens = tokenize(f.read())
        assert len(tokens) == 9
        assert tokens[0] == '{' and tokens[-1] == '}'
        assert tokens[1] == '"key"' and tokens[2] == ":" and tokens[3] == '"value"'
        assert tokens[4] == ','
        assert tokens[5] == '"key2"' and tokens[6] == ":" and tokens[7] == '"value"'

def test_tokenizer_for_array_elements_and_nested_objects():
    #Directly skipping to step4 file, please refer to that
    with open(f"{basic_test_path}/step4/valid2.json") as f:
        tokens = tokenize(f.read())
        assert len(tokens) == 23
        assert tokens[0] == '{' and tokens[-1] == '}'
        assert tokens[1] == '"key"' and tokens[3] == '"value"'
        #Test a non string value being stored without double quotes
        assert tokens[7] == '101'
        #Test whether inner object got tokenized correctly
        assert tokens[11] == '{' and tokens[15] == '}'
        assert tokens[12] == '"inner key"' and tokens[14] == '"inner value"'


