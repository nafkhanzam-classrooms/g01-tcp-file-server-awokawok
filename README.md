[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama           | NRP        | Kelas     |
| ---            | ---        | ----------|
| Salwa Nadia Maharani | 5025241041 | Pemrograman Jaringan D |
| Naura Rossa Azalia | 5025241041 | Pemrograman Jaringan D |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```
https://youtu.be/lRTvD_PcLpg
```

## Penjelasan Program

**`client.py`**
### Deskripsi 
Client berfungsi sebagai penghubung antara pengguna dan server. Client dapat mengirimkan perintah ke server seperti melihat daftar file, mengunggah file, dan mengunduh file.
#### Cara Kerja
##### 1. Membuat Koneksi 
```py
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```
client membuat koneksi ke server menggunakan protokol TCP dengan alamat IP dan port tertentu

##### 2. Mengirim Data (Framing)
```py
def send_msg(sock, data):
    header = struct.pack(">I", len(data))
    sock.sendall(header + data)
```
Data dikirim menggunakan teknik **framing**, yaitu dengan menambahkan header berupa panjang data agar server dapat membaca data dengan benar

##### 3. Menerima Data
```py
def recv_msg(sock):
```
Client membaca header terlebih dahulu untuk mengetahui panjang data, kemudian membaca isi data sesuai panjanng tersebut.

##### 4. Command System
Client mendukung beberapa perintah:
- `/list` untuk melihat daftar file di server
- `/upload <filename>` untuk mengunggah file ke server
- `/download <filename>` untuk mengunduh file dari server

**`server-sync.py`**
### Deskripsi
Server synchronous adalah server yang hanya dapat menangani satu client dalam satu waktu. Server ini menggunakan metode blocking.
#### Cara Kerja
##### 1. Setup Server
```py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
```
Server dibuat menggunakan socket TCP, kemudian di-bind ke alamat dan port tertentu untuk menerima koneksi.

##### 2. Menerima Koneksi
```py
conn, addr = server.accept()
```
Server menerima koneksi dari client. Proses ini bersifat blocking, sehingga server akan menunggu hingga ada client yang terhubung. 

##### 3. Menerima Data
```py
data = recv_msg(conn)
```
Server menerima data dari client. Selama proses ini, server tidak dapat melayani client lain.

##### 4. Proses Perintah
Server memproses perintah dari client:
- `/list` untuk menampilkan daftar file
- `/upload` untuk menerima file dari client
- `/download` untuk mengirim file ke client

**Kekurangan**
- Tidak dapat menangani banyak client secara bersamaan
- Client lain harus menunggu (blocking)

**`server-thread.py`**
### Deskripsi
Server thread adalah server yang dapat menangani banyak client secara bersamaan dengan menggunakan thread.
#### Cara Kerja
##### 1. Import Threading
```py
import threading
```
Digunakan untuk menjalankan beberapa proses secara bersamaan dalam satu program.

##### 2. Fungsi Handler Client
```py
def handle_client(conn, addr):
```
Fungsi ini digunakan untuk menangani komunikasi dengan satu client.

##### 3. Membuat Thread
```py
threading.Thread(target=handle_client, args=(conn, addr)).start()
```
Setiap client yang terhubung akan dibuatkan thread baru sehingga dapat dilayani secara paralel.

##### 4. Loop Komunikasi 
```py
while True:
```
Setiap thread akan terus berjalan untuk melayani client masing-masing tanpa mengganggu client lain.

**Kelebihan**
- Dapat menangani banyak client (multi-client)
- Tidak blocking seperti server synchronous

**Kekurangan**
- Menggunakan lebih banyak resource (CPU & memory)
- Kurang efisien jika jumlah client sangat banyak

**`server-select.py`**
### Deskripsi
Teknik pemrograman menggunakan fitur `select()` yang memungkinkan server menangani banyak client secara bersamaan dalam satu thread. Pada pendekatan ini, server hanya memproses socket yang siap dibaca sehingga lebih efisien dalam penggunaan resource dibandingkan pendekatan multi-threading.

#### Cara Kerja
##### 1. Import Select
```py
import select
```

##### 2. Setup Server
```py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)
```
Server membuat socket TCP, melakukan binding, kemudian mengaktifkan mode non-blocking

##### 3. Cek Socket 
```py
inputs = [server]
```
List berisi semua socket yang dipantau, yaitu:
- socket server
- socket client

##### 4. Menggunakan Select 
```py
readable, _, _ = select.select(inputs, [], [])
```
Server akan memilih socket yang siap dioperasikan

##### 5. State Management 
```py
client_states[sock] = {
    "mode": "upload",
    "filename": filename
}
```
Mencegah client gagal mengirimkan datanya dikarenakan dalam model `select`, data tidak selalu dikirim dan diterima dalam satu waktu

##### 6. Implementasi Fitur
a. `/list`
Menampilkan daftar file yang ada dalam folder server
b. `/upload`
Tahap 1: set state
Tahap 2: terima file dan simpan
c. `/download`
Server membaca file kemudian mengirim status (OK / ERROR) lalu mengirim isi file

**`server-poll.py`**
### Deskripsi
Pendekatan `poll` ini memiliki cara kerja yang sama dengan `select` yaitu bersifat event-driven dan non-blocking namun versi lebih scalable nya.

#### Cara Kerja
##### 1. Import Select
```py
import select
```
Pada pendekatan ini gunakan `poll()`

##### 2. Setup Server
```py
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
server.setblocking(False)
```
Sama seperti pendekatan `select`, server membuat socket TCP, melakukan binding, kemudian mengaktifkan mode non-blocking

##### 3. Inisialisasi Poll
```py
poller = select.poll()
poller.register(server, select.POLLIN)
```
- `POLLIN` menandakan socket siap dibaca

##### 4. Event Loop
```py
events = poller.poll()
for fd, flag in events:
```
Server melakukan loop untuk menunggu event

##### 5. Handling Client Connection
```py
conn, addr = server.accept()
conn.setblocking(False)
poller.register(conn, select.POLLIN)
```
Ketika ada client baru, maka server menerima koneksi dan mendaftarkan client ke `poll`

##### 6. Implementasi Fitur
a. `/list`
Menampilkan daftar file yang ada dalam folder server
b. `/upload`
Tahap 1: set state
Tahap 2: terima file dan simpan
c. `/download`
Server membaca file kemudian mengirim status (OK / ERROR) lalu mengirim isi file

## Screenshot Hasil
`sever-sync.py`

![WhatsApp Image 2026-03-25 at 21 55 44](https://github.com/user-attachments/assets/e6f2b870-4d9f-49a1-8bbc-1cae588990e8)

![WhatsApp Image 2026-03-25 at 21 55 44 (1)](https://github.com/user-attachments/assets/8ba455fb-2eb5-4d86-a47f-3918bd5b8ab5)


`server-thread.py`

![WhatsApp Image 2026-03-25 at 21 51 05](https://github.com/user-attachments/assets/def17735-8506-4026-ab3c-5c535da23a39)

![WhatsApp Image 2026-03-25 at 21 51 05 (1)](https://github.com/user-attachments/assets/4b777e13-e112-443a-a8c6-0a066b303857)

`server-select.py`

<img width="1213" height="793" alt="image" src="https://github.com/user-attachments/assets/1797b2dd-9038-4e01-987d-04b4a68eed16" />

<img width="1212" height="791" alt="image" src="https://github.com/user-attachments/assets/c043207e-8151-4314-9e26-0b067684e6e0" />


`server-poll.py`

<img width="1212" height="787" alt="image" src="https://github.com/user-attachments/assets/04df2f0c-efb3-4fef-af6d-9bad0b8e3620" />

<img width="1211" height="762" alt="image" src="https://github.com/user-attachments/assets/e2318ee0-16cc-4460-a494-ee7acd6c41f9" />



