from utils.stego_algo import hide_bytes_in_image, extract_bytes_from_image

# 1. Siapkan data dummy
pesan_asli = b"Halo, ini adalah pesan rahasia untuk tes LSB!"
print(f"Pesan Asli: {pesan_asli}")

# 2. Siapkan gambar wadah (pastikan ada file 'test.png' atau 'test.jpg' di folder ini)
# Jika tidak ada, buat gambar hitam polos pake python:
from PIL import Image
dummy_img = Image.new('RGB', (100, 100), color = 'red')
dummy_img.save('test_cover.png')

# 3. TEST ENCODE (Menyembunyikan)
print("--- Mulai Menyembunyikan ---")
stego_image = hide_bytes_in_image('test_cover.png', pesan_asli)
# Simpan hasilnya (Format harus PNG agar LSB tidak rusak kena kompresi)
stego_image.save('hasil_test.png') 
print("Gambar steganografi tersimpan di 'hasil_test.png'")

# 4. TEST DECODE (Membaca)
print("--- Mulai Membaca ---")
pesan_ditemukan = extract_bytes_from_image('hasil_test.png')

print(f"Pesan Ditemukan: {pesan_ditemukan}")

# 5. Validasi
if pesan_asli == pesan_ditemukan:
    print("✅ SUKSES! Pesan cocok 100%.")
else:
    print("❌ GAGAL! Pesan tidak sama.")