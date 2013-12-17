#include "common.h"

int* int_var(int i) {
    int* p = instance(int);
    *p = i;
    return p;
}

int chars_comparator(void* p1, void* p2) {
    char* str1 = (char*) p1;
    char* str2 = (char*) p2;
    int len1 = strlen(str1);
    int len2 = strlen(str2);
    int len = len1 < len2 ? len1 : len2;
    int i;
    int r;
    for (i = 0; i < len1; i++) {
        r = str1[i] - str2[i];
        if (r != 0) {
            return r;
        }
    }
    return len1 == len ? -1 : len2 == len ? 0 : 1;
}

unsigned int chars_hash(void* p) {
    char* str = (char*) p;
    unsigned int h = 0;
    int len = strlen(str);
    int i;
    for (i = 0; i < len; i++) {
        h = 31*h + str[i];
    }
    return h;
}

