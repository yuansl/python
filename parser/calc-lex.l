%{
#ifndef YYSTYPE
#define YYSTYPE double
#endif
#include "calc-grammar.tab.h"
extern YYSTYPE yylval;
%}
D [0-9.]
%%
[ \t]* {;}
{D}+  { sscanf(yytext, "%lf", &yylval); return NUMBER; }
"+"   return PLUS;
"-"   return MINUS;
"*"   return MUL;
"/"   return DIV;
"%"   return MOD;
"&&"  return AND;
"||"  return OR;
"\n"  return EOLN;
"("   return LPAREN;
")"   return RPAREN;
"log2" return LOG2;
"sin" return SIN;
"<"   return LT;
"<="  return LE;
">"   return GT;
">="  return GE;
"=="  return EQ;
"!"   return NOT;
"if"  return IF;
"then" return THEN;
";"    return SEMICOLON;
"while" return WHILE;
"do"  return DO;
"done" return DONE;
"="    return ASSIGN;
"[a-zA-Z_][a-zA-Z0-9_]+"  printf("IDENT `%s`", yytext); return IDENT;
"[a-z]+" printf("THIS IDENT `%s`", yytext); return IDENT;

%%
