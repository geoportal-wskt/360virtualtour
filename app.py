import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import requests
import shutil
from datetime import datetime

st.set_page_config(page_title="GIS-DS 360 Generator", layout="wide")

# ==========================================
# 1. KONFIGURASI KREDENSIAL & ROLE
# ==========================================
USERS = {
    "admin_gis": {"password": "Infra12345%", "role": "admin", "nama": "Administrator GIS"},
    "tim_proyek": {"password": "proyek2026", "role": "proyek", "nama": "Tim Lapangan Proyek"}
}

# ==========================================
# 2. SISTEM LOGIN (SESSION STATE)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_full_name = ""

def login_ui():
    st.sidebar.image("https://github.com/geoportal-wskt/360virtualtour/blob/main/logo_w360.png?raw=true", width=200)
    st.sidebar.title("🔐 Akses Internal")
    
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.user_full_name = USERS[username]["nama"]
                st.rerun()
            else:
                st.error("Username atau Password salah!")

if not st.session_state.logged_in:
    login_ui()
    st.info("💡 Silakan masukkan kredensial pada sidebar untuk mengakses sistem.")
    st.stop()
else:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user_role = None
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.write(f"👤 **User:** {st.session_state.user_full_name}")
    st.sidebar.write(f"🔰 **Role:** {st.session_state.user_role.upper()}")

# =========================================================
# 3. FUNGSI UPDATE DATABASE GOOGLE SHEETS
# =========================================================
def update_projects_database(nama_proyek, path_relatif_folder, tanggal_str):
    url = "https://docs.google.com/forms/d/e/1FAIpQLSd_jfuTzmgiMTNfkJnj6tyTlakhav6y5583POSBhYX4RvTGvQ/formResponse"
    payload = {
        "entry.1909594847": nama_proyek,
        "entry.1997775924": path_relatif_folder,
        "entry.473746175": tanggal_str,
        "entry.1021577494": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entry.2051024028": st.session_state.get('user_full_name', 'System')
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        st.error(f"⚠️ Gagal sinkronisasi ke Cloud. Error: {e}")

# ==========================================
# 4. UI APLIKASI UTAMA (GENERATOR)
# ==========================================

header_html = f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #e5e7eb;">
    <div style="flex: 1;">
        <h1 style="margin: 0; padding: 0; font-size: 2.2rem; font-weight: bold; color: #1f2937;">
            W-360 Virtual Tour Generator
        </h1>
        <h3 style="margin: 8px 0 0 0; padding: 0; font-size: 1.2rem; font-weight: normal; color: #4b5563;">
            Digital Survey & GIS - Divisi Infrastruktur
        </h3>
    </div>
    <div style="margin-left: 20px;">
        <img src="https://github.com/geoportal-wskt/360virtualtour/blob/main/logo_w360.png?raw=true" style="height: 90px; object-fit: contain;">
    </div>
</div>
"""

# Menampilkan header ke layar Streamlit
st.markdown(header_html, unsafe_allow_html=True)

st.subheader("1. Pengaturan Proyek")
col_proj, col_date = st.columns(2)

with col_proj:
    list_proyek = [
        "PROYEK TOL JAPEK 2 SELATAN PAKET 3 INDUK", "Pelabuhan Patimban", 
        "Probolinggo-Banyuwangi Paket 3 (JOP 25%)", "Proyek Jalan Kretek - Girijati",
        "Jalan Tol Ciawi Sukabumi Seksi 3A", "Patimban Acces Toll Road Package 2",
        "Tol Serang - Panimbang Seksi 3 JOI 27,5%", "Jalan Tol IKN Seksi 3B-2 : Segmen KKT Kariangau",
        "JALAN TOL CIAWI - SUKABUMI SEKSI 3B", "Pembangunan Jalan Kawasan Komplek Yudikatif",
        "Jln Singaraja - Mengwitani P01 (JOI 51%)", "Penanganan Bencana Alam Sumatera",
        "Jembatan Penghubung Pulau Kalimantan - Pulau Laut (JOI 20%)", "Penanganan Bencana Kota Langsa Aceh",
        "Jalan Kota Bireuen - Kota Takengon", "Jembatan Aras Sambilan II (Lubuk Sidup)",
        "Bendungan Bener Paket II JOP 83,5%", "Bendungan Tiga Dihaji (57%) JOI 57%",
        "Bendungan Jragung Paket 1", "PROYEK BENDUNGAN MBAY JOP 70%", "Pengarah Rukoh",
        "PROYEK PEMBANGUNAN IPAL 1,2,3 IKN JOI70%", "RENTANG IRRIGATION LOS 01 JOP 60%",
        "Pembangunan Bendungan Cibeet (JOI 57,9%)", "Bendungan Karangnongko Paket II JOI 55%",
        "PEMB. BANGUNAN PENGARAH BEND. RUKOH KAB.", "Pembangunan Struktur Jembatan Musi",
        "REHABILITASI D.I CIBALIUNG KABUPATEN PAN", "Bendungan Jragung Paket 4",
        "PERBAIKAN JALAN TOL KAPB JOP 70%", "Irigasi Belitang Lempuing Pkt 2 JOP 60%",
        "Irigasi Belitang Lempuing Pkt 3 JOP 60%", "Irigasi Belitang Lempuing Pkt 1 JOP 34%",
        "Jaringan Utama D.I Cimanuk Cisanggarung", "Construction Of KSCS Package 1 JOP 55%",
        "Jaringan Utama DI Sumatera II Tahap 3", "Jaringan Utama D.I Daerah NTT II Tahap 3",
        "Jaringan Utama D.I Sulsel Paket 4 Tahap 3", "Jaringan Utama D.I Kalimantan 4 Tahap 3",
        "Irigasi KSPP Kab. Merauke Pkt 1 JOP 50%", "Tanggap Darurat Bencana Alam Kabupaten Serdang B",
        "Pelabuhan Tanjung Priuk JICT", "Preservasi Sugih Waras-Muara Enim",
        "Jembatan Pendekat Pulau Laut-Tanah Bumbu", "Proyek Rehabilitasi Jaringan Irigasi D.I./D.I.R. Provinsi Sumatera Selatan",
        "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket I", "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket III",
        "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket IV", "Lanjutan Pembangunan Bend Temef JOP 65%",
        "Pengaman Pantai KEK Tj. Lesung Paket 1", "Sedimentasi Bend Sumbawa JOI 65%",
        "PROYEK JEMBATAN KRAMASAN", "Rentang Irrigation Modernization Project",
        "JEMBATAN MUSI", "PROYEK PENGENDALI BANJIR BIMA", "JI Salamdarma Gadung Pawelutan JOP 60%",
        "Bendungan Rukoh Paket 2 JOP 58%", "Proyek Pengendalian Banjir Loji", "Peningkatan Jalan KIPP Paket D (JOI 65%)"
    ]
    list_proyek = list(dict.fromkeys(list_proyek))
    nama_proyek = st.selectbox("Pilih Nama Proyek", list_proyek)

with col_date:
    tanggal_survey = st.date_input("Tanggal Pengambilan Data", datetime.now())
    periode_str = tanggal_survey.strftime("%Y%m%d")
    tanggal_format_indo = tanggal_survey.strftime("%d %b %Y")

st.markdown("---")

st.subheader("2. Upload & Pemetaan Hotspot Visual (Multi Hotspot)")
uploaded_files = st.file_uploader("Unggah foto panorama 360", type=['jpg', 'jpeg'], accept_multiple_files=True)

semua_hotspot_data = {}
custom_labels_dict = {}

if uploaded_files:
    nama_file_list = [f.name for f in uploaded_files]
    
    for i, file in enumerate(uploaded_files):
        with st.expander(f"📍 Pengaturan Foto {i+1}: {file.name}", expanded=True):
            
            label_titik = st.text_input(f"🏷️ Nama Lokasi / STA", value=f"Titik {i+1}", key=f"label_{i}")
            custom_labels_dict[i] = label_titik
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            b64 = base64.b64encode(file.getvalue()).decode()
            img_uri = f"data:image/jpeg;base64,{b64}"
            
            st.markdown("**1. Klik area target di gambar (Koordinat otomatis tersalin):**")
            html_preview = f"""
            <html>
            <head>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css"/>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
            </head>
            <body style="margin:0;">
                <div id="panorama" style="width:100%; height:350px;"></div>
                <div style="position:absolute; top:10px; left:10px; background:rgba(0,0,0,0.8); color:#00ff00; padding:10px; font-family:monospace; border-radius:5px; font-size:14px; border: 1px solid #00ff00; pointer-events:none;">
                    PITCH: <span id="p">0.00</span> | YAW: <span id="y">0.00</span> <br>
                    <span id="status" style="color: #f1c40f; font-weight: bold;">Siap diklik!</span>
                </div>
                <script>
                    var viewer = pannellum.viewer('panorama', {{
                        "type": "equirectangular", "panorama": "{img_uri}", "autoLoad": true, "showControls": false
                    }});
                    
                    viewer.on('mousedown', function(event) {{
                        var coords = viewer.mouseEventToCoords(event);
                        var pitch = coords[0].toFixed(2);
                        var yaw = coords[1].toFixed(2);
                        
                        document.getElementById('p').innerText = pitch;
                        document.getElementById('y').innerText = yaw;
                        
                        var clipboardData = pitch + "\\t" + yaw;
                        var textArea = document.createElement("textarea");
                        textArea.value = clipboardData;
                        textArea.style.position = "fixed";
                        textArea.style.top = "0";
                        textArea.style.left = "0";
                        document.body.appendChild(textArea);
                        textArea.focus();
                        textArea.select();
                        try {{
                            document.execCommand('copy');
                            document.getElementById('status').innerText = "✓ TERSALIN! Klik sel Pitch -> Ctrl+V";
                            setTimeout(() => document.getElementById('status').innerText = "", 4000);
                        }} catch (err) {{
                            document.getElementById('status').innerText = "Gagal menyalin otomatis";
                        }}
                        document.body.removeChild(textArea);
                    }});
                </script>
            </body>
            </html>
            """
            components.html(html_preview, height=350)
            
            st.markdown("**2. Masukkan koordinat (Klik sel Pitch -> Ctrl+V):**")
            df_initial = pd.DataFrame({"Target Foto": [""], "Teks Hotspot": ["Maju ke depan"], "Pitch": [0.0], "Yaw": [0.0]})
            edited_df = st.data_editor(
                df_initial,
                column_config={
                    "Target Foto": st.column_config.SelectboxColumn("Pindah Ke Foto", options=nama_file_list, required=True),
                    "Teks Hotspot": st.column_config.TextColumn("Label Teks", required=True),
                    "Pitch": st.column_config.NumberColumn("Angka Pitch (Paste disini)", step=0.1),
                    "Yaw": st.column_config.NumberColumn("Angka Yaw", step=0.1)
                },
                num_rows="dynamic",
                key=f"editor_{i}",
                use_container_width=True
            )
            semua_hotspot_data[i] = edited_df

st.markdown("---")

# ==========================================
# 5. LOGIKA GENERATOR UTAMA
# ==========================================
if st.button("🚀 Generate Virtual Tour", type="primary", use_container_width=True, key="btn_generate_main"):
    if uploaded_files:
        with st.spinner("Memproses gambar, merakit Hotspot, dan menyiapkan ZIP..."):
            folder_proyek = "".join([c for c in nama_proyek if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
            base_path = os.path.join("Portal_Tour_360", folder_proyek, periode_str)
            os.makedirs(base_path, exist_ok=True)

            file_list = []
            b64_list = []
            
            for file in uploaded_files:
                file_path = os.path.join(base_path, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                file_list.append(file.name)
                encoded = base64.b64encode(file.getvalue()).decode()
                b64_list.append(f"data:image/jpeg;base64,{encoded}")

            footer_html_items = []
            for i, b64 in enumerate(b64_list):
                label_nama = custom_labels_dict[i] 
                item = f'<div class="thumb-container"><img src="{b64}" class="thumb" onclick="viewer.loadScene(\'scene_{i}\')"><div style="margin-top: 5px;">{label_nama}</div></div>'
                footer_html_items.append(item)
            footer_content = " ".join(footer_html_items)

            scenes_js = ""
            for i, name in enumerate(file_list):
                label_nama = custom_labels_dict[i] 
                hotspots_js_array = []
                df_hs = semua_hotspot_data[i]
                
                for index, row in df_hs.iterrows():
                    target_name = row["Target Foto"]
                    if pd.isna(target_name) or target_name == "":
                        continue 
                    target_idx = nama_file_list.index(target_name)
                    pitch = row["Pitch"]
                    yaw = row["Yaw"]
                    text = row["Teks Hotspot"]
                    hs_string = f'{{ "pitch": {pitch}, "yaw": {yaw}, "type": "scene", "text": "{text}", "sceneId": "scene_{target_idx}" }}'
                    hotspots_js_array.append(hs_string)
                
                gabungan_hotspot = ", ".join(hotspots_js_array)
                scenes_js += f'"scene_{i}": {{ "title": "{label_nama}", "type": "equirectangular", "panorama": "{name}", "hotSpots": [{gabungan_hotspot}] }},'

            password_proyek = USERS["tim_proyek"]["password"]
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <script>
                    (function() {{
                        if (localStorage.getItem("session_gis_waskita") !== "active") {{
                            alert("Sesi tidak ditemukan. Silakan login terlebih dahulu di Dashboard Utama.");
                            window.location.href = "../../../index.html"; 
                        }}
                    }})();
                </script>
                <title>{nama_proyek} | {tanggal_format_indo}</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css"/>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
                <style>
                    body {{ margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #000; overflow: hidden; }}
                    #main-content {{ width: 100vw; height: 100vh; position: relative; }}
                    #header {{ position: absolute; top: 0; width: 100%; background: rgba(0,0,0,0.8); color: white; padding: 15px 25px; z-index: 10; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; border-bottom: 2px solid #3498db; }}
                    #panorama {{ width: 100vw; height: 100vh; }}
                    #footer {{ position: absolute; bottom: 35px; width: 100%; background: rgba(0,0,0,0.7); padding: 12px; z-index: 10; display: flex; gap: 15px; overflow-x: auto; border-top: 1px solid #444; align-items: center; }}
                    .thumb-container {{ text-align: center; color: white; font-size: 11px; font-weight: bold; min-width: 100px; }}
                    .thumb {{ width: 110px; height: 65px; object-fit: cover; cursor: pointer; border: 2px solid #555; border-radius: 4px; transition: 0.2s; }}
                    .thumb:hover {{ border-color: #3498db; transform: scale(1.05); }}
                    #copyright-bar {{ position: absolute; bottom: 0; left: 0; width: 100%; background-color: #002d55; color: white; text-align: center; padding: 8px 0; font-size: 0.8em; z-index: 20; letter-spacing: 0.5px; }}
                </style>
            </head>
            <body>
                <div id="main-content">
                    <div id="header">
                        <div><strong>PROYEK:</strong> {nama_proyek}<br><span style="font-size: 0.8em;">Periode: {tanggal_format_indo}</span></div>
                        <a href="../../../index.html" style="background: #3498db; color: white; text-decoration: none; padding: 7px 18px; border-radius: 5px; font-weight: bold;">← Kembali</a>
                    </div>
                    <div id="panorama"></div>
                    <div id="copyright-bar">Tim GIS DS Divisi Infrastruktur PT Waskita Karya © 2026</div>
                    <div id="footer">{footer_content}</div>
                </div>
                <script>
                    // HAPUS FUNGSI checkPass(), SISA INISIALISASI PANNELLUM SAJA
                    var viewer = pannellum.viewer('panorama', {{
                        "default": {{ "firstScene": "scene_0", "autoLoad": true, "sceneFadeDuration": 1000 }},
                        "scenes": {{ {scenes_js} }}
                    }});
                </script>
            </body>
            </html>
            """            
            with open(os.path.join(base_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(html_template)
            
            relative_folder_path = f"Portal_Tour_360/{folder_proyek}/{periode_str}"
            update_projects_database(nama_proyek, relative_folder_path, tanggal_format_indo)
            
            zip_name_only = f"Tour360_{folder_proyek}_{periode_str}"
            path_untuk_zip = os.path.join(folder_proyek, periode_str)
            shutil.make_archive(zip_name_only, 'zip', root_dir="Portal_Tour_360", base_dir=path_untuk_zip)
            
            st.session_state["zip_name_only"] = zip_name_only
            st.session_state["tour_generated"] = True

        st.success(f"✅ Tur Berhasil Dibuat dan Tersimpan di Database Dashboard!")
        st.toast('Data berhasil disinkronkan ke Google Sheets!', icon='✅')
        st.toast('File ZIP siap diunduh.', icon='📦')
        st.snow()

# Tombol Download akan muncul setelah proses selesai dan aman dari reset Streamlit
if st.session_state.get("tour_generated"):
    zip_name_only = st.session_state["zip_name_only"]
    if os.path.exists(f"{zip_name_only}.zip"):
        st.info("📦 File kompresi siap diunduh. Pastikan mengunduh sebelum membuat tur baru.")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            with open(f"{zip_name_only}.zip", "rb") as f:
                st.download_button(
                    label="💾 Download ZIP (Struktur Folder)",
                    data=f,
                    file_name=f"{zip_name_only}.zip",
                    mime="application/zip",
                    use_container_width=True,
                    key="btn_download_final"
                )
        with col_dl2:
            st.link_button("🌐 Buka Album Virtual Tour", url="https://geoportal-wskt.github.io/360virtualtour/", use_container_width=True)


# ==========================================
# 6. FITUR ADMIN: EDIT / HAPUS GALERI
# ==========================================
if st.session_state.get("user_role") == "admin":
    st.markdown("---")
    st.subheader("🛠️ Manajemen Galeri Lokal (Admin Only)")
    
    path_portal = "Portal_Tour_360"
    if os.path.exists(path_portal):
        projects = [d for d in os.listdir(path_portal) if os.path.isdir(os.path.join(path_portal, d))]
        
        if projects:
            col_admin1, col_admin2 = st.columns(2)
            with col_admin1:
                sel_proj = st.selectbox("Pilih Proyek untuk Diedit", projects, key="admin_sel_proj")
            
            if sel_proj:
                dates = [d for d in os.listdir(os.path.join(path_portal, sel_proj))]
                if dates:
                    with col_admin2:
                        sel_date = st.selectbox("Pilih Tanggal Survey", dates, key="admin_sel_date")
                    
                    target_dir = os.path.join(path_portal, sel_proj, sel_date)
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(f"🗑️ Hapus Permanen {sel_date}", type="secondary", key="admin_btn_del"):
                            shutil.rmtree(target_dir)
                            st.warning(f"Folder {sel_date} telah dihapus dari server lokal.")
                            st.rerun()
                    
                    with col_btn2:
                        if st.button(f"👁️ Hide/Unhide Galeri", key="admin_btn_hide"):
                            if not sel_date.startswith("_HIDDEN_"):
                                os.rename(target_dir, os.path.join(path_portal, sel_proj, f"_HIDDEN_{sel_date}"))
                                st.info("Galeri berhasil disembunyikan.")
                            else:
                                new_date = sel_date.replace("_HIDDEN_", "")
                                os.rename(target_dir, os.path.join(path_portal, sel_proj, new_date))
                                st.success("Galeri ditampilkan kembali.")
                            st.rerun()
                else:
                    st.info("Belum ada tanggal/data pada proyek ini.")
        else:
            st.info("Belum ada proyek yang dibuat.")

        st.toast('Data berhasil disinkronkan ke Google Sheets!', icon='✅')
        st.toast('File ZIP siap diunduh.', icon='📦')