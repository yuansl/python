#ifndef COMMENT_H
#define COMMENT_H

#include "comm_util.h"

void match_comment(const char *src, FILE *writeto);
char *remove_comments(const char *filename);

#endif
