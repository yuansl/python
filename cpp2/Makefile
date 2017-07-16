CC=gcc
CFLAGS= -g -Wall
CPPFLAGS = -I$(HOME)/lib -DDEBUG_RELEASE2
LDFLAGS = -L$(HOME)/lib
LDLIBS = -lutil1

RM=rm -f

OBJS = ident.o token.o

all: token

token: token.o
	$(CC) $(CFLAGS) -o $@ token.o $(LDFLAGS) $(LDLIBS)

.PHONY: clean
clean:
	$(RM) $(OBJS)
