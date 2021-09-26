#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

// Sabantuy{0h_1t_d035n7_s33m_v3ry_3d1bl3}
char flag[64];
uint8_t menu[] = "pancakes_berries_chocolate_milk_waffles_cupcakes_croissants\x00";
uint8_t correct_rc4_enc[] = {36, 149, 127, 252, 213, 205, 108, 230, 173, 52, 59, 81, 50, 209, 232, 165, 178, 40, 220, 46, 171, 253, 236, 168, 154, 138, 64, 120, 33, 13, 13, 97, 98, 16, 115, 42, 13, 118, 109};

void setup(void);
void swap(unsigned char *a, unsigned char *b);
int KSA(char *key, unsigned char *S);
int PRGA(unsigned char *S, char *plaintext, unsigned char *ciphertext);
int RC4(char *key, char *plaintext, unsigned char *ciphertext);

int main() {
    setup();
    puts("+++++***** I'm FlagEater +++++*****");
    puts("+++++***** I eat all flags +++++*****");

    printf("{?} Do you have something for me? ");
    int nbytes = read(0, flag, 40);

    if (flag[nbytes - 1] == '\n') {
        flag[nbytes - 1] = '\0';
    }

    uint32_t FlagSize = strlen(flag);

    // check flag size and format
    if (FlagSize != 39) {
        puts("{-} I don't like that, thanks.");
        return -1;
    }

    if (strncmp(flag, "Sabantuy{", 9) != 0) {
        puts("{-} This is not my type!");
        return -1;
    }

    if (flag[strlen(flag)-1] != '}') {
        puts("{-} I don't want to eat this!");
        return -1;
    }

    uint32_t OutEncSize = strlen(flag);
    uint8_t* EncFlag = (uint8_t*) malloc(OutEncSize);
    memset(EncFlag, 0x0, OutEncSize);

    RC4(menu, flag, EncFlag);

    if (!memcmp(EncFlag, correct_rc4_enc, strlen(flag))) {
        puts("{+} So tasty!!");
        puts("Ohh..");
        puts("I think I'm about to burst");
        puts("***BOOOOOOOM***");
        return 0;
    } else {
        puts("{+} So tasty!!");
        return -1;
    }
    
    return 0;
};

void setup(void) {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);
};

#define N 256   // 2^8

void swap(unsigned char *a, unsigned char *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
};
int KSA(char *key, unsigned char *S) {

    int len = strlen(key);
    int j = 0;

    for(int i = 0; i < N; i++)
        S[i] = i;

    for(int i = 0; i < N; i++) {
        j = (j + S[i] + key[i % len]) % N;

        swap(&S[i], &S[j]);
    }

    return 0;
};
int PRGA(unsigned char *S, char *plaintext, unsigned char *ciphertext) {

    int i = 0;
    int j = 0;

    for(size_t n = 0, len = strlen(plaintext); n < len; n++) {
        i = (i + 1) % N;
        j = (j + S[i]) % N;

        swap(&S[i], &S[j]);
        int rnd = S[(S[i] + S[j]) % N];

        ciphertext[n] = rnd ^ plaintext[n];

    }

    return 0;
}
int RC4(char *key, char *plaintext, unsigned char *ciphertext) {
    unsigned char S[N];
    KSA(key, S);
    PRGA(S, plaintext, ciphertext);
    return 0;
};
