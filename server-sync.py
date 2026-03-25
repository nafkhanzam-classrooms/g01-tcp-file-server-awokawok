import socket
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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server jalan di {HOST}:{PORT}")

conn, addr = server.accept()
print("Terhubung ke", addr)

while True:
    data = recv_msg(conn)
    if not data:
        break

    msg = data.decode()

    print("Command:", msg)

    # LIST FILE
    if msg == "/list":
        files = os.listdir(FILES_DIR)
        response = "\n".join(files) if files else "Tidak ada file"
        send_msg(conn, response.encode())

    # UPLOAD FILE
    elif msg.startswith("/upload"):
        _, filename = msg.split()

        file_data = recv_msg(conn)

        with open(os.path.join(FILES_DIR, filename), "wb") as f:
            f.write(file_data)

        send_msg(conn, f"Upload {filename} berhasil".encode())

    # DOWNLOAD FILE
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
        send_msg(conn, b"Command tidak diketahui")

conn.close()
server.close()