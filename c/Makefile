#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void print_usage(const char *program_name) {
    printf("Usage:\n");
    printf("  %s <file>\n", program_name);
}

static int compute_sha256_file(const char *path, char output[65]) {
    FILE *fp = fopen(path, "rb");
    unsigned char buffer[4096];
    unsigned char digest[32];
    unsigned int h[8] = {
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    };
    unsigned int k[64] = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befff a, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    };
    unsigned char data[64];
    unsigned long long bitlen = 0;
    size_t datalen = 0;
    size_t i;
    size_t bytes_read;

    if (fp == NULL) {
        return 0;
    }

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), fp)) > 0) {
        for (i = 0; i < bytes_read; ++i) {
            data[datalen++] = buffer[i];
            if (datalen == 64) {
                unsigned int a, b, c, d, e, f, g, gg;
                unsigned int m[64];
                unsigned int t1, t2;
                for (int j = 0; j < 16; ++j) {
                    m[j] = ((unsigned int)data[j * 4] << 24) |
                           ((unsigned int)data[j * 4 + 1] << 16) |
                           ((unsigned int)data[j * 4 + 2] << 8) |
                           ((unsigned int)data[j * 4 + 3]);
                }
                for (int j = 16; j < 64; ++j) {
                    unsigned int s0 = ((m[j - 15] >> 7) | (m[j - 15] << 25)) ^ ((m[j - 15] >> 18) | (m[j - 15] << 14)) ^ (m[j - 15] >> 3);
                    unsigned int s1 = ((m[j - 2] >> 17) | (m[j - 2] << 15)) ^ ((m[j - 2] >> 19) | (m[j - 2] << 13)) ^ (m[j - 2] >> 10);
                    m[j] = m[j - 16] + s0 + m[j - 7] + s1;
                }
                a = h[0]; b = h[1]; c = h[2]; d = h[3]; e = h[4]; f = h[5]; gg = h[6]; unsigned int hh = h[7];
                for (int j = 0; j < 64; ++j) {
                    unsigned int S1 = ((e >> 6) | (e << 26)) ^ ((e >> 11) | (e << 21)) ^ ((e >> 25) | (e << 7));
                    unsigned int ch = (e & f) ^ ((~e) & gg);
                    unsigned int temp1 = hh + S1 + ch + k[j] + m[j];
                    unsigned int S0 = ((a >> 2) | (a << 30)) ^ ((a >> 13) | (a << 19)) ^ ((a >> 22) | (a << 10));
                    unsigned int maj = (a & b) ^ (a & c) ^ (b & c);
                    unsigned int temp2 = S0 + maj;
                    hh = gg;
                    gg = f;
                    f = e;
                    e = d + temp1;
                    d = c;
                    c = b;
                    b = a;
                    a = temp1 + temp2;
                }
                h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += gg; h[7] += hh;
                datalen = 0;
                bitlen += 512;
            }
        }
    }

    bitlen += (unsigned long long)datalen * 8;
    data[datalen++] = 0x80;
    if (datalen > 56) {
        while (datalen < 64) {
            data[datalen++] = 0;
        }
        datalen = 0;
    }
    while (datalen < 56) {
        data[datalen++] = 0;
    }
    for (i = 0; i < 8; ++i) {
        data[56 + i] = (unsigned char)(bitlen >> (8 * (7 - i)));
    }

    {
        unsigned int a, b, c, d, e, f, g, gg;
        unsigned int m[64];
        unsigned int t1, t2;
        for (int j = 0; j < 16; ++j) {
            m[j] = ((unsigned int)data[j * 4] << 24) |
                   ((unsigned int)data[j * 4 + 1] << 16) |
                   ((unsigned int)data[j * 4 + 2] << 8) |
                   ((unsigned int)data[j * 4 + 3]);
        }
        for (int j = 16; j < 64; ++j) {
            unsigned int s0 = ((m[j - 15] >> 7) | (m[j - 15] << 25)) ^ ((m[j - 15] >> 18) | (m[j - 15] << 14)) ^ (m[j - 15] >> 3);
            unsigned int s1 = ((m[j - 2] >> 17) | (m[j - 2] << 15)) ^ ((m[j - 2] >> 19) | (m[j - 2] << 13)) ^ (m[j - 2] >> 10);
            m[j] = m[j - 16] + s0 + m[j - 7] + s1;
        }
        a = h[0]; b = h[1]; c = h[2]; d = h[3]; e = h[4]; f = h[5]; g = h[6]; gg = h[7];
        for (int j = 0; j < 64; ++j) {
            unsigned int S1 = ((e >> 6) | (e << 26)) ^ ((e >> 11) | (e << 21)) ^ ((e >> 25) | (e << 7));
            unsigned int ch = (e & f) ^ ((~e) & g);
            unsigned int temp1 = gg + S1 + ch + k[j] + m[j];
            unsigned int S0 = ((a >> 2) | (a << 30)) ^ ((a >> 13) | (a << 19)) ^ ((a >> 22) | (a << 10));
            unsigned int maj = (a & b) ^ (a & c) ^ (b & c);
            unsigned int temp2 = S0 + maj;
            gg = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }
        h[0] += a; h[1] += b; h[2] += c; h[3] += d; h[4] += e; h[5] += f; h[6] += g; h[7] += gg;
    }

    for (i = 0; i < 8; ++i) {
        digest[i * 4] = (unsigned char)((h[i] >> 24) & 0xffu);
        digest[i * 4 + 1] = (unsigned char)((h[i] >> 16) & 0xffu);
        digest[i * 4 + 2] = (unsigned char)((h[i] >> 8) & 0xffu);
        digest[i * 4 + 3] = (unsigned char)(h[i] & 0xffu);
    }

    for (i = 0; i < 32; ++i) {
        static const char *hex = "0123456789abcdef";
        output[i * 2] = hex[(digest[i] >> 4) & 0x0f];
        output[i * 2 + 1] = hex[digest[i] & 0x0f];
    }
    output[64] = '\0';
    fclose(fp);
    return 1;
}

int main(int argc, char **argv) {
    char digest[65];

    if (argc != 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (!compute_sha256_file(argv[1], digest)) {
        fprintf(stderr, "Unable to hash file: %s\n", argv[1]);
        return 1;
    }

    printf("%s  %s\n", digest, argv[1]);
    return 0;
}
