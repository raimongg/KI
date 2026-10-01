# ========================================================
# IMPLEMENTASI MANUAL DES (DATA ENCRYPTION STANDARD)
# Tidak menggunakan library cryptography apapun.
# ========================================================

# --- TABEL PERMUTASI DES ---
# Initial Permutation (IP)
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (IP-1)
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

# Expansion Table (E)
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

# Permutation Table (P)
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]

# S-BOXES (8 buah, masing-masing 4x16)
S_BOX = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

# PC1, PC2, Shift Tabel untuk Key Generation
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# --- FUNGSI PEMBANTU (HELPERS) ---
def string_to_bits(s):
    return "".join(f"{byte:08b}" for byte in s)

def bytes_to_bits(b):
    return "".join(f"{byte:08b}" for byte in b)

def bits_to_bytes(bits):
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

def xor(b1, b2):
    return "".join("1" if bit1 != bit2 else "0" for bit1, bit2 in zip(b1, b2))

def permute(block, table):
    return "".join(block[i - 1] for i in table)

# --- KEY SCHEDULE (GENERATE 16 SUBKEYS) ---
def generate_keys(key):
    # Pastikan key 8 bytes (64 bits)
    key = (key + b'\0'*8)[:8]
    key_bits = bytes_to_bits(key)
    
    # PC-1
    key_bits = permute(key_bits, PC1)
    L, R = key_bits[:28], key_bits[28:]
    
    subkeys = []
    for shift in SHIFTS:
        # Left Shift
        L = L[shift:] + L[:shift]
        R = R[shift:] + R[:shift]
        # PC-2
        subkeys.append(permute(L + R, PC2))
    return subkeys

# --- PROSES SATU BLOK (64-BIT) ---
def des_block(block_bits, subkeys, is_decrypt=False):
    # 1. Initial Permutation
    block = permute(block_bits, IP)
    L, R = block[:32], block[32:]
    
    # Balik urutan subkey jika dekripsi
    keys = reversed(subkeys) if is_decrypt else subkeys
    
    # 2. 16 Rounds Feistel
    for key in keys:
        # Expansion
        exp_R = permute(R, E)
        # XOR dengan Subkey
        xor_R = xor(exp_R, key)
        
        # S-Box Substitution
        sbox_out = ""
        for i in range(8):
            chunk = xor_R[i*6:(i+1)*6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            val = S_BOX[i][row][col]
            sbox_out += f"{val:04b}"
            
        # P-Box Permutation
        f_res = permute(sbox_out, P)
        
        # XOR dengan L dan Swap
        new_R = xor(L, f_res)
        L = R
        R = new_R
        
    # 3. Final Permutation (IP-1) - Swap terakhir dibatalkan
    return permute(R + L, IP_INV)

# --- PKCS7 PADDING UNTUK BLOCK CIPHER ---
def pad(data_bytes):
    padding_len = 8 - (len(data_bytes) % 8)
    return data_bytes + bytes([padding_len] * padding_len)

def unpad(data_bytes):
    padding_len = data_bytes[-1]
    return data_bytes[:-padding_len]

# --- FUNGSI UTAMA ENKRIPSI & DEKRIPSI ---
def des_encrypt(key_bytes, plaintext_bytes):
    subkeys = generate_keys(key_bytes)
    padded = pad(plaintext_bytes)
    bits = bytes_to_bits(padded)
    
    cipher_bits = ""
    # Proses per 64-bit (8 bytes = 64 bits karakter '1'/'0')
    for i in range(0, len(bits), 64):
        block = bits[i:i+64]
        cipher_bits += des_block(block, subkeys, is_decrypt=False)
        
    return bits_to_bytes(cipher_bits)

def des_decrypt(key_bytes, ciphertext_bytes):
    subkeys = generate_keys(key_bytes)
    bits = bytes_to_bits(ciphertext_bytes)
    
    plain_bits = ""
    for i in range(0, len(bits), 64):
        block = bits[i:i+64]
        plain_bits += des_block(block, subkeys, is_decrypt=True)
        
    padded_plain = bits_to_bytes(plain_bits)
    return unpad(padded_plain)