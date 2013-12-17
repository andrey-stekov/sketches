#include <stdlib.h>
#include "common.h"
#include "dbg.h"

#ifndef __slist
#define __slist

struct _slist {
    struct _slist* next;
    unsigned char type;
    void* value;
};

typedef struct _slist slist;

slist* new_slist(unsigned char type, void* value);
slist* slist_tail(slist* list);
void slist_push(slist* list, unsigned char type, void* value);
void* slist_poll(slist* list, unsigned char* type);
void slist_free(slist* list);
void slist_iterate(slist* list, void (*func)(void* value));
void slist_append(slist* head, slist* tail);

/**********************************/
/**            TESTS             **/
/**********************************/
#ifdef __TEST_SLIST

void print_int_list(slist* list) {
    printf("[");

    slist* current = list;

    while (current) {
        int* v = current->value;
        current = slist_tail(current);
        printf("%d, ", *v);
    }

    printf("]\n");
}

#define POLL_AND_PRINT \
    unsigned char t; \
    int* a = (int*) slist_poll(list, &t); \
    printf("slist->poll = %d <type=%d>\n", *a, t); \
    free(a);


int main() {
    slist* list = new_slist(7, int_var(0));

    int i;
    for (i = 1; i < 10; i++) {
        slist_push(list, 7, int_var(i));
    }

    print_int_list(list);

    while (slist_tail(list)) {
        POLL_AND_PRINT;
        print_int_list(list);
    }
    POLL_AND_PRINT;

    return 0;
}

#endif

#endif /* __slist */
