#include "token.h"

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

int token_entry = 0;

bool issymbol(int c)
{
	if (c <= 0 || c >= 128)
		return false;
	return symbol_map[c];
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

void match_comment(const char *src, FILE *writeto)
{
	const char *p = src;

	while (*p) {
		if (status == INCOMMENT) {
			if (p[0] == '*' && p[1] == '/') {
				p += 2;
				status = OUTCOMMENT;
				continue;
			}
			p++;
			continue;
		}
		
		if (p[0] == '/') {
			if (p[1] == '/') {
				/* ignore whole line after the '//' */
				fputc('\n', writeto);
				return;
			}
			
			if (p[1] == '*') {
				status = INCOMMENT;
				p += 2;
				continue;
			}
		}
		
		fputc(*p, writeto);
		p++;
	}
	
}

char *remove_comments(const char *filename)
{
	static char fileout[MAX_NAME];
	char linebuf[MAX_LINE];
	FILE *fp;
	FILE *fout;

	fp = fopen(filename, "r");
	if (fp == NULL)
		err_sys("fopen(%s, 'r') error", filename);

	strcpy(fileout, "/tmp/");
	strcat(fileout, filename);

	fout = fopen(fileout, "w");
	if (fout == NULL)
		err_sys("fopen(%s, 'w') error", fileout);

	while (fgets(linebuf, sizeof(linebuf), fp) != NULL) {
		match_comment(linebuf, fout);
	}
	fclose(fp);
	fclose(fout);
	return fileout;
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

struct token *create_token(const char *token_name)
{
	struct token *tk = calloc(1, sizeof(*tk));
	if (tk == NULL)
		return tk;
	
	strcpy(tk->token_name, token_name);
	tk->attr.type = IDENTIFIER;
	tk->attr.entry = token_entry;
	strcpy(tk->alias_name, token_name);
	if (token_name[strlen(token_name)-1] == '(') {
		tk->alias_name[strlen(token_name) - 1] = '\0';
		if (!strequal(tk->alias_name, "sizeof"))
			tk->attr.type = FUNCTION;
	}

	return tk;
}

struct token *create_token2(const char *token_name, enum token_type type)
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

struct token *match_token(regex_t *preg, const char *line, struct token *list_head)
{
	char token_name[MAX_NAME];
	regmatch_t pmatch[MAX_REGMATCH];
	const char *s = line;
	struct token *token;
	while (regexec(preg, s, MAX_REGMATCH, pmatch, 0) == 0) {
		strcut(token_name, s, pmatch[0].rm_so, pmatch[0].rm_eo);

		printf("Token: `%s`\n", token_name);
		token = find_token_definition(list_head, token_name);
		if (token == NULL) {
			token = create_token(token_name);
			if (token == NULL)
				err_sys("create_token");
			
			if (list_head == NULL) {
				list_head = token;
			} else {
				token->next = list_head->next;
				list_head->next = token;
			}
		}
		s += pmatch[0].rm_eo;
	}
	return list_head;
}

struct token *generate_tokens(const char *filename)
{
	struct token *token_list_head = NULL;
	FILE *fp;
	char linebuf[MAX_LINE];
	regex_t *preg;
	
	fp = fopen(filename, "r");
	if (fp == NULL)
		err_sys("fopen(%s, r) error", filename);
	
	preg = reg_compile("[[:alpha:]_][[:alnum:]_]*[ \\t]*\\(?");
	if (preg == NULL) {
		fclose(fp);
		err_sys("reg_compile error");
	}
	
	while (fgets(linebuf, sizeof(linebuf), fp) != NULL)
		token_list_head = match_token(preg, linebuf, token_list_head);
	
	fclose(fp);
	regfree(preg);
	free(preg);
	return token_list_head;
}

void print_token_list(struct token *list_head)
{
	struct token *cur = list_head;
	while (cur != NULL) {
		printf("%s ",
		       cur->alias_name);
		cur = cur->next;
	}
}

struct token *generate_token(const char *token_name, struct token *list_head)
{
	struct token *token = create_token(token_name);
	if (token == NULL)
		err_sys("create_token error");
	if (list_head == NULL) {
		list_head = token;
	} else {
		token->next = list_head->next;
		list_head->next = token;
	}
	return list_head;
}

struct token *recognize_token(const char *line, struct token *list_head)
{
	int c;
	int i;
	char token_name[MAX_NAME] = {0};
	const char *p = skip_spaces(line);
	struct token *tail = list_head;
	struct token *token = NULL;
	enum token_type type;
	if (p == NULL)
		return NULL;

	if (status == INCOMMENT) {
		while (*p) {
			if (p[0] == '*' && p[1] == '/') {
				p += 2;
				status = OUTCOMMENT;
				break;
			}
			p++;
		}
	}

	while (tail && tail->next != NULL)
		tail = tail->next;
	
	while (*p) {
		c = *p++;
		if (isalpha(c) || c == '_') {
			type = IDENTIFIER;
			token_name[0] = c;
			for (i = 1; *p && isident(*p); i++, p++)
				token_name[i] = *p;
			token_name[i] = '\0';

		} else if (isdigit(c)) {
			type = NUMBER;			
			token_name[0] = c;
			for (i = 1; *p && isdigit(*p); i++, p++)
				token_name[i] = *p;
			token_name[i] = '\0';

		} else if (issymbol(c)) {
			i = 0;
			token_name[i++] = c;
			type = SYMBOL;
			/*
			 * `++`, `--`, `->`, `+=`, `-=`, `*=`, `/=`,
			 * `%=`, `<=`, `>=`, `|=`, `&=`, `^=`,
			 * `\'`, '\''
			 */

			if (c == '\"') {
				type = STRING;
				for (; *p && *p != '\"'; i++, p++)
					token_name[i] = *p;
				if (*p != '\"')
					err_msg(0, "syntax on `%s`", line);
				token_name[i++] = *p++;
			} else if (c == '\'') {
				/* '\x00', '\377' */
				// for '\x00', '\ooo', '\t', '\'', '\"', 'a'...
				if (*p == '\\') {
					token_name[i++] = '\\';
					p++;
					if (*p == 'x') {
						token_name[i++] = *p++;
						int xdigit_cnt = 2;
						while (isdigit(*p) && xdigit_cnt > 0) {

							token_name[i++] = *p++;
							xdigit_cnt--;
						}
						if (xdigit_cnt > 0)
							err_msg(0, "syntax on `%s`", line);
					} else if (isdigit(*p)) {
						int oct_cnt = 3;
						while (isdigit(*p) && oct_cnt > 0) {
							token_name[i++] = *p++;
							oct_cnt--;
						}
							
					} else {
						token_name[i++] = *p++;
					}
						
					if (*p != '\'') {
						err_msg(0, "syntax on `%s`", p);
					} else {
						token_name[i++] = *p++;
					}
				} else {
					for (; *p && *p != '\''; i++, p++)
						token_name[i] = *p;
					if (*p != '\'') {
						err_msg(0, "syntax on `%s`", p);
					} else {
						token_name[i++] = *p++;
					}
				}
			} else {
				if (issymbol(*p)) {
					if (c == '+') {
						switch (*p) {
						case '+':
						case '=':
							token_name[i++] = *p++;
							token_name[i] = '\0';
							break;
						default:
							err_msg(0, "Unknown token: %c%c", c, *p);
							break;
						}
					} else if (c == '-') {
						switch (*p) {
						case '-':
						case '>':
						case '=':
							token_name[i++] = *p++;
							token_name[i] = '\0';
							break;
						default:
							err_msg(0, "Unknown token %c%c", c, *p);
							break;
						}
					} else if (c == '*' ||
						   c == '/' ||
						   c == '%' ||
						   c == '&' ||
						   c == '|' ||
						   c == '^' ||
						   c == '<' ||
						   c == '>' ||
						   c == '=' ||
						   c == '!') {
						token_name[i++] = *p++;
					}
				}
			}
		} else {
			continue;
		}
		token_name[i] = '\0';
		if (token && token->attr.type == IDENTIFIER && token_name[0] == '(') {
			token->attr.type = FUNCTION;
			token = NULL;
		}
		
		token_entry++;
		token = create_token2(token_name, type);
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
		token_list_head = recognize_token(linebuf, token_list_head);
	
	fclose(fp);
	
	return token_list_head;
}

int main(int argc, char **argv)
{
	char *filename;
	if (argc < 2)
		err_msg(1, "Usage: %s filename...", argv[0]);

	for (optind = 1; optind < argc; optind++) {
		filename = remove_comments(argv[optind]);	
		struct token *list_head = match_tokens(filename);
		print_token_list(list_head);
	}
	return 0;
}
