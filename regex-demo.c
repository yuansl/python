#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <regex.h>
#include <unistd.h>

#define MAX_REGMATCH 10
#ifndef MAX_LINE
#define MAX_LINE 2048
#endif
#define MAX_REGMATCH 5

#define err_sys(msg) do { perror(msg); exit(EXIT_FAILURE); } while (0)

struct ident_list {
	char ident_name[64];
	int linum;
	char src_file[256];
	char regexp[MAX_LINE];
	struct ident_list *next;
} IDENT_HEAD;

typedef struct {
	int x;
	int y;
	char CARD_NBR[19+1];
	int BANK;
	char CUSTR_NBR[30+1];
	int XACCOUNT;
} card_tdef, bank_tdef, custr_tdef;

typedef card_tdef acct_tdef;
const char *keywords[] = {
	"bool",
	"_Bool",
	"true",
	"false",
	"void",
	"int",
	"long",
	"unsigned",
	"short",
	"double",
	"float",
	"char",
	"const",
	"size_t",
	"ssize_t",
	"for",
	"if",
	"while",
	"do",
	"union",
	"struct",
	"extern",
	"return",
	"goto",
	"break",
	"switch",
	"continue",
	"case",
	"default",
	"sizeof",
	"NULL",
	"EXIT_SUCCESS",
	"EXIT_FAILURE",
	"exit"
};

char *strcut(char *dst, const char *src, ssize_t so, ssize_t eo)
{
	ssize_t i;

	for (i = 0; i < eo - so; i++)
		dst[i] = src[i + so];
	dst[i] = '\0';
	return dst;
}

int main(void)
{
	regex_t preg;
	regmatch_t match[MAX_REGMATCH];	
	int err;
	char errbuf[128];
	const char *pattern = "tblacct(\\.|->)[[:alnum:]]+";
	const char *string = "tTblAcct->XACCOUNT; tTblAcct.BANK\n";
	const char *p;

	err = regcomp(&preg, pattern, REG_EXTENDED | REG_ICASE);
	if (err != 0) {
		regerror(err, &preg, errbuf, sizeof(errbuf));
		fprintf(stderr, "regcomp error: %s\n", errbuf);
		exit(1);
	}
	int last_eo = 0;

	int count = 0;
	char buf[1024];
	p = string;
	while (regexec(&preg, p, 10, match, REG_NOTBOL) == 0) {
		int i;
		strcut(buf, p, match[0].rm_so, match[0].rm_eo);
		printf("entire matched string: %s string[%d:%d]\n", buf, match[i].rm_so, match[i].rm_eo);		
		for (i = 1; match[i].rm_so != -1; i++) {
			strcut(buf, p, match[i].rm_so, match[i].rm_eo);
			printf("matched: %s string[%d:%d]\n", buf, match[i].rm_so, match[i].rm_eo);
			last_eo = match[i].rm_eo;
			break;
		}
		printf("last_eo=%d\n", last_eo);
		p += last_eo;
		if (++count >= 2)
			break;
	}
	
	if (err != 0) {
		regerror(err, &preg, errbuf, sizeof(errbuf));
		fprintf(stderr, "regexec error: %s\n", errbuf);
		exit(2);
	}

	regfree(&preg);
	return 0;
}

void find_definition(const char *token)
{
}

bool iskeyword(const char *identifier)
{
	for (int i = 0; keywords[i] != NULL; i++)
		if (strcmp(identifier, keywords[i]) == 0)
			return true;
	return false;
}

char *strip(char *dst, const char *string)
{
	const char *p = string;
	
	if (p == NULL)
		return NULL;
	
	while (*p != '\0' && isspace(*p))
		p++;
	while (*p != '\0')
		*dst++ = *p++;
	*dst = '\0';	
	if (dst[-1] == '\n')
		dst[-1] = '\0';

	return dst;
}

struct ident_list *find_identifier_definition(const char *identifier)
{
	struct ident_list *next = IDENT_HEAD.next;
	while (next != NULL) {
		if (strcmp(next->ident_name, identifier) == 0)
			return next;
		next = next->next;
	}
	return NULL;
}

/*
 * Test if the `identifier` is part of c-string
 * e.g. string = "something and identifier";
 */
bool isinsidestring(const char *string, const char *identifier)
{
	if (strstr(string, identifier) != NULL && strchr(string, '"') != NULL)
		return true;
	
	return false;
}

void do_match(regex_t *handle, int linum, const char *string)
{
	regmatch_t matched[MAX_REGMATCH];
	char identifier[64];
	const char *cur_pos = string;

	while (regexec(handle, cur_pos, MAX_REGMATCH, matched, REG_NOTBOL) == 0) {
		strcut(identifier, cur_pos, matched[0].rm_so, matched[0].rm_eo);
		if (!iskeyword(identifier) &&
		    !isinsidestring(string, identifier)) {
			struct ident_list *ident;
			ident = find_identifier_definition(identifier);
			if (ident == NULL) {
				ident = calloc(1, sizeof(*ident));
				strcpy(ident->ident_name, identifier);
				strip(ident->regexp, string);
				ident->linum = linum;
				ident->next = IDENT_HEAD.next;
				IDENT_HEAD.next = ident;
#ifdef DEBUG
				printf("matched identifier: %s at line %d\n",
				       identifier, linum);
#endif
			} else {
				printf("%s has been defined before: /^%s$/\n",
				       identifier, ident->regexp);
			}
		}
		cur_pos += matched[0].rm_eo;
	}
}

void traval_list(struct ident_list *list_head)
{
	struct ident_list *prev, *p;

	prev = NULL;
	p = list_head;
	while (p != NULL) {
		printf("%d: %s /^%s$/\n", p->linum, p->ident_name, p->regexp);
		prev = p->next;
		free(p);
		p = prev;
	}
}

/*
 * tags format:
 *
 * identifier-name src-file /^regular expression$/
 */
void generate_tags(const char *src_file)
{
	FILE *fp, *fout;
	char buf[MAX_LINE];
	int err;
	char errbuf[128];
	regex_t *handle;
	const char *identifier_pattern = "[[:alpha:]_][[:alnum:]_]+";
	int linum;		/* line number */

	fp = fopen(src_file, "r");
	if (fp == NULL)
		err_sys("fopen error");

	fout = fopen("tags", "w");
	if (fout == NULL)
		err_sys("fopen error");

	handle = calloc(1, sizeof(*handle));
	err = regcomp(handle, identifier_pattern, REG_EXTENDED | REG_ICASE);
	if (err != 0) {
		regerror(err, handle, errbuf, sizeof(errbuf));
		fprintf(stderr, "regcomp error: %s\n", errbuf);
	}
	
	linum = 0;
	while (fgets(buf, sizeof(buf), fp) != NULL) {
		linum++;
		if (buf[0] == '#')
			continue;

		do_match(handle, linum, buf);
	}
	
	fclose(fp);
	fclose(fout);
	regfree(handle);
	free(handle);
}
