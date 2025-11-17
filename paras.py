#######
# Paras (Yet another Parser)
#######
from atoms import *
from errors import BipatSyntax,BipatManager

## AST CLASSES
class Node:
    def __init__(self,name:str):
        self.left = None
        self.right =None # will be nodes fix later
        self.mid = None # for ternary operators like arrays
        self.name = name

    
    def __repr__(self):
        return f'NODE={self.name} - LEFT={self.left}, MID={self.mid}, RIGHT={self.right}'

### Main Parser Class
class Parser:
    def __init__(self,tokens:list[dict],error_manager:BipatManager) -> None:
        self._tokens = tokens
        self.error_manager = error_manager

        ## RULES
        self.keyword_rules = {
    "func_dec":[
        self.rule_fn_name,
        self.rule_left_small,
        self.rule_right_small,
        self.rule_function_block
    ],

        "var_dec":[
            self.rule_var_dec_name,
            self.rule_equals,
            self.rule_var_dec,
            self.rule_semicolon,
        ],

        "cond":[
                self.rule_if_statement,
                self.rule_if_block,
        ],

        "while":[
            self.rule_while_statement,
            self.rule_while_block,
        ]
}
        # explained in ast.txt
        self.AST = []

        self.current_function_block = []
        self.current_working_function = "1" # TODO: outside world

        self.workingNode = None


    def _get_tokens_till(self,_start,_till) -> tuple[list,int]:
        # stating from index _start, returns all the token till value "_till"
        _list = []
        for i in range(_start,len(self._tokens)):
            if self._tokens[i].val == _till:
                return (_list,i)
            else:
                _list.append(self._tokens[i])
        return None
    
    # definition of various rules returns a tuple (True,no_of_tokens to skip)
    def rule_fn_name(self,_key,_value,_ind) -> tuple:
        if _key == "NAME":
            self.current_function_block.clear() # new function
            self.current_working_function = _value
            return (True,1)
        else:
            return (False,"Expected A Name for Function\n Use 'main' for the main function")
        
    def rule_var_dec_name(self,_key,_value,_ind) -> tuple:
        _ = Node(name="VAR_DEC")
        _.left = _value
        self.workingNode = _
        return (True,1) if _key == "NAME" else (False,"Expected a Name for a Variable")

    def rule_left_small(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == "left_small" else (False,f"Expected a '{BRACKETS['left_small']}'")

    def rule_right_small(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == "right_small" else (False,f"Expected a '{BRACKETS["right_small"]}'")

    def rule_equals(self,_,_value,_ind)-> tuple:
        return (True,1) if _value == "EQUALS" else (False,f"Expected a {EQUALS}")
    
    def rule_if_statement(self,keys,val,_ind) -> tuple:
        _ = Node('COND')
        _.left = 'if'
        self.workingNode = _

        _,_indg = self.evaluate_mathematical_expression(keys,val,_ind,evaluate_till="left_curly")
        self.current_function_block.append(self.workingNode)
        
        return _[0],_indg - _ind + 1

    def rule_while_statement(self,keys,val,_ind) -> tuple:
        _ = Node('COND')
        _.left = 'while'
        self.workingNode = _

        _,_indg = self.evaluate_mathematical_expression(keys,val,_ind,evaluate_till="left_curly")
        self.current_function_block.append(self.workingNode)
        
        return _[0],_indg - _ind + 1

    
    
    def evaluate_mathematical_expression(self,keys,val,_ind,workingNode=None,evaluate_till="SEMI",isMid=False):
        workingNode = self.workingNode if not workingNode else workingNode

        if self._tokens[_ind+1].val == "left_square":
            temp_node = Node('ARRAY_ACCESS')
            temp_node.left = val  # variable name
            
            # evaluate the index
            _,_indg = self.evaluate_mathematical_expression(self._tokens[_ind+2].type,self._tokens[_ind+2].val,_ind+2,evaluate_till="right_square",workingNode=temp_node)
            
            # check for errors using _ and _indg
            # print(self._tokens[_indg+1])

            # now move forward
        

            self._tokens[_ind:_indg+2] = [temp_node]
            val = temp_node
            # return self.evaluate_mathematical_expression(self._tokens[_indg+1].type,self._tokens[_indg+1].val,_indg+1,)

        # print(self._tokens)
        print(self._tokens[_ind+1])


        if self._tokens[_ind+1].val == evaluate_till: # for single valued stuff
            # could be array
            
            try:
                if self._tokens[_ind].name == "ARRAY_ACCESS":
                    
                    if not isMid:
                        workingNode.right = self._tokens[_ind]
                    else:
                        workingNode.mid = self._tokens[_ind]
                    return (True,1), _ind
            except AttributeError:
                pass
            
            # this means this is just one thing
            if keys == "NUMBER" or keys == "NAME":
                if not isMid:
                    workingNode.right = val
                else:
                    workingNode.mid = val
                return (True,1),_ind
            else:
                return (False,f"Expected some value"),_ind
   
        else:
                ## for an entire expression
            if self._tokens[_ind+1].type == "OPERATOR":
                new_node = Node(self._tokens[_ind+1].val)

          
                new_node.left = val

                if isMid:
                    workingNode.mid = new_node
                else:
                    workingNode.right = new_node
                    
                ## aghh
                keys = self._tokens[_ind + 2].type
                val = self._tokens[_ind + 2].val

                return self.evaluate_mathematical_expression(keys=keys,val=val,_ind = _ind + 2, workingNode=new_node,evaluate_till=evaluate_till)


    

    def rule_var_dec(self,keys,val,_ind) -> tuple:   
        ## if array
        _indg = _ind
        if val == "left_square":
            # array detected
            array_values = []
            _ind +=1
            while self._tokens[_ind].val != "right_square":
                if self._tokens[_ind].val == "COMMA":
                    _ind +=1 # skip comma
                elif self._tokens[_ind].type == "NUMBER":
                    array_values.append(self._tokens[_ind].val)
                    _ind +=1
                else:
                    return (False,"Expected a number inside array declaration"),_ind
            _ = Node('ARRAY_DEC')
            _.left = array_values
            self.workingNode.right = _
            return (True, _ind-_indg+1)  # tokens to skip
        # if not array 
        _,_indg = self.evaluate_mathematical_expression(keys,val,_ind)
        return _[0],_indg - _ind + 1
            
    
    def rule_semicolon(self,keys,_,_ind) -> tuple:
        self.current_function_block.append(self.workingNode)
        return (True,1) if keys == "SEMI" else (False, f"Expected a {SEMI}")
    
    def rule_if_block(self,_,_value,_ind) -> tuple:
        if _value == 'left_curly':
            new = self.parse(_ind + 1, till = 'right_curly') # parse after the curly bracket
            if new == -1:
                return (False,f'Expected to Close the if statement using a {BRACKETS['right_curly']}')
            self.current_function_block.append(Node('END_IF'))
            return (True,new-_ind)
        else:
            return (False,"IF Blocks MUST start with '{'")
    
    def rule_while_block(self,_,_value,_ind) -> tuple:
        if _value == 'left_curly':
            new = self.parse(_ind + 1, till = 'right_curly') # parse after the curly bracket
            if new == -1:
                return (False,f'Expected to Close the while statement using a {BRACKETS['right_curly']}')
            self.current_function_block.append(Node('END_WHILE'))
            return (True,new-_ind)
        else:
            return (False,"IF Blocks MUST start with '{'")
    
    def rule_function_block(self,_,_value,_ind)-> tuple:
        
        if _value == "left_curly": # blocks start with curly 
            ## Now Parse after left_curly till the next right_curly
            new = self.parse(_ind+1,till="right_curly") # parse after the curly bracket
            
            self.AST.append((self.current_working_function,self.current_function_block))
            if new == -1:
                return (False,f'Expected to Close the function using a {BRACKETS['right_curly']}')
            # print(new-_ind) is the covered
            return (True,new-_ind)
        
        else:
            return (False,"Function Blocks Start with '{'")
    
    
    def _parse_keyword(self,index):
        '''Parses the keyword according to the grammar'''
        _keyword = self._tokens[index].val
        _rules = self.keyword_rules[_keyword] 

        _covered = 0 # REMEMBER : minimum tokens to skip will be rules
        # see if rule for a keyword is followed else it is a syntax error
        rules_index = 0
        while  rules_index < len(_rules):
            token_keys = self._tokens[index+rules_index+1+_covered].type
            token_values = self._tokens[index+rules_index+1+_covered].val
            _line_no = self._tokens[index+rules_index+1+_covered].line_no
            _index_no = self._tokens[index+rules_index+1+_covered].pos

            response = _rules[rules_index](token_keys,token_values,index+rules_index+1+_covered) # call the specific rule book function
            if response[0]:
                rules_index += 1   
                _covered += (response[1]-1)

            else:
                self.error_manager.show_error_and_exit(BipatSyntax,response[1],_line_no,_index_no)
                rules_index +=1
        return _covered + rules_index +1 

    def _parse_names(self,index):
        ## like a = 5; after assigning a variable


        # next shold be equals 
        if self._tokens[index+1].val != "EQUALS" :
            if self._tokens[index+1].type != "UN_OPERATOR": # or uniary operation
                # or array assignment
                if self._tokens[index+1].val != "left_square":
                    self.error_manager.show_error_and_exit(BipatSyntax,"Expected an Equals Sign after name",self._tokens[index+1].line_no,self._tokens[index+1].pos)
                    return
                else: # if is array assignment
                    _ = Node("ARRAY_ASSIGN")
                    self.workingNode = _
                    self.workingNode.left = self._tokens[index].val  # variable name

                    # evaluate the index
                    _,_indg = self.evaluate_mathematical_expression(self._tokens[index+2].type,self._tokens[index+2].val,index+2,evaluate_till="right_square",isMid=True)
                    
                    
                    # should be equal to now 
                    if self._tokens[_indg+2].val != "EQUALS":
                        self.error_manager.show_error_and_exit(BipatSyntax,"Expected an Equals Sign after array index",self._tokens[_indg+1].line_no,self._tokens[_indg+1].pos)
                        return
            
                    # now evaluate the right side expression
                    _,_indg2 = self.evaluate_mathematical_expression(self._tokens[_indg+3].type,self._tokens[_indg+3].val,_indg+3)
                    self.current_function_block.append(self.workingNode)
                    return _indg2 - index +2 # for semi
            else:
                if self._tokens[index+1].val == "INC":
                    _ =Node("INC")
                    _.left = self._tokens[index].val # variable name
                    self.current_function_block.append(_)
                    return 3 # for semi
                elif self._tokens[index+1].val == "DEC":
                    _ =Node("DEC")
                    _.left = self._tokens[index].val # variable name
                    self.current_function_block.append(_)
                    return 3 # for semi
        # if equals then evaluate the expression
        _ = Node("VAR_ASSIGN")
        self.workingNode = _
        _.left = self._tokens[index].val # variable name
        _,_indg = self.evaluate_mathematical_expression(self._tokens[index+2].type,self._tokens[index+2].val,index+2)
        self.current_function_block.append(self.workingNode)
        return _indg - index + 2 # for semi

    def parse(self,current=0,till=None):
        # parsing different keywords
        # keywords are parsed as stuff that always follow a 
        # pattern
        # current means from where to start (tokens list) 
        # to maintain recursivity -> till, parse till what 

        while current < len(self._tokens):
            current_token = self._tokens[current]

            if till and (till == current_token.val): # useful for blocks
                current += 1 
                return current

            elif current_token.type == 'KEYWORD':
                covered_ = self._parse_keyword(current)
                current += covered_
            elif current_token.type == "NAME":
                covered_ = self._parse_names(current)
                current += covered_
            else:
                print(current_token.type,current_token.val)
                self.error_manager.show_error_and_exit(BipatSyntax,"Syntax vv Error",current_token.line_no,current_token.pos)
        
        # if top level didn't find till
        if till:
            return -1
         
        # self.error_manager.show_error_and_exit(SyntaxError,"NOT IMPLEMENTED  2")
        return self.AST