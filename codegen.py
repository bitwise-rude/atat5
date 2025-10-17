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
FOOTER = "HLT"

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
            return f'''{self.value}
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

        # Variables are stored as list
        self._variables = [] 

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
                    return f"LXI H,{to_hex(int(_.memory))}\nMOV {reg},M"
            else:
                self.bipat_manager.show_error_and_exit(BipatVariableNotFound,f"No Variable Named:{node}")
        except TypeError:
            if node.name == 'add':
                _ = self._eval_expression(node.left)
                _footer = "\nADD B\nMOV B,A"

            return  self._eval_expression(node.right,"B")+"\n"+_ +_footer
        


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
                break
        else: # no main function
            self.bipat_manager.show_error_and_exit(BipatSyntax,"No main Function Found")
        
        final_code = HEADER + self.generated_code + FOOTER
        print(final_code)