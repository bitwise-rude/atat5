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