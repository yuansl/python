%{
#ifndef YYSTYPE
#define YYSTYPE double
#endif
#include "y.tab.h"
#include <math.h>
extern YYSTYPE yylval;
%}
D [0-9.]
%%
[ \t] {;}
{D}+  { sscanf(yytext, "%lf", &yylval); printf("TOKEN: `%f`\n", yylval); return NUMBER; }
"+" printf("TOKNE: `%s`\n", yytext);return PLUS;
"-" printf("TOKNE: `%s`\n", yytext);return MINUS;
"*" return MUL;
"/" return DIV;
"%"  return MOD;
"!!" return NOT;
"||" return OR;
"\n" printf("TOKEN: new-line\n"); return EOLN;
%%
