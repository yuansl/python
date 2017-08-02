%{
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

#ifndef YYSTYPE
#define YYSTYPE double
#endif
extern int yylex();
extern int yyerror(const char *s);
%}

%token NUMBER MOD EOLN SEMICOLON NOT OR SPACE LPAREN RPAREN
%token PLUS MINUS DIV MUL POW
%left PLUS MINUS
%left MUL DIV
%left LPAREN RPAREN
%%
Grammar: stmt EOLN                     { printf("%f\n", $$); exit(0); }
       ;

stmt: /* Empty */
      | expr
      ;

expr:  LPAREN expr RPAREN { $$=$2; }
       | mul_expr 
       | add_expr         
       ;

mul_expr:  expr MUL expr            { $$ = $1 * $3; }
	   | expr DIV expr         { $$ = $1 / $3; }
           | expr MOD expr         { $$ = (int)$1 % (int)$3; }
	   | term
	   ;

add_expr: expr PLUS expr               { $$ = $1 + $3; }
	   |expr MINUS expr	       { $$ = $1 - $3; }
	   ;

term: NUMBER {$$=$1;}
       ;
%%
