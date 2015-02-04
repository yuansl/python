#include <string.h>
#include <stdlib.h>
#include <stdio.h>
/* A hack for parse a douban music url
 * e.g: 
 * http://www.xiami.com/song/playlist/id/82479/object_name/default/object_id/0 
 * this is just a xml file, the real location (I mean *.mp3 or other form )is 
 * marked as <Location>, but the value string is encoded with an algorithm,
 * so, the follow parser will deal with it.
 */
void parsestr(const char *str)
{
	int slen = strlen(str + 1);
	int rows = str[0] - '0';
	int cols = slen / rows;
	int right_rows = slen % rows;
	char new_str[rows][cols + 2];
	const char *p = str + 1;
	char ret[1024], real_ret[1024];
	int i, j, ct;
	
	for (i = 0; i < right_rows; i++) {
		strncpy(new_str[i], p, cols + 1);
		new_str[i][cols + 1] = '\0';
		p += cols + 1;
	}
	for (; i < rows; i++) {
		strncpy(new_str[i], p, cols);
		new_str[i][cols] = '\0';
		p += cols;
	}
	ct = 0;
	for (j = 0; j < cols; j++) 
		for (i = 0; i < rows; i++)
			ret[ct++] = new_str[i][j];

	for (i = 0; i < right_rows; i++)
		ret[ct++] = new_str[i][j];
	ret[ct] = '\0';
	p = ret;
	i = 0;
	while (*p) {
		if (*p == '%') {
			switch (*++p) {
			case '2':
				real_ret[i] = '/';
				break;
			case '3':
				if (*(p + 1) == 'F')
					real_ret[i] = '?';
				else if (*(p + 1) == 'D')
					real_ret[i] = '=';
				else
					real_ret[i] = ':';
				break;
			case '5':
				real_ret[i] = '0';
				break;
			default:
				fprintf(stderr, "Fatal error\n");
				exit(EXIT_FAILURE);
			}
			i++;
			p += 2;
			continue;
		} 
		real_ret[i++] = *p++;
	}
}
