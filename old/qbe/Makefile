BIN = qbe

V = @
OBJDIR ?= ../build/qbe/obj

SRC      = main.c util.c parse.c cfg.c mem.c ssa.c alias.c load.c copy.c \
           fold.c live.c spill.c rega.c gas.c
BEDROCKSRC = bedrock/targ.c bedrock/abi.c bedrock/isel.c bedrock/emit.c
SRCALL   = $(SRC) $(BEDROCKSRC)

BEDROCKOBJ = $(BEDROCKSRC:%.c=$(OBJDIR)/%.o)
OBJ      = $(SRC:%.c=$(OBJDIR)/%.o) $(BEDROCKOBJ)

CFLAGS += -Wall -fPIC -Wextra -std=c99 -g -pedantic

$(OBJDIR)/$(BIN): $(OBJ) $(OBJDIR)/timestamp
	@test -z "$(V)" || echo "ld $@"
	$(V)$(CC) $(LDFLAGS) $(OBJ) -o $@

bedrock: $(OBJDIR)/$(BIN)

help:
	@printf '%s\n' 'QBE targets:'
	@printf '  %-10s %s\n' 'bedrock' 'Build the Bedrock-enabled QBE binary.'
	@printf '  %-10s %s\n' 'check' 'Run the QBE test suite.'
	@printf '  %-10s %s\n' 'clean' 'Remove QBE build artifacts.'
	@printf '  %-10s %s\n' 'clean-gen' 'Remove QBE build artifacts and generated config.h.'

$(OBJDIR)/%.o: %.c $(OBJDIR)/timestamp
	@test -z "$(V)" || echo "cc $<"
	$(V)$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR)/timestamp:
	@mkdir -p $(OBJDIR)
	@mkdir -p $(OBJDIR)/bedrock
	@touch $@

$(OBJ): all.h ops.h
$(BEDROCKOBJ): bedrock/all.h
$(OBJDIR)/main.o: config.h

install: $(OBJDIR)/$(BIN)
	mkdir -p "$(DESTDIR)/$(PREFIX)/bin/"
	cp $< "$(DESTDIR)/$(PREFIX)/bin/"

uninstall:
	rm -f "$(DESTDIR)/$(PREFIX)/bin/$(BIN)"

clean:
	rm -fr $(OBJDIR)

clean-gen: clean
	rm -f config.h

check: $(OBJDIR)/$(BIN)
	tools/test.sh all

src:
	@echo $(SRCALL)

80:
	@for F in $(SRCALL);                       \
	do                                         \
		awk "{                             \
			gsub(/\\t/, \"        \"); \
			if (length(\$$0) > $@)     \
				printf(\"$$F:%d: %s\\n\", NR, \$$0); \
		}" < $$F;                          \
	done

.PHONY: help bedrock clean clean-gen check src 80 install uninstall
