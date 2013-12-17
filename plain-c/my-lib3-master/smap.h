#include "common.h"
#include "slist.h"

#ifndef __smap
#define __smap

#define SMAP_DEFAULT_BUCKETS_COUNT 64
#define __SMAP_NODE_TYPE 7

struct _smap {
    unsigned short buckets_count;
    unsigned int size;
    slist** buckets;
    int (*key_comparator)(void*, void*);
    unsigned int (*hash_func)(void*);
};

typedef struct _smap smap;

struct _smap_node {
    void* key;
    void* value;
};

typedef struct _smap_node smap_node;

smap* new_smap(unsigned short buckets_count, int (*key_comparator)(void*, void*), unsigned int (*hash_func)(void*));
void smap_put(smap* map, void* key, void* value);
void* smap_get(smap* map, void* key);
void smap_rem(smap* map, void* key);
void smap_free(smap* map);
unsigned int __smap_get_bucket_index(smap* map, void* key);
smap_node* __smap_get_node(smap* map, void* key);
void __smap_free_node(void* node);

#define new_smapd(key_comparator, hash_func) new_smap(SMAP_DEFAULT_BUCKETS_COUNT, key_comparator, hash_func)


/**********************************/
/**            TESTS             **/
/**********************************/

#ifdef __TEST_SMAP

char* new_key(int i) {
    char* p = malloc(7);
    sprintf(p, "key #%d", i);
    return p;
}

void print_map(smap* map) {
    printf("\n============================\n");

    int i;
    for (i = 0; i < 10; i++) {
        char* key = new_key(i);
        int* a = smap_get(map, key);
        if (a) {
            printf("%s => %d\n", key, *a);
        } else {
            printf("%s => NULL\n", key);
        }
        free(key);
    }

    printf("\n============================\n");
}

int main() {
    smap* map = new_smapd(&chars_comparator, &chars_hash);

    int i;
    for (i = 0; i < 10; i++) {
        smap_put(map, new_key(i), int_var(i));
    }

    print_map(map);

    char* key = new_key(4);
    smap_rem(map, key);
    free(key);
    print_map(map);

    smap_free(map);

    return 0;
}

#endif

#endif /* __smap */
