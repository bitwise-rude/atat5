### Stores the definition of what keywords and atomic vaues to use

import string


### Defining the atoms, if you wanna change something change the keys
KEYWORDS = {'fn':'func_dec','let':'var_dec'} 
BRACKETS ={
            "(":    "left_small"   ,
            ")":    "right_small" ,
            "{":    "left_curly"   ,
             "}":   "right_curly" ,
            }
EQUALS = "="
SEMI = ";"
NAMES = string.ascii_letters+"_" # anything except keyword is NAMES
NUMBERS = "0123456789"