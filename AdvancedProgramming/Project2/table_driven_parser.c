/*
* Table-Driven Parser for 'Calculator' language
* writte by Angel Salcido and Diana Ramirez for CSC 521 Spring 2020 - Project 2
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {read, write, id, literal, becomes,
                addOp, subOp, mulOp, divOp, lparen, rparen, eof} token;

extern char token_image[];

char *names[] = {"read", "write", "id", "literal", "becomes",
                "add", "sub", "mul", "div", "lparen", "rparen", "eof"};

static token input_token;

FILE *src;


/****************************************************************************
 **************************** PARSE TABLE ***********************************
 ****************************************************************************/

// all symbols in language
typedef enum {program, stmt_list, stmt, expr, term_tail,
                term, factor, factor_tail, mult_op, add_op,
                $$, eps, identifier, assignment, input,
                output, plus, minus, star, slash,
                lpar, rpar, number} symbol;
char *sym_names[] = { "program", "stmt_list", "stmt", "expr", "term_tail",
                      "term", "factor", "factor_tail", "mult_op", "add_op",
                      "$$", "epsilon", "id", ":=", "read",
                      "write", "+", "-", "*", "/",
                      "(", ")", "number"};
// symbols that are terminals
symbol terminals[] = {slash, star, minus, plus,
                      number, identifier, lpar, rpar, eps,
                      assignment, input, output, $$};
// symbols that are nonterminals
symbol nonterminals[] = {program, stmt_list, stmt,
                         expr, term_tail, term, factor,
                         factor_tail, add_op, mult_op};


// stores action: {predict:0 or error:1}; production: {[symbol1, symbol2, ... , symbol5], [], [], []}
struct table_item
{
    int action;
    symbol production[4];
};
// complete hard-coded parse table -- based on figure 2.20
struct table_item parseTable[sizeof(nonterminals)/sizeof(*nonterminals)][sizeof(names)/sizeof(*names)] = {
    {{0, {stmt_list, $$}},                  {1, {}},                        {0, {stmt_list, $$}},       {0, {stmt_list, $$}},       {1, {}}, {1, {}},                       {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {0, {stmt_list, $$}}},  // program
    {{0, {stmt, stmt_list}},                {1, {}},                        {0, {stmt, stmt_list}},     {0, {stmt, stmt_list}},     {1, {}}, {1, {}},                       {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {0, {eps}}},            // stmt_list
    {{0, {identifier, assignment, expr}},   {1, {}},                        {0, {input, identifier}},   {0, {output, expr}},        {1, {}}, {1, {}},                       {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {1, {}}},               // stmt
    {{0, {term, term_tail}},                {0, {term, term_tail}},         {1, {}},                    {1, {}},                    {1, {}}, {0, {term, term_tail}},        {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {1, {}}},               // expr
    {{0, {eps}},                            {1, {}},                        {0, {eps}},                 {0, {eps}},                 {1, {}}, {1, {}},                       {0, {eps}}, {0, {add_op, term, term_tail}},     {0, {add_op, term, term_tail}},     {1, {}},                                {1, {}},                                {0, {eps}}},            // term_tail
    {{0, {factor, factor_tail}},            {0, {factor, factor_tail}},     {1, {}},                    {1,},                       {1, {}}, {0, {factor, factor_tail}},    {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {1, {}}},               // term
    {{0, {eps}},                            {1, {}},                        {0, {eps}},                 {0, {eps}},                 {1, {}}, {1,},                          {0, {eps}}, {0, {eps}},                         {0, {eps}},                         {0, {mult_op, factor, factor_tail}},    {0, {mult_op, factor, factor_tail}},    {0, {eps}}},            // factor_tail
    {{0, {identifier}},                     {0, {number}},                  {1, {}},                    {1, {}},                    {1, {}}, {0, {lpar, expr, rpar}},       {1, {}},    {1, {}},                            {1, {}},                            {1, {}},                                {1, {}},                                {1, {}}},               // factor
    {{1, {}},                               {1, {}},                        {1, {}},                    {1, {}},                    {1, {}}, {1, {}},                       {1, {}},    {0, {plus}},                        {0, {minus}},                       {1, {}},                                {1, {}},                                {1, {}}},               // add_op
    {{1, {}},                               {1, {}},                        {1, {}},                    {1, {}},                    {1, {}}, {1, {}},                       {1, {}},    {1, {}},                            {1, {}},                            {0, {star}},                            {0, {slash}},                           {1, {}}},               // mult_op
};//    id,                                 literal,                         read,                       write,                        :=,       (,                             ),          +,                                  -,                                  *,                                       /,                                      $$


// get row index into parse table
int nonTermInd(symbol s) {
    switch (s)
    {
    case program:
        return 0;
    case stmt_list:
        return 1;
    case stmt:
        return 2;
    case expr:
        return 3;
    case term_tail:
        return 4;
    case term:
        return 5;
    case factor_tail:
        return 6;
    case factor:
        return 7;
    case add_op:
        return 8;
    case mult_op:
        return 9;
    default:
        return -1;
    }
}
// get column index into parse table
int tokenInd(token t) {
    switch (t)
    {
    case id:
        return 0;
    case literal:
        return 1;
    case read:
        return 2;
    case write:
        return 3;
    case becomes:
        return 4;
    case lparen:
        return 5;
    case rparen:
        return 6;
    case addOp:
        return 7;
    case subOp:
        return 8;
    case mulOp:
        return 9;
    case divOp:
        return 10;
    case eof:
        return 11;
    default:
        return -1;
    }
}

void error() {
    printf("syntax error\n");
    exit(1);
}
// Parse Stack
symbol parseStack[128];
int topOfStack = 0;

int isTerminal(symbol s) {
    for(int i = 0; i < (sizeof(terminals)/sizeof(*terminals)); i++)
    {
        if(terminals[i] == s) { return 1; }
    }

    return 0;
}

void match(symbol s) {

    printf("symbol-%s, token-%s\n", sym_names[s], names[input_token]);
    printf("symbol-%d, token-%d\n", s, input_token);
    printf("\tTOS: %s\n", sym_names[parseStack[topOfStack]]);
    switch(input_token) {  //matching tokens
        case read:
            if((strcmp(sym_names[s], "read")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("--SYNTAX ERROR. token does not match prediction");
              }
            break;
        case write:
            if((strcmp(sym_names[s], "write")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case id:
            if((strcmp(sym_names[s], "id")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  printf("s = %s\n\n", sym_names[s]);
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case literal:
            if(strcmp(sym_names[s], "number")){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("case#SYNTAX ERROR. token does not match prediction");
              }
            break;
        case becomes:
            if((strcmp(sym_names[s], ":=")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case addOp:
            if((strcmp(sym_names[s], "add")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case subOp:
            if((strcmp(sym_names[s], "sub")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case mulOp:
            if((strcmp(sym_names[s], "mul")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case divOp:
            if((strcmp(sym_names[s], "div")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case lparen:
            if((strcmp(sym_names[s], "(")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case rparen:
            if((strcmp(sym_names[s], ")")==0)){
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();
              } else {
                  puts("SYNTAX ERROR. token does not match prediction");
              }
            break;
        case eof:
            if((strcmp(sym_names[s], "epsilon")==0)){
                  puts("testing ------------------- epsilon");
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();

              } else if ((strcmp(sym_names[s], "number")==0)) {
                  puts("testing ------------------- number");
                  printf ("the token is: %s - match found.\n",names[input_token]);
                  topOfStack--;  //remove read from stack
                  input_token =scan();

              }else {
                  puts("SYNTAX ERROR. token does not match prediction");
                  //input_token =scan();

              }
            break;
        default:
            error();
            printf("syntax error \n");
            exit(1);
        }
    }

int main(int argc, char* argv[])
{
    FILE *src;
    char *prog_prefix;
    char file_name[32];


    symbol expSymbol;
    int ntermInd;
    int tokInd;
    struct table_item item;

    prog_prefix = "./programs/";

    strcpy(file_name, prog_prefix);

    // program name was passed in as cl arg
    if (argc > 1)
    {
        strcat(file_name, argv[1]);
        printf("opening file: %s\n\n\n", file_name);
        src = fopen(file_name, "r");

        // failed to open file
        if (src == NULL)
        {
            perror("Error while opening the file.\n");
            exit(EXIT_FAILURE);
        }
    }else
        src = NULL;

    setSource(src);

    // init parse stack
    parseStack[topOfStack] = program;
    //input_token = scan();

    do
    {
        expSymbol = parseStack[topOfStack];
        //printf("\ncurrent expected symbol: %s\n", sym_names[expSymbol]);
        //printf("current input token: %s\n\n", names[input_token]);

        // check if top of stack is terminal or non-terminal
        if (isTerminal(expSymbol))
        {
            printf("\texpected symbol is terminal: %s\n", sym_names[expSymbol]);
            input_token =scan();
            match(expSymbol);
            expSymbol = parseStack[topOfStack];

            if (expSymbol == $$)
            {
                printf("success -- no lexical or syntactical errors");
                break;
            }

        } else
        {
            printf("expected symbol is not a terminal: %s\n", sym_names[expSymbol]);

            ntermInd = nonTermInd(expSymbol);
            tokInd = tokenInd(input_token);

            printf("parse table indexes\t symbol: [%d], token: [%d]\n", ntermInd, tokInd);

            if (ntermInd >= 0 && tokInd >= 0)
            {
                // check parse table
                item = parseTable[ntermInd][tokInd];

                if (item.action == 1)
                {
                    // syntax error found
                    printf("\nSYNTAX ERROR - incompatible (%s - %s)\n", sym_names[expSymbol], names[input_token]);
                } else
                {
                    // push production to stack
                    for (int i = 3; i >= 0; i--)
                    {
                        if (item.production[i] != NULL)
                        {
                            printf("\tPushing to parse stack: %s\n", sym_names[item.production[i]]);
                            parseStack[topOfStack] = item.production[i];
                            if (i != 0)
                                topOfStack++;
                        }
                    }
                }

                printf("parse stack: \n");
                for (int i = topOfStack; i >= 0; i--)
                {
                    printf("\t(%d): %s\n", i, sym_names[parseStack[i]]);
                }
                printf("\n\n");
            }
            else
            {
                printf("index error: symbol-%s, token-%s", expSymbol, input_token);
            }
        }

    }while(topOfStack >0);

    if (src != NULL)
        fclose(src);

    return(0);
}
