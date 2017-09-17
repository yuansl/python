#include "token.h"
#include "preprocessor.h"
#include "macro.h"

int main(int argc, char **argv)
{
	char *filename;
	struct token *list_head;

	if (argc < 2)
		err_msg(1, "Usage: %s filename...", argv[0]);

	for (optind = 1; optind < argc; optind++) {
		filename = preprocessor(argv[optind]);
		list_head = match_tokens(filename);
		print_token_list(list_head);
	}
	return 0;
}
