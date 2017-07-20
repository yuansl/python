CC=gcc

CFLAGS= -g -Wall
AR = ar
ARFLAGS = rvs
RANLIB = ranlib
RM=rm -f

OBJS = comm_util.o
ARCHIVE = libutil1.a

all: $(ARCHIVE)

$(ARCHIVE): comm_util.o
	$(AR) $(ARFLAGS) $@ comm_util.o

.PHONY: clean
clean:
	$(RM) $(OBJS)
