# 🎯 Object Tracking with 2 Servos and ESP32-CAM

Saya membuat proyek di mana kamera (ESP32-CAM) akan mengikuti pergerakan objek menggunakan bantuan dua buah servo: satu untuk **pan (horizontal)** dan satu lagi untuk **tilt (vertikal)**. Misalnya, saat objek bergerak ke kiri, maka kamera juga akan ikut bergerak ke kiri.

📺 **Tonton demonya di YouTube:**  
[https://www.youtube.com/watch?v=2TU9Fy5hJ-A](https://www.youtube.com/watch?v=2TU9Fy5hJ-A)

---

## 🔧 Langkah-Langkah Pembuatan

### 1. Wiring Proyek

![Wiring](img/wiring.png)

💡 **Tips:**
- Gunakan **dua sumber daya (battery) terpisah**, masing-masing 5V:
  - Satu untuk **ESP32-CAM**
  - Satu lagi untuk **servo dan elektronik lainnya**

---

### 2. Upload Code ke WEMOS

Upload file `arduino.txt` ke board WEMOS Anda.

---

### 3. Upload Code ke ESP32-CAM

![ESP32-CAM](img/ESP_32_CAM.png)

- Hubungkan ESP32-CAM ke komputer
- Pilih board yang sesuai di Arduino IDE
- Gunakan contoh kode dari library ESP32-CAM

---

### 4. Jalankan Kode Python di Komputer

Jalankan file `arduino color tracking camera.py`.

Sebelumnya, pastikan beberapa hal berikut telah Anda sesuaikan:

#### ✅ Ganti IP Kamera:
```python
ip_cam_url = "http://192.168.220.211:81/stream"  # Sesuaikan dengan IP ESP32-CAM Anda
```

#### ✅ Ubah Warna Objek yang Akan Dideteksi:
```python
color = "#581845"  # Ganti dengan warna target Anda (format HEX)
```

#### ✅ Tambahkan Delay untuk Sinkronisasi (Opsional):
Jika Anda mengalami delay antara ESP32-CAM dan komunikasi Bluetooth, Anda bisa menambahkan delay seperti berikut:
```python
current_time = time.time()
if current_time - last_sent >= 0.4:  # 400 ms
    ser.write(('a' + str(int(Xposition)) + 'b' + str(int(Yposition))).encode())
    last_sent = current_time
```

---

## ⚙️ Pengaturan Tambahan

- Setelah program berjalan, ubah **nilai di pojok kanan atas** GUI Python ke lebih dari `300` agar servo dapat bergerak.
  
---

Jika ada pertanyaan atau ingin diskusi lebih lanjut, silakan tinggalkan komentar di video atau repository ini. Selamat mencoba! 🚀
