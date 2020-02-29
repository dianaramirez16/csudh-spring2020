/*
* Table-Driven Parser for 'Calculator' language
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {read, write, id, literal, becomes,
                addOp, subOp, mulOp, divOp, lparen, rparen, eof} token;

extern char token_image[];

char* names[] = {"read", "write", "id", "literal", "becomes",
                "add", "sub", "mul", "div", "lparen", "rparen", "eof"};

static token input_token;

FILE *src;

int main(int argc, char* argv[])
{
    char* prog_prefix;
    char file_name[32];

    prog_prefix = "./programs/";

    strcpy(file_name, prog_prefix);

    // program name was passed in as cl arg
    if (argc > 1)
    {
        strcat(file_name, argv[1]);
        printf("opening file: %s\n", file_name);
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

    input_token = scan();
    printf ("the token is %s \n", names[input_token]);
    program();

    if (src != NULL)
        fclose(src);

    return(0);
}