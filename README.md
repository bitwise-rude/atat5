# ATAT5 -> A high level language that compiles to 8085 assembly
-- COOL COOL COOL


## BUGS
- Semicolon is checked in the new line too fix that ## FIXED

## STUFF
- variable names or anything can be abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_ nothing except this

- if you wanna change keywords or = change the values in the dict

- lexer stores the tokens as {KEYWORD:(stuff,line_no,Page_no)}

- Every rule in a rulebook is a method of parser class that returns stuff, or the Error

- For stuff begining with names like Variable names, i have only implemented storage like (a = 5 or a = b)

## MUST DO
- i have used right curly bracket as the default parenthesis to end inside the prase function

## TODO
- make error system more robust by indicating the line where error occured
-   make thing for floats

