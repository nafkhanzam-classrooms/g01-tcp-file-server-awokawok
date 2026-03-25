[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/mRmkZGKe)
# Network Programming - Assignment G01

## Anggota Kelompok
| Nama           | NRP        | Kelas     |
| ---            | ---        | ----------|
| Salwa Nadia Maharani | 5025241041 | Program Jaringan D |
| Naura Rossa Azalia | 5025241041 | Program Jaringan D |

## Link Youtube (Unlisted)
Link ditaruh di bawah ini
```

```

## Penjelasan Program

**`client.py`**
### Deskripsi 
Client berfungsi sebagai penghubung antara pengguna dan server. Client dapat mengirimkan perintah ke server seperti melihat daftar file, mengunggah file, dan mengunduh file.
#### Cara Kerja
##### 1. Membuat Koneksi 
```
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```
client membuat koneksi ke server menggunakan protokol TCP dengan alamat IP dan port tertentu

##### 2. Mengirim Data (Framing)
```
def send_msg(sock, data):
    header = struct.pack(">I", len(data))
    sock.sendall(header + data)
```
Data dikirim menggunakan teknik **framing**, yaitu dengan menambahkan header berupa panjang data agar server dapat membaca data dengan benar

##### 3. Menerima Data
```
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
```
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
```
Server dibuat menggunakan socket TCP, kemudian di-bind ke alamat dan port tertentu untuk menerima koneksi.

##### 2. Menerima Koneksi
```
conn, addr = server.accept()
```
Server menerima koneksi dari client. Proses ini bersifat blocking, sehingga server akan menunggu hingga ada client yang terhubung. 

##### 3. Menerima Data
```
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
```
import threading
```
Digunakan untuk menjalankan beberapa proses secara bersamaan dalam satu program.

##### 2. Fungsi Handler Client
```
def handle_client(conn, addr):
```
Fungsi ini digunakan untuk menangani komunikasi dengan satu client.

##### 3. Membuat Thread
```
threading.Thread(target=handle_client, args=(conn, addr)).start()
```
Setiap client yang terhubung akan dibuatkan thread baru sehingga dapat dilayani secara paralel.

##### 4. Loop Komunikasi 
```
while True:
```
Setiap thread akan terus berjalan untuk melayani client masing-masing tanpa mengganggu client lain.

**Kelebihan**
- Dapat menangani banyak client (multi-client)
- Tidak blocking seperti server synchronous

**Kekurangan**
- Menggunakan lebih banyak resource (CPU & memory)
- Kurang efisien jika jumlah client sangat banyak



## Screenshot Hasil
