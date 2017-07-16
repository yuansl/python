#ifndef TOKEN_H
#define TOKEN_H

#include "comm_util.h"

enum token_type {
	SYMBOL,
	KEYWORD,
	IDENTIFIER,
	FUNCTION,
	NUMBER,
	STRING,
	COMMENT,
	CHARACTER
};

struct token {
	char token_name[MAX_NAME];
	char alias_name[MAX_NAME];
	struct {
		enum token_type type;
		int entry;
	} attr;

	struct token *next;
};

enum {
	OUTCOMMENT,
	INCOMMENT
} status;

struct token *find_token_definition(struct token *list_head, const char *token_name);
struct token *create_token(const char *token_name);
struct token *match_token(regex_t *preg, const char *line, struct token *list_head);
struct token *generate_tokens(const char *filename);

#endif
