#include "remove_comments.h"
#include "token.h"

static void match_comment(const char *src, FILE *writeto);

char *remove_comments(const char *filename)
{
	FILE *fp;
	FILE *fout;
	char linebuf[MAX_LINE];	
	static char fileout[MAX_NAME];

	fp = fopen(filename, "r");
	if (fp == NULL)
		err_sys("fopen(%s, 'r') error", filename);

	sprintf(fileout, "/tmp/%s", filename);

	fout = fopen(fileout, "w");
	if (fout == NULL)
		err_sys("fopen(%s, 'w') error", fileout);

	while (fgets(linebuf, sizeof(linebuf), fp) != NULL)
		match_comment(linebuf, fout);

	fclose(fp);
	fclose(fout);
	return fileout;
}

static void match_comment(const char *src, FILE *writeto)
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
