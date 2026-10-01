import socket
import threading

# ==========================================
# 1. IMPLEMENTASI MANUAL ALGORITMA RC4
# ==========================================
def rc4_crypt(key: str, data: bytes) -> bytes:
    """Fungsi manual untuk Enkripsi dan Dekripsi menggunakan RC4"""
    key_bytes = key.encode('utf-8')
    
    # Key-Scheduling Algorithm (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
        
    # Pseudo-Random Generation Algorithm (PRGA)
    out = []
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K) # Proses XOR
        
    return bytes(out)

# ==========================================
# 2. PENGATURAN TRANSMISI & KEY
# ==========================================
PRE_SHARED_KEY = "KunciDES67" # Key sudah disepakati (Tidak dikirim!)
HOST = '127.0.0.1'
PORT = 65432

def receive_messages(conn):
    """Thread untuk menerima dan mendekripsi pesan"""
    while True:
        try:
            ciphertext = conn.recv(1024)
            if not ciphertext:
                break
            
            # Dekripsi manual
            decrypted_bytes = rc4_crypt(PRE_SHARED_KEY, ciphertext)
            plaintext = decrypted_bytes.decode('utf-8')
            
            print(f"\n[+] Ciphertext diterima (Hex): {ciphertext.hex()}")
            print(f"[Client] Pesan Asli: {plaintext}\nAnda: ", end="")
        except:
            print("\nKoneksi terputus.")
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[*] Menunggu koneksi dari Client di {HOST}:{PORT}...")
    
    conn, addr = server_socket.accept()
    print(f"[*] Terhubung dengan {addr}\n")
    
    # Jalankan thread untuk menerima pesan agar tidak memblokir input
    recv_thread = threading.Thread(target=receive_messages, args=(conn,))
    recv_thread.daemon = True
    recv_thread.start()
    
    # Main thread untuk mengirim pesan
    while True:
        pesan = input("Anda: ")
        if pesan.lower() == 'exit':
            break
            
        # Enkripsi manual
        ciphertext = rc4_crypt(PRE_SHARED_KEY, pesan.encode('utf-8'))
        conn.sendall(ciphertext)

if __name__ == "__main__":
    start_server()