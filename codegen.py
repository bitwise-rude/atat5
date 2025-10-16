################## Generates CODE based on AST
from errors import *

#############3 - Header to the ASSEMBLY CODE
HEADER = '''
; Compiled through ATAT5
; Om Ganapati Namah
; Ganapatti Baba Moreya

'''

############3 - Footer to the ASSEMBLY CODE
FOOTER = '''HLT
'''

### some function
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
        return f'''LXI H,0{to_hex(self.memory)}H
MVI M,0{to_hex(int(self.value))}H
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


    def generate(self):
        # check for the main function
        for (fn_name,nodes) in self._ast:
            if fn_name == 'main':
                # main function executes from here after
                # see what type of node this is 
                for node in nodes:
                    if node.name == "VAR_DEC":
                        # varaible declearatoni
                        _ = Variable(node.left,self._var_memory,node.right)
                        self.generated_code += _.generate_initial_code()
                        self._variables.append(_)
                        self._var_memory += 1
                break
        else: # no main function
            self.bipat_manager.show_error_and_exit(BipatSyntax,"No main Function Found")
        
        final_code = HEADER + self.generated_code + FOOTER
        print(final_code)