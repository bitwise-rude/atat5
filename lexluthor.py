from errors import BipatManager,IdentifierUnknown
from atoms import *

###################3
#   Tokenizer
###################3

class Token:
    def __init__(self,type,line_no,pos,val):
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

    def tokenize(self) -> list[Token]:
        '''
            return type
                {
                    TOKEN's list
                }
        '''
        keywords_reversed = {v:k for k, v in KEYWORDS.items()}
        booleans_reversed = {v:k for k, v in BOOLEANS.items()}
        operators_reversed = {v:k for k, v in OPERATORS.items()}
        brackets_reversed = {v:k for k,v in BRACKETS.items()}

        for _line_no,current_line in enumerate(self._raw):
            _pos = 0
            
            while _pos < len(current_line):

                _temp_string = ""

                checking_letter = current_line[_pos]

                # # checking 2 letter stuff
                found_ = False
                for k,v in MULTIWORD.items():
                    ## for two letter only
                    if checking_letter == v[1][0] :
                        if _pos+1 < len(current_line) and current_line[_pos+1] == v[1][1]:
                            _ = Token(v[0],_line_no,_pos,k)
                            _pos +=2
                            self.tokens.append(_)
                            found_ = True
                            break
                
                def consume_till(VAR,_pos):
                    # consumes till the position indicates value from VAR
                    _temp_string = ""
                
                    while _pos<len(current_line) and current_line[_pos] in VAR:
                        _temp_string += current_line[_pos]
                        _pos += 1 
                    return _temp_string,_pos 
             
                if found_:
                    continue

                elif checking_letter in NAMES: ##
                    # search until a non-name character is found
                    _temp_string, _pos= consume_till(NAMES,_pos)
                    # what we've found could be a  keyword or a name
                    if _temp_string in KEYWORDS.values():
                        _=Token("KEYWORD",_line_no,_pos,keywords_reversed[_temp_string])
                        self.tokens.append(_)
                    ##boolean
                    elif _temp_string in BOOLEANS.values():
                        _ =Token("NUMBER",_line_no,_pos,"1" if booleans_reversed[_temp_string]== 'true' else "0")
                        self.tokens.append(_)
                    else:
                        _ = Token("NAME",_line_no,_pos,_temp_string)
                        self.tokens.append(_)
                
                # do similar thing for numbers
                elif checking_letter in NUMBERS:
                    # search until a non-number character  is found
                    _temp_string,_pos = consume_till(NUMBERS,_pos)
                
                    _ = Token("NUMBER",_line_no,_pos,_temp_string)
                    self.tokens.append(_)
        
                # comment checking
                elif checking_letter == COMMENT:
                    # don't care till a new line
                    while _pos < len(current_line) and current_line[_pos] != "\n":
                        _pos +=1 
                  
                
                # don't care for a space or new line
                elif checking_letter == " " or checking_letter == "\n": 
                    _pos += 1
                
                # brackets
                elif checking_letter in BRACKETS.values():
                    # REMEMBER: the dictionary keys value mumbo jumbo shit
                    _ = Token("PARENTHESIS",_line_no,_pos,brackets_reversed[checking_letter])
                    self.tokens.append(_)
                    _pos += 1
                
                # operations
                elif checking_letter in OPERATORS.values():
                    _  = Token("OPERATOR",_line_no,_pos,operators_reversed[checking_letter])
                    self.tokens.append(_)
                    _pos += 1 
                
                # equals to
                elif checking_letter == EQUALS:
                    _ = Token("EQUALS",_line_no,_pos,EQUALS)
                    self.tokens.append(_)
                    _pos += 1

                # semi colon
                elif checking_letter == SEMI:
                    _ = Token("SEMI",_line_no,_pos,SEMI)
                    self.tokens.append(_)
                    _pos += 1
                
       
                else:
                    self.error_manager.show_error_and_exit(IdentifierUnknown,"Unknown Identifier",_line_no+1,_pos+1)
    
        
        return self.tokens



