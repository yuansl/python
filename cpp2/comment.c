#include "comment.h"
#include "preprocessor.h"

void skip_comment(const char *src, FILE *writeto)
{
	const char *p = src;

	while (*p) {
		if (status == INCOMMENT) {
			if (p[0] == '*' && p[1] == '/') {
				p += 2;
				status = NORMAL;
			} else {
				p++;
			}
		} else if (status == INSTRING) {
		until_string_end:
			for (; *p && *p != '\"'; p++)
				fputc(*p, writeto);
			if (*p == '\"') {
				if (p[-1] == '\\' && p[-2] != '\\') {
					fputc(*p++, writeto);
					goto until_string_end;
				}
				fputc(*p++, writeto);
			}
			status = NORMAL;
		} else {
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
			} else if (p[0] == '\"') {
				if (p[1] != '\'')
					status = INSTRING;
			}
			fputc(*p, writeto);
			p++;
		}
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
	strcat(fileout, basename((char *)filename));

	fout = fopen(fileout, "w");
	if (fout == NULL)
		err_sys("fopen(%s, 'w') error", fileout);

	while (fgets(linebuf, sizeof(linebuf), fp) != NULL)
		skip_comment(linebuf, fout);
	fclose(fp);
	fclose(fout);
	return fileout;
}
