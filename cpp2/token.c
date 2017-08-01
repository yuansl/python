#include "token.h"

#include "preprocessor.h"

int token_entry = 0;

static const char *keywords[] = {
	"bool",
	"if",
	"else",
	"while",
	"do",
	"for",
	"void",
	"int",
	"unsigned",
	"short",
	"long",
	"char",
	"float",
	"double",
	"EXIT_FAILURE",
	"EXIT_SUCCESS",
	"goto",
	"switch",
	"case",
	"default",
	"break",
	"sizeof",
	"include",
	"define",
	"ifdef",
	"defined",
	"endif",
	"elif",
	"main",
	"NULL",
	NULL
};

static const char symbol_map[128] = {
	['#'] = 1, ['('] = 1, [')'] = 1, ['['] = 1, [']'] = 1, ['{'] = 1,
	['}'] = 1, ['\''] = 1, ['\"'] = 1, ['+'] = 1, ['-'] = 1, ['*'] = 1,
	['/'] = 1, ['%'] = 1, ['&'] = 1, ['|'] = 1, ['^'] = 1, ['!'] = 1,
	['<'] = 1, ['>'] = 1, ['='] = 1, ['?'] = 1, [':'] = 1, [','] = 1,
	[';'] = 1, ['.'] = 1, ['\\'] = 1
};

static const char lookahead_symbol[128] = {
	['+'] = 1, ['-'] = 1, ['!'] = 1, ['*'] = 1, ['/'] = 1, ['%'] = 1,
	['&'] = 1, ['|'] = 1, ['^'] = 1, ['<'] = 1, ['>'] = 1, ['='] = 1
};

static const char *token_type_desc[] = {
	[SYMBOL] = "SYMBOL",
	[KEYWORD] = "KEYWORD",
	[IDENTIFIER] = "IDENTIFIER",
	[FUNCTION] = "FUNCTION",
	[NUMBER] = "NUMBER",
	[STRING] = "STRING",
	[CHARACTER] = "CHARACTER",
	NULL
};

bool issymbol(int c)
{
	if (c <= 0 || c >= 128)
		return false;
	return symbol_map[c];
}

bool lookahead(int c)
{
	if (c <= 0 || c >= 128)
		return false;
	return lookahead_symbol[c];
}

bool isident(int c)
{
	return isalnum(c) || c == '_';
}

const char *token_desc(enum token_type type)
{
	return token_type_desc[type];
}

bool iskeyword(const char *token)
{
	for (int i = 0; keywords[i] != NULL; i++)
		if (strequal(token, keywords[i]))
			return true;
	return false;
}


struct token *find_token_definition(struct token *list_head, const char *token_name)
{
	struct token *target = list_head;
	while (target != NULL) {
		if (strequal(target->token_name, token_name))
			return target;
		target = target->next;
	}
	return NULL;
}

struct token *create_token(const char *token_name, enum token_type type)
{
	struct token *tk = calloc(1, sizeof(*tk));
	if (tk == NULL)
		return tk;
	
	strcpy(tk->token_name, token_name);

	tk->attr.type = type;
	tk->attr.entry = token_entry;
	strcpy(tk->alias_name, token_name);
	
	if (iskeyword(tk->alias_name))
		tk->attr.type = KEYWORD;
	return tk;
}

void print_token_list(struct token *list_head)
{
	struct token *cur = list_head;
	while (cur != NULL) {
		printf("ToKEN: %s\n", cur->token_name);
		cur = cur->next;
	}
}

const char *recognize_character(char *token_name, int *offset, const char *string, const char *line)
{
	const char *p = string;
	int i = *offset;
	
	/* for CHARACTER: '\x00', '\377' */
	// and '\x00', '\ooo', '\t', '\'', '\"', 'a'...
	if (*p == '\\') {
		token_name[i++] = '\\';
		p++;
		if (*p == 'x') {
			/* for hexdecimal */
			token_name[i++] = *p++;
			int xdigit_cnt = 2;
			while (isxdigit(*p) && xdigit_cnt > 0) {
				token_name[i++] = *p++;
				xdigit_cnt--;
			}
		} else if (isdigit(*p)) {
			/* for octal */
			int oct_cnt = 3;
			while (isdigit(*p) && oct_cnt > 0) {
				token_name[i++] = *p++;
				oct_cnt--;
			}
		} else {
			token_name[i++] = *p++;
		}
	} else {
		token_name[i++] = *p++;
	}
	if (*p != '\'') {
		err_msg(0, "CHARACTER syntax error on `%s`", string);
		return NULL;
	}
	token_name[i++] = *p++;
	*offset = i;
	return p;
}

struct token *recognize_token(const char *filename, const char *line, struct token *list_head)
{
	int c;
	int i;
	char token_name[MAX_NAME] = {0};
	struct token *tail;
	struct token *token = NULL;
	enum token_type type;
	const char *p = skip_spaces(line);
	if (p == NULL)
		return list_head;

	tail = list_head;
	while (tail && tail->next != NULL)
		tail = tail->next;

	if (status == PARTSTRING) {
		assert(tail != NULL);
		i = strlen(tail->token_name);
		for (; *p && *p != '\"'; i++, p++) {
			if (p[0] == '\\' && isspace(p[1])) {
				tail->token_name[i] = '\0';
				return list_head;
			}
			tail->token_name[i] = *p;
		}
		if (*p == '\"') {
			status = NORMAL;
			tail->token_name[i++] = '\"';
			tail->token_name[i] = '\0';
			p++;
		} else {
			err_msg(1, "Unexpected EOL on  %s:`%s`", filename, line);
		}
	}
	
	while (*p) {
		c = *p++;
		i = 0;		
		if (isalpha(c) || c == '_') { /* for identifiers */
			type = IDENTIFIER;
			token_name[i++] = c;
			for (; *p && isident(*p); i++, p++)
				token_name[i] = *p;

		} else if (isdigit(c)) { /* for numbers */
			type = NUMBER;
			token_name[i++] = c;
			if (!isdigit(*p) && *p == 'x')
				token_name[i++] = *p++;
			
			for (; *p && isxdigit(*p); i++, p++)
				token_name[i] = *p;

		} else if (issymbol(c)) {
			/* for terminal symbols in c */
			type = SYMBOL;			
			token_name[i++] = c;
			/*
			 * `++`, `--`, `->`, `+=`, `-=`, `*=`, `/=`,
			 * `%=`, `<=`, `>=`, `|=`, `&=`, `^=`,
			 * `\'`, '\''
			 */
			if (c == '"' && *p != '\'') { /* for c-string */
				type = STRING;
			until_string_end:
				for (; *p && *p != '"'; i++, p++) {
					if (p[0] == '\\' && isspace(p[1])) {
						status = PARTSTRING;
						break;
					}
					token_name[i] = *p;
				}
				if (*p == '"') {
					if (p[-1] == '\\' && p[-2] != '\\') {
						token_name[i++] = *p++;
						goto until_string_end;
					}
					token_name[i++] = *p++;
				} else if (*p == '\\') {
					/* PARTSTRING */
					token_name[i] = '\0';
					token = create_token(token_name, type);
					if (tail == NULL) {
						list_head = token;
					} else {
						token->next = tail->next;
						tail->next = token;
					}
					return list_head;
				}
			} else if (c == '\'') {
				/* for c character e.g. 'a' */
				type = CHARACTER;
				p = recognize_character(token_name, &i, p, line);
				if (p == NULL) {
					err_msg(0, "At %s:`%s`", filename, line);
					return list_head;
				}
			} else {
				if (lookahead(c)) {
					/* lookahead */
					switch (c) {
					case '+':
						switch (*p) {
						case '+':
						case '=':
							token_name[i++] = *p++;
							token_name[i] = '\0';
							break;
						default:
							if (isdigit(*p)) {
								type = NUMBER;
								for (; *p && isdigit(*p); i++, p++)
									token_name[i] = *p;
							}
							break;
						}
						break;
					case '-':
						switch (*p) {
						case '-':
						case '>':
						case '=':
							token_name[i++] = *p++;
							token_name[i] = '\0';
							break;
						default:
							if (isdigit(*p)) {
								type = NUMBER;
								for (; *p && isdigit(*p); i++, p++)
									token_name[i] = *p;
							}
							break;
						}
						break;
					case '&':
						switch (*p) {
						case '&':
						case '=':
							token_name[i++] = *p++;
							break;
						default:
							break;
						}
						break;
					case '|':
						switch (*p) {
						case '|':
						case '=':
							token_name[i++] = *p++;
							break;
						default:
							break;
						}
					case '<':
						switch (*p) {
						case '<':
						case '=':
							token_name[i++] = *p++;
							break;
						}
						break;				
					case '>':
						switch (*p) {
						case '>':
						case '=':
							token_name[i++] = *p++;
							break;
						}
						break;
					case '!':
					case '/':
					case '*':
					case '%':
					case '^':
					case '=':
						if (*p == '=')
							token_name[i++] = *p++;
						break;
					default:
						break;
					}
				}
			}
		} else {	/* skip newline/space/ etc */
			continue;
		}
		token_name[i] = '\0';
		if (token && token->attr.type == IDENTIFIER && token_name[0] == '(') {
			token->attr.type = FUNCTION;
			token = NULL; /* last token should be deleted */
		}
		
		token_entry++;
		token = create_token(token_name, type);
		if (token == NULL)
			err_sys("create_token error");

		if (tail == NULL) {
			list_head = tail = token;
		} else {
			token->next = tail->next;
			tail->next = token;
			tail = token;
		}
		token_name[0] = '\0';
	}
	
	return list_head;
}

struct token *match_tokens(const char *filename)
{
	struct token *token_list_head = NULL;
	FILE *fp;
	char linebuf[MAX_LINE];
	
	fp = fopen(filename, "r");
	if (fp == NULL)
		err_sys("fopen(%s, r) error", filename);

	while (fgets(linebuf, sizeof(linebuf), fp) != NULL)
		token_list_head = recognize_token(filename, linebuf, token_list_head);
	
	fclose(fp);
	
	return token_list_head;
}
