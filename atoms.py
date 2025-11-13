### Stores the definition of what keywords and atomic vaues to use

import string


### Defining the atoms, if you wanna change something change the keys
KEYWORDS = {'func_dec':'fx',
            'var_dec':'let',
            'cond':'if',
            'while':'while',
            'else':'else'
            }
 
BRACKETS ={
             "left_small":"("   ,
             "right_small":")"   ,
            "left_curly":"{"      ,
             "right_curly":"}"    ,
             "left_square":"[",
             "right_square":"]"
            }
COMMENT = "#"
OPERATORS = {'add':'+','sub':'-','less_than':"<","greater_than":">",}
MULTIWORD = {"INC":("UN_OPERATOR","++"),
             "DEC":("UN_OPERATOR","--"),
             "EQUALS_TO":("OPERATOR","=="),
             "NOT_EQUALS_TO":("OPERATOR","!="),
             "LESS_THAN_EQ":("OPERATOR","<="),
             "GREATER_THAN_EQ":("OPERATOR",">=")
             }
EQUALS = "="
BOOLEANS={"true":"true",'false':'false'}
SEMI = ";"
COMMA = ","
NAMES = string.ascii_letters+"_" # anything except keyword is NAMES/VARIABLES

NUMBERS = "0123456789"