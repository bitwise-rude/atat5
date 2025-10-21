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
        self._temp_label_index = 0


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
            return f"MVI {reg},0{to_hex(int(node))}H"
        except ValueError:
            _ =self._variable_of(node)
            if _: # is a variable
                if reg == "A":
                    return f"LDA 0{to_hex(int(_.memory))}H"
                else:
                    return f"LXI H,0{to_hex(int(_.memory))}H\nMOV {reg},M"
            else:
                self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node}")
        except TypeError:
            if node.name == 'add':
                _ = self._eval_expression(node.left,reg=reg)
                _footer = "\nADD B\nMOV B,A"
            
            elif node.name == 'sub':
                _ = self._eval_expression(node.left,reg=reg)
                _footer = "\nSUB B\nMOV B,A"
            
            elif node.name == 'EQUALS_TO':
                _ = self._eval_expression(node.left,reg=reg)
                _footer = f"\nCMP B\nJZ TEMP{self._temp_label_index}\nMVI B,00H\nJMP TEMP{self._temp_label_index+1}\nTEMP{self._temp_label_index}:\nMVI B,01H\nTEMP{self._temp_label_index+1}:\n"
                self._temp_label_index += 2
              


            
            else:
                self.bipat_manager.show_error_and_exit(BipatSyntax,"Invalid Expression Node")

            return  self._eval_expression(node.right,"B")+"\n"+_ +_footer
    
    def _eval_conditional(self,node,label):
            _ = self._eval_expression(node)
            return _ + f"\nMVI A,00H\nCMP B\nJNC {label}"
            
        

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
                       
                    elif node.name == "COND":
                        if node.left == "if":
                            self.generated_code += "\n"+self._eval_conditional(node.right,f'LABEL{self._label_index}') + "\n"
                        
                    elif node.name == "END_IF":
                        self.generated_code += f"\nLABEL{self._label_index}:\n"
                        self._label_index += 1
                    
                       
                break
        else: # no main function
            self.bipat_manager.show_error_and_exit(BipatSyntax,"No main Function Found")
        
        final_code = HEADER + self.generated_code + FOOTER
        print(final_code)