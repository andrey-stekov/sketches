#include "slist.h"

slist* new_slist(unsigned char type, void* value) {
    slist* list = instance(slist);
    list->type = type;
    list->value = value;
    list->next = NULL;
    return list;
}

slist* slist_tail(slist* list) {
    assert(list);
    return list->next;
}

void slist_push(slist* list, unsigned char type, void* value) {
    assert(list);
    slist* current = list;
    while (current->next) { current = current->next; }
    current->next = new_slist(type, value);
}

void* slist_poll(slist* list, unsigned char* type) {
    assert(list);

    slist* prev = NULL;
    slist* current = list;
    while (current->next) {
        prev = current;
        current = current->next;
    }

    if (prev != NULL) {
        prev->next = NULL;
    }

    *type = current->type;
    void* val = current->value;
    free(current);
    return val;
}

void slist_free(slist* list) {
    assert(list);
    free(list->value);

    if (list->next)
        slist_free(list->next);
    free(list);
}

void slist_iterate(slist* list, void (*func)(void* value)) {
    assert(list);
    slist* current = list;

    while (current) {
        func(current->value);
        current = current->next;
    }
}

void slist_append(slist* head, slist* tail) {
    assert(head);
    assert(tail);

    slist* prev = NULL;
    slist* current = head;

    while (current) {
        prev = current;
        current = current->next;
    }

    prev->next = tail;
}
