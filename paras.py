#######
# Paras (Yet another Parser)
#######
from atoms import *
from errors import BipatSyntax,BipatManager
#### Rules


###############
## Rule Book 
##############
# Keyword rules
class Rule:
    # Consists Rules functions
    #override
    def function_block_rule():
        pass



KEYWORD_RULES = {
    "func_dec":[
        lambda _key,_: (1,1) if _key == "NAME" else (False,"Expected a variable"), # Wow, every rule is a function
        lambda _,_value: (1,1) if _value == "left_small" else (False,"Expected a '('"),
        lambda _,_value:(1,1) if _value == "right_small" else (False,"Expected a ')"),
        # block
        lambda _key,_value: (1,1) if _key == "block" else (False,"Expected a Block")
    ],

    "var_dec":[]
}


### Main Parser Class
class Parser:
    def __init__(self,tokens:list[dict],error_manager:BipatManager) -> None:
        self._tokens = tokens
        self.error_manager = error_manager

        ## RULES
        self.keyword_rules = {
    "func_dec":[
        self.rule_name,
        self.rule_left_small,
        self.rule_right_small,
        self.rule_function_block
    ],

        "var_dec":[]
}
    
    # definition of various rules
    def rule_name(self,_key,_):
        return (1,1) if _key == "NAME" else (False,"Expected a variable")

    def rule_left_small(self,_,_value):
        return (1,1) if _value == "left_small" else (False,"Expected a '('")

    def rule_right_small(self,_,_value):
        return (1,1) if _value == "right_small" else (False,"Expected a ')")
    
    def rule_function_block(self,_key,_):
        return (1,1) if _key == "block" else (False,"Expected a Block")

    
    def _parse_keyword(self,index):
        '''Parses the keyword according to the grammar'''
        _keyword_tup = self._tokens[index]["KEYWORD"]
        _keyword = _keyword_tup[0]
        # _line_no = _keyword_tup[1]
        # _index_no = _keyword_tup[2]
        _rules = KEYWORD_RULES[_keyword] 
        
        # see if rule for a keyword is followed else it is a syntax error
        rules_index = 0
        while  rules_index+index < len(_rules):
            token_keys = list(self._tokens[index+rules_index+1].keys())[0]
            token_values = list(self._tokens[index+rules_index+1].values())[0][0]
            _line_no = list(self._tokens[index+rules_index+1].values())[0][1]
            _index_no = list(self._tokens[index+rules_index+1].values())[0][2]

            response = _rules[rules_index](token_keys,token_values) # call the specific rule book function
            if response[0]:
                rules_index += 1   
            else:
                self.error_manager.show_error_and_exit(BipatSyntax,response[1],_line_no,_index_no)
                rules_index +=1

    def parse(self):
        # parsing different keywords
        # keywords are parsed as stuff that always follow a 
        # pattern
        print(self._tokens)

        for i in range(len(self._tokens)):
            token_type = list(self._tokens[i].keys())[0]

            if token_type == 'KEYWORD':
                self._parse_keyword(i)