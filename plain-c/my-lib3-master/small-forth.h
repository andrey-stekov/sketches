#ifndef __small_forth
#define __small_forth

#define FORTH_PUSH_NUMBER 0x00

#define FORTH_ADD 0x01
#define FORTH_SUB 0x02
#define FORTH_MUL 0x03
#define FORTH_DIV 0x04
#define FORTH_MOD 0x05

#define FORTH_SWAP 0x11
#define FORTH_DUP 0x12
#define FORTH_OVER 0x13
#define FORTH_ROT 0x14
#define FORTH_DROP 0x15

#define FORTH_LOAD 0x21
#define FORTH_STORE 0x22

struct forth_context {
    int pc;
    int sp;
    int memory_size;
    int stack_size;
    int* memory;
    int* stack;
    smap* words;
};

typedef forth_context struct forth_context;

forth_context* new_forth_context(int memory_size, int stack_size);
forth_context_free(forth_context*);

forth_context_free(forth_context*);

#endif
