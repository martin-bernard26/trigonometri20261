import streamlit as st
import requests
from datetime import datetime

st.set_page_config(layout="wide")

tulisan_html = '''
<style>
#judul{
font-family:Elephant;
font-size:50px;
color:green;
text-shadow:2px 2px red, -2px -2px blue;
text-align:center;
}
#sub{
color:white;
text-shadow: 2px 2px 2px black, -2px -2px -2px black;
font-size:18px;
}
</style>
<body>
    <div id='judul'>Trigonometri</div>
    <div id='sub'>disusun oleh: Martin Bernard, M.Pd</div>
</body>
'''

st.components.v1.html(tulisan_html,height=200)

if "kumpulan" not in st.session_state:
    st.session_state["kumpulan"] = {"kover":True,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}

#=============

def diskusi():
    """
Diskusi Trigonometri — Streamlit + Firebase Realtime Database (REST, tanpa SDK)
================================================================================
Aplikasi forum diskusi sederhana untuk mata kuliah Trigonometri.

Integrasi ke Firebase dilakukan lewat REST API bawaan Firebase Realtime
Database (cukup HTTP GET/POST biasa via `requests`) — TANPA firebase-admin
SDK dan TANPA API key / kredensial apa pun. Ini bekerja karena Firebase
Realtime Database bisa diakses langsung lewat URL-nya selama Rules
mengizinkan akses publik (lihat panduan setup di bagian bawah aplikasi).

Cara menjalankan:
    pip install streamlit requests
    streamlit run diskusi_trigonometri_streamlit.py
"""

# https://diskusimatematika-7a30c-default-rtdb.firebaseio.com/
    FIREBASE_DB_URL = "https://diskusimatematika-7a30c-default-rtdb.firebaseio.com"

    TOPICS = [
    "Sudut & Radian",
    "Perbandingan Trigonometri",
    "Sudut-Sudut Berelasi",
    "Grafik Fungsi Trigonometri",
    "Identitas Trigonometri",
    "Diskusi Umum",
    ]

    TOPIC_COLORS = {
    "Sudut & Radian": "#2A4494",
    "Perbandingan Trigonometri": "#1C8A6E",
    "Sudut-Sudut Berelasi": "#B2455B",
    "Grafik Fungsi Trigonometri": "#D1552F",
    "Identitas Trigonometri": "#6B4FA0",
    "Diskusi Umum": "#636E85",
    }


    # ---------------------------------------------------------------------
    # Gaya tampilan
    # ---------------------------------------------------------------------
    st.markdown("""
<style>
    .msg-card{
        background:#FFFFFF; border:1px solid #E5E7EF; border-radius:12px;
        padding:14px 16px; margin-bottom:10px; border-left:4px solid var(--accent, #2A4494);
    }
    .msg-head{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px; }
    .msg-name{ font-weight:700; font-size:14.5px; color:#1B2436; }
    .msg-time{ font-size:11.5px; color:#8A93A6; font-family:monospace; }
    .msg-body{ font-size:14.5px; color:#1B2436; line-height:1.55; white-space:pre-wrap; }
    .topic-badge{
        display:inline-block; padding:4px 12px; border-radius:20px;
        font-size:12px; font-weight:700; color:#fff; margin-bottom:14px;
    }
</style>
    """, unsafe_allow_html=True)


    # ---------------------------------------------------------------------
    # Helper: akses Firebase Realtime Database lewat REST (tanpa SDK)
    # ---------------------------------------------------------------------
    def topic_key(topic: str) -> str:
        return topic.lower().replace(" ", "_").replace("&", "dan").replace("-", "_")


    def get_messages(topic: str):
        url = f"{FIREBASE_DB_URL}/diskusi/{topic_key(topic)}.json"
        try:
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return []
            items = [v for v in data.values() if isinstance(v, dict)]
            items.sort(key=lambda m: m.get("waktu", ""))
            return items
        except Exception as e:
            st.error(f"Gagal memuat diskusi dari Firebase: {e}")
            return []


    def post_message(topic: str, nama: str, pesan: str) -> bool:
        url = f"{FIREBASE_DB_URL}/diskusi/{topic_key(topic)}.json"
        payload = {
            "nama": nama,
            "pesan": pesan,
            "waktu": datetime.now().strftime("%d %b %Y, %H:%M"),
        }
        try:
            # POST ke endpoint .json akan membuat ID unik otomatis (seperti push()
            # pada SDK), murni lewat HTTP biasa — tidak ada API key yang dikirim.
            resp = requests.post(url, json=payload, timeout=8)
            resp.raise_for_status()
            return True
        except Exception as e:
            st.error(f"Gagal mengirim pesan ke Firebase: {e}")
            return False


    # ---------------------------------------------------------------------
    # UI
    # ---------------------------------------------------------------------
    st.title("📐 Diskusi Trigonometri")
    st.caption("Program Studi Pendidikan Matematika — IKIP Siliwangi")

    topic = st.selectbox("Pilih topik diskusi", TOPICS)
    color = TOPIC_COLORS.get(topic, "#2A4494")
    st.markdown(f'<span class="topic-badge" style="background:{color};">{topic}</span>', unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("🔄 Refresh diskusi"):
            st.rerun()

    messages = get_messages(topic)

    if not messages:
        st.info("Belum ada diskusi pada topik ini. Jadilah yang pertama bertanya atau menanggapi!")
    else:
        for m in messages:
            st.markdown(f"""
        <div class="msg-card" style="--accent:{color};">
            <div class="msg-head">
                <span class="msg-name">{m.get('nama', 'Anonim')}</span>
                <span class="msg-time">{m.get('waktu', '')}</span>
            </div>
            <div class="msg-body">{m.get('pesan', '')}</div>
        </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.subheader("Tulis Komentar / Pertanyaan")

    with st.form("form_diskusi", clear_on_submit=True):
        nama = st.text_input("Nama")
        pesan = st.text_area("Pesan", height=100, placeholder="Tulis pertanyaan atau tanggapan Anda tentang topik ini…")
        submitted = st.form_submit_button("Kirim")
        if submitted:
            if not nama.strip() or not pesan.strip():
                st.warning("Mohon isi nama dan pesan terlebih dahulu.")
            else:
                if post_message(topic, nama.strip(), pesan.strip()):
                    st.success("Pesan terkirim!")
                    st.rerun()

    with st.expander("⚙️ Panduan Setup Firebase (untuk dosen)"):
        st.markdown("""
Aplikasi ini terhubung ke **Firebase Realtime Database** lewat REST API bawaan
Firebase — **tanpa firebase-admin SDK dan tanpa API key** — sehingga dependensi
Python yang dibutuhkan hanya `streamlit` dan `requests`.

1. Buka [Firebase Console](https://console.firebase.google.com), lalu buat proyek baru (gratis, tidak perlu kartu kredit untuk paket Spark).
2. Di menu kiri pilih **Build → Realtime Database** → **Create Database** → pilih lokasi server → mulai dalam mode *test*.
3. Salin **URL database** yang tampil di bagian atas halaman (formatnya seperti `https://nama-proyek-default-rtdb.asia-southeast1.firebasedatabase.app`).
4. Tempelkan URL tersebut ke variabel `FIREBASE_DB_URL` di bagian atas kode ini.
5. Buka tab **Rules**, lalu gunakan aturan berikut agar node `diskusi` bisa diakses tanpa autentikasi (khusus untuk forum kelas):

```json
{
  "rules": {
    "diskusi": {
      ".read": true,
      ".write": true
    }
  }
}
```

6. ⚠️ Aturan di atas terbuka bagi siapa saja yang mengetahui URL database — cukup memadai untuk diskusi kelas jangka pendek, tetapi **jangan simpan data sensitif** dengan pengaturan ini. Setelah semester selesai, kosongkan Rules (`".write": false`) atau hapus database.
7. Jalankan aplikasi secara lokal dengan `streamlit run diskusi_trigonometri_streamlit.py`, atau deploy gratis ke [Streamlit Community Cloud](https://streamlit.io/cloud) agar mahasiswa dapat mengakses dari perangkat mana pun.
    """)

    st.caption("Martin Bernard, M.Pd. — IKIP Siliwangi, Program Studi Pendidikan Matematika")

#=============

def latar():
    tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/trigkov.html" width="100%" height="1500">
    </iframe>
    '''
    st.components.v1.html(tulisan_html1,height=1500)
def rancangan():
    menu = st.tabs(['RPS','Referensi'])
    with menu[0]:
        tulisan_html1='''
    <iframe src="https://drive.google.com/file/d/1of6dLByYZBM7IQS9k1LnVMzy3GCWcF6B/preview" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        with st.expander("Trigonometry version 2"):
            tulisan_html1='''
    <iframe src="https://drive.google.com/file/d/1Aj0dY_4rdNn4xrIR_phszuWAE5a3yJaI/preview" width="100%" height="1500">
    </iframe>
    '''
            st.components.v1.html(tulisan_html1,height=1500)
        with st.expander("Mathematic Trigonometry"):
            tulisan_html1='''
    <iframe src="https://drive.google.com/file/d/1rZNy0W3jBkWDUVPKRgPb0MZ5c8MpIpTl/preview" width="100%" height="1500">
    </iframe>
    '''
            st.components.v1.html(tulisan_html1,height=1500)
def testDiagnosa():
    tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/diagnosa.html" width="100%" height="1500">
    </iframe>
    '''
    st.components.v1.html(tulisan_html1,height=1500)
def modul1():
    menu = st.tabs(['Materi','Latihan'])
    with menu[0]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/trigonometri1.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/radian.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
def modul2():
    tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/trigonometri2.html" width="100%" height="1500">
    </iframe>
    '''
    st.components.v1.html(tulisan_html1,height=1500)

def modul3():
    menu = st.tabs(['Modul','Pengumpulan Tugas Grafik'])
    with menu[0]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/berelasi.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/latihan3.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    
def modul4():
    menu = st.tabs(['Modul','Latihan'])
    with menu[0]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/pertemuan4.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/latihan4.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
        
#==============

if st.session_state["kumpulan"]["kover"]:
    latar()
if st.session_state["kumpulan"]["referensi"]:
    rancangan()
if st.session_state["kumpulan"]["diagnosa"]:
    testDiagnosa()
if st.session_state["kumpulan"]["pertemuan1"]:
    modul1()
if st.session_state["kumpulan"]["pertemuan2"]:
    modul2()
if st.session_state["kumpulan"]["pertemuan3"]:
    modul3()
if st.session_state["kumpulan"]["pertemuan4"]:
    modul4()
if st.session_state["kumpulan"]["diskusian"]:
    diskusi()

#==============


if st.sidebar.button("Latar"):
    st.session_state["kumpulan"] = {"kover":True,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("RPS dan Referensi"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":True,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Test Diagnosa"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":True,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 1"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":True, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 2"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":True, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 3"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":True,
                                    "pertemuan4":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 4"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":True,"diskusian":False}
    st.rerun()
st.sidebar.markdown("---")
if st.sidebar.button("Forum Diskusi"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"diskusian":True}
    st.rerun()
