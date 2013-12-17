#include "smap.h"

smap* new_smap(unsigned short buckets_count, int (*key_comparator)(void*, void*), unsigned int (*hash_func)(void*)) {
    smap* map = instance(smap);
    map->size = 0;
    map->buckets_count = buckets_count;
    map->buckets = calloc(buckets_count, sizeof(slist*));
    map->key_comparator = key_comparator;
    map->hash_func = hash_func;

    int i;
    for (i = 0; i < buckets_count; i++) {
        map->buckets[i] = NULL;
    }

    return map;
}

void smap_put(smap* map, void* key, void* value) {
    smap_node* node = __smap_get_node(map, key);

    if (!node) {
        unsigned int ind = __smap_get_bucket_index(map, key);
        node = instance(smap_node);
        node->key = key;
        node->value = value;

        if (map->buckets[ind]) {
            slist* new_node = new_slist(__SMAP_NODE_TYPE, node);
            slist_append(new_node, map->buckets[ind]);
            map->buckets[ind] = new_node;
            //slist_push(map->buckets[ind], __SMAP_NODE_TYPE, node);
        } else {
            map->buckets[ind] = new_slist(__SMAP_NODE_TYPE, node);
        }
    } else {
        node->value = value;
    }
}

void* smap_get(smap* map, void* key) {
    smap_node* node = __smap_get_node(map, key);
    return node->value;
}

void smap_rem(smap* map, void* key) {
    smap_node* node = __smap_get_node(map, key);
    void* p = node->value;
    node->value = NULL;
    map->size--;
    free(p);
}

void smap_free(smap* map) {
    int i;
    for (i = 0; i < map->buckets_count; i++) {
        if (map->buckets[i]) {
            slist_iterate(map->buckets[i], &__smap_free_node);
            slist_free(map->buckets[i]);
        }
    }
    free(map->buckets);
    free(map);
}

unsigned int __smap_get_bucket_index(smap* map, void* key) {
    unsigned int hash = map->hash_func(key);
    return hash % map->buckets_count;
}

smap_node* __smap_get_node(smap* map, void* key) {
    slist* bucket = map->buckets[__smap_get_bucket_index(map, key)];
    while (bucket) {
        assert(bucket->value);
        smap_node* node = bucket->value;
        bucket = slist_tail(bucket);
        if (map->key_comparator(node->key, key)) {
            return node;
        }
    }
    return NULL;
}

void __smap_free_node(void* p) {
    smap_node* node = (smap_node*) p;
    free(node->key);
    free(node->value);
}

