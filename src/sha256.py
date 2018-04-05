"""
    SHA256 implementation based on the official NIST (National instiute of Standards
    and Technology) publication:
    https://csrc.nist.gov/csrc/media/publications/fips/180/4/final/documents/fips180-4-draft-aug2014.pdf

    Publication No: FIPS 180-4

"""

# bit constants (standard)
BLOCK_SIZE = 512
WORD_SIZE = 32
DIGEST_SIZE = 256

SHA256_PRIMES =
[
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

SHA256_INITS = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

# SHA256 functions
def Ch(x, y, z):
    return (x & y) ^ (~x & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def ROTR(x, n):
    return (x >> n) | (x << WORD_SIZE - n)

def ROTL(x, n):
    return ROTR(x, WORD_SIZE - n)

def SHR(x, n):
    return (x >> n)

def SIGMA0(x):
    return ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)

def SIGMA1(x):
    return ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)

def GAMMA0(x):
    return ROTR(x, 7) ^ ROTR(x, 18) ^ SHR(x, 3)

def GAMMA1(x):
    return ROTR(x, 17) ^ ROTR(x, 19) ^ ROTR(x, 10)

# helper function for scheduling, by @kenboo98
def concat_8_to_32(x):
    return ((x[0]<<24) | (x[1]<<16) | (x[2]<<8) | x[3]) & 0xFFFFFFFF

def SHA256(string):

    buffer = buffer(str(string)) # if the string was unicode
    length = len(buffer)
    num_bytes = (len/8) & 0xffffffff

    [a, b, c, d, e, f, g, h] = SHA256_INITS

    i = 0
    while length >= BLOCK_SIZE/8:
        data = [ord(char) for char in buffer[i:(i+BLOCK_SIZE/8)]]

        len -= BLOCK_SIZE/8
        i += BLOCK_SIZE/8

        w = []
        for i in range(16):
            w[i] = concat_8_to_32(data[i*4:(i+1)*4])
        for i in range(16, 64):
            w[i] = (SIGMA1(w[i - 2]) + w[i - 7] + SIGMA0(w[i - 15]) + w[i - 16]) & 0xffffffff
