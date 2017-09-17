#include "preprocessor.h"
#include "comment.h"
#include "macro.h"

enum state status = NORMAL;

struct cpp_ctx *preprocessor(const char *filename)
{
	struct cpp_ctx *ctx = calloc(1, sizeof(*ctx));
	assert(ctx != NULL);
	strcpy(ctx->filename, remove_comments(filename));

	ctx->macro_list = find_all_macros(ctx->filename);
	return ctx;
}
