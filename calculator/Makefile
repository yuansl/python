CC=gcc
CFLAGS = -g -Wall

LEX = flex
YACC = bison
YFLAGS = -d -l
LDLIBS = -lfl -lm
LDFLAGS = -L.

OBJS =  *.tab.[ch] calc-lex.c *.o
PROGRAM = calc

all: $(PROGRAM)

calc: calc-lex.o calc-grammar.tab.o main.o
	$(CC) $(CFLAGS) -o $@ main.o calc-lex.o calc-grammar.tab.o $(LDLIBS)

calc-lex.c: calc-grammar.tab.h calc-lex.l
	$(LEX) -o $@ calc-lex.l

calc-grammar.tab.c calc-grammar.tab.h: calc-grammar.y
	$(YACC) $(YFLAGS) calc-grammar.y

.PHONY: clean

clean:
	$(RM) $(OBJS) $(PROGRAM)
