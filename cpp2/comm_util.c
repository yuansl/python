#include "comm_util.h"

bool strequal(const char *s1, const char *s2)
{
	return strcmp(s1, s2) == 0;
}

char *strcut(char *dst, const char *src, off_t so, off_t eo)
{
	off_t i;
	if (dst == NULL)
		return NULL;
	for (i = 0; i < eo - so && src[i + so]; i++)
		dst[i] = src[i + so];
	dst[i] = '\0';
	return dst;
}

void err_msg(bool die, const char *fmt, ...)
{
	va_list ap;
	char errbuf[MAX_LINE];
	va_start(ap, fmt);
	vsprintf(errbuf, fmt, ap);
	fprintf(stderr, "%s\n", errbuf);
	va_end(ap);
	if (die)
		exit(EXIT_FAILURE);
}

regex_t *reg_compile(const char *regex_pattern)
{
	regex_t *preg;
	int err;
	char errbuf[MAX_LINE];
	
	preg = calloc(1, sizeof(*preg));
	if (preg == NULL)
		return preg;

	err = regcomp(preg, regex_pattern, REG_ICASE | REG_EXTENDED);
	if (err != 0) {
		regerror(err, preg, errbuf, sizeof(errbuf));
		fprintf(stderr, "regcomp error: %s\n", errbuf);
		goto err_exit;
	}
	return preg;
err_exit:
	free(preg);
	return NULL;
}

const char *skip_spaces(const char *s)
{
	if (s == NULL)
		return NULL;
	while (*s && isspace(*s))
		s++;
	return s;
}
