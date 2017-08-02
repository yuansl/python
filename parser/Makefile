CC=gcc
CFLAGS = -g -Wall

LEX = flex
YASS = yacc
YFLAGS = -d
LDLIBS = -lfl -lm
LDFLAGS = -L.

OBJS = calc.c  y.tab.o y.tab.c 

all: calc

calc: calc-lex.o y.tab.o
	$(CC) $(CFLAGS) -o $@ calc-lex.o y.tab.o $(LDLIBS)

calc-lex.c: y.tab.h calc-lex.l
	$(LEX) -o $@ calc-lex.l

y.tab.c y.tab.h: calc-grammar.y
	$(YACC) $(YFLAGS) calc-grammar.y

.PHONY: clean

clean:
	$(RM) $(OBJS)
