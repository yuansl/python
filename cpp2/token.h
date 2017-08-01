#ifndef TOKEN_H
#define TOKEN_H

#include "comm_util.h"

enum token_type {
	SYMBOL,
	KEYWORD,
	IDENTIFIER,
	FUNCTION,
	DIRECTIVE,
	NUMBER,
	STRING,
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

struct token *find_token_definition(struct token *list_head, const char *token_name);
struct token *create_token(const char *token_name, enum token_type type);
struct token *match_tokens(const char *filename);
void print_token_list(struct token *list_head);
struct token *recognize_token(const char *filename, const char *line, struct token *list_head);
#endif
