import socket
import threading

# ==========================================
# 1. IMPLEMENTASI MANUAL ALGORITMA RC4
# ==========================================
def rc4_crypt(key: str, data: bytes) -> bytes:
    """Fungsi manual untuk Enkripsi dan Dekripsi menggunakan RC4"""
    key_bytes = key.encode('utf-8')
    
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
        
    out = []
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)
        
    return bytes(out)

# ==========================================
# 2. PENGATURAN TRANSMISI & KEY
# ==========================================
PRE_SHARED_KEY = "KunciDES67" # Harus sama dengan Server
HOST = '127.0.0.1'
PORT = 65432

def receive_messages(client_socket):
    """Thread untuk menerima dan mendekripsi pesan"""
    while True:
        try:
            ciphertext = client_socket.recv(1024)
            if not ciphertext:
                break
                
            # Dekripsi manual
            decrypted_bytes = rc4_crypt(PRE_SHARED_KEY, ciphertext)
            plaintext = decrypted_bytes.decode('utf-8')
            
            print(f"\n[+] Ciphertext diterima (Hex): {ciphertext.hex()}")
            print(f"[Server] Pesan Asli: {plaintext}\nAnda: ", end="")
        except:
            print("\nKoneksi terputus dari server.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("[*] Berhasil terhubung ke Server!\n")
    
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()
    
    while True:
        pesan = input("Anda: ")
        if pesan.lower() == 'exit':
            break
            
        # Enkripsi manual
        ciphertext = rc4_crypt(PRE_SHARED_KEY, pesan.encode('utf-8'))
        client_socket.sendall(ciphertext)

if __name__ == "__main__":
    start_client()