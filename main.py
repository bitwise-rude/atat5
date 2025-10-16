import lexluthor
import paras
import sys
import errors
import codegen

def read_file() -> list[str]:
    # read file from argument
    if len(sys.argv) > 1:
        try:
            file_ = open(sys.argv[1],'r')
        except:
            print_invalid_usage_error("FILE NOT FOUND")
        contents = file_.readlines()
        file_.close()
        return contents
    print_invalid_usage_error(f"USE:     {sys.argv[0]} <filename>")

def print_invalid_usage_error(msg:str) -> None:
    print(f"\n\tINVALID USAGE:\n\t\t{msg}")
    quit()
 
contents:list[str] = read_file()

bipat_manager = errors.BipatManager(contents)

tokenizer_obj = lexluthor.Tokenizer(contents,bipat_manager)
tokens = tokenizer_obj.tokenize()

parser_obj = paras.Parser(tokens,bipat_manager)
AST = parser_obj.parse()

codegen_obj = codegen.CodeGen(AST,bipat_manager)
codegen_obj.generate()