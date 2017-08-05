%{
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#ifndef YYSTYPE
#define YYSTYPE double
#endif
extern int yylex();
extern int yyerror(const char *s);
%}

%token NUMBER EOLN LOG2 SIN EXIT
%left OR
%left AND
%left LT LE GT GE EQ
%token PLUS MINUS 
%left PLUS MINUS
%left MUL DIV POW MOD
%left NOT
%left LPAREN RPAREN
%%

Grammar: %empty /* Empty */
         | Grammar stmt
         ;

stmt: expr_stmt
      | exit_stmt
      ;

exit_stmt: EXIT                   { printf("exiting...\n"); exit(0); } 
           ;

expr_stmt: expr EOLN              { printf(">>> %f\n", $$); }
           ;

expr:  LPAREN expr RPAREN { $$=$2;}
       | mul_expr                 
       | add_expr                 
       | math_expr
       ;

mul_expr:  expr MUL expr          { $$ = $1 * $3; }
	   | expr DIV expr        { $$ = $1 / $3; }
           | expr MOD expr        { $$ = (int)$1 % (int)$3; }
	   | term
	   ;

add_expr:  expr PLUS expr         { $$ = $1 + $3; }
	   | expr MINUS expr	  { $$ = $1 - $3; }
	   ;

math_expr: LOG2 LPAREN expr RPAREN
           { $$ = log2($3); }
           | SIN LPAREN expr RPAREN
	   { $$ = sin($3); }
           ;

term: NUMBER { $$=$1; }
      ;
%%
