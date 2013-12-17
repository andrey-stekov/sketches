#include <stdlib.h>
#include <assert.h>
#include <string.h>

#ifndef __common
#define __common

#define instance(T) (T*) malloc(sizeof(T))

#define MAX(A, B) A > B ? A : B
#define MIN(A, B) A < B ? A : B

int* int_var(int i);
int chars_comparator(void* p1, void* p2);
unsigned int chars_hash(void* p);

#endif /* __common */
