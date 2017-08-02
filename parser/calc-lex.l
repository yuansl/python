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
"!!"  return NOT;
"||"  return OR;
"\n"  return EOLN;
"("   return LPAREN;
")"   return RPAREN;
%%
