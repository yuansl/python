#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include "comm_util.h"

enum state {
	NORMAL,
	OUTCOMMENT,
	INCOMMENT,
	INSTRING,
	PARTSTRING,
	RECG_MACRO_NAME,
	RECG_MACRO_PARAMS,
	RECG_MACRO_BODY
};

struct cpp_ctx {
	struct macro *macro_list;
	char filename[MAX_NAME];
};

struct cpp_ctx *preprocessor(const char *filename);

extern enum state status;

#endif
