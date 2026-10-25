import streamlit as st
import requests
from datetime import datetime
import base64

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
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}

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
def modul5():
    menu = st.tabs(['Modul','Diskusi','Soal Tantangan','Latihan','Pembahasan'])
    with menu[0]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/pertemuan5.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/diskusi5.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
        st.markdown('---')
        st.title('Diskusi Mahasiswa')
        st.write('Masukan identitas Anda Nama dan NIM')
        alamat_url = 'https://diskusimatematika-7a30c-default-rtdb.firebaseio.com/soalTrig1.json'
        with st.form(key='Masukan_mahasiswa1',clear_on_submit=True):
            nama = st.text_input('Masukan Nama Anda')
            nim = st.text_input('Masunak NIM Anda')
            masukan = st.text_area('Masukan')
            tombol1 = st.form_submit_button('Kirimkan')
            if tombol1:
                if nama.strip()=="" or nim.strip()=="" or masukan.strip()=="":
                    st.error("Identitas Anda belum lengkap")
                else:
                    kumpulan={
                        "nama":nama,
                        "nim":nim,
                        "masukan":masukan
                        }
                    try:
                        response = requests.post(alamat_url,json=kumpulan)
                        if response.status_code==200:
                            st.success("Data Anda sudah Masuk")
                        else:
                            st.error("Data Anda Gagal Masuk")
                    except Exception as e:
                        st.error("Terjadi kesalahan di sistem")
        tekan = st.button("Lihat Pendapat Mahasiswa")
        if tekan:
            ambil_data = requests.get(alamat_url)
            st.write(ambil_data.json())
                    
    with menu[2]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/tantangan5.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)
        st.markdown('---')
        st.title('Form Masukan Mahasiswa')
        st.write('Silahkan masukan identitas dan aspirasi Anda di bawah ini.')
        firebase_url = 'https://diskusimatematika-7a30c-default-rtdb.firebaseio.com/identitas.json'
        with st.form(key='form_masukan',clear_on_submit=True):
            nama = st.text_input("Nama Lengkap")
            nim = st.text_input("NIM (Nomor Induk Mahasiswa)")
            masukan = st.text_area("Masukan/Kritik/Saran")
            submit_button = st.form_submit_button(label="Kirim Masukan")
        if submit_button:
            if nama.strip() == "" or nim.strip() == "" or masukan.strip()=="":
                st.error("Semua kolom harus diisi")
            else:
                payload = {
                    'nama':nama,
                    'nim':nim,
                    'masukan':masukan
                }
                try:
                    response = requests.post(firebase_url,json=payload)
                    if response.status_code == 200:
                        st.success("Terima kasuh!")
                    else:
                        st.error("Gagal menyimpan data")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"terjadi kesalahan koneksi: {e}")
                        
    with menu[3]:
        tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/latihan5.html" width="100%" height="1500">
    </iframe>
    '''
        st.components.v1.html(tulisan_html1,height=1500)

    with menu[4]:
        st.title("Menyelesaikan Diskusi")
        st.markdown('---')
        st.write("Diskusi Nomor 1")
        st.markdown('---')
        st.markdown('''
        ### Buktikan bahwa $\sin{\\theta}\\times{\\cot{\\theta}}=\\cos{\\theta}$
        #### diketahui bahwa $\cot{\\theta}=\\frac{\\cos{\\theta}}{\\sin{\\theta}}$ kebalikan rumus $\\tan{\\theta}=\\frac{\\sin{\\theta}}{\\cos{\\theta}}$
        #### Sehingga $\\sin{\\theta}\\times{\\cot{\\theta}}=\\sin{\\theta}\\times{\\frac{\\cos{\\theta}}{\\sin{\\theta}}}=\\cos{\\theta}$
        ''')
        st.markdown('---')
        st.write("Diskusi Nomor 2")
        st.markdown('---')
        url_gambar = 'https://res.cloudinary.com/dfkw4ux0e/image/upload/v1791868582/trig1_coasgk.png'
        st.image(url_gambar, caption="Gambar Segitiga Siku-siku", width=500)
        st.markdown('''
        ### Buktikan bahwa $1-\\cos^{2}{\\theta}=\\sin^{2}{\\theta}$
        #### diketahui bahwa $\\sin{\\theta}=\\frac{a}{c}$
        #### dan $\\cos{\\theta}=\\frac{b}{c}$
        ### Proses Pembuktian
        #### $$1-\\cos^{2}{\\theta}$$
        #### $$1-(\\frac{b}{c})^{2}$$
        ### Ubah 1 dengan $1=\\frac{1}{1}$
        #### $$\\frac{1}{1}-(\\frac{b}{c})^{2}$$
        #### $$\\frac{1}{1}-\\frac{b^2}{c^2}$$
        ### Samakan penyebutnya yaitu $c^{2}$
        #### $$\\frac{1}{1}-\\frac{b^{2}}{c^{2}}=\\frac{c^{2}}{c^{2}}-\\frac{b^{2}}{c^{2}}$$
        #### $$\\frac{c^{2}}{c^{2}}-\\frac{b^{2}}{c^{2}}=\\frac{c^{2}-b^{2}}{c^2}$$
        #### $$\\frac{c^{2}-b^{2}}{c^2}=\\frac{a^{2}}{c^{2}}$$ (Pythagoras)
        #### $$\\frac{a^{2}}{c^{2}}=(\\frac{a}{c})^{2}=\\sin{\\theta}$$
        ''')
        st.markdown('---')
        st.write("Diskusi Nomor 3")
        st.markdown('---')
        st.markdown('''
        ### Buktikan bahwa $\\sec^{2}{\\theta}-\\tan^{2}{\\theta}=1$
        #### diketahui bahwa $\\sec{\\theta}=\\frac{1}{\\cos{\\theta}}$ (Kebalikan)
        #### dan $\\tan{\\theta}=\\frac{\\sin^{2}{\\theta}}{\\cos{\\theta}}$
        ### Proses Pembuktian
        #### $$\\sec^{2}{\\theta}-\\tan^{2}{\\theta}=?$$
        #### $$\\sec^{2}{\\theta}-\\tan^{2}{\\theta}=(\\frac{1}{\\cos{\\theta}})^{2}-(\\frac{\\sin{\\theta}}{\\cos{\\theta}})^{2}$$
        ####  $$(\\frac{1}{\\cos{\\theta}})^{2}-(\\frac{\\sin{\\theta}}{\\cos{\\theta}})^{2}=\\frac{1}{\\cos^{2}{\\theta}}-\\frac{\\sin^{2}{\\theta}}{\\cos^{2}{\\theta}}$$
        ### Penyebutnya sudah sama yaitu $\\cos^{2}{\\theta}$
        #### $$\\frac{1}{\\cos^{2}{\\theta}}-\\frac{\\sin^{2}{\\theta}}{\\cos^{2}{\\theta}}=\\frac{1-sin^{\\theta}}{\\cos^{2}{\\theta}}$$
        ### ingat bahwa $\\sin^{2}{\\theta}+\\cos^{2}{\\theta}=1$ atau $1-\\sin^{2}{\\theta}=cos^{2}{\\theta}$
        #### $$\\frac{1-sin^{\\theta}}{\\cos^{2}{\\theta}}=\\frac{\\cos^{2}{\\theta}}{\\cos^{2}{\\theta}}=1$$
        ''')

def modul6():
    menu = st.tabs(['Modul','Latihan','Tugas HOTS','Pembahasan'])
    with menu[0]:
        tulisan_html1='''
        <iframe src="https://martin-bernard26.github.io/trigonometri2026/aturantrig.html" width="100%" height="1500">
        </iframe>
        '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        tulisan_html1='''
        <iframe src="https://martin-bernard26.github.io/trigonometri2026/latihan6.html" width="100%" height="1500">
        </iframe>
        '''
        st.components.v1.html(tulisan_html1,height=1500)
        st.title("Masukan Pendapat Mahasiswa")
        st.write("Isi identitas kemudian berikan masukan")
        firebase_url1 = 'https://diskusimatematika-7a30c-default-rtdb.firebaseio.com/disk6.json'
        with st.form(key='form_masukan1',clear_on_submit=True):
            nama = st.text_input("Nama Lengkap",key='nama1')
            nim = st.text_input("NIM (Nomor Induk Mahasiswa)",key='nim1')
            masukan = st.text_area("Masukan/Kritik/Saran",key='masukan1')
            submit_button = st.form_submit_button(label="Kirim Masukan")
        if submit_button:
            if nama.strip() == "" or nim.strip() == "" or masukan.strip()=="":
                st.error("Semua kolom harus diisi")
            else:
                payload = {
                    'nama':nama,
                    'nim':nim,
                    'masukan':masukan
                }
                try:
                    response = requests.post(firebase_url1,json=payload)
                    if response.status_code == 200:
                        st.success("Terima kasuh!")
                    else:
                        st.error("Gagal menyimpan data")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"terjadi kesalahan koneksi: {e}")
        tekan = st.button("Lihat Pendapat Mahasiswa1")
        if tekan:
            ambil_data = requests.get(firebase_url1)
            st.write(ambil_data.json())
        st.write("Diskusi Memecahkan Masalah")
        tulisan_html1='''
        <iframe src="https://martin-bernard26.github.io/trigonometri2026/diskusi6.html" width="100%" height="1500">
        </iframe>
        '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[2]:
        tulisan_html1='''
        <iframe src="https://martin-bernard26.github.io/trigonometri2026/hots6.html" width="100%" height="1500">
        </iframe>
        '''
        st.components.v1.html(tulisan_html1,height=1500)
        st.title("Masukan Tugas Mahasiswa")
        st.write("Isi identitas kemudian berikan masukan")
        GF_url = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLSdEX0bpBRbnXYAjbVlXuGUkWi8V9K5JWNW1HMgnWJhJBNRjRA/formResponse'
        with st.form(key='form_masukan2',clear_on_submit=True):
            nama = st.text_input("Nama Lengkap",key='nama2')
            nim = st.text_input("NIM (Nomor Induk Mahasiswa)",key='nim2')
            masukan = st.text_input("tugas berdasarkan alamat link Anda",key='tugas1')
            submit_button = st.form_submit_button(label="Kirim Masukan")
        if submit_button:
            if nama.strip() == "" or nim.strip() == "" or masukan.strip()=="":
                st.error("Semua kolom harus diisi")
            else:
                payload = {
                    'entry.128394463':nama,
                    'entry.68797093':nim,
                    'entry.33243599':masukan
                }
                try:
                    response = requests.post(GF_url,data=payload,timeout=10)
                    if response.status_code == 200:
                        st.success("Terima kasuh!")
                    else:
                        st.error("Gagal menyimpan data")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"terjadi kesalahan koneksi: {e}")
    with menu[3]:
        st.title("GeoGebra 🔗 Firebase Tanpa Kredensial (REST API) 🌍")
        FIREBASE_DB_URL = "https://diskusimatematika-7a30c-default-rtdb.firebaseio.com"
        NODE_PATH = "gambar_geogebra"
 
        st.title("📐 GeoGebra + Firebase Gallery")
        st.caption("Program Studi Pendidikan Matematika — IKIP Siliwangi")
        st.write(
    "Buat konstruksi apa saja di applet GeoGebra di sebelah kiri, simpan "
    "gambarnya ke Firebase, lalu lihat hasilnya muncul di galeri sebelah kanan."
        )
 
        col_ggb, col_gallery = st.columns([1.3, 1])
 
        # ----------------------------------------------------------------------
        # Kolom kiri: applet GeoGebra + tombol simpan (semuanya jalan di browser,
        # mengirim langsung ke Firebase lewat fetch() -- tidak lewat Python).
        # ----------------------------------------------------------------------
        with col_ggb:
            st.subheader("1. Buat Konstruksi")
            st.caption('Gambar apa saja, lalu isi nama Anda dan klik "Simpan Gambar ke Firebase".')
 
            geogebra_html = f"""
    <div id="ggb-element"></div>
    <div style="margin-top:12px; display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
      <input id="nama-input" type="text" placeholder="Nama Anda"
             style="flex:1; min-width:160px; padding:9px 11px; border:1px solid #ccc;
                    border-radius:8px; font-family:sans-serif; font-size:14px;">
      <button id="save-btn"
              style="padding:10px 18px; border:none; border-radius:8px; background:#2A4494;
                     color:#fff; font-weight:600; font-family:sans-serif; font-size:14px; cursor:pointer;">
        💾 Simpan Gambar ke Firebase
      </button>
    </div>
    <div id="status" style="margin-top:8px; font-family:sans-serif; font-size:13px; color:#555;"></div>
 
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <script>
      var FIREBASE_DB_URL = "{FIREBASE_DB_URL}";
      var NODE_PATH = "{NODE_PATH}";
 
      var params = {{
        appName: "classic",
        width: 680,
        height: 440,
        showToolBar: true,
        showAlgebraInput: true,
        showMenuBar: false,
        showResetIcon: true,
        enableRightClick: true,
        errorDialogsActive: false,
        useBrowserForJS: true
      }};
 
      window.addEventListener("load", function(){{
        var applet = new GGBApplet(params, true);
        applet.inject("ggb-element");
      }});
 
      function isFirebaseConfigured(){{
        return FIREBASE_DB_URL.indexOf("NAMA-PROYEK-ANDA") === -1;
      }}
 
      document.getElementById("save-btn").addEventListener("click", function(){{
        var statusEl = document.getElementById("status");
        var nama = document.getElementById("nama-input").value.trim() || "Anonim";
 
        if(!window.ggbApplet){{
          statusEl.textContent = "⏳ GeoGebra belum selesai dimuat, coba lagi sebentar.";
          return;
        }}
        if(!isFirebaseConfigured()){{
          statusEl.textContent = "⚠️ Firebase belum dikonfigurasi (lihat Panduan Setup di bawah aplikasi Streamlit).";
          return;
        }}
 
        statusEl.textContent = "Mengambil gambar dari GeoGebra…";
        var base64Png;
        try {{
          // scale=1, transparent=false, dpi=72 -- cukup untuk pratinjau galeri
          base64Png = window.ggbApplet.getPNGBase64(1, false, 72);
        }} catch(err) {{
          statusEl.textContent = "Gagal mengambil gambar: " + err;
          return;
        }}
 
        statusEl.textContent = "Mengunggah ke Firebase…";
        fetch(FIREBASE_DB_URL + "/" + NODE_PATH + ".json", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            nama: nama,
            gambar: base64Png,
            waktu: new Date().toLocaleString("id-ID", {{
              day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
            }})
          }})
        }})
        .then(function(r){{ if(!r.ok) throw new Error("HTTP " + r.status); return r.json(); }})
        .then(function(){{
          statusEl.textContent = "✅ Tersimpan! Klik \\"Refresh Galeri\\" di panel kanan Streamlit untuk melihatnya.";
        }})
        .catch(function(err){{
          statusEl.textContent = "❌ Gagal menyimpan ke Firebase: " + err;
        }});
      }});
    </script>
    """
 
            st.components.v1.html(geogebra_html, height=620, scrolling=True)
 
            # ----------------------------------------------------------------------
        # Kolom kanan: galeri -- Streamlit (Python) membaca ulang data dari
        # Firebase lewat REST API biasa (requests.get), lalu menampilkannya.
        # ----------------------------------------------------------------------
        with col_gallery:
            st.subheader("2. Galeri Gambar Tersimpan")
 
            if st.button("🔄 Refresh Galeri"):
                st.rerun()
 
            def is_configured() -> bool:
                return "NAMA-PROYEK-ANDA" not in FIREBASE_DB_URL
 
            if not is_configured():
                st.warning('Firebase belum dikonfigurasi. Buka "Panduan Setup Firebase" di bawah halaman ini.')
            else:
                try:
                    resp = requests.get(f"{FIREBASE_DB_URL}/{NODE_PATH}.json", timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                except Exception as e:
                    data = None
                    st.error(f"Gagal memuat galeri dari Firebase: {e}")
 
                if data:
                    items = [v for v in data.values() if isinstance(v, dict) and v.get("gambar")]
                    items.sort(key=lambda x: x.get("waktu", ""), reverse=True)
                    if not items:
                        st.info("Belum ada gambar tersimpan.")
                    for item in items:
                        try:
                            img_bytes = base64.b64decode(item["gambar"])
                            st.image(img_bytes, caption=f"{item.get('nama', 'Anonim')} · {item.get('waktu', '')}")
                        except Exception:
                            st.caption("(Satu entri gagal ditampilkan -- data gambar tidak valid.)")
                elif is_configured():
                    st.info("Belum ada gambar tersimpan. Buat konstruksi di sebelah kiri lalu simpan.")

def modul7():
    menu = st.tabs(['Modul','Video','Diskusi dengan Geogebra'])
    with menu[0]:
        tulisan_html1='''
        <iframe src="https://martin-bernard26.github.io/trigonometri2026/modulp7.html" width="100%" height="1500">
        </iframe>
        '''
        st.components.v1.html(tulisan_html1,height=1500)
    with menu[1]:
        st.title("Luas Segitiga")
        st.video("https://youtu.be/ABCMRSYRBys")
    with menu[2]:
        st.title("GeoGebra 🔗 Firebase Tanpa Kredensial (REST API) 🌍")
        FIREBASE_DB_URL = "https://diskusimatematika-7a30c-default-rtdb.firebaseio.com"
        NODE_PATH = "luas-segitiga/posts"
 
        st.title("📐 GeoGebra + Firebase Gallery")
        st.caption("Program Studi Pendidikan Matematika — IKIP Siliwangi")
        st.write(
    "Buat konstruksi apa saja di applet GeoGebra di sebelah kiri, simpan "
    "gambarnya ke Firebase, lalu lihat hasilnya muncul di galeri sebelah kanan."
        )
 
        col_ggb, col_gallery = st.columns([1.3, 1])
 
        # ----------------------------------------------------------------------
        # Kolom kiri: applet GeoGebra + tombol simpan (semuanya jalan di browser,
        # mengirim langsung ke Firebase lewat fetch() -- tidak lewat Python).
        # ----------------------------------------------------------------------
        with col_ggb:
            st.subheader("1. Buat Konstruksi")
            st.caption('Gambar apa saja, lalu isi nama Anda dan klik "Simpan Gambar ke Firebase".')
 
            geogebra_html = f"""
    <div id="ggb-element"></div>
    <div style="margin-top:12px; display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
      <input id="nama-input" type="text" placeholder="Nama Anda"
             style="flex:1; min-width:160px; padding:9px 11px; border:1px solid #ccc;
                    border-radius:8px; font-family:sans-serif; font-size:14px;">
      <button id="save-btn"
              style="padding:10px 18px; border:none; border-radius:8px; background:#2A4494;
                     color:#fff; font-weight:600; font-family:sans-serif; font-size:14px; cursor:pointer;">
        💾 Simpan Gambar ke Firebase
      </button>
    </div>
    <div id="status" style="margin-top:8px; font-family:sans-serif; font-size:13px; color:#555;"></div>
 
    <script src="https://www.geogebra.org/apps/deployggb.js"></script>
    <script>
      var FIREBASE_DB_URL = "{FIREBASE_DB_URL}";
      var NODE_PATH = "{NODE_PATH}";
 
      var params = {{
        appName: "classic",
        width: 680,
        height: 440,
        showToolBar: true,
        showAlgebraInput: true,
        showMenuBar: false,
        showResetIcon: true,
        enableRightClick: true,
        errorDialogsActive: false,
        useBrowserForJS: true
      }};
 
      window.addEventListener("load", function(){{
        var applet = new GGBApplet(params, true);
        applet.inject("ggb-element");
      }});
 
      function isFirebaseConfigured(){{
        return FIREBASE_DB_URL.indexOf("NAMA-PROYEK-ANDA") === -1;
      }}
 
      document.getElementById("save-btn").addEventListener("click", function(){{
        var statusEl = document.getElementById("status");
        var nama = document.getElementById("nama-input").value.trim() || "Anonim";
 
        if(!window.ggbApplet){{
          statusEl.textContent = "⏳ GeoGebra belum selesai dimuat, coba lagi sebentar.";
          return;
        }}
        if(!isFirebaseConfigured()){{
          statusEl.textContent = "⚠️ Firebase belum dikonfigurasi (lihat Panduan Setup di bawah aplikasi Streamlit).";
          return;
        }}
 
        statusEl.textContent = "Mengambil gambar dari GeoGebra…";
        var base64Png;
        try {{
          // scale=1, transparent=false, dpi=72 -- cukup untuk pratinjau galeri
          base64Png = window.ggbApplet.getPNGBase64(1, false, 72);
        }} catch(err) {{
          statusEl.textContent = "Gagal mengambil gambar: " + err;
          return;
        }}
 
        statusEl.textContent = "Mengunggah ke Firebase…";
        fetch(FIREBASE_DB_URL + "/" + NODE_PATH + ".json", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            nama: nama,
            gambar: base64Png,
            waktu: new Date().toLocaleString("id-ID", {{
              day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
            }})
          }})
        }})
        .then(function(r){{ if(!r.ok) throw new Error("HTTP " + r.status); return r.json(); }})
        .then(function(){{
          statusEl.textContent = "✅ Tersimpan! Klik \\"Refresh Galeri\\" di panel kanan Streamlit untuk melihatnya.";
        }})
        .catch(function(err){{
          statusEl.textContent = "❌ Gagal menyimpan ke Firebase: " + err;
        }});
      }});
    </script>
    """
 
            st.components.v1.html(geogebra_html, height=620, scrolling=True)
 
            # ----------------------------------------------------------------------
        # Kolom kanan: galeri -- Streamlit (Python) membaca ulang data dari
        # Firebase lewat REST API biasa (requests.get), lalu menampilkannya.
        # ----------------------------------------------------------------------
        with col_gallery:
            st.subheader("2. Galeri Gambar Tersimpan")
 
            if st.button("🔄 Refresh Galeri"):
                st.rerun()
 
            def is_configured() -> bool:
                return "NAMA-PROYEK-ANDA" not in FIREBASE_DB_URL
 
            if not is_configured():
                st.warning('Firebase belum dikonfigurasi. Buka "Panduan Setup Firebase" di bawah halaman ini.')
            else:
                try:
                    resp = requests.get(f"{FIREBASE_DB_URL}/{NODE_PATH}.json", timeout=10)
                    resp.raise_for_status()
                    data = resp.json()
                except Exception as e:
                    data = None
                    st.error(f"Gagal memuat galeri dari Firebase: {e}")
 
                if data:
                    items = [v for v in data.values() if isinstance(v, dict) and v.get("gambar")]
                    items.sort(key=lambda x: x.get("waktu", ""), reverse=True)
                    if not items:
                        st.info("Belum ada gambar tersimpan.")
                    for item in items:
                        try:
                            img_bytes = base64.b64decode(item["gambar"])
                            st.image(img_bytes, caption=f"{item.get('nama', 'Anonim')} · {item.get('waktu', '')}")
                        except Exception:
                            st.caption("(Satu entri gagal ditampilkan -- data gambar tidak valid.)")
                elif is_configured():
                    st.info("Belum ada gambar tersimpan. Buat konstruksi di sebelah kiri lalu simpan.")


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
if st.session_state["kumpulan"]["pertemuan5"]:
    modul5()
if st.session_state["kumpulan"]["pertemuan6"]:
    modul6()
if st.session_state["kumpulan"]["pertemuan7"]:
    modul7()
if st.session_state["kumpulan"]["diskusian"]:
    diskusi()


#==============


if st.sidebar.button("Latar"):
    st.session_state["kumpulan"] = {"kover":True,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("RPS dan Referensi"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":True,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Test Diagnosa"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":True,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 1"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":True, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 2"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":True, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 3"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":True,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 4"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":True,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 5"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":True,"pertemuan6":False,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 6"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":True,"pertemuan7":False,"diskusian":False}
    st.rerun()
if st.sidebar.button("Pertemuan 7"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":True,"diskusian":False}
    st.rerun()
st.sidebar.markdown("---")
if st.sidebar.button("Forum Diskusi"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False,"pertemuan5":False,"pertemuan6":False,"pertemuan7":False,"diskusian":True}
    st.rerun()

