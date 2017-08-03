#include <stdio.h>
#include <ctype.h>
#include <string.h>

char format[20];
char *programe;

extern void warning(const char *s, char *t);
int yyparse (void);

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
