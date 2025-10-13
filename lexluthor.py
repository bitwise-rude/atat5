import string
from errors import IdentifierUnknown

###################3
#   Tokenizer
###################3

### Defining the atoms
KEYWORDS = ['fn','int']
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

class Tokenizer:
    def __init__(self,raw_contents:str) -> None:
        self._raw = raw_contents
        self.tokens = []

    def tokenize(self) -> list[dict]:
        _index = 0

        while _index < len(self._raw):

            _temp_string = ""
            _index2 = _index # required for second level fetch

            checking_word = self._raw[_index]

            if checking_word in NAMES:
                # search until a non-name character is found
                while  self._raw[_index2]  in NAMES:
                    
                    _temp_string += self._raw[_index2]
                    _index2 += 1
                # what we've found could be a  keyword or a name
                if _temp_string in KEYWORDS:
                    self.tokens.append({"KEYWORD":_temp_string})
                else:
                    self.tokens.append({"NAME":_temp_string})
            
            # do similar thing for numbers
            elif checking_word in NUMBERS:
                # search until a non-number character is found
                while  self._raw[_index2]  in NUMBERS:
                    
                    _temp_string += self._raw[_index2]
                    _index2 += 1
                # what we've found could be a  keyword or a name
                self.tokens.append({"NUMBER":_temp_string})
            
            # don't care for a space or new line
            elif checking_word == " " or checking_word == "\n": 
                _index2 += 1
            
            # brackets
            elif checking_word in BRACKETS.keys():
                self.tokens.append({"PARENTHESIS":BRACKETS[self._raw[_index]]})
                _index2 += 1
            
            # equals to
            elif checking_word == EQUALS:
                self.tokens.append({"EQUALS":EQUALS})
                _index2 += 1

            # semi colon
            elif checking_word == SEMI:
                self.tokens.append({"SEMI":SEMI}) 
                _index2 += 1
            
            
            else:
                print(IdentifierUnknown("Unknown Identifier"))
                quit()
            _index = _index2
            
        return self.tokens



