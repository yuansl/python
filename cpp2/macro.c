#include "macro.h"

#include "preprocessor.h"

#define macro_\
	demo(msg,\
	     msg2,msg3) do {\
	} while (0)

#define demo2 2
#define good_this_is_a_so_long_long_macro_defin\
	e_but_I_done

static const char *store_macro_name(char *macro_name, const char *macro_stmt)
{
	const char *p = macro_stmt;
	int i;
	
	for (i = strlen(macro_name); *p && i < MAX_NAME; i++, p++) {
		if (*p == '(' || isspace(*p)) {
			if (*p == '(')
				status = RECG_MACRO_PARAMS;
			else
				status = RECG_MACRO_BODY;
			p++;
			break;
		} else if (p[0] == '\\' && isspace(p[1])) {
			p++;
			break;
		}
		macro_name[i] = *p;
	}
	
	if (*p) {
		err_msg(0, "WARNING: Macro name is too long");
		macro_name[i] = '\0';
		return "";
	}
	
	return p;
}

static const char *store_macro_params(char (*macro_params)[MAX_NAME], const char *params_start)
{
	/* macro params should be ( |,param1,param2) ) */
	const char *p = params_start;

	for (; *p && *p != ')'; p++) {
		if (*p == ',') {
				/* next macro param */
				macro_params[i][j] = '\0';
				i++;
				p++;
		} else if (p[0] == '\\' && isspace(p[1])) {
			
		}
	}
	if (*p == ')') {
		status = RECG_MACRO_BODY;
		p += 1;
	}
	return p;
}

static const char *store_macro_body(char *macro_body, int offset, const char *body_stmt)
{
	const char *p = body_stmt;
	return p;
}

void save_macro_entry(struct macro *macro, const char *macro_stmt)
{
	assert(macro != NULL);
	
	int len;
	static char buf[BUFSIZ] = {0};
	const char *p = skip_spaces(p);
	while (*p) {
		switch (status) {
		case RECG_MACRO_NAME:
			p = store_macro_name(macro->macro_name, p);
			break;
		case RECG_MACRO_PARAMS:
			p = store_macro_params(buf, p);
			break;
		case RECG_MACRO_BODY:
			p = store_macro_body(buf, p);
			break;
		default:	/* NORMAL state */
			p++;
			break;
		}
	}
}

const struct macro *macro_exists(const struct macro *list_head, const char *macro_name)
{
	const struct macro *target = list_head;

	while (target != NULL) {
		if (strequal(target->macro_name, macro_name))
			break;
		target = target->next;
	}
	return target;
}

/* A macro stmt is like : #define xxxx xxxx */
struct macro *find_macro_entry(struct macro *list_head, const char *line)
{
	struct macro *macro;
	struct macro *tail;
	const char *p = skip_spaces(line);
	
	tail = list_head;
	while (tail && tail->next != NULL)
		tail = tail->next;

	if (status != NORMAL) {
		macro = tail;
		save_macro_entry(macro, p);		
	} else {
		if (*p == '#') {
			/* # define macro_name() macro_body */
			p = strstr(p, "define");
			if (p == NULL)
				break;

			p += strlen("define");
			macro = calloc(1, sizeof(*macro));
			assert(macro != NULL);
			status = RECG_MACRO_NAME;			
			save_macro_entry(macro, p);
			if (macro_exists(macro->macro_name)) {
				free(macro);
			} else {
				if (tail == NULL) {
					list_head = macro;
				} else {
					macro->next = tail->next;
					tail->next = macro;
					tail = macro;
				}
			}
		}
	}

	return list_head;
}

struct macro *find_all_macros(const char *src_file)
{
	struct macro *list_head = NULL;
	FILE *fp;
	char linebuf[MAX_LINE];
	char macro_name[MAX_NAME];

	fp = fopen(src_file, "r");
	if (fp != NULL) {
		status = NORMAL;
		/* It's ok if there is no macros in a src file */
		while (fgets(linebuf, sizeof(linebuf), fp) != NULL)
			list_head = find_macro_entry(linebuf, list_head);

		fclose(fp);
	}
	return list_head;
}
