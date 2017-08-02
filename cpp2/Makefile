CC=gcc
CFLAGS= -g -Wall
CPPFLAGS = -I$(HOME)/lib -DDEBUG_RELEASE2
LDFLAGS = -L$(HOME)/lib
LDLIBS = -lutil1

RM=rm -f

OBJS = ident.o token.o comment.o
PROGRAM = token
all: $(PROGRAM)

token: main.o token.o comment.o preprocessor.o macro.o
	$(CC) $(CFLAGS) -o $@ main.o token.o comment.o preprocessor.o macro.o $(LDFLAGS) $(LDLIBS)

.PHONY: clean
clean:
	$(RM) $(OBJS)
