#######
# Paras (Yet another Parser)
#######
from atoms import *
#### Rules

# Keyword rules
KEYWORD_RULES = {
    "func_dec":[
        {"NAME":""}, # Empty values means, anything can be there like fn foo(){}
        {"PARENTHESIS":"left_small"},
        {"PARENTHESIS":"right_small"},
        {"BLOCK":""},
        ]
}


### Main Parser Class
class Parser:
    def __init__(self,tokens:list[dict]) -> None:
        self._tokens = tokens
    
    def _parse_keyword(self,_keyword):
        '''Parses the keyword according to the grammar'''
        print(_keyword)


    def parse(self):
        # parsing different keywords
        # keywords are parsed as stuff that always follow a 
        # pattern
        print(self._tokens)

        for tkns in self._tokens:
            token_type = list(tkns.keys())[0]

            if token_type == 'KEYWORD':
                self._parse_keyword(tkns[token_type])