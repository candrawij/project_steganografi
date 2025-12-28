import io
import zipfile
from PIL import Image # Pastikan import ini ada

# Import logika teman
try:
    from utils.stego_algo import hide_bytes_in_image, extract_bytes_from_image
    from utils.file_manager import split_data, merge_data
except ImportError:
    print("⚠️ Warning: Modul stego_algo atau file_manager belum ditemukan.")

def process_encryption(secret_file_obj, cover_files_list):
    # 1. BACA FILE RAHASIA
    file_bytes = secret_file_obj.getvalue()
    num_images = len(cover_files_list)
    
    # 2. PECAH FILE
    try:
        chunks = split_data(file_bytes, num_images)
    except Exception as e:
        raise ValueError(f"Gagal memecah file: {e}")

    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        
        # 3. LOOP SETIAP POTONGAN & GAMBAR
        for i in range(num_images):
            current_chunk = chunks[i]
            current_cover_file = cover_files_list[i] # Ini masih UploadedFile
            
            # --- PERBAIKAN DISINI ---
            # Kita harus convert UploadedFile menjadi Pillow Image dulu
            current_cover_image = Image.open(current_cover_file) 
            # ------------------------
            
            try:
                # Sekarang yang dikirim adalah 'current_cover_image' (Objek Gambar), bukan file mentah
                stego_image = hide_bytes_in_image(current_cover_image, current_chunk)
            except ValueError as e:
                raise ValueError(f"Gambar ke-{i+1} terlalu kecil! Error: {e}")
            
            # 4. SIMPAN HASIL KE MEMORI
            img_byte_arr = io.BytesIO()
            stego_image.save(img_byte_arr, format='PNG')
            
            # 5. MASUKKAN KE ZIP
            img_filename = f"secure_shard_{i+1}.png"
            zip_file.writestr(img_filename, img_byte_arr.getvalue())

    zip_buffer.seek(0)
    return zip_buffer, "stego_result.zip"

def process_decryption(stego_files_list):
    extracted_chunks = []
    
    # 1. LOOP SETIAP GAMBAR
    for img_file in stego_files_list:
        try:
            # --- PERBAIKAN JUGA DISINI ---
            # Saat dekripsi juga sama, harus dibuka sebagai Image dulu
            img_object = Image.open(img_file)
            # -----------------------------

            data = extract_bytes_from_image(img_object)
            
            if data:
                extracted_chunks.append(data)
                
        except Exception as e:
            print(f"Gagal mengekstrak dari salah satu gambar: {e}")
            continue
    
    if not extracted_chunks:
        raise ValueError("Tidak ditemukan data rahasia di gambar manapun!")

    # 2. GABUNGKAN DATA
    full_file_bytes = merge_data(extracted_chunks)
    
    # 3. OUTPUT
    return io.BytesIO(full_file_bytes), "restored_file_output"