#######
# Paras (Yet another Parser)
#######
from atoms import *
from errors import BipatSyntax
#### Rules


###############
## Rule Book 
##############
# Keyword rules
class Rule:
    # Consists Rules functions
    #override
    def name_rule(self,stuff):
        pass



KEYWORD_RULES = {
    "func_dec":[
        lambda _key,_value: True if _key == "NAME" else False, # Wow, every rule is a function
        lambda _key,_value: True if _value == "left_small" else False,
        lambda _key,_value: True if _value == "right_small" else False,
        # block
        lambda _key,_value: True if _key == "block" else False
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
            token_keys = list(self._tokens[index+i+1].keys())[0]
            token_values = list(self._tokens[index+i+1].values())[0][0]
            
            if _rules[i](token_keys,token_values):
                print("OK")
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