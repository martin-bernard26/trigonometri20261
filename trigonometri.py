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
    st.session_state["kumpulan"] = {"kover":True,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False}

#=============

def latar():
    tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/trigkov.html" width="100%" height="1500">
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
    tulisan_html1='''
    <iframe src="https://martin-bernard26.github.io/trigonometri2026/berelasi.html" width="100%" height="1500">
    </iframe>
    '''
    st.components.v1.html(tulisan_html1,height=1500)
#==============

if st.session_state["kumpulan"]["kover"]:
    latar()
if st.session_state["kumpulan"]["diagnosa"]:
    testDiagnosa()
if st.session_state["kumpulan"]["pertemuan1"]:
    modul1()
if st.session_state["kumpulan"]["pertemuan2"]:
    modul2()
if st.session_state["kumpulan"]["pertemuan3"]:
    modul3()

#==============


if st.sidebar.button("Latar"):
    st.session_state["kumpulan"] = {"kover":True,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False}
    st.rerun()
if st.sidebar.button("Test Diagnosa"):
    st.session_state["kumpulan"] = {"kover":False,"diagnosa":True,"pertemuan1":False, "pertemuan2":False, "pertemuan3":False}
    st.rerun()
if st.sidebar.button("Pertemuan 1"):
    st.session_state["kumpulan"] = {"kover":False,"diagnosa":False,"pertemuan1":True, "pertemuan2":False, "pertemuan3":False}
    st.rerun()
if st.sidebar.button("Pertemuan 2"):
    st.session_state["kumpulan"] = {"kover":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":True, "pertemuan3":False}
    st.rerun()
if st.sidebar.button("Pertemuan 3"):
    st.session_state["kumpulan"] = {"kover":False,"diagnosa":False,"pertemuan1":False, "pertemuan2":False, "pertemuan3":True}
    st.rerun()
