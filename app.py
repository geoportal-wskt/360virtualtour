import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import json
import requests
from datetime import datetime

# ==========================================
# 0. KONFIGURASI GITHUB (WAJIB DIISI)
# ==========================================
GITHUB_TOKEN = "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" 
REPO_OWNER = "geoportal-wskt"
REPO_NAME = "360virtualtour"
BRANCH = "main"

st.set_page_config(page_title="GIS-DS 360 Generator", layout="wide")

# ==========================================
# 1. KONFIGURASI KREDENSIAL & ROLE
# ==========================================
USERS = {
    "admin_gis": {"password": "Infra12345%", "role": "admin", "nama": "Administrator GIS"},
    "tim_proyek": {"password": "proyek2026", "role": "proyek", "nama": "Tim Lapangan Proyek"}
}

# ==========================================
# 2. HELPER FUNCTIONS (GITHUB & GFORM)
# ==========================================

def push_to_github(file_path, content, is_image=False):
    """Mengirim file fisik ke repositori GitHub"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    if is_image:
        encoded_content = base64.b64encode(content).decode('utf-8')
    else:
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

    data = {
        "message": f"Upload {file_path} via GIS-DS 360 Generator",
        "content": encoded_content,
        "branch": BRANCH
    }

    # Cek apakah file sudah ada untuk mendapatkan SHA (supaya bisa update/overwrite)
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data["sha"] = res.json()["sha"]

    response = requests.put(url, headers=headers, json=data)
    return response.status_code

def update_projects_database(nama_proyek, path_relatif_folder, tanggal_str):
    """Mengirim metadata ke Google Sheets via Google Form"""
    url = "https://docs.google.com/forms/d/e/1FAIpQLSd_jfuTzmgiMTNfkJnj6tyTlakhav6y5583POSBhYX4RvTGvQ/formResponse"
    payload = {
        "entry.1909594847": nama_proyek,
        "entry.1997775924": path_relatif_folder,
        "entry.473746175": tanggal_str,
        "entry.1021577494": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entry.2051024028": st.session_state.get('user_full_name', 'System')
    }
    return requests.post(url, data=payload)

# ==========================================
# 3. SISTEM LOGIN & AUTH
# ==========================================
def init_auth():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.session_state.user_full_name = ""

def login_ui():
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/id/a/af/Waskita_Karya_logo.svg", width=200)
    st.sidebar.title("🔐 Akses Internal")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.user_full_name = USERS[username]["nama"]
                st.rerun()
            else:
                st.error("Salah password!")

init_auth()
if not st.session_state.logged_in:
    login_ui()
    st.stop()

# ==========================================
# 4. UI APLIKASI UTAMA
# ==========================================
st.title("🏗️ 360 Professional Tour Generator")
st.markdown("### Digital Survey & GIS - Divisi Infrastruktur")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Pengaturan Proyek ---
col_proj, col_date = st.columns(2)
with col_proj:
    list_proyek = ["PROYEK TOL JAPEK 2 SELATAN PAKET 3 INDUK", "Pelabuhan Patimban", "Probolinggo-Banyuwangi Paket 3 (JOP 25%)", "Proyek Jalan Kretek - Girijati", "Bendungan Bener Paket II JOP 83,5%", "Pembangunan Struktur Jembatan Musi", "Pelabuhan Tanjung Priuk JICT"] # Potong untuk contoh
    nama_proyek = st.selectbox("Pilih Nama Proyek", list_proyek)

with col_date:
    tanggal_survey = st.date_input("Tanggal Pengambilan Data", datetime.now())
    periode_str = tanggal_survey.strftime("%Y%m%d")
    tanggal_format_indo = tanggal_survey.strftime("%d %b %Y")

st.markdown("---")
uploaded_files = st.file_uploader("Unggah foto panorama 360", type=['jpg', 'jpeg'], accept_multiple_files=True)

semua_hotspot_data = {}
custom_labels_dict = {}

if uploaded_files:
    nama_file_list = [f.name for f in uploaded_files]
    for i, file in enumerate(uploaded_files):
        with st.expander(f"📍 Foto {i+1}: {file.name}"):
            label_titik = st.text_input(f"🏷️ Lokasi/STA", value=f"Titik {i+1}", key=f"label_{i}")
            custom_labels_dict[i] = label_titik
            
            b64 = base64.b64encode(file.getvalue()).decode()
            img_uri = f"data:image/jpeg;base64,{b64}"
            
            # Preview Pannellum (Dipotong untuk ringkas, tetap gunakan code Anda yang asli)
            components.html(f"Preview Frame...", height=350) 
            
            df_initial = pd.DataFrame({"Target Foto": [""], "Teks Hotspot": ["Maju"], "Pitch": [0.0], "Yaw": [0.0]})
            semua_hotspot_data[i] = st.data_editor(df_initial, num_rows="dynamic", key=f"ed_{i}")

# ==========================================
# 5. LOGIK GENERATE & PUSH TO GITHUB
# ==========================================
if st.button("🚀 Generate & Publish Virtual Tour", type="primary"):
    if uploaded_files:
        # Nama folder di GitHub
        folder_slug = "".join([c for c in nama_proyek if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
        path_di_github = f"{folder_slug}/{periode_str}"
        
        with st.spinner("⏳ Mengunggah file ke GitHub (Jangan tutup browser)..."):
            try:
                # 1. Upload Foto-foto ke GitHub
                for i, file in enumerate(uploaded_files):
                    file_bytes = file.getvalue()
                    push_to_github(f"{path_di_github}/{file.name}", file_bytes, is_image=True)

                # 2. Rakit HTML Template (Gunakan variabel template dari kode Anda)
                # ... (Gunakan logika scenes_js dan footer_content dari kode Anda) ...
                
                # --- LOGIKA RAKIT SCENE (DARI KODE ANDA) ---
                scenes_js = "" # ... isi sesuai loop Anda ...
                footer_content = "" # ... isi sesuai loop Anda ...
                html_template = f"<html>...</html>" # ... template lengkap Anda ...

                # 3. Upload index.html ke GitHub
                push_to_github(f"{path_di_github}/index.html", html_template, is_image=False)

                # 4. Catat ke Google Sheets via Form
                update_projects_database(nama_proyek, path_di_github, tanggal_format_indo)

                st.success(f"✅ Berhasil! Proyek '{nama_proyek}' sudah LIVE di Dashboard.")
                st.balloons()
            
            except Exception as e:
                st.error(f"Gagal memproses: {e}")