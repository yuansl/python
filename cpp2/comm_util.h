#ifndef COMM_UTIL_H
#define COMM_UTIL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdarg.h>
#include <regex.h>
#include <unistd.h>
#include <errno.h>

#define MAX_LINE 4096
#define MAX_NAME 256
#define MAX_REGMATCH 2

#define err_sys(fmt, ...)						\
	do {								\
		char tmp[MAX_LINE];					\
		sprintf(tmp, fmt, ##__VA_ARGS__);			\
		err_msg(1, "%s:%d: %s: %s",				\
			__FILE__, __LINE__, tmp, strerror(errno));	\
	} while (0)

bool strequal(const char *s1, const char *s2);
char *strcut(char *dst, const char *src, off_t so, off_t eo);
regex_t *reg_compile(const char *regex_pattern);
void err_msg(bool die, const char *fmt, ...);
const char *skip_spaces(const char *s);

#endif
