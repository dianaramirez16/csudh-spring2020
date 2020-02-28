#include <stdio.h>
#include "ctype.h"

typedef enum {read, write, id, literal, becomes,
                add, sub, mul, div, lparen, rparen, eof} token;

char token_image[100];

token scan() {
    static int c = ' ';
        /* next available char; extra (int) width accommodates EOF */
    int i = 0;              /* index into token_image */

    /* skip white space */
    while (isspace(c)) {
        c = getchar();
    }
    if (c == EOF)
        return eof;
    if (isalpha(c)) {
        do {
            token_image[i++] = c;
            c = getchar();
        } while (isalpha(c) || isdigit(c) || c == '_');
        token_image[i] = '\0';
        if (!strcmp(token_image, "read")) return read;
        else if (!strcmp(token_image, "write")) return write;
        else return id;
    }
    else if (isdigit(c)) {
        do {
            token_image[i++] = c;
            c = getchar();
        } while (isdigit(c));
        token_image[i] = '\0';
        return literal;
    } else switch (c) {
        case ':':
            if (c = getchar() != '=') {
                fprintf(stderr, "lexical error\n");
                exit(1);
            } else {
                c = getchar();
                return becomes;
            }
            break;
        case '+': c = getchar(); return add;
        case '-': c = getchar(); return sub;
        case '*': c = getchar(); return mul;
        case '/': c = getchar(); return div;
        case '(': c = getchar(); return lparen;
        case ')': c = getchar(); return rparen;
        default:
            printf("lexical error\n");
            exit(1);
    }
}
