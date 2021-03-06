'''
    The following is a SHA 256 implementation by Kenta Tellambura and Danish Dua

    Based on the official NIST (National instiute of Standards
    and Technology) publication:
    https://csrc.nist.gov/csrc/media/publications/fips/180/4/final/documents/fips180-4-draft-aug2014.pdf

    Publication No: FIPS 180-4

    Usage:
        - Initilize a SHA256 object with string to be hashed as argument
        - hexdigest to get the hash string in hex format
'''


'''
    Functions defined in SHA standards:
'''

def ch(x,y,z):
    return ((x & y) ^ (~x & z)) & 0xFFFFFFFF

def maj(x,y,z):
    return ((x & y) ^(x & z) ^ (y & z)) & 0xFFFFFFFF

def rotr(x,n):
    return ((x >> n) | (x << (32-n))) & 0xFFFFFFFF

def sigma0(x):
    return (rotr(x,2) ^ rotr(x,13) ^rotr(x,22)) & 0xFFFFFFFF

def sigma1(x):
    return (rotr(x,6) ^ rotr(x,11) ^ rotr(x,25)) & 0xFFFFFFFF

def omega0(x):
    return (rotr(x,7) ^ rotr(x,18) ^ (x>>3)) & 0xFFFFFFFF

def omega1(x):
    return (rotr(x,17) ^ rotr(x,19)^ (x>>10)) & 0xFFFFFFFFFFF

'''
    Helper functions
'''

def concat_8_to_32(x):
    '''
        x - list of 4, 8 bit numbers
        returns - 32bit integer
    '''
    return ((x[0]<<24)|(x[1]<<16)|(x[2]<<8)|x[3])&0xFFFFFFFF

'''
    SHA 256 constants
'''
k_vals = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

'''
    Actual Hashing algorithm
'''

class SHA256():
    """
        SHA256 class generates the hash

        Usage:
            sha256hash = SHA256("string").hexdigest()
    """

    def __init__(self, message):
        self._update(message)

    def _update(self, message):
        '''
            Calculates the initial hash by appending to the message
            Args:
                message - to initialize the string to be hashed as a class var
        '''
        if type(message) != str:
            raise TypeError

        try:
            self.message += message
        except AttributeError:
            self.message = message

        self.hash = [0x6a09e667, 0xbb67ae85, 0x3c6ef372 ,0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

        self.padded = self._pad_message(self.message)
        self.n_blocks = len(self.padded)//64

        for i in range(self.n_blocks):
            self._compute_hash(self._message_schedule(self.padded[i*64:(i+1)*64]))


    def _pad_message(self, original):
        '''
            Pads the initial string to be hashed to a multiple of 512 bits in size
            Args:
                original - original string to be padded to a block size (512 bits)
            Returns:
                padded - original string padded to a block size (512 bits) as 8 bit integer array
        '''
        padded = list()

        l = len(original)*8
        k = 448 - (l % 512)

        if k < 0:
            k += 512

        for letter in original:
            padded.append(ord(letter))

        padded.append(0x80)

        for _ in range(int(k/8 - 1)):
            padded.append(0x00)

        # pad with 64 bits of l
        for i in range(7,-1,-1):
            padded.append((l>>(i*8)) & 0xFF)

        return padded

    def _message_schedule(self, block):
        '''
            Prepares messge block to be hashed
            Args:
                block - 512 bit block as an array of 64 8-bit integers
            Returns:
                ms - An array of 64 32-bit integers scheduled to be processed
                    according to the NISP standard algorithm
        '''
        ms = [None]*64

        for i in range(16):
            ms[i] = concat_8_to_32(block[i*4:(i+1)*4])

        for i in range(16,64):
            ms[i] = (omega1(ms[i-2]) + ms[i-7] + omega0(ms[i-15]) + ms[i-16]) % 0x100000000

        return ms

    def _compute_hash(self, message_schedule):
        '''
            Hashing algorithm (hashing rounds based on message_schedule)
            Args:
                message_schedule - An array of 64 32-bit integers scheduled to be processed
                    according to the NISP standard algorithm
        '''
        a,b,c,d,e,f,g,h = self.hash

        for i in range(len(message_schedule)):
            t1 = h + sigma1(e) + ch(e,f,g) + k_vals[i] + message_schedule[i]
            t2 = sigma0(a) + maj(a,b,c)
            h = g
            g = f
            f = e
            e = (d + t1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xFFFFFFFF

        # set the new hashes
        working_vars = [a,b,c,d,e,f,g,h]

        for i in range(len(self.hash)):
           self.hash[i] = (working_vars[i] + self.hash[i]) & 0xFFFFFFFF

    def hexdigest(self):
        '''
            Converts the final hash to hexadecimal string
            Returns:
                hash_string - hex of the hash as a string
        '''
        hash_string = ""

        for hash in self.hash:
            hash_string += hex(hash)[2:len(hex(hash))]

        return hash_string

# for testing 
if __name__ == "__main__":
    print(SHA256("root").hexdigest())
