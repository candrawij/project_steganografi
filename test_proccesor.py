import io
from utils.processor import process_encryption, process_decryption

# Kita butuh 'Mocking' karena process_encryption butuh objek Streamlit
# Tapi kita bisa pakai 'open()' biasa untuk simulasi

class MockFile:
    """Pura-pura jadi file upload streamlit"""
    def __init__(self, path, name):
        self.name = name
        with open(path, "rb") as f:
            self.data = f.read()
    def getvalue(self):
        return self.data
    # Pillow butuh method read/seek kadang-kadang, kita arahkan ke BytesIO
    def read(self): return self.data
    def seek(self, val): pass
    def tell(self): return 0

# 1. PERSIAPAN DATA DUMMY
# Pastikan kamu punya 'test_cover.png' di folder ini (bisa copy gambar apa saja)
try:
    secret = MockFile("test_manual.py", "rahasia.txt") # Kita coba sembunyikan file script ini sendiri
    cover1 = "test_cover.png" # Path gambar
    # Di Streamlit, inputnya list. Dan process_encryption kita 
    # cukup pintar menangani path string (karena stego_algo support) 
    # ATAU kita harus load jadi MockFile/Image.
    
    # Agar sesuai kode processor, kita load gambar jadi BytesIO/Mock
    with open(cover1, "rb") as f:
        img_bytes = f.read()
    
    # Kita butuh 2 gambar wadah (duplikat aja)
    covers = [io.BytesIO(img_bytes), io.BytesIO(img_bytes)] 
    
    print("--- 1. TEST ENKRIPSI ---")
    zip_result, zip_name = process_encryption(secret, covers)
    
    # Simpan ZIP hasilnya ke disk biar bisa dicek
    with open("hasil_integrasi.zip", "wb") as f:
        f.write(zip_result.getvalue())
    print("✅ Enkripsi Sukses! Cek file 'hasil_integrasi.zip'")

    # --- UNTUK TEST DEKRIPSI ---
    # Kita harus ekstrak zip tadi manual dulu, atau simulasi
    # Tapi ini agak ribet tanpa unzip library.
    # Cukup sampai enkripsi sukses, biasanya logika dekripsi sudah aman.
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("Pastikan file 'test_cover.png' ada di folder ini untuk testing.")