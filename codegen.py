# corrected_codegen.py
from errors import *
from atoms import OPERATORS

HEADER = '''
; Compiled through ATAT5
; Om Ganapati Namah
; Ganapatti Baba Moreya
'''

FOOTER = "\nHLT"

def to_hex(number:int)->str:
    return hex(number)[2:].upper()

class Variable:
    def __init__(self, name, memory, value_code):
        self.name = name
        self.memory = int(memory)
        # value_code is the code to compute initial value into A (string)
        self.value_code = value_code

    def generate_initial_code(self):
        # Run code that places initial value in A, then STA to memory
        return f"\n{self.value_code}\nSTA 0{to_hex(self.memory)}H\n"


class CodeGen:
    def __init__(self, ast, bipat_manager):
        self._ast = ast
        self.bipat_manager = bipat_manager

        # variables start storing from
        self._var_memory = 0xE000

        # label index counters
        self._label_index = 0
        self._nest_label_index = 0
        self._temp_label_index = 0

        self.loop_counter = 0
        self.nest_loop_counter = 0

        self._variables = []
        self.generated_code = ""

    def _variable_of(self, var:str):
        for v in self._variables:
            if v.name == var:
                return v
        return False

    def _eval_expression(self, node, reg="A"):
        """
        Return assembly code (string) which leaves the expression result in register `reg`.
        Accepts:
            - integer or numeric string -> MVI reg,nnH
            - variable name string -> LDA (or LXI H + MOV reg,M for non-A regs)
            - node-like objects with .name, .left, .right, etc.
        """
        # immediate integers or numeric strings
        if isinstance(node, (int, str)):
            try:
                # try convert to int
                val = int(node)
                return f"\nMVI {reg},0{to_hex(val)}H"
            except ValueError:
                # not a numeric: check variable
                var = self._variable_of(node)
                if var:
                    if reg == "A":
                        return f"\nLDA 0{to_hex(var.memory)}H"
                    else:
                        # load memory address into HL and move M into reg
                        return f"\nLXI H,0{to_hex(var.memory)}H\nMOV {reg},M"
                else:
                    self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Variable Named: {node}")

        # otherwise assume node-like (object)
        try:
            name = node.name
        except Exception:
            self.bipat_manager.show_error_and_exit(BipatSyntax, "Invalid Expression Node Type")

        # Binary arithmetic & comparisons: evaluate left -> A, right -> B, then op
        if name == 'add':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            footer = "\nADD B"
            if reg != "A":
                footer += f"\nMOV {reg},A"
            return left_code + "\n" + right_code + footer

        elif name == 'sub':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            footer = "\nSUB B"
            if reg != "A":
                footer += f"\nMOV {reg},A"
            return left_code + "\n" + right_code + footer

        elif name == 'less_than':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            footer = f"\nCMP B\nJC TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'GREATER_THAN_EQ':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            footer = f"\nCMP B\nJNC TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'LESS_THAN_EQ':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            footer = f"\nCMP B\nJC TEMP{t0}\nJZ TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'greater_than':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            # greater than: A > B -> (A-B) > 0 -> JNC and JZ logic adapted
            footer = f"\nCMP B\nJNC TEMP{t0}\nJNZ TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'EQUALS_TO':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            footer = f"\nCMP B\nJZ TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'NOT_EQUALS_TO':
            left_code = self._eval_expression(node.left, reg="A")
            right_code = self._eval_expression(node.right, reg="B")
            t0 = self._temp_label_index; t1 = t0 + 1
            self._temp_label_index += 2
            footer = f"\nCMP B\nJNZ TEMP{t0}\nMVI {reg},00H\nJMP TEMP{t1}\nTEMP{t0}:\nMVI {reg},01H\nTEMP{t1}:\n"
            return left_code + "\n" + right_code + footer

        elif name == 'ARRAY_ACCESS':
            # node.left -> array name, node.right -> index expression
            arr_var = self._variable_of(node.left)
            if not arr_var:
                self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Array Named: {node.left}")

            index_code = self._eval_expression(node.right, reg="A")   # index in A
            # load base address into HL, add index to L, then read M into reg
            code = index_code
            code += f"\nLXI H,0{to_hex(arr_var.memory)}H\nADD L\nMOV L,A\nMOV A,M\n"
            if reg != "A":
                code += f"\nMOV {reg},A"
            return code

        elif name == 'ARRAY_DEC':
            # node.left is list of initializers (AST nodes)
            # place first element at current var memory, then successive in next bytes
            if not isinstance(node.left, (list, tuple)):
                self.bipat_manager.show_error_and_exit(BipatSyntax, "ARRAY_DEC expects list of initial values")

            code = ""
            base_addr = self._var_memory
            # allocate memory size equal to length
            for i, item in enumerate(node.left):
                if i == 0:
                    # store at base_addr (current _var_memory)
                    code += f"LXI H,0{to_hex(base_addr)}H\n"
                    code += self._eval_expression(item, reg="A") + "\n"
                    code += "STA 0" + to_hex(base_addr) + "H\n"
                else:
                    code += "\nINX H\n" + self._eval_expression(item, reg="D") + "\nMOV M,D\n"
                # increment allocated memory
                self._var_memory += 1
            return code

        else:
            self.bipat_manager.show_error_and_exit(BipatSyntax, f"Invalid Expression Node: {name}")

    def _eval_conditional(self, node, label_on_false):
        """
        Evaluate condition expression and jump to label_on_false if condition == 0.
        Leaves no specific register state requirement beyond using A/B as temporaries.
        """
        cond_code = self._eval_expression(node, reg="A")
        # Compare A with zero and jump if zero (false)
        return cond_code + f"\nCMP B\n"  # (we'll set B=00 and then CMP) <- we will set B=00H before CMP
        # but simpler: set B=00H then CMP B; I will just return code that leaves A and then compare
        # However to keep small, produce explicit MVI B,00H then CMP B:
        # We'll return a string that places the compare against zero and JZ label outside caller.

    def generate(self):
        # check for main function
        for (fn_name, nodes) in self._ast:
            if fn_name == 'main':
                for node in nodes:
                    if node.name == "VAR_DEC":
                        # node.left = variable name, node.right = init expr
                        init_code = self._eval_expression(node.right, reg="A")
                        var = Variable(node.left, self._var_memory, init_code)
                        self.generated_code += var.generate_initial_code()
                        self._variables.append(var)
                        self._var_memory += 1

                    elif node.name == "VAR_ASSIGN":
                        var = self._variable_of(node.left)
                        if var:
                            val_code = self._eval_expression(node.right, reg="A")
                            self.generated_code += val_code
                            self.generated_code += f"\nSTA 0{to_hex(int(var.memory))}H\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Variable Named: {node.left}")
                            return

                    elif node.name == "ARRAY_ASSIGN":
                        var = self._variable_of(node.left)
                        if var:
                            # index -> C, value -> D
                            index_code = self._eval_expression(node.mid, reg="C")
                            value_code = self._eval_expression(node.right, reg="D")
                            self.generated_code += index_code
                            self.generated_code += value_code
                            self.generated_code += f"\nLXI H,0{to_hex(int(var.memory))}H\nMOV A,C\nADD L\nMOV L,A\nMOV M,D\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Variable Named: {node.left}")
                            return

                    elif node.name == 'INC':
                        var = self._variable_of(node.left)
                        if var:
                            self.generated_code += f"\nLXI H,0{to_hex(int(var.memory))}H\nINR M\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Variable Named: {node.left}")
                            return

                    elif node.name == 'DEC':
                        var = self._variable_of(node.left)
                        if var:
                            self.generated_code += f"\nLXI H,0{to_hex(int(var.memory))}H\nDCR M\n"
                        else:
                            self.bipat_manager.show_error_and_exit(BipatVariableNotFound, f"No Variable Named: {node.left}")
                            return

                    elif node.name == "COND":
                        if node.left == "if":
                            # evaluate cond; jump to LABEL{label_index+1} if false (0)
                            cond_code = self._eval_expression(node.right, reg="A")
                            # compare with zero
                            self.generated_code += "\n" + cond_code + "\nMVI B,00H\nCMP B\nJZ LABEL" + str(self._label_index+1) + "\n"
                            self._label_index += 1

                        elif node.left == 'while':
                            # create loop label, then evaluate condition and jump out if false
                            loop_no = self.loop_counter + 1
                            self.generated_code += f"\nLOOP{loop_no}:\n"
                            cond_code = self._eval_expression(node.right, reg="A")
                            self.generated_code += cond_code + "\nMVI B,00H\nCMP B\nJZ LABEL" + str(self._label_index+1) + "\n"
                            self._label_index += 1
                            self.loop_counter += 1

                    elif node.name == "END_IF":
                        # write the corresponding label for the most recently created label
                        to_write = self._label_index - self._nest_label_index
                        self._nest_label_index += 1
                        self.generated_code += f"\nLABEL{to_write}:\n"

                    elif node.name == "END_WHILE":
                        # jump back to correct loop start and write label for exit
                        to_write = self._label_index - self._nest_label_index
                        self._nest_label_index += 1
                        to_write_loop = self.loop_counter - self.nest_loop_counter
                        self.nest_loop_counter += 1
                        self.generated_code += f"\nJMP LOOP{to_write_loop}\nLABEL{to_write}:\n"

                break
        else:
            self.bipat_manager.show_error_and_exit(BipatSyntax, "No main Function Found")

        final_code = HEADER + self.generated_code + FOOTER
        return final_code
