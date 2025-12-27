from PIL import Image

# 1. STOPPER: Penanda unik untuk mengetahui kapan data berakhir.
STOPPER = b"#####EOF#####"

def _bytes_to_bin(data_bytes):
    """Mengubah bytes menjadi string biner (contoh: b'A' -> '01000001')"""
    data_bytes += STOPPER
    return ''.join([format(b, '08b') for b in data_bytes])

def _bin_to_bytes(bin_str):
    """Mengubah string biner kembali ke bytes"""
    all_bytes = bytearray()
    for i in range(0, len(bin_str), 8):
        byte_chunk = bin_str[i:i+8]
        if len(byte_chunk) == 8:
            all_bytes.append(int(byte_chunk, 2))
    return bytes(all_bytes)

def hide_bytes_in_image(image_input, data):
    """
    Menyisipkan data bytes ke dalam gambar menggunakan teknik LSB.
    :param image_input: Path file gambar (str) ATAU Objek Gambar (PIL Image)
    :param data: Data dalam bentuk bytes (b'...')
    :return: Objek PIL Image baru yang berisi pesan
    """
    if isinstance(image_input, str):
        img = Image.open(image_input)
    else:
        img = image_input

    img = img.convert("RGB")
    
    pixels = list(img.getdata())
    
    binary_data = _bytes_to_bin(data)
    data_len = len(binary_data)
    
    if data_len > len(pixels) * 3:
        raise ValueError(f"Data terlalu besar! Butuh {data_len} bit, gambar cuma punya {len(pixels)*3} slot.")

    new_pixels = []
    data_index = 0

    for pixel in pixels:
        r, g, b = pixel
        new_rgb = []
        
        for val in [r, g, b]:
            if data_index < data_len:
                # Logika LSB:
                # 1. Ubah nilai warna jadi genap (val & ~1)
                # 2. Tambahkan bit data (0 atau 1)
                bit_to_hide = int(binary_data[data_index])
                new_val = (val & ~1) | bit_to_hide
                new_rgb.append(new_val)
                data_index += 1
            else:
                # Jika data sudah habis, biarkan nilai piksel asli
                new_rgb.append(val)
        
        new_pixels.append(tuple(new_rgb))

    new_img = Image.new("RGB", img.size)
    new_img.putdata(new_pixels)
    
    return new_img

def extract_bytes_from_image(image_input):
    """
    Mengekstrak data bytes dari gambar steganografi.
    """
    if isinstance(image_input, str):
        img = Image.open(image_input)
    else:
        img = image_input

    img = img.convert("RGB")
    pixels = list(img.getdata())

    binary_str = ""
    found_stopper = False
    
    # Loop semua piksel
    for pixel in pixels:
        if found_stopper:
            break
            
        r, g, b = pixel
        for val in [r, g, b]:
            # Ambil bit terakhir (LSB) -> val modulo 2
            binary_str += str(val % 2)
            
            if len(binary_str) % 8 == 0:
                current_bytes = _bin_to_bytes(binary_str)
                if current_bytes.endswith(STOPPER):
                    return current_bytes[:-len(STOPPER)]
    
    # Jika sampai habis tidak ketemu stopper (mungkin gambar bukan stego atau rusak)
    return b"" # Kembalikan kosong