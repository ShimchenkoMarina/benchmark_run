#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define CACHE_SIZE_MB 30


int main() {
    #pragma omp parallel
    {
        volatile const size_t size = CACHE_SIZE_MB*1024*1024;
        int i, j;
        char *c = malloc(size);
        for (i = 0; i < 5; i++)
            for (j = 0; j < size; j++)
                c[j] = i*j;
    }
}

