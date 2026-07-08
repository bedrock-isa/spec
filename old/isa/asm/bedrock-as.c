#include "bedrock_asm.h"

#include <stdio.h>
#include <string.h>

static void usage(FILE *fp)
{
    fputs("usage: bedrock-as [-o output.o] input.s\n", fp);
}

int main(int argc, char **argv)
{
    const char *input = 0;
    const char *output = "a.o";
    BedrockAsm ctx;
    int index;

    for (index = 1; index < argc; ++index) {
        if (strcmp(argv[index], "-o") == 0) {
            if (index + 1 >= argc) {
                usage(stderr);
                return 2;
            }
            output = argv[++index];
        } else if (strcmp(argv[index], "--help") == 0 || strcmp(argv[index], "-h") == 0) {
            usage(stdout);
            return 0;
        } else if (argv[index][0] == '-') {
            fprintf(stderr, "bedrock-as: unknown option %s\n", argv[index]);
            usage(stderr);
            return 2;
        } else if (input == 0) {
            input = argv[index];
        } else {
            fprintf(stderr, "bedrock-as: multiple input files are not supported yet\n");
            return 2;
        }
    }

    if (input == 0) {
        usage(stderr);
        return 2;
    }

    bedrock_asm_init(&ctx);
    if (!bedrock_asm_parse_file(&ctx, input) || ctx.error_count != 0u) {
        bedrock_asm_free(&ctx);
        return 1;
    }
    if (!bedrock_asm_write_elf64(&ctx, output)) {
        fprintf(stderr, "bedrock-as: failed to write %s\n", output);
        bedrock_asm_free(&ctx);
        return 1;
    }
    bedrock_asm_free(&ctx);
    return 0;
}
