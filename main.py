import lexluthor
import paras
import sys

def read_file() -> str:
    # read file from argument
    if len(sys.argv) > 1:
        try:
            file_ = open(sys.argv[1],'r')
        except:
            print_invalid_usage_error("FILE NOT FOUND")
        contents = file_.read()
        file_.close()
        return contents
    print_invalid_usage_error(f"USE:     {sys.argv[0]} <filename>")

def print_invalid_usage_error(msg:str) -> None:
    print(f"\n\tINVALID USAGE:\n\t\t{msg}")
    quit()
 
contents = read_file()

tokenizer_obj = lexluthor.Tokenizer(contents)
tokens = tokenizer_obj.tokenize()

parser_obj = paras.Parser(tokens)
parser_obj.parse()