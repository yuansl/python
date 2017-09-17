#include "directives.h"

struct directive find_directive(struct token *list_head)
{
	struct directive *directive;

	struct token *cur = list_head;
	while (cur) {
		if (strequal(cur->token_name, "#")) {
			if (cur->next && strequal(cur->next->token_name,"define")) {
				break;
			}
		}
		cur = cur->next;
	}
	if (cur != NULL) {
		while (cur != NULL) {
			printf("Token: %s\n", cur->token_name);
			cur = cur->next;
		}
	}
}
