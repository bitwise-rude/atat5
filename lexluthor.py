from errors import BipatManager,IdentifierUnknown
from atoms import *

###################3
#   Tokenizer
###################3

class Token:
    def __init__(self,type,line_no,pos,val=None):
        self.type = type
        self.line_no = line_no
        self.val = val
        self.pos = pos
    def __repr__(self):
        return self.type + "  " + self.val + "\n"


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

                # # checking multi letter stuff
                found_ = False
                for k,v in MULTIWORD.items():
                    ## for two letter only
                    if checking_word == v[1][0] :
                        if current_line[_index2+1] == v[1][1]:
                            _ = Token(v[0],_line_no,_index,k)
                            _index2 +=2
                            self.tokens.append(_)
                            found_ = True
                            break
                
                if found_:
                    _index = _index2
                   
                    continue

                elif checking_word in NAMES:
                    # search until a non-name character is found
                    while  current_line[_index2]  in NAMES:
                        
                        _temp_string += current_line[_index2]
                        _index2 += 1
                    # what we've found could be a  keyword or a name
        
                    if _temp_string in KEYWORDS.values():
                        _=Token("KEYWORD",_line_no,_index,list(KEYWORDS)[list(KEYWORDS.values()).index(_temp_string)])
                        self.tokens.append(_)
                    ##boolean
                    elif _temp_string in BOOLEANS.values():
                        _ = _=Token("NUMBER",_line_no,_index,"1" if list(BOOLEANS)[list(BOOLEANS.values()).index(_temp_string)]== 'true' else 0)
                        self.tokens.append(_)
                    else:
                        _ = Token("NAME",_line_no,_index,_temp_string)
                        self.tokens.append(_)
                
                # do similar thing for numbers
                elif checking_word in NUMBERS:
                    # search until a non-number character  is found
                    while  current_line[_index2]  in NUMBERS:
                        _temp_string += current_line[_index2]
                        _index2 += 1

                    _ = Token("NUMBER",_line_no,_index,_temp_string)
                    self.tokens.append(_)
                
          
                    
    
                
                # comment checking
                elif checking_word == COMMENT:
                    # don't care till a new line
                    while current_line[_index2] != "\n":
                        _index2 +=1
                
                # don't care for a space or new line
                elif checking_word == " " or checking_word == "\n": 
                    _index2 += 1
                
                # brackets
                elif checking_word in BRACKETS.values():

                    # REMEMBER: the dictionary keys value mumbo jumbo shit
                    _ = Token("PARENTHESIS",_line_no,_index,list(BRACKETS)[list(BRACKETS.values()).index(current_line[_index])])
                    self.tokens.append(_)
                    _index2 += 1
                
                # operations
                elif checking_word in OPERATORS.values():
                    _  = Token("OPERATOR",_line_no,_index,list(OPERATORS)[list(OPERATORS.values()).index(current_line[_index])])
                    self.tokens.append(_)
                    _index2 += 1 
                
                # equals to
                elif checking_word == EQUALS:
                    _ = Token("EQUALS",_line_no,_index,EQUALS)
                    self.tokens.append(_)
                    _index2 += 1

                # semi colon
                elif checking_word == SEMI:
                    _ = Token("SEMI",_line_no,_index,SEMI)
                    self.tokens.append(_)
                    _index2 += 1
                
       
                else:
                    self.error_manager.show_error_and_exit(IdentifierUnknown,"Unknown Identifier",_line_no+1,_index+1)
    
                _index = _index2
        
        print(self.tokens)
        return self.tokens



