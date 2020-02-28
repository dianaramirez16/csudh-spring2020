# Top-Down LL(1) Parser for the Calculator Language with Comments

## /given
  Source code provided as part of the assignment.
## /programs
  Simple examples of "calculator" language

## Simple “calculator” language
  The calculator allows values to be read into (numeric) variables, which may then be used in
  expressions. The values of the expressions in turn can be written to the output. It is a simple language
  because the control flow is strictly linear (no loops, if statements, or other jumps).

## Two kinds of implementation of LL top-down parsing
    1. Recursive Descent Parser
        - constructs a parse tree from the root down
        - predicting at each step which production will be used to expand the current node based on the next
          available token of input
        - reports any syntactical errors if any
        - each subroutine corresponds, one to one, to a nonterminal of the grammar that defines the language
        
    2. Table Driven Parser
        - requires a stack and parse table
        - The parser operates in a loop which pops the top symbol off the stack and performs the following actions
            If the popped symbol is a terminal
            --> the parser attempts to match it against an incoming token from the scanner
                If the match fails
                --> the parser announces a syntax error
            If the popped symbol is a nonterminal
            --> the parser uses it together with the next available input token to index into the two-dimensional
                table that tells it which production to predict (or whether to announce a syntax error).
                   
## Tasks
    1. Check if comments have correct forms (either /*…*/ or //). Second, the parser.c does not take a file 
       name as user input. Fix the programs so that it can take a calculator language program (with comments)
       and find if it has lexical error and syntax error or not.
    2. Implement scanner and parser using table-driven parsing (C programming language).
    
## Extra Credit
    1. Currently, the parser only prints out a universal error message “syntax error” without referring to a 
       specific line of the program. Augment parser.c such that more detailed and informative error messages are 
       printed out.
    2. Come up with a few programs with lexical errors (beyond comments) with corresponding error message printed.
