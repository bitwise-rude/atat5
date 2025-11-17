################## Generates CODE based on AST
from errors import *
from atoms import OPERATORS

#############3 - Header to the ASSEMBLY CODE
HEADER = '''
; Compiled through ATAT5
; Om Ganapati Namah
; Ganapatti Baba Moreya
'''

############3 - Footer to the ASSEMBLY CODE
FOOTER = "\nHLT"

### some functions
def to_hex(number:int)->str:
    # REturns a number in hex represetnation
    return hex(number)[2:].upper()


########
class Variable:
    def __init__(self,name,memory,value):
        self.name = name
        self.memory = memory
        self.value = value

    def generate_initial_code(self):
            return f'''\n{self.value}
STA 0{to_hex(self.memory)}H
'''


##########################3
#   Main Code Gen Class
##########################3
class CodeGen:
    def __init__(self,ast,bipat_manager:BipatManager):
        self._ast = ast
        self.bipat_manager = bipat_manager

        # variables start storing from
        self._var_memory = 0xE000

        # label index
        self._label_index = 0
        self._nest_lablel_index = 0
        self._temp_label_index = 0
        self.loop_counter = 0 # later combine to single
        self.nest_loop_counter = 0


        # Variables are stored as list
        self._variables = [] 

        # residues are used by block enders
        self._residue = ""

        # assembly code
        self.generated_code = ""

        
    
    def _variable_of(self,var:str):
        for vars in self._variables:
            if vars.name == var:
                return vars
        return False

    def _eval_expression(self,node,reg="A"): # right now str and int but will be fixed for actual nodes also
        # will always be the right node
        try:
            return f"\nMVI {reg},0{to_hex(int(node))}H"
        except ValueError:
            _ =self._variable_of(node)
            if _: # is a variable
                if reg == "A":
                    return f"\nLDA 0{to_hex(int(_.memory))}H"
                else:
                    return f"\nLXI H,0{to_hex(int(_.memory))}H\nMOV {reg},M"
            else:
                self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node}")
        except TypeError:
            if node.name == 'add':
                _ = self._eval_expression(node.left,reg="A")
                _footer = "\nADD B"

                if reg !="A":
                    _footer += f"\nMOV {reg},A"


            elif node.name == 'sub':
                _ = self._eval_expression(node.left,reg="A")
                _footer = "\nSUB B"

                if reg !="A":
                    _footer += f"\nMOV {reg},A"
            
            elif node.name == 'less_than':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJC TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
            
            elif node.name == 'GREATER_THAN_EQ':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJNC TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
            
            elif node.name == 'LESS_THAN_EQ':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJC TEMP{self._temp_label_index}\nJZ TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2

            elif node.name == 'greater_than':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJNC TEMP{self._temp_label_index}\nJNZ TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
            
            elif node.name == 'EQUALS_TO':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJZ TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
            elif node.name == 'NOT_EQUALS_TO':
                _ = self._eval_expression(node.left,reg="A")
                _footer = f"\nCMP B\nJNZ TEMP{self._temp_label_index}\nMVI {reg},00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI {reg},01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
            
            # array
            elif node.name == 'ARRAY_ACCESS':
                # get array
                _code = self._eval_expression(node.right,reg="A") # getting index

                # move to reg 'A' if not in 'A'
                # if reg != "A":
                #     _code += f"\nMOV A,{reg}"
                # give error if not exist for below line
                existing = self._variable_of(node.left) # getting the memory
                

                _code += f"\nLXI H,0{to_hex(existing.memory)}H\nADD L\nMOV L,A\nMOV A,M\n"

                if reg != "A":
                    _code += f"\nMOV {reg},A"
                
                return _code

            elif node.name == 'ARRAY_DEC':    
                # array first value stored in memory, at the first since first is taken
                # since all values are evaluted before hand
                # and first is pointed by the variable name
                
                _code = f"LXI H,0{to_hex(self._var_memory)}H\n" + self._eval_expression(node.left[0],reg=reg) 

                for i in range(1,len(node.left)):
                    self._var_memory += 1
                    _code += "\nINX H\n" + self._eval_expression(node.left[i],reg="D") + "\nMOV M,D\n" 

                return  _code#tmp fix

            else:
                self.bipat_manager.show_error_and_exit(BipatSyntax,"Invalid Expression Node")
            
            
            return  self._eval_expression(node.right,"B")+"\n"+_ +_footer
    
    def _eval_conditional(self,node,label):
            _ = self._eval_expression(node)
            return _ + f"\nMOV B,A\nMVI A,00H\nCMP B\nJNC {label}"
            
    def generate(self):
        # check for the main function
        for (fn_name,nodes) in self._ast:
            if fn_name == 'main':
                # main function executes from here after
                # see what type of node this is 
                for node in nodes:
                    if node.name == "VAR_DEC":
                        _ = Variable(node.left,self._var_memory,self._eval_expression(node.right))
    
                        self.generated_code += _.generate_initial_code()

                        self._variables.append(_)
                        self._var_memory += 1
                    
                    elif node.name == "VAR_ASSIGN":
                        wanna_assign = self._variable_of(node.left)
                        if wanna_assign:
                            _ = self._eval_expression(node.right)
                            # self.generated_code+=wanna_assign.generate_initial_code()
                            self.generated_code += _
                            self.generated_code += f"\nSTA 0{to_hex(int(wanna_assign.memory))}H\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node.left}")
                            return
                    
                    elif node.name == "ARRAY_ASSIGN":
                        wanna_assign = self._variable_of(node.left)
                        if wanna_assign:
                            # calculate the index
                            _index_code = self._eval_expression(node.mid,"C") 
                            _value_code = self._eval_expression(node.right,"D") 

                            self.generated_code += _index_code
                            self.generated_code += _value_code
                            self.generated_code += f"\nLXI H,0{to_hex(int(wanna_assign.memory))}H\nMOV A,C\nADD L\nMOV L,A\nMOV M,D\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node.left}")
                            return
                    
                    elif node.name == 'INC':
                        wanna_assign = self._variable_of(node.left)
                        if wanna_assign:
                            self.generated_code += f"\nLDA 0{to_hex(int(wanna_assign.memory))}H\nINR A\nSTA 0{to_hex(int(wanna_assign.memory))}H\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node.left}")
                            return
                    elif node.name == 'DEC':
                        wanna_assign = self._variable_of(node.left)
                        if wanna_assign:
                            
                            self.generated_code += f"\nLDA 0{to_hex(int(wanna_assign.memory))}H\nDCR A\nSTA 0{to_hex(int(wanna_assign.memory))}H\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node.left}")
                            return
                       
                    elif node.name == "COND":
                        if node.left == "if":
                            self.generated_code += "\n"+self._eval_conditional(node.right,f'LABEL{self._label_index+1}') + "\n"
                            self._label_index += 1
                        
                        elif node.left == 'while':
                            self.generated_code += f"\nLOOP{self.loop_counter+1}:"+self._eval_conditional(node.right,f'LABEL{self._label_index+1}') + "\n"
                            self._label_index += 1
                            self.loop_counter += 1

                    elif node.name == "END_IF":
                        to_write = self._label_index - self._nest_lablel_index
                        self._nest_lablel_index += 1
                        self.generated_code += f"\nLABEL{to_write}:\n"
                      

                    # nested not done for this 
                    # make nested work by implementing as above
                    elif node.name == "END_WHILE":
                        to_write = self._label_index - self._nest_lablel_index
                        self._nest_lablel_index += 1

                        to_write_loop = self.loop_counter - self.nest_loop_counter
                        self.nest_loop_counter += 1
                        self.generated_code += f"\nJMP LOOP{to_write_loop}\nLABEL{to_write}:\n"
                        
                break
        else: # no main function
            self.bipat_manager.show_error_and_exit(BipatSyntax,"No main Function Found")
        
        final_code = HEADER + self.generated_code + FOOTER
        return final_code