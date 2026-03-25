import socket
import threading
import os
import struct

HOST = '127.0.0.1'
PORT = 5000
FILES_DIR = "files"

os.makedirs(FILES_DIR, exist_ok=True)

def send_msg(sock, data):
    header = struct.pack(">I", len(data))
    sock.sendall(header + data)

def recv_msg(sock):
    header = sock.recv(4)
    if not header:
        return None
    length = struct.unpack(">I", header)[0]

    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            return None
        data += chunk       
    return data

# HANDLE CLIENT (THREAD)
def handle_client(conn, addr):
    print(f"[+] Client terhubung: {addr}")

    while True:
        data = recv_msg(conn)
        if not data:
            break

        msg = data.decode()
        print(f"[{addr}] Command:", msg)

        # LIST
        if msg == "/list":
            files = os.listdir(FILES_DIR)
            response = "\n".join(files) if files else "Tidak ada file"
            send_msg(conn, response.encode())

        # UPLOAD
        elif msg.startswith("/upload"):
            _, filename = msg.split()
            file_data = recv_msg(conn)

            with open(os.path.join(FILES_DIR, filename), "wb") as f:
                f.write(file_data)

            send_msg(conn, f"Upload {filename} berhasil".encode())

        # DOWNLOAD
        elif msg.startswith("/download"):
            _, filename = msg.split()
            filepath = os.path.join(FILES_DIR, filename)

            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    file_data = f.read()

                send_msg(conn, b"OK")
                send_msg(conn, file_data)
            else:
                send_msg(conn, b"ERROR")

        else:
            send_msg(conn, b"Command tidak dikenal")

    print(f"[-] Client disconnect: {addr}")
    conn.close()

# MAIN SERVER
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server THREAD jalan di {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    # bikin thread baru untuk tiap client
    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )
    client_thread.start()