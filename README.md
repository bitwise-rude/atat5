# ATAT5 -> A high level language that compiles to 8085 assembly
-- COOL COOL COOL

## Next thing to do
-- PRECEDENCE DOESN"T WORK HAVEN"T IMPLEMENTED IT SO DO IT NOW

## BUGS

- the lexer should check for names until there is a space, eg iff would also be regarded as if and f would produce an error, (no this is not the case), make multi word in the same palce
as the keyword cehcker

- for checking for mathematical check end for non number character not semi colon and for booleans too

- block counter? what a shame change it?

- if statement should make a node not conditional evaluator



## STUFF
- variable names or anything can be abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ nothing except this

- if you wanna change keywords or = change the values in the dict

- lexer stores the tokens as {KEYWORD:(stuff,line_no,Page_no)}

- Every rule in a rulebook is a method of parser class that returns stuff, or the Error

- For stuff begining with names like Variable names, i have only implemented storage like (a = 5 or a = b)

- Should i make workingNodes a list?

## MUST DO
- i have used right curly bracket as the default parenthesis to end inside the prase function

## TODO
- make error system more robust by indicating the line where error occured
- maybe make after label stuff indent to improve looks
-   make thing for floats

