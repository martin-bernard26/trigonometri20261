import streamlit as st

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
                                    "pertemuan4":False}

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

#==============


if st.sidebar.button("Latar"):
    st.session_state["kumpulan"] = {"kover":True,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("RPS dan Referensi"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":True,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("Test Diagnosa"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":True,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("Pertemuan 1"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":True, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("Pertemuan 2"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":True, "pertemuan3":False,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("Pertemuan 3"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":True,
                                    "pertemuan4":False}
    st.rerun()
if st.sidebar.button("Pertemuan 4"):
    st.session_state["kumpulan"] = {"kover":False,"referensi":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False,
                                    "pertemuan4":True}
    st.rerun()
