import math

def split_data(file_bytes, num_chunks):
    """
    Memecah file bytes menjadi beberapa potongan dengan header urutan.
    Format Header: b"Index|Total|" contoh: b"1|5|"
    
    :param file_bytes: Data file asli (bytes)
    :param num_chunks: Jumlah potongan/gambar wadah (int)
    :return: List of bytes (chunk yang sudah ada headernya)
    """
    if num_chunks <= 0:
        raise ValueError("Jumlah potongan harus lebih dari 0")
        
    total_size = len(file_bytes)
    chunk_size = math.ceil(total_size / num_chunks)
    
    chunks_with_header = []
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        
        payload = file_bytes[start:end]
        
        if not payload:
            continue
            
        # BUAT HEADER
        header_str = f"{i+1}|{num_chunks}|"
        header_bytes = header_str.encode('utf-8')
        
        final_chunk = header_bytes + payload
        chunks_with_header.append(final_chunk)
        
    return chunks_with_header

def merge_data(list_of_chunks):
    """
    Menggabungkan kembali potongan-potongan data menjadi file utuh.
    Fungsi ini akan membaca header, mengurutkan, menghapus header, lalu menyatukan.
    
    :param list_of_chunks: List berisi bytes dari hasil ekstraksi steganografi
    :return: Bytes file utuh
    """
    if not list_of_chunks:
        return b""
        
    sorted_buffer = []
    
    for chunk in list_of_chunks:
        try:
            # PARSING HEADER
            
            first_pipe = chunk.find(b'|')
            second_pipe = chunk.find(b'|', first_pipe + 1)
            
            if first_pipe == -1 or second_pipe == -1:
                print("Warning: Chunk rusak atau tidak ada header. Melewati chunk ini.")
                continue
                
            # Ekstrak Angka Urutan
            index_str = chunk[:first_pipe]
            index = int(index_str)
            
            # Ambil Data Bersih (Payload)
            clean_payload = chunk[second_pipe+1:]
            
            sorted_buffer.append((index, clean_payload))
            
        except ValueError:
            print("Error parsing header. Chunk corrupt.")
            continue
            
    # URUTKAN BERDASARKAN INDEX (item[0])
    sorted_buffer.sort(key=lambda x: x[0])
    
    # GABUNGKAN DATA (Reassembly)
    final_file_bytes = b"".join([item[1] for item in sorted_buffer])
    
    return final_file_bytes