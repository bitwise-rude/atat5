from errors import BipatManager,IdentifierUnknown
from atoms import *

###################3
#   Tokenizer
###################3


class Tokenizer:
    def __init__(self,raw_contents:list[str],error_manager:BipatManager) -> None:
        self._raw = raw_contents
        self.tokens = []
        self.error_manager = error_manager

    def tokenize(self) -> list[dict]:
        '''
            return type
                {
                    KEYWORD : (let, line_no, index_no)
                }
        '''
        for _line_no in range(len(self._raw)):
            current_line = self._raw[_line_no]
            _index = 0
            
            while _index < len(current_line):

                _temp_string = ""
                _index2 = _index # required for second level fetch

                checking_word = current_line[_index]

                if checking_word in NAMES:
                    # search until a non-name character is found
                    while  current_line[_index2]  in NAMES:
                        
                        _temp_string += current_line[_index2]
                        _index2 += 1
                    # what we've found could be a  keyword or a name
                
                    if _temp_string in KEYWORDS.values():
                        self.tokens.append({"KEYWORD":(list(KEYWORDS)[list(KEYWORDS.values()).index(_temp_string)],_line_no,_index)})
                    else:
                        self.tokens.append({"NAME":(_temp_string,_line_no,_index)})
                
                # do similar thing for numbers
                elif checking_word in NUMBERS:
                    # search until a non-number character  is found
                    while  current_line[_index2]  in NUMBERS:
                        _temp_string += current_line[_index2]
                        _index2 += 1
            
                    self.tokens.append({"NUMBER":(_temp_string,_line_no,_index)})
                
                # don't care for a space or new line
                elif checking_word == " " or checking_word == "\n": 
                    _index2 += 1
                
                # brackets
                elif checking_word in BRACKETS.values():

                    # REMEMBER: the dictionary keys value mumbo jumbo shit
                    self.tokens.append({"PARENTHESIS":(list(BRACKETS)[list(BRACKETS.values()).index(current_line[_index])],_line_no,_index)})
                    _index2 += 1
                
                # equals to
                elif checking_word == EQUALS:
                    self.tokens.append({"EQUALS":(EQUALS,_line_no,_index)})
                    _index2 += 1

                # semi colon
                elif checking_word == SEMI:
                    self.tokens.append({"SEMI":(SEMI,_line_no,_index)}) 
                    _index2 += 1
                
                
                else:
                    self.error_manager.show_error_and_exit(IdentifierUnknown,"Unknown Identifier",_line_no+1,_index+1)
    
                _index = _index2
                
        return self.tokens



