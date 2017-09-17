#ifndef DIRECTIVES_H
#define DIRECTIVES_H

struct directive {
	struct token *tk;
	struct directive *next;
};

#endif
