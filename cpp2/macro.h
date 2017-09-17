#ifndef MACRO_H
#define MACRO_H

#include "comm_util.h"

struct macro {
	char macro_name[MAX_NAME];
	char macro_params[MAX_PARAM][MAX_NAME];
	char macro_body[MAX_LINE];
	char buf[BUFSIZ];
	struct macro *next;
};

struct macro *find_macro(struct macro *list_head, const char *line);
struct macro *find_all_macros(const char *src_file);

#endif
