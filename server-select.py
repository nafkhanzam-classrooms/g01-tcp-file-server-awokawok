import socket
import select
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
    try:
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
    except:
        return None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)

inputs = [server]
client_states = {}  # STATE PER CLIENT

print(f"Server SELECT jalan di {HOST}:{PORT}")

while True:
    readable, _, _ = select.select(inputs, [], [])

    for sock in readable:
        if sock == server:
            conn, addr = server.accept()
            conn.setblocking(False)
            inputs.append(conn)
            print(f"[+] Client terhubung: {addr}")

        else:
            data = recv_msg(sock)

            if not data:
                print("[-] Client disconnect")
                inputs.remove(sock)
                client_states.pop(sock, None)
                sock.close()
                continue

            # 🔥 CEK STATE DULU
            state = client_states.get(sock)

            if state and state["mode"] == "upload":
                filename = state["filename"]

                with open(os.path.join(FILES_DIR, filename), "wb") as f:
                    f.write(data)

                send_msg(sock, f"Upload {filename} berhasil".encode())
                del client_states[sock]
                continue

            msg = data.decode()
            print("Command:", msg)

            # LIST
            if msg == "/list":
                files = os.listdir(FILES_DIR)
                response = "\n".join(files) if files else "Tidak ada file"
                send_msg(sock, response.encode())

            # UPLOAD (SET STATE)
            elif msg.startswith("/upload"):
                try:
                    _, filename = msg.split()
                    client_states[sock] = {
                        "mode": "upload",
                        "filename": filename
                    }
                except:
                    send_msg(sock, b"Format salah")

            # DOWNLOAD
            elif msg.startswith("/download"):
                try:
                    _, filename = msg.split()
                    filepath = os.path.join(FILES_DIR, filename)

                    if os.path.exists(filepath):
                        with open(filepath, "rb") as f:
                            file_data = f.read()

                        send_msg(sock, b"OK")
                        send_msg(sock, file_data)
                    else:
                        send_msg(sock, b"ERROR")
                except:
                    send_msg(sock, b"Format salah")

            else:
                send_msg(sock, b"Command tidak dikenal")