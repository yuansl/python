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

%token NUMBER  EOLN SEMICOLON SPACE LOG2 SIN IF THEN AND
%left OR
%left AND
%left LT LE GT GE EQ
%token PLUS MINUS 
%left PLUS MINUS
%left MUL DIV POW MOD
%left NOT
%left LPAREN RPAREN
%%
Grammar: stmt EOLN                { printf("%f\n", $$); exit(0); }
       ;

stmt: /* Empty */
      | expr
      | stmt SEMICOLON stmt       { $$ = $3; }
      | if_stmt
      ;

expr:  LPAREN expr RPAREN { $$=$2; }
       | mul_expr
       | add_expr
       | math_expr
       | logic_expr
       | cond_expr
       ;

if_stmt: IF cond_expr THEN stmt
       ;

mul_expr:  expr MUL expr            { $$ = $1 * $3; }
	   | expr DIV expr         { $$ = $1 / $3; }
           | expr MOD expr         { $$ = (int)$1 % (int)$3; }
	   | term
	   ;

add_expr:  expr PLUS expr              { $$ = $1 + $3; }
	   | expr MINUS expr	       { $$ = $1 - $3; }
	   ;

math_expr: LOG2 LPAREN expr RPAREN
           { $$ = log2($3); }
           | SIN LPAREN expr RPAREN
	   { $$ = sin($3); }
           ;

cond_expr: lt_expr
           | le_expr
           | gt_expr
           | ge_expr
           | not_expr
           | eq_expr
           ;

lt_expr: expr LT expr { $$ = $1 < $3; }
;
le_expr: expr LE expr { $$ = $1 <= $3; }
;
gt_expr: expr GT expr { $$ = $1 > $3; }
;
ge_expr: expr GE expr { $$ = $1 >= $3; }
; 

logic_expr: expr AND expr { if ($1 && $3) $$=1; else $$=0; }
            | expr OR  expr { if ($1 || $3) $$=1; else $$=0; }
;
not_expr: NOT expr { if ((int)$2 != 0)$$ = 0; else $$=1; }
;
eq_expr: expr EQ expr { if ($1 == $3) $$=1; else $$=0; }
         ;

term: NUMBER { $$=$1; }
      ;
%%
