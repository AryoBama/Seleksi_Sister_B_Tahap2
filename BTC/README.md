# BTC

## Cara menjalankan
Berikut cara menjalankan langsung 3 nodes
Pastikan work directory berada di folder root bukan folder BTC
1. Terminal 1
  ```bash
  python -m BTC.app --port 5000 -peers http://127.0.0.1:5001, http://127.0.0.1:5002 --difficulty 4
  ```
2. Terminal 2
  ```bash
  python -m BTC.app --port 5001 -peers http://127.0.0.1:5000, http://127.0.0.1:5002 --difficulty 4
  ```
3. Terminal 3
  ```bash
  python -m BTC.app --port 5002 -peers http://127.0.0.1:5000, http://127.0.0.1:5001 --difficulty 4
  ```

## Endpoint utama yang dapat digunakan
1. /transaction
   Berfungsi menambahkan transaksi ke transaksi pool
   
   Contoh perintah:
   ```bash
   curl -X POST -H "Content-Type: application/json" ^ -d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":50}" ^ http://127.0.0.1:5000/transaction
   ```
2. /transactions
   Melihat daftar transaksi di pool
   
   Contoh perintah:
   ```bash
   curl -X GET http://127.0.0.1:5000/transactions
   ```
3. /mine
   Menambang untuk menambahkan block baru ke node
   
   Contoh perintah:
   ```bash
   curl -X GET http://127.0.0.1:5000/mine
   ```
5. /chain
   Melihat daftar block
   
   Contoh perintah:
   ```bash
   curl -X GET http://127.0.0.1:5000/chain
   ```
