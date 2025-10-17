### Stores the definition of what keywords and atomic vaues to use

import string


### Defining the atoms, if you wanna change something change the keys
KEYWORDS = {'func_dec':'fx','var_dec':'let','cond':'if'} 
BRACKETS ={
             "left_small":"("   ,
             "right_small":")"   ,
            "left_curly":"{"      ,
             "right_curly":"}"    ,
            }
COMMENT = "#"
OPERATORS = {'add':'+','sub':'-'}
MULTIWORD = {"EQUALS_TO":("CONDITIONAL_OPERATOR","==")}
EQUALS = "="
SEMI = ";"
NAMES = string.ascii_letters+"_" # anything except keyword is NAMES
NUMBERS = "0123456789"