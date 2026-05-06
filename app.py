import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import base64
import json  # <-- TAMBAHAN BARU: Wajib untuk membuat database dashboard
from datetime import datetime

st.set_page_config(page_title="GIS-DS 360 Generator", layout="wide")

# ==========================================
# FUNGSI UPDATE HUB DASHBOARD (VERSI JSON)
# ==========================================
# Fungsi ini menggantikan fungsi lama yang mengedit HTML statis, 
# sekarang fokus membuat projects.json untuk Dashboard Tailwind yang baru.
def update_projects_database(nama_proyek, path_relatif_folder, tanggal_str):
    db_path = "projects.json"
    
    # 1. Cek atau buat data awal
    if os.path.exists(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data_proyek = json.load(f)
        except:
            data_proyek = []
    else:
        data_proyek = []

    # 2. Siapkan entri baru
    new_entry = {
        "nama": nama_proyek,
        "path": path_relatif_folder,
        "tanggal": tanggal_str,
        "timestamp": datetime.now().strftime("%Y%m%d%H%M%S")
    }

    # 3. Masukkan jika belum ada (mencegah duplikat)
    if not any(d.get('path') == path_relatif_folder for d in data_proyek):
        data_proyek.append(new_entry)
        # Urutkan berdasarkan yang terbaru
        data_proyek.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # 4. Tulis ke file JSON
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data_proyek, f, indent=4)


# ==========================================
# UI APLIKASI UTAMA (TIDAK ADA YANG DIUBAH)
# ==========================================
st.title("🏗️ 360 Professional Tour Generator")
st.markdown("### Digital Survey & GIS - Divisi Infrastruktur")

st.subheader("1. Pengaturan Proyek")
col_proj, col_date = st.columns(2)

with col_proj:
    # Daftar Proyek Lengkap Divisi Infrastruktur
    list_proyek = [
        "PROYEK TOL JAPEK 2 SELATAN PAKET 3 INDUK",
        "Pelabuhan Patimban",
        "Probolinggo-Banyuwangi Paket 3 (JOP 25%)",
        "Proyek Jalan Kretek - Girijati",
        "Jalan Tol Ciawi Sukabumi Seksi 3A",
        "Patimban Acces Toll Road Package 2",
        "Tol Serang - Panimbang Seksi 3 JOI 27,5%",
        "Jalan Tol IKN Seksi 3B-2 : Segmen KKT Kariangau",
        "JALAN TOL CIAWI - SUKABUMI SEKSI 3B",
        "Pembangunan Jalan Kawasan Komplek Yudikatif",
        "Jln Singaraja - Mengwitani P01 (JOI 51%)",
        "Penanganan Bencana Alam Sumatera",
        "Jembatan Penghubung Pulau Kalimantan - Pulau Laut (JOI 20%)",
        "Penanganan Bencana Kota Langsa Aceh",
        "Jalan Kota Bireuen - Kota Takengon",
        "Jembatan Aras Sambilan II (Lubuk Sidup)",
        "Bendungan Bener Paket II JOP 83,5%",
        "Bendungan Tiga Dihaji (57%) JOI 57%",
        "Bendungan Jragung Paket 1",
        "PROYEK BENDUNGAN MBAY JOP 70%",
        "Pengarah Rukoh",
        "PROYEK PEMBANGUNAN IPAL 1,2,3 IKN JOI70%",
        "RENTANG IRRIGATION LOS 01 JOP 60%",
        "Pembangunan Bendungan Cibeet (JOI 57,9%)",
        "Bendungan Karangnongko Paket II JOI 55%",
        "PEMB. BANGUNAN PENGARAH BEND. RUKOH KAB.",
        "Pembangunan Struktur Jembatan Musi",
        "REHABILITASI D.I CIBALIUNG KABUPATEN PAN",
        "Bendungan Jragung Paket 4",
        "PERBAIKAN JALAN TOL KAPB JOP 70%",
        "Irigasi Belitang Lempuing Pkt 2 JOP 60%",
        "Irigasi Belitang Lempuing Pkt 3 JOP 60%",
        "Irigasi Belitang Lempuing Pkt 1 JOP 34%",
        "Jaringan Utama D.I Cimanuk Cisanggarung",
        "Construction Of KSCS Package 1 JOP 55%",
        "Jaringan Utama DI Sumatera II Tahap 3",
        "Jaringan Utama D.I Daerah NTT II Tahap 3",
        "Jaringan Utama D.I Sulsel Paket 4 Tahap 3",
        "Jaringan Utama D.I Kalimantan 4 Tahap 3",
        "Irigasi KSPP Kab. Merauke Pkt 1 JOP 50%",
        "Tanggap Darurat Bencana Alam Kabupaten Serdang B",
        "Pelabuhan Tanjung Priuk JICT",
        "Preservasi Sugih Waras-Muara Enim",
        "Jembatan Pendekat Pulau Laut-Tanah Bumbu",
        "Proyek Rehabilitasi Jaringan Irigasi D.I./D.I.R. Provinsi Sumatera Selatan",
        "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket I",
        "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket III",
        "Rehabilitasi D.I Kewenangan Daerah di Provinsi Banten Paket IV",
        "Lanjutan Pembangunan Bend Temef JOP 65%",
        "Pengaman Pantai KEK Tj. Lesung Paket 1",
        "Sedimentasi Bend Sumbawa JOI 65%",
        "PROYEK JEMBATAN KRAMASAN",
        "Rentang Irrigation Modernization Project",
        "JEMBATAN MUSI",
        "PROYEK PENGENDALI BANJIR BIMA",
        "JI Salamdarma Gadung Pawelutan JOP 60%",
        "Bendungan Rukoh Paket 2 JOP 58%",
        "Proyek Pengendalian Banjir Loji",
        "Peningkatan Jalan KIPP Paket D (JOI 65%)"
    ]
    
    # Menghapus duplikasi barangkali ada nama proyek yang sama persis
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
            
            # --- INPUT NAMA CUSTOM ---
            label_titik = st.text_input(
                f"🏷️ Nama Lokasi / STA", 
                value=f"Titik {i+1}", 
                key=f"label_{i}", 
                help="Teks ini akan muncul di thumbnail bawah dan sebagai judul panorama."
            )
            custom_labels_dict[i] = label_titik
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            b64 = base64.b64encode(file.getvalue()).decode()
            img_uri = f"data:image/jpeg;base64,{b64}"
            
            # --- LAYAR PREVIEW INTERAKTIF ---
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
                            document.getElementById('status').innerText = "✓ TERSALIN! Klik sel Pitch lalu tekan Ctrl+V";
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
            
            # --- TABEL MULTI-HOTSPOT ---
            st.markdown("**2. Masukkan koordinat (Klik sel Pitch -> Ctrl+V):**")
            
            df_initial = pd.DataFrame({
                "Target Foto": [""],
                "Teks Hotspot": ["Maju ke depan"],
                "Pitch": [0.0],
                "Yaw": [0.0]
            })
            
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

if st.button("🚀 Generate Virtual Tour", type="primary"):
    if uploaded_files:
        folder_proyek = "".join([c for c in nama_proyek if c.isalnum() or c in (' ', '_')]).strip().replace(" ", "_")
        base_path = os.path.join("Portal_Tour_360", folder_proyek, periode_str)
        os.makedirs(base_path, exist_ok=True)

        file_list = []
        b64_list = []
        
        with st.spinner("Memproses gambar dan merakit Multi-Hotspot..."):
            for file in uploaded_files:
                file_path = os.path.join(base_path, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                file_list.append(file.name)
                
                encoded = base64.b64encode(file.getvalue()).decode()
                b64_list.append(f"data:image/jpeg;base64,{encoded}")

            # Thumbnail Galeri Bawah dengan Custom Label
            footer_html_items = []
            for i, b64 in enumerate(b64_list):
                label_nama = custom_labels_dict[i] 
                item = f'<div class="thumb-container"><img src="{b64}" class="thumb" onclick="viewer.loadScene(\'scene_{i}\')"><div style="margin-top: 5px;">{label_nama}</div></div>'
                footer_html_items.append(item)
            footer_content = " ".join(footer_html_items)

            # Logika Scene dengan Custom Label
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

            # Template HTML Utama
            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{nama_proyek} | {tanggal_format_indo}</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css"/>
                <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
                <style>
                    body {{ margin: 0; font-family: sans-serif; background: #000; overflow: hidden; }}
                    #header {{ position: absolute; top: 0; width: 100%; background: rgba(0,0,0,0.8); color: white; padding: 15px 25px; z-index: 10; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; border-bottom: 2px solid #3498db; }}
                    #panorama {{ width: 100vw; height: 100vh; }}
                    #footer {{ position: absolute; bottom: 35px; width: 100%; background: rgba(0,0,0,0.7); padding: 12px; z-index: 10; display: flex; gap: 15px; overflow-x: auto; border-top: 1px solid #444; align-items: center; }}
                    .thumb-container {{ text-align: center; color: white; font-size: 11px; font-weight: bold; min-width: 100px; }}
                    .thumb {{ width: 110px; height: 65px; object-fit: cover; cursor: pointer; border: 2px solid #555; border-radius: 4px; transition: 0.2s; }}
                    .thumb:hover {{ border-color: #3498db; transform: scale(1.05); }}
                    #back-btn {{ background: #3498db; color: white; text-decoration: none; padding: 7px 18px; border-radius: 5px; font-weight: bold; }}
                    #copyright {{ position: absolute; bottom: 110px; right: 20px; color: rgba(255,255,255,0.4); font-size: 0.75em; z-index: 5; }}
                    #copyright-bar {{ position: absolute; bottom: 0; left: 0; width: 100%; background-color: #002d55; color: white; text-align: center; padding: 8px 0; font-size: 0.8em; z-index: 20; letter-spacing: 0.5px; }}
                </style>
            </head>
            <body>
                <div id="header">
                    <div><strong>PROYEK:</strong> {nama_proyek}<br><span style="font-size: 0.8em;">Periode: {tanggal_format_indo}</span></div>
                    <a href="../../../index.html" id="back-btn">← Kembali ke Hub</a>
                </div>
                <div id="panorama"></div>
                <div id="copyright-bar">Tim GIS DS Divisi Infrastruktur PT Waskita Karya © 2026</div>
                <div id="footer">{footer_content}</div>
                <script>
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
            
            # --- PEMANGGILAN FUNGSI BARU ---
            relative_folder_path = f"Portal_Tour_360/{folder_proyek}/{periode_str}"
            update_projects_database(nama_proyek, relative_folder_path, tanggal_format_indo)
            
        st.success(f"✅ Tur Berhasil Dibuat dan Tersimpan di Database Dashboard!")
        st.balloons()