#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <regex.h>
#include <unistd.h>

#define MAX_REGMATCH 10

typedef struct {
	int x;
	int y;
	char CARD_NBR[19+1];
	int BANK;
	char CUSTR_NBR[30+1];
	int XACCOUNT;
} card_tdef, bank_tdef, custr_tdef;

typedef card_tdef acct_tdef;

#if 0
int L040_account_bal(card_tdef *ptTblCard, bank_tdef *ptTblBank, custr_tdef *ptTblCustr, acct_tdef *ptTblAcct)
{
	acct_tdef tTblAcct;
	ptTblBank->x = ptTblCard->x + ptTblCustr->x +
		ptTblCustr->x;

	tTblAcct.XACCOUNT = ptTblBank->x +
		ptTblAcct->XACCOUNT;
	
	return 0;
}
#endif
char *strcut(char *dst, const char *src, size_t so, size_t eo)
{
	int i;
	for (i = 0; i < eo - so; i++)
		dst[i] = src[i+so];
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
