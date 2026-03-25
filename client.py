import socket
import struct
import os

HOST = '127.0.0.1'
PORT = 5000

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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

print("Terhubung ke server!")

while True:
    cmd = input(">> ")

    # LIST
    if cmd == "/list":
        send_msg(client, cmd.encode())
        response = recv_msg(client)
        print(response.decode())

    # UPLOAD
    elif cmd.startswith("/upload"):
        try:
            _, filepath = cmd.split()

            if not os.path.exists(filepath):
                print("File tidak ditemukan!")
                continue

            filename = os.path.basename(filepath)

            send_msg(client, f"/upload {filename}".encode())

            with open(filepath, "rb") as f:
                file_data = f.read()

            send_msg(client, file_data)

            response = recv_msg(client)
            print(response.decode())

        except:
            print("Format: /upload namafile")

    # DOWNLOAD
    elif cmd.startswith("/download"):
        try:
            _, filename = cmd.split()

            send_msg(client, cmd.encode())

            status = recv_msg(client)

            if status == b"OK":
                file_data = recv_msg(client)

                with open(filename, "wb") as f:
                    f.write(file_data)

                print("Download berhasil:", filename)
            else:
                print("File tidak ditemukan di server")

        except:
            print("Format: /download namafile")

    else:
        print("Command tidak valid")