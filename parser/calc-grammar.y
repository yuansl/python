%{
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

#define YYSTYPE double
double calcfact();
double reg[99];
char format[20];
extern int yylex();
extern int yyerror(const char *s);
%}

%token NUMBER MOD EOLN SEMICOLON NOT OR SPACE
%token PLUS MINUS DIV MUL POW
%left PLUS MINUS
%left MUL DIV
	 
%%
start: stmt EOLN { printf("%f\n", $$); $$=0; }
       ;

stmt: /* Empty */
      | expr
      ;

expr:  mul_expr 
       | add_expr 
       ;

 mul_expr: mul_expr MUL term           { $$ = $1 * $3; }
	   | mul_expr DIV term         { $$ = $1 / $3; }
	   | term
	   ;

 add_expr: expr PLUS expr           {$$ = $1 + $3; }
	   |expr MINUS expr	    {$$ = $1 - $3; }
	   ;
term: NUMBER {$$=$1;}
       ;
%%
	 
#include <stdio.h>
#include <ctype.h>
#include <string.h>
char *programe;
YYSTYPE yylval;
extern void warning(const char *s, char *t);

int main(int argc, char **argv)
{
	programe = argv[0];
	strcpy(format, "%g\n");
	yyparse();
	return 0;
}

int yyerror(const char *s)
{
	warning(s, NULL);
	yyparse();
	return 0;
}

void warning(const char *s, char *t)
{
	fprintf(stderr, "%s: %s\n", programe, s);
	if (t)
		fprintf(stderr, " %s\n", t);
}
