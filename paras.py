#######
# Paras (Yet another Parser)
#######
from atoms import *
from errors import BipatSyntax
#### Rules

# Keyword rules
KEYWORD_RULES = {
    "func_dec":[
        {"NAME":""}, # Empty values means, anything can be there like fn foo(){}
        {"PARENTHESIS":"left_small"},
        {"PARENTHESIS":"right_small"},
        {"BLOCK":""},
    ],

    "var_dec":[]
}


### Main Parser Class
class Parser:
    def __init__(self,tokens:list[dict]) -> None:
        self._tokens = tokens
    
    def _parse_keyword(self,index):
        '''Parses the keyword according to the grammar'''
        _keyword_tup = self._tokens[index]["KEYWORD"]
        _keyword = _keyword_tup[0]
        _line_no = _keyword_tup[1]
        _index_no = _keyword_tup[2]
        _rules = KEYWORD_RULES[_keyword] 
        
        # see if rule for a keyword is followed else it is a syntax error
        for i in range(len(_rules)):
            rule_keys = list(_rules[i].keys())[0]
            rule_value = list(_rules[i].values())[0]

            token_keys = list(self._tokens[index+i+1].keys())[0]
            token_values = list(self._tokens[index+i+1].values())[0][0]
            print(rule_keys,rule_value,token_keys,token_values)
            if rule_keys == token_keys: # mactchin keys
                # if empty no need 
                if rule_value !="":
                    if rule_value == token_values:
                        pass# good
                    else:
                        print("ERR") # error
            else:
                print("ERR") # error





    def parse(self):
        # parsing different keywords
        # keywords are parsed as stuff that always follow a 
        # pattern
        print(self._tokens)

        for i in range(len(self._tokens)):
            token_type = list(self._tokens[i].keys())[0]

            if token_type == 'KEYWORD':
                self._parse_keyword(i)