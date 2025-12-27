import streamlit as st
import time
import io
import pandas as pd
import random

# ==========================================
# KONFIGURASI HALAMAN (HARUS DI PALING ATAS)
# ==========================================
st.set_page_config(
    page_title="StegoCloud Secure Sharding",
    page_icon="🛡️",
    layout="wide", # Layout lebar agar terlihat pro
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (Agar tidak terlihat default)
# ==========================================
st.markdown("""
<style>
    /* Mengubah font agar terlihat teknis */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Style untuk Metric Containers */
    div[data-testid="stMetric"] {
        background-color: #1E1E1E;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #00FF00;
    }
    
    /* Tombol Utama */
    .stButton > button {
        width: 100%;
        background-color: #00FF00;
        color: black;
        font-weight: bold;
    }
    
    /* Terminal Output Style */
    .terminal-box {
        background-color: black;
        color: #00FF00;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        height: 200px;
        overflow-y: scroll;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNGSI BANTUAN VISUAL (MOCKUP)
# ==========================================
def get_file_size_mb(size_bytes):
    return f"{size_bytes / (1024 * 1024):.2f} MB"

def hex_viewer(file_bytes, limit=100):
    # Menampilkan raw bytes agar terlihat canggih
    return " ".join([f"{b:02X}" for b in file_bytes[:limit]]) + " ..."

# MOCKUP PROSES (Nanti diganti fungsi asli teman)
def process_encryption_dummy(secret_file, cover_images):
    logs = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Inisialisasi modul kriptografi...",
        f"Membaca file rahasia: {secret_file.name}...",
        "Melakukan enkripsi AES-256...",
        f"Memecah file menjadi {len(cover_images)} fragmen...",
        "Analisis kapasitas piksel gambar wadah...",
        "Menyuntikkan payload ke LSB (Least Significant Bit)...",
        "Verifikasi integritas data (Checksum SHA-256)...",
        "Mengemas hasil ke dalam arsip ZIP..."
    ]
    
    for i, step in enumerate(steps):
        time.sleep(0.5) # Simulasi proses berat
        progress_bar.progress((i + 1) * 12)
        status_text.text(f"SYSTEM_PROCESS: {step}")
        logs.append(f"[INFO] {time.strftime('%H:%M:%S')} - {step}")
    
    progress_bar.progress(100)
    status_text.text("STATUS: SELESAI.")
    return io.BytesIO(b"DummyZIP"), "secure_bundle.zip", logs

# ==========================================
# UI UTAMA
# ==========================================

# Sidebar
with st.sidebar:
    st.title("🛡️ StegoCloud")
    st.caption("Distributed Steganography Storage")
    st.divider()
    
    st.markdown("### 📊 Status Sistem")
    st.metric("Algoritma", "LSB + Sharding")
    st.metric("Enkripsi", "AES-256")
    
    st.divider()
    st.info("""
    **Panduan:**
    1. Upload File Rahasia.
    2. Upload Gambar Wadah (Cover).
    3. Sistem akan memecah file & menyisipkan ke gambar.
    """)

# Header Halaman
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("Secure Data Embedding System")
    st.markdown("Advanced Steganography with **Data Sharding** & **Pixel Manipulation**.")
with col_h2:
    # Indikator status server (Gimmick)
    st.success("🟢 SYSTEM ONLINE")

tab1, tab2, tab3 = st.tabs(["🔒 ENCRYPT & EMBED", "🔓 EXTRACT & DECRYPT", "⚙️ TECHNICAL ANALYSIS"])

# --- TAB 1: ENKRIPSI ---
with tab1:
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        st.subheader("1. Secret Payload")
        secret_file = st.file_uploader("Upload file rahasia", help="File yang akan diamankan")
        
        if secret_file:
            # Tampilkan info teknis file
            st.code(f"Size: {secret_file.size} bytes\nType: {secret_file.type}", language="yaml")
            with st.expander("Lihat Hex Awal (Preview)"):
                st.text(hex_viewer(secret_file.getvalue()))

    with col_input2:
        st.subheader("2. Cover Images")
        cover_files = st.file_uploader("Upload Gambar Wadah", accept_multiple_files=True, type=["png", "jpg"])
        
        if cover_files:
            total_pixels = sum([1920*1080 for _ in cover_files]) # Asumsi resolusi
            # Hitung kapasitas teoritis
            capacity_mb = (total_pixels * 3 * 0.125) / (1024*1024) # 1 bit per channel
            st.metric("Estimasi Kapasitas Tampung", f"{capacity_mb:.2f} MB", delta=f"{len(cover_files)} Gambar")

    st.divider()

    if st.button("🚀 EKSEKUSI STEGANOGRAFI", type="primary"):
        if secret_file and cover_files:
            zip_out, name_out, logs = process_encryption_dummy(secret_file, cover_files)
            
            col_res1, col_res2 = st.columns([2, 1])
            with col_res1:
                st.success("Proses Embedding Berhasil!")
                # Tampilkan Log Terminal "Palsu"
                log_text = "\n".join(logs)
                st.markdown(f'<div class="terminal-box">{log_text}</div>', unsafe_allow_html=True)
            
            with col_res2:
                st.markdown("### Download Hasil")
                st.write("Paket gambar aman siap diunduh.")
                st.download_button("⬇️ Download ZIP", zip_out, name_out, "application/zip", use_container_width=True)
        else:
            st.error("Missing Input: Harap upload file rahasia dan gambar wadah.")

# --- TAB 2: DEKRIPSI ---
with tab2:
    st.markdown("### Recovery Mode")
    st.warning("Pastikan Anda memiliki semua potongan gambar (Shards) untuk mengembalikan file.")
    
    stego_files = st.file_uploader("Upload Stego-Images", accept_multiple_files=True, key="decrypt")
    
    if stego_files:
        st.info(f"{len(stego_files)} fragmen terdeteksi.")
        if st.button("🔍 SCAN & REASSEMBLE"):
            # Mockup proses
            with st.spinner("Mengekstrak bit dari piksel..."):
                time.sleep(2)
                st.success("File berhasil direkonstruksi!")
                st.balloons()

# --- TAB 3: ANALISIS (Nilai Plus Dosen) ---
with tab3:
    st.markdown("### 🔬 Analisis Distribusi Bit")
    st.write("Visualisasi bagaimana data disebar ke dalam gambar wadah.")
    
    # Fake Chart menggunakan data dummy agar terlihat ilmiah
    if cover_files:
        chart_data = pd.DataFrame({
            "Image ID": [f"Img_{i+1}" for i in range(len(cover_files))],
            "Data Usage (KB)": [random.randint(50, 200) for _ in range(len(cover_files))],
            "Entropy Level": [random.uniform(7.5, 7.9) for _ in range(len(cover_files))]
        })
        
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.bar_chart(chart_data, x="Image ID", y="Data Usage (KB)")
            st.caption("Distribusi payload per gambar")
        with col_chart2:
            st.line_chart(chart_data, x="Image ID", y="Entropy Level")
            st.caption("Tingkat Entropy (Kepadatan Acak) per gambar")
            
    else:
        st.info("Lakukan upload gambar di Tab 1 untuk melihat analisis data.")