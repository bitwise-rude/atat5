#######
# Paras (Yet another Parser)
#######
from atoms import *
from errors import BipatSyntax,BipatManager


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

        "var_dec":[
            self.rule_name,
            self.rule_equals,
            self.rule_numbers,
            self.rule_semicolon,
        ]
}
        # explained in ast.txt
        self.AST = []
    
    # definition of various rules returns a tuple (True,no_of_tokens to skip)
    def rule_name(self,_key,_,_ind) -> tuple:
        return (True,1) if _key == "NAME" else (False,"Expected a variable")

    def rule_left_small(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == "left_small" else (False,f"Expected a '{BRACKETS['left_small']}'")

    def rule_right_small(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == "right_small" else (False,f"Expected a '{BRACKETS["right_small"]}'")

    def rule_equals(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == EQUALS else (False,f"Expected a {EQUALS}")

    def rule_numbers(self,keys,_,_ind) -> tuple:
        return (True,1) if keys == "NUMBER" else (False, f"Expected a Number Literal")
    
    def rule_semicolon(self,keys,_,_ind) -> tuple:
        return (True,1) if keys == "SEMI" else (False, f"Expected a {SEMI}")
    
    def rule_function_block(self,_,_value,_ind)-> tuple:
        if _value == "left_curly": # blocks start with curly 
            ## Now Parse after left_curly till the next right_curly
            new = self.parse(_ind+1,till="right_curly") # parse after the curly bracket

            if new == -1:
                return (False,f'Expected to Close the function using a {BRACKETS['right_curly']}')
            # print(new-_ind) is the covered
            return (True,new-_ind)
        
        else:
            return (False,"Function Blocks Start with '{")
    
    
    def _parse_keyword(self,index):
        '''Parses the keyword according to the grammar'''
        _keyword_obj = self._tokens[index]
        _keyword = _keyword_obj.val

        _rules = self.keyword_rules[_keyword] 

        _covered = 0 # REMEMBER : minimum tokens to skip will be rules
        # see if rule for a keyword is followed else it is a syntax error
        rules_index = 0
        while  rules_index < len(_rules):
            # token_keys = self._tokens[index+rules_index+1].type
            # token_values = list(self._tokens[index+rules_index+1].values())[0][0]
            # _line_no = list(self._tokens[index+rules_index+1].values())[0][1]
            # _index_no = list(self._tokens[index+rules_index+1].values())[0][2]

            token_keys = self._tokens[index+rules_index+1].type
            token_values = self._tokens[index+rules_index+1].val
            _line_no = self._tokens[index+rules_index+1].line_no
            _index_no = self._tokens[index+rules_index+1].pos

            response = _rules[rules_index](token_keys,token_values,index+rules_index+1) # call the specific rule book function
            if response[0]:
                rules_index += 1   
                _covered += (response[1]-1)

            else:
                self.error_manager.show_error_and_exit(BipatSyntax,response[1],_line_no+1,_index_no+1)
                rules_index +=1
        return _covered + rules_index +1 

    def parse(self,current=0,till=None):
        # parsing different keywords
        # keywords are parsed as stuff that always follow a 
        # pattern
        # current means from where to start (tokens list) 
        # to maintain recursivity -> till, parse till what 


        while current < len(self._tokens):
            token_type = self._tokens[current].type
            token_type_value = (self._tokens[current]).val
            
            if till and (till == token_type_value): # useful for blocks
                current += 1 
                return current

            elif token_type == 'KEYWORD':
                covered_ = self._parse_keyword(current)
                current += covered_
            
            else:
                self.error_manager.show_error_and_exit(SyntaxError,"NOT IMPLEMENTED")
        
        # if top level didn't find till
        if till:
            return -1
         
        # self.error_manager.show_error_and_exit(SyntaxError,"NOT IMPLEMENTED  2")