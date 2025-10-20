##################
## Errors (विपत) \ Bipat #
##################
# Errors (Compile Time) are called Bipat which in Nepali translates to Problem

class Bipat:
    """ Top Level Error """
    # Every other Error is a child of this
    def __init__(self,kind,msg):
        self._kind = kind
        self._msg = msg
    def __repr__(self) -> str:
        return f"\nBIPAT OCCURED\n\t\tTYPE:{self._kind}\n\n\t{self._msg}"
    
class IdentifierUnknown(Bipat):
    def __init__(self, msg):
        super().__init__("IdentifierUnknown", msg)     

class BipatSyntax(Bipat):
    def __init__(self,  msg):
        super().__init__('BipatSyntax', msg)

class BipatVariableNotFound(Bipat):
    def __init__(self,  msg):
        super().__init__("Variable Not Found", msg)

class BipatManager():
    """ Manages Bipat"""
    def __init__(self,raw_code):
        self._raw_code = raw_code
    
    def show_error_and_exit(self,error_kind,msg:str,line_no=0,word_no=0):
        try:
            print(error_kind(msg))
            print("\n")
            print(self._raw_code[line_no])
            print(" " * (len(self._raw_code[line_no])-word_no)+"^^"*2)
            print(f"ERROR AT LINE:POS {line_no+1}:{word_no+1}")
        except:
            pass

        quit()

        