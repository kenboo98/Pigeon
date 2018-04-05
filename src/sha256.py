import hashlib
def ch(x,y,z):
    return ((x&y)^(~x&z))&0xFFFFFFFF

def maj(x,y,z):
    return ((x&y)^(x&z)^(y&z))&0xFFFFFFFF
#rotate right 32 bit number by n
def rotr(x,n):
    #bit shift right n times
    return ((x>>n) | (x<<(32-n)))&0xFFFFFFFF


def sigma0(x):
    return (rotr(x,2)^rotr(x,13)^rotr(x,22))&0xFFFFFFFF
 
def sigma1(x):
    return (rotr(x,6)^rotr(x,11)^rotr(x,25))&0xFFFFFFFF

def omega0(x):
    return (rotr(x,7)^rotr(x,18)^(x>>3))&0xFFFFFFFF

def omega1(x):
    return (rotr(x,17)^rotr(x,19)^(x>>10))&0xFFFFFFFF
'''
x - list of 4, 8 bit numbers
returns - 32bit integer
'''
def concat_8_to_32(x):
    return ((x[0]<<24)|(x[1]<<16)|(x[2]<<8)|x[3])&0xFFFFFFFF

class Hasher():
    k_vals = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

    def __init__(self, message):
        self.message = message
        self.padded = self.pad_message(message)
        print(self.padded)
        self.hash = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
        self.n_blocks = len(self.padded)//64
        for i in range(self.n_blocks):
            self.compute_hash(self.message_schedule(self.padded[i*64:(i+1)*64]))
        
    
    '''
    original - original message to pad. Only accepts normal ascii strings
    padded - array of 8 bit integeres. length is multiple of 64(512bits)
    '''
    def pad_message(self,original):
        padded = list()
        l = len(original)*8
        k = 448 - (l%512)
        if k<0:
            k = (k + 512)      
        for letter in original:
            padded.append(ord(letter))
        padded.append(0x80)
        for _ in range(int(k/8-1)):
            padded.append(0x00)
        #pad with 64 bits of l
        for i in range(7,-1,-1):
            padded.append((l>>(i*8))&0xFF)
        return padded
    '''
    block - array of size 64 with 8 bit integers. 512 bits today
    returns - ms, an array of 64, 32 integers. 
    '''
    def message_schedule(self,block):
        ms = [None]*64
        for i in range(16):
            ms[i] = concat_8_to_32(block[i*4:(i+1)*4])
        for i in range(16,64):
            ms[i] = (omega1(ms[i-2])+ms[i-7]+omega0(ms[i-15])+ms[i-16])%0x100000000
        return ms
    '''
    The actual hashing algorithm. Takes in a single message schedule and sets the new hash
    '''
    def compute_hash(self, message_schedule):
        working_vars = self.hash
        for i in range(len(message_schedule)):
            T1 = (working_vars[7]+sigma1(working_vars[4])+ch(working_vars[4],working_vars[5],working_vars[6])+Hasher.k_vals[i]+message_schedule[i])%0x100000000
            T2 = (sigma0(working_vars[0])+maj(working_vars[0],working_vars[1],working_vars[2]))%0x100000000
            working_vars[7] = self.hash[6]
            working_vars[6] = self.hash[5]
            working_vars[5] = self.hash[4]
            working_vars[4] = (self.hash[3] + T1)%0x100000000
            working_vars[3] = self.hash[2]
            working_vars[2] = self.hash[1]
            working_vars[1] = self.hash[0]
            working_vars[0] = (T1+T2)%0x100000000
        #set the new hashes
        for i in range(len(self.hash)):
           self.hash[i] = (working_vars[i] + self.hash[i])%0x100000000


    def get_hash_string(self):
        hash_string = ""
        for hash in self.hash:
            hash_string += hex(hash)[2:len(hex(hash))]
        return hash_string

#test 
if __name__ == "__main__":

    test = "amir"
    hasher = Hasher(test)
    correct_hasher = hashlib.sha256()
    correct_hasher.update(test)
    print(hasher.get_hash_string)
    print(hex(correct_hasher.hexdigest()))




    



    
       
        