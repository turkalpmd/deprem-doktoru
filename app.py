from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import time
import matplotlib.image as mpimg
PAGE_TITLE = "Peditari Defteri"
PAGE_ICON = ":wave:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)
with st.sidebar:
    choose = option_menu("Pediatrik doz hesaplama", ["Rutin",
                                                     "Kritik ilaçlar",
                                                     "Antibiyotik",
                                                     "Tetanoz Profilaksisi",
                                                     "Glasgow Koma Skoru",
                                                     "CRUSH Sendromu",
                                                     "Hipotermi ve Yönetimi",
                                                     "ChatGPT",
                                                     "Uygulama geliştiricileri"
                                                     ],
                         icons=['bi bi-calculator-fill',
                                'life-preserver',
                                'bi bi-calculator-fill',
                                'bi bi-calculator-fill',
                                'bi bi-calculator-fill',
                                'wrench',
                                'thermometer-snow',
                                'cpu',
                                'person-badge'],
                         # icons = https://icons.getbootstrap.com/
                         menu_icon="app-indicator", 
                         default_index=0,
                         styles={
                                "container": {"padding": "5!important"},
                                "background-color": "#fafafa",
                                "icon": {"font-size": "25px"},
                                "color": "orange",
                                
                                "nav-link": {"font-size": "16px",
                                             "text-align": "left",
                                             "margin":"0px" },

                                "--hover-color": "#eee",
                                "nav-link-selected": {"background-color": "#02ab21"},
                                }
                        )

if choose == "Rutin":    
    st.title("Rutin Formüller")
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.info("Mayi Hesaplama")
        col2.warning("Vitaller")
        col3.error("Girişimsel formüller")
    with st.container():    
        st.info("Yaşı ay veya yıl olarak seçebilirsiniz")
        st.error("Kilo girilmezse yaşa göre tahmini kiloya göre sonuçlar hesaplanır")
        def Vital(age,age_type):
            if age_type == "year":
                age = age*12        
            if age<1:
                age_dict_index="0 gün - 1 ay"            
            if age>=1 and age<3:
                age_dict_index="≥1 ay-3 ay"
            if age>=3 and age<12:
                age_dict_index="≥3 ay-1 yaş"
            if age>=12 and age<24:
                age_dict_index="≥1 yaş-2 yaş"
            if age>=24 and age<48:
                age_dict_index="≥2 yaş-4 yaş"
            if age>=48 and age<60:
                age_dict_index="≥4 yaş-6 yaş"
            if age>=60 and age<120:
                age_dict_index="≥6 yaş-10 yaş"
            if age>=120 and age<156:
                age_dict_index="≥10 yaş-13 yaş"
            if age>=156:
                age_dict_index=">13 yaş"
            age_dict = {
                        "0 gün - 1 ay":[">205",">60","<60","<36 °C veya >38 °C"],
                        "≥1 ay-3 ay":[">205",">60","<70","<36 °C veya >38 °C"],
                        "≥3 ay-1 yaş":[">190",">60","<70","<36 °C veya >38.5 °C"],
                        "≥1 yaş-2 yaş":[">190",">40",f"<{int(70+(age/6))}","<36 °C veya >38.5 °C"],
                        "≥2 yaş-4 yaş":[">140",">40",f"<{int(70+(age/6))}","<36 °C veya >38.5 °C"],
                        "≥4 yaş-6 yaş":[">140",">34",f"<{int(70+(age/6))}","<36 °C veya >38.5 °C"],
                        "≥6 yaş-10 yaş":[">140",">30",f"<{int(70+(age/6))}","<36 °C veya >38.5 °C"],
                        "≥10 yaş-13 yaş":[">100",">30","<90","<36 °C veya >38.5 °C"],
                        ">13 yaş":[">100",">16","<90","<36 °C veya >38.5 °C"]
                        }
            df = pd.DataFrame({
                "Yaş":[age_dict_index],
                "Kalp hızı/dk":[age_dict[age_dict_index][0]],
                "Solunum sayısı/dk":[age_dict[age_dict_index][1]],
                "Sistolik Kan Basıncı (mmHg)":[age_dict[age_dict_index][2]],
                "Vücut Sıcaklığı":[age_dict[age_dict_index][3]],
            })
            return df,age_dict_index,age_dict[age_dict_index][0],age_dict[age_dict_index][1],age_dict[age_dict_index][2],age_dict[age_dict_index][3]
        def estimated_body_weight(age, unit="mo"):
            if unit == "mo":
                return np.round(((4 + age) / 2 if age < 12 else 8 + ((age / 12) * 2) if age < 120 else 3.3 * (age / 12)),2)
            else:
                return np.round(((4 + age) / 2 if age < 1 else 8 + (age * 2) if age < 10 else 3.3 * age),2)
        def ideal_kalori(yas, cinsiyet):
            kalori = {
                2: {'Erkek': 1250, 'Kız': 1250},
                3: {'Erkek': 1350, 'Kız': 1250},
                4: {'Erkek': 1500, 'Kız': 1350},
                5: {'Erkek': 1650, 'Kız': 1450},
                6: {'Erkek': 1800, 'Kız': 1600},
                7: {'Erkek': 1850, 'Kız': 1800},
                8: {'Erkek': 2050, 'Kız': 1900},
                9: {'Erkek': 2100, 'Kız': 2000},
                10: {'Erkek': 2300, 'Kız': 2050},
                11: {'Erkek': 2400, 'Kız': 2150},
                12: {'Erkek': 2450, 'Kız': 2250},
                13: {'Erkek': 2600, 'Kız': 2250},
                14: {'Erkek': 2750, 'Kız': 2200},
                15: {'Erkek': 2950, 'Kız': 2000},
                16: {'Erkek': 3050, 'Kız': 1800},
                17: {'Erkek': 3000, 'Kız': 1600},
                18: {'Erkek': 3000, 'Kız': 1500}
            }
            return kalori[yas][cinsiyet]
        def holiday_segar(kilo):
            if kilo <= 10:
                totalmayi = kilo * 100
            elif kilo <= 20:
                totalmayi = 1000 + (kilo - 10) * 50
            else:
                totalmayi = 1500 + (kilo - 20) * 20            
            na = int(3*totalmayi/100)
            k = int(2*totalmayi/100)
            nacl = na*2
            glu = totalmayi-nacl
            kalori = np.round((glu*0.05*4),2)
            hız = np.round((totalmayi/24),2)
            totalmayi = f"Holiday-Segar formülüne göre total mayi miktarı: {totalmayi} ml'dir, {nacl} ml %3 NaCl ve {k} ml KCl {glu} ml, %5'lik dekstroz ile hazırlanır ve {hız} mL/sacd hızda uygulanır (kalori miktarı = {kalori} kcal)."
            return totalmayi
        def VYA(kilo):
            return ((kilo*4)+7)/(kilo+90)
        def endotracheal_tube_diameter_child(age:int):
            diameter = 4 + (age / 4)
            ins_length = 12 + (age / 2)
            return f"Çapı: {diameter} ± 0.5 ve kaflı veya {diameter} ± 0.5 ve kafsız tüp ve insizyon uzunluğu: {ins_length} cm olacak şekilde önerilir"
        def calculate_cvc_size(weight):
            size_ranges = {
                (0, 3): "4F kateter Jugüler ven için 4 cm, Femoral ven için 5 cm",
                (3, 5): "4-4.5 Fr kateter Jugüler ven için 5 cm, Femoral ven için 8 cm",
                (5, 7): "4-4.5 Fr kateter Jugüler ven için 6 cm, Femoral ven için 8 cm",
                (7, 10): "4-4.5 Fr kateter Jugüler ven için 7 cm, Femoral ven için 8 cm",
                (10, 13): "4.5-5.5 Fr kateter Jugüler ven için 8 cm, Femoral ven için 13 cm",
                (13, 20): "4.5-5.5 Fr kateter Jugüler ven için 9 cm, Femoral ven için 13 cm",
                (20, 30): "5.5-7 Fr kateter Jugüler ven için 10 cm, Femoral ven için 16 cm",
                (30, 40): "5.5-7 Fr kateter Jugüler ven için 11 cm, Femoral ven için 16 cm",
                (40, 50): "7-8.5 Fr kateter Jugüler ven için 12 cm, Femoral ven için 16-20 cm",
                (50, 60): "7-8.5 Fr kateter Jugüler ven için 13 cm, Femoral ven için 16-20 cm",
                (60, 70): "7-8.5 Fr kateter Jugüler ven için 14 cm, Femoral ven için 16-20 cm",
                (70, 80): "7-8.5 Fr kateter Jugüler ven için 15 cm, Femoral ven için 16-20 cm",
                (80, float("inf")): "7-8.5 Fr kateter Jugüler ven için 16 cm, Femoral ven için 16-20 cm"
            }
            for range_, size in size_ranges.items():
                if weight < range_[1]:
                    return size      
            return f"SVK için {weight} ağırlığındaki çocukta {result} kateter kullanılması önerilir "   
        def urinary_catheter(age):
            result = "5-8" if age < 1 else "8" if age < 3 else "10" if age < 6 else "10-12" if age < 12 else "14"
            return f"{age} yaşındaki çocuk için {result} Fr idrar sondası kullanılmalıdır"
        def laringeal_maske_ve_cuff_vol(kilo):
            if kilo < 5:
                maske_numarasi, cuff_vol = 1, 4
            elif kilo < 10:
                maske_numarasi, cuff_vol = 1.5, 7
            elif kilo < 20:
                maske_numarasi, cuff_vol = 2, 10
            elif kilo < 30:
                maske_numarasi, cuff_vol = 2.5, 14
            elif kilo < 50:
                maske_numarasi, cuff_vol = 3, 20
            elif kilo < 70:
                maske_numarasi, cuff_vol = 4, 30
            else:
                maske_numarasi, cuff_vol = 5, 40
            return f"{kilo} kg bir çocuk için {maske_numarasi} numaralı LMA seçilir ve maks cuff volümü {cuff_vol} mL'dir"
        col1,col2=st.columns(2)
        ay = col1.number_input("Yaş (ay)", 0,217,0,1)
        yıl = col1.number_input("Yaş (yıl)", 0,18,0,1)
        kilo = col2.number_input("Ağırlık (kg)", 0,100,0,1)
        sex = col2.radio("Cinsiyet",("","Erkek","Kız"),horizontal=True,index=0)
        st.info("Kullanılacak ekipmanı seç: Endo trakeal tüp, Santral venöz katter, idrar sondası, LMA")
        tools = st.multiselect("Kullanılacak ekipmanı seç",["Endotrakeal tüp",
                                                            "Santral venöz kateter",
                                                            "İdrar Sondası",
                                                            "Laringeal maske",
                                                            ])        
        if st.button("Öneri al"):
            if sex=="Erkek" or sex=='Kız':
                if yıl:
                    ay = yıl*12
                    age_type = 'year'
                else:
                    age_type='mo'
                st.error("Sınır Değerler ÇAYD sayfasından alınmıştır")
                df,yaş_cat,hr,br,skb,temp = Vital(ay, age_type)
                st.table(df)
                tahmini_ağırlık  = estimated_body_weight(ay, unit="mo")
                if kilo:
                    st.info(f"Gerçek ağırlık: {kilo}")
                    kullanılan_kilo = "gerçek"
                else:
                    st.info(f"Tahmini ağırlık: {tahmini_ağırlık}")
                    kilo = tahmini_ağırlık
                    kullanılan_kilo = "tahmini"                
                vya = np.round((VYA(kilo)),2)
                st.info(f"Kiloya göre vücut yüzey alanı: {vya} m2")
                if ay>=24:
                    ideal_kalori_ = ideal_kalori(int(ay/12), sex)
                    st.info(f"{int(ay/12)} yaşındaki {sex} hasta için günlük ideal kalori : {ideal_kalori_} kcal/gün")
                if kilo>0:
                    st.info(holiday_segar(kilo))
                    st.warning("Bu solüsyon günlük kalori gereksiniminin %20’sini sağlar. Kısıtlı bir süre için (genellikle 5-7 günden kısa) bu karbonhidrat miktarı protein yıkımını önlemek için genellikle yeterlidir;\
                                ancak eğer daha uzun süreli bir parenteral tedavi gerekeceği ön görülüyorsa daha yüksek dekstrozlu solüsyonlar gerekecektir\
                                ve nihai dekstroz konsantrasyonu %10-12,5’u geçecekse santral venöz kateter ile verilmelidir.")
                if tools:
                    tools_dict = {
                    "Endotrakeal tüp":endotracheal_tube_diameter_child(int(ay/12)),
                    "Santral venöz kateter":calculate_cvc_size(kilo),
                    "İdrar Sondası":urinary_catheter(int(ay/12)),
                    "Laringeal maske":laringeal_maske_ve_cuff_vol(kilo),    
                    }
                    for i in range(len(tools)):
                        st.info(tools_dict[tools[i]])
            else:
                st.error("Cinsiyet seçmelisin!!")
if choose == "Kritik ilaçlar":
    units = {
    "Midazolam":"mg/kg/saat",
    "Lasix":"mg/kg/saat",
    "Fentanil":"mcg/kg/saat",
    "Precedex":"mcg/kg/saat",
    "Ketamin":"mcg/kg/dakika",
    "Dopamin":"mcg/kg/dakika",
    "Dobutamin":"mcg/kg/dakika",
    "Adrenalin":"mcg/kg/dakika",
    "Nöradrenalin":"mcg/kg/dakika",
    "Levosimendan":"mg/kg/dk",
    "Milrinon":"mcg/kg/dakika",
    "İnsülin":"ü/kg/saat",  
            }
    starter_dose =  {
    "Midazolam":0.1,
    "Lasix":0.1,
    "Fentanil":1,
    "Precedex":0.2,
    "Ketamin":5,
    "Dopamin":10,
    "Dobutamin":5,
    "Adrenalin":0.1,
    "Nöradrenalin":0.1,
    "Levosimendan":0.1,
    "Milrinon":0.25,
    "İnsülin":0.1,    
            }
    talimatlar =  {
    "Midazolam":"infüzyon",
    "Lasix":"infüzyon",
    "Fentanil":"infüzyon",
    "Precedex":"infüzyon",
    "Ketamin":"infüzyon",
    "Dopamin":"infüzyon",
    "Dobutamin":"infüzyon",
    "Adrenalin":"infüzyon",
    "Nöradrenalin":"infüzyon",
    "Levosimendan":"infüzyon",
    "Milrinon":"infüzyon",
    "İnsülin":"4 saatlik infüzyon",
            }
    def Doser(unit,dose,kg):
        if unit=="mg/kg/saat":
            return np.round((dose*kg*24),2)
        if unit=="mcg/kg/saat":
            return np.round((dose*kg*0.024),2)
        if unit=="mcg/kg/dakika":
            return np.round((dose*kg*1.44),2)         
        if unit=="ü/kg/saat":
            return np.round((dose*kg*24),2)
        if unit=="mg/kg/gün":
            return np.round((dose*kg),2)        
    st.header("Kiloya göre ilaç dozu hesaplama")
    st.write("Not: Önerilere açığız, geliştirilmeye devam edilecek, mobil uygulama geliştirilmekte")
    st.write("İletişim: aitech4med@gmail.com")
    st.write("İlaçlar günlük total doza göre hesaplanmıştır, yaygın kullanım talimatları tablo olarak verilmiştir")
    st.markdown("<center><a href = https://docs.google.com/document/d/e/2PACX-1vTZkrb9VVimmtUykF-6mPPgx-_XDpb3rGe5O6rzxKnxdcqBWQIWpPqRklV2tpQW08Mrn7BRMQvJC0Y4/pub ><h7 style= 'color: red;'> Ayrıntılı ve Geniş Bilgiler için ziyaret edebilirsiniz </h7></a></center>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
                drugs = st.multiselect('Dozunu hesaplanacak ilaçlar', [ "Midazolam",
                                                                        "Lasix",
                                                                        "Fentanil",
                                                                        "Precedex",
                                                                        "Ketamin",
                                                                        "Dopamin",
                                                                        "Dobutamin",
                                                                        "Adrenalin",
                                                                        "Nöradrenalin",
                                                                        "Milrinon",
                                                                        "İnsülin",
                                                                        ])        
        with col2:        
            kg = st.number_input(label="Ağırlık Kilogram",step=.1,format="%f")            
    with st.container():
        if st.button("Hesapla"):                
            for i in drugs:                    
                unit = units[i]
                dose = starter_dose[i]
                starter = Doser(unit,dose,kg)
                if i == "İnsülin":
                    st.write(f"{i} için günlük doz : {starter} ünite/gün")
                else:
                    st.write(f"{i} için günlük doz : {starter} mg/gün")                
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Heseplama Referansları ve Talimatlar")
    st.write("Maksiumum dozlar IV dozlara göre yazıldı, dozlar hasta kliniğine göre arttırılabilir")
    df = pd.read_csv("./table/drugs.csv")
    st.table(df[df.İlaç.isin(drugs)])            
if choose == "Antibiyotik":
    units = {
    "Ampisilin":"mg/kg/gün",
    "Sülbaktam ampisilin":"mg/kg/gün",
    "Amoksisilin klavunat":"mg/kg/gün",
    "Trimetoprim sulfameteksazol":"mg/kg/gün",
    "Vankomisin":"mg/kg/gün",
    "Meropenem":"mg/kg/gün",
    "Klaritromisin":"mg/kg/gün",
    "Sefiksim":"mg/kg/gün",
    "Siprofloksasin":"mg/kg/gün",
    "Metronidazol":"mg/kg/gün",
    "Seftriakson":"mg/kg/gün",
    "Klindamisin":"mg/kg/gün",
    "Sefazolin":"mg/kg/gün",
    "Flukanazol":"mg/kg/gün",
    "Amikasin":"mg/kg/gün",
    "Piperasilin tazobaktam":"mg/kg/gün",    
    "Gentamisin":"mg/kg/gün",
            }
    starter_dose =  {
    "Ampisilin":100,
    "Sülbaktam ampisilin":100,
    "Amoksisilin klavunat":80,
    "Trimetoprim sulfameteksazol":10,
    "Vankomisin":40,
    "Meropenem":60,
    "Klaritromisin":15,
    "Sefiksim":8,
    "Siprofloksasin":30,
    "Metronidazol":30,
    "Seftriakson":100,
    "Klindamisin":40,
    "Sefazolin":75,
    "Flukanazol":12,
    "Amikasin":15,
    "Piperasilin tazobaktam":300,
    "Gentamisin":7.5
            }
    talimatlar =  {
    "Ampisilin":"günde 4 kez max (12000 mg)",
    "Sülbaktam ampisilin":"günde 4 kez max (8000 mg)",
    "Amoksisilin klavunat":"günde 2 kez max (4000 mg)",
    "Trimetoprim sulfameteksazol":"günde 2 kez max (320 mg TMP)",
    "Vankomisin":"günde 4 kez max (yok)",
    "Meropenem":"günde 3 kez max (6000 mg)",
    "Klaritromisin":"günde 2 kez max (1000 mg)",
    "Sefiksim":"günde 2 kez max (800 mg)",
    "Siprofloksasin":"günde 2 kez max (1200 mg)",
    "Metronidazol":"günde 3 kez max (1500 mg)",
    "Seftriakson":"günde 2 kez max (4000 mg)",
    "Klindamisin":"günde 3 kez max (1800 mg)",
    "Sefazolin":"günde 3 kez max (3000 mg)",
    "Flukanazol":"günde 1 kez max (800 mg - ilk doz hesaplanan dozun 2 katı olarak)",
    "Amikasin":"günde 1 kez max (1500 mg)",
    "Piperasilin tazobaktam":"günde 4 kez max (16000 mg)",
    "Gentamisin":"günde 3 kez max (120 mg)",
            }
    def Doser(unit,dose,kg):
        if unit=="mg/kg/saat":
            return np.round((dose*kg*24),2)
        if unit=="mcg/kg/saat":
            return np.round((dose*kg*0.024),2)
        if unit=="mcg/kg/dakika":
            return np.round((dose*kg*1.44),2) 
        if unit=="ü/kg/saat":
            return np.round((dose*kg*24),2)
        if unit=="mg/kg/gün":
            return np.round((dose*kg),2)        
    st.header("Kiloya göre ilaç dozu hesaplama")
    st.write("Not: Önerilere açığız, geliştirilmeye devam edilecek, mobil uygulama geliştirilmekte")
    st.write("İletişim: aitech4med@gmail.com")
    st.write("İlaçlar günlük total doza göre hesaplanmıştır, yaygın kullanım talimatları tablo olarak verilmiştir")
    st.warning("Antibiyotikler nefrotoksik olabilir Crush sendromu açısından dikkat ediniz!")
    st.markdown("<center><a href = https://docs.google.com/document/d/e/2PACX-1vTZkrb9VVimmtUykF-6mPPgx-_XDpb3rGe5O6rzxKnxdcqBWQIWpPqRklV2tpQW08Mrn7BRMQvJC0Y4/pub ><h7 style= 'color: red;'> Ayrıntılı ve Geniş Bilgiler için ziyaret edebilirsiniz </h7></a></center>", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
                drugs = st.multiselect('Dozunu hesaplanacak ilaçlar', [
                                                                        "Ampisilin",
                                                                        "Sülbaktam ampisilin",
                                                                        "Amoksisilin klavunat",
                                                                        "Trimetoprim sulfameteksazol",
                                                                        "Vankomisin",
                                                                        "Meropenem",
                                                                        "Klaritromisin",
                                                                        "Sefiksim",
                                                                        "Siprofloksasin",
                                                                        "Metronidazol",
                                                                        "Seftriakson",
                                                                        "Klindamisin",
                                                                        "Sefazolin",
                                                                        "Flukanazol",
                                                                        "Amikasin",
                                                                        "Piperasilin tazobaktam"
                                                                        "Gentamisin"
                                                                        ])        
        with col2:            
            kg = st.number_input(label="Ağırlık Kilogram",step=.1,format="%f")            
    with st.container():
        if st.button("Hesapla"):                
            for i in drugs:                   
                unit = units[i]
                dose = starter_dose[i]
                starter = Doser(unit,dose,kg)
                st.write(f"{i} için günlük doz : {starter} mg/gün")               
    st.write("")
    st.write("")
    st.write("")
    st.subheader("Heseplama Referansları ve Talimatlar")
    st.write("Maksiumum dozlar IV dozlara göre yazıldı, dozlar hasta kliniğine göre arttırılabilir")
    df = pd.read_csv("./table/drugs.csv")
    st.table(df[df.İlaç.isin(drugs)])            
if choose=="Glasgow Koma Skoru":
    with st.container():
        col1, col2, col3 = st.columns(3)       
        with col2:
            st.subheader("Yaş Seçimi")
    with st.container():
        col1, col2, col3 = st.columns(3)        
        with col2:
            yaş = st.selectbox("Yaş Seçimi", ("2 yaş altı","2 yaş üstü"),index=0,label_visibility='hidden') 
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    with st.container():
        col1, col2, col3 = st.columns(3)
        if yaş=="2 yaş üstü":            
            with col1:
                goz = st.radio(
                                                "Göz", 
                                                    (
                                                        "Spontan açık",
                                                        "Sözel uyaranla açılıyor",
                                                        "Ağrılı uyaranla açılıyor",
                                                        "Yanıtsız"
                                                    )
                                                    )
            with col2:
                verbal = st.radio(
                                                "Verbal", 
                                                    (
                                                        "Oryente",
                                                        "Konfüze",
                                                        "Uygunsuz Kelimeler",
                                                        "Anlamsız Kelime ve Sesler",
                                                        "Yanıtsız"
                                                    )
                                                    )                                            
            with col3:
                motor = st.radio(
                                                "Motor", 
                                                    (
                                                        "Emirlere uyuyor",
                                                        "Ağrıyı lokalize ediyor",
                                                        "Ağrılı uyaran ile çekme",
                                                        "Fleksör tonus",
                                                        "Ekstansör tonus",
                                                        "Yanıtsız"
                                                    )
                                                    )                                            
                goz_map = {
                                                        "Spontan açık":4,
                                                        "Sözel uyaranla açılıyor":3,
                                                        "Ağrılı uyaranla açılıyor":2,
                                                        "Yanıtsız":1        
                }
                verbal_map = {
                                                        "Oryente":5,
                                                        "Konfüze":4,
                                                        "Uygunsuz Kelimeler":3,
                                                        "Anlamsız Kelime ve Sesler":2,
                                                        "Yanıtsız":1                    
                }
                motor_map = {
                                                        "Emirlere uyuyor":6,
                                                        "Ağrıyı lokalize ediyor":5,
                                                        "Ağrılı uyaran ile çekme":4,
                                                        "Fleksör tonus":3,
                                                        "Ekstansör tonus":2,
                                                        "Yanıtsız":1                    
                }     
            goz_score = goz_map[goz]
            verbal_score = verbal_map[verbal]
            motor_score = motor_map[motor]
        else:
            with col1:
                goz = st.radio(
                                                "Göz", 
                                                    (
                                                        "Spontan açık",
                                                        "Sözel uyaranla açılıyor",
                                                        "Ağrılı uyaranla açılıyor",
                                                        "Yanıtsız"
                                                    )
                                                    )
            with col2:
                verbal = st.radio(
                                                "Verbal", 
                                                    (
                                                        "Bıdılama, mırıldanma",
                                                        "Ağlama",
                                                        "Ağrılı uyaranla ağlama",
                                                        "Ağrılı uyaranla inilti",
                                                        "Yanıtsız",
                                                    )
                                                    )                                            
            with col3:
                motor = st.radio(
                                                "Motor", 
                                                    (
                                                        "Spontan hareketli",
                                                        "Dokunma ile çekme",
                                                        "Ağrılı uyaran ile çekme",
                                                        "Fleksör tonus",
                                                        "Ekstansör tonus",
                                                        "Yanıtsız"
                                                    )
                                                    )                                            
                goz_map = {

                                                        "Spontan açık":4,
                                                        "Sözel uyaranla açılıyor":3,
                                                        "Ağrılı uyaranla açılıyor":2,
                                                        "Yanıtsız":1

                }
                verbal_map = {

                                                        "Bıdılama, mırıldanma":5,
                                                        "Ağlama":4,
                                                        "Ağrılı uyaranla ağlama":3,
                                                        "Ağrılı uyaranla inilti":2,
                                                        "Yanıtsız":1,

                }
                motor_map = {

                                                        "Spontan hareketli":6,
                                                        "Dokunma ile çekme":5,
                                                        "Ağrılı uyaran ile çekme":4,
                                                        "Fleksör tonus":3,
                                                        "Ekstansör tonus":2,
                                                        "Yanıtsız":1

                }                
            goz_score = goz_map[goz]
            verbal_score = verbal_map[verbal]
            motor_score = motor_map[motor]
    with st.container():
        col1, col2, col3 = st.columns(3)        
        with col2:
            if st.button("Hesapla"):
                gks = goz_score+verbal_score+motor_score
                st.error(f"Glaskow Koma Skoru {gks}")   
                df = pd.read_csv("./table/gks.csv")
                df = df[[yaş,'Puanlama']]
                st.table(df)
if choose == "Tetanoz Profilaksisi":
    with st.container():
        col1, col2 = st.columns(2)        
        with col1:    
            asi = st.selectbox("Aşı durumu",(
                                                "Son 5 yılda aşı yapılmış - en az 3 aşılı",
                                                "Son 5-10 yılda aşı yapılmış - en az 3 aşılı",
                                                ">10 yılda aşı yapılmış - en az 3 aşılı",
                                                "Aşı durumu bilinmiyor - <3 aşılı"

            ))
        with col2:
            yara = st.selectbox("Yara durumu",(
                                                "Temiz yara",
                                                "Kirli yara"

            ))
            if yara == "Temiz yara":
                if asi == "Son 5 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı ve Tetanoz immünoglobine gerek yok"
                if asi == "Son 5-10 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı ve Tetanoz immünoglobine gerek yok"
                if asi == ">10 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı yapılmalıdır, Tetanoz immünoglobine gerek yok"
                if asi == "Aşı durumu bilinmiyor - <3 aşılı":
                    oneri = "Aşı yapılmalıdır, Tetanoz immünoglobine gerek yok"
            if yara == "Kirli yara":
                if asi == "Son 5 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı ve Tetanoz immünoglobine gerek yok"
                if asi == "Son 5-10 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı yapılmalıdır, Tetanoz immünoglobine gerek yok"
                if asi == ">10 yılda aşı yapılmış - en az 3 aşılı":
                    oneri = "Aşı yapılmalıdır, Tetanoz immünoglobine gerek yok"
                if asi == "Aşı durumu bilinmiyor - <3 aşılı":
                    oneri = "Aşı ve Tetanoz immünoglobini yapılmalıdır"     
    with st.container():
        if st.button("Sorgula"): 
            st.error(f"Tetanoz profilaksisi önerisi: {oneri}")               
if choose == "CRUSH Sendromu":
    def VYA(kilo):
        return ((kilo*4)+7)/(kilo+90)
    def Mayi(kilo,mayi=15,sf=0.5,duration=1):
        '''
        Mayi hesaplanırken 15 ml baz alındı 20 de seçilebilir
        Default Saatlik hesaplanacak, günlük de seçilebilir olacak
        '''
        total = kilo*duration*mayi
        if sf == 0.5:
            sf = total/2
            deks = total/2
            bikarb = np.round(((total/1000)*5),2)
            reçete = f" {duration} saat için total mayi: {total} mL'dir, {deks} mL %5 dekstroz ve {sf} mL %0.9 NaCl ve {bikarb} kadar bikarbonat ampülü ({10*bikarb} mL) ile hazırlayınız"
        else:
            sf = total
            reçete = f" {duration} saat için total mayi: {total} mL'dir,{sf} mL %0.9 NaCl ile hazırlayınız"            
        return reçete
    st.header("Crush Sendromunda Sıvı Uygulaması")
    with st.container():
        col1,col2,col3 = st.columns(3)
        col1.info("Afet Alanında")
        col2.warning("Transfer Anında")
        col3.error("Hastanede")
    with st.container():
        alan = st.selectbox("Konumu belirt", ("Afet Alanında","Transfer Anında","Hastanede"),index=2)
        if alan == "Afet Alanında":
            st.header("Afet Alanında Sıvı Uygulaması")
            col1, col2, col3  = st.columns(3)
            weight = col1.number_input("Ağırlık (kg)", value=0)
            duration = col2.number_input("Mayi süresi (saat)", value=0)
            maruziyet = col3.selectbox("Maruziyet süresi", ("Uzun","Kısa"))
            radio_choice = st.radio("", ("Damar Yolu Bulunduysa", "Enkaz altında damar yolu açılamadıysa"),horizontal=True)
            mayi = 15
            if weight>0 and duration>0:
                if st.button("Öneri oluştur"):
                    if maruziyet == "Uzun":
                        sf = 0.5
                    else:
                        sf = 1                 
                    if radio_choice == "Damar Yolu Bulunduysa":
                        st.write("1. Göçük altında ulaşılan ilk ekstremiteye damar yolu aç")
                        st.write(f"2. {Mayi(weight,mayi,sf,duration)}")
                        st.write("3. Uzun süre enkaz altında kalan hastada %0.45 NaCl %5 Dekstroz (1/2) içine 50 mEq/L bikarbonat eklenerek verilmelidir.")
                        st.write("4. Enkazdan çıkarılma 120 dk’dan uzun sürüyorsa sıvı tedavisi gözden geçirilmelidir; Sıvı 10 cc/kg/saate veya daha düşük bir seviyeye azaltılabilir.")
                        st.warning("5. Sıvıların içinde POTASYUM olmamasına dikkat edilmelidir.")
                        st.warning("6. Ringer laktat gibi potasyumlu sıvılardan kaçınılmalıdır.")
                    else:
                        st.write("1. İntraosseöz yol açılarak sıvı verilmeye çalışılmalıdır.")
                        st.write(f"2.{Mayi(weight,mayi,sf,duration)}")
                        st.write("3. Uzun süre enkaz altında kalan hastada %0.45 NaCl %5 Dekstroz (1/2) içine 50 mEq/L bikarbonat eklenerek verilmelidir.")
                        st.write("4. Enkazdan çıkarılma 120 dk’dan uzun sürüyorsa sıvı tedavisi gözden geçirilmelidir; sıvı 10 mL/kg/saate veya daha düşük bir seviyeye azaltılabilir.")                    
        if alan == "Transfer Anında":
            col1, col2, col3  = st.columns(3)
            weight = col2.number_input("Ağırlık (kg)", value=0)
            if st.button("Öneri oluştur"):
                if weight>0:
                    st.write(f"6 saatlik mayi %0.45 NaCl ve %5 dekstrozla; {Mayi(weight,10,0.5,6)}")
                    st.warning("Yakın vital bulgu ve yüklenme bulgularının takibi yapılmalıdır")
                    st.error("Crush Sendromu açısından idrar çıkarımını takip et!!")
                else:
                    st.error("Kilo 0 seçilemez!")        
        if alan == "Hastanede":    
            col1, col2,  = st.columns(2)
            weight = col1.number_input("Ağırlık (kg)", value=0)    
            #duration = col2.number_input("Süre (saat)", value=1)
            idrar = col2.selectbox("İdrar Çıkarımı", ("İdrar Çıkarımı","Anüri-Oligüri","İdrar Çıkarımı var"))            
            if idrar=="Anüri-Oligüri":
                cikardigi = st.number_input("Çıkardığı sıvı", value=0)
                totalmayi = np.round((400*VYA(weight)+cikardigi),2)
            else:
                totalmayi = np.round(3000*VYA(weight),2)
            komplikasyonlar = st.multiselect("Komplikasyonu seç",(
                                                                    "Rabdomiyoliz",
                                                                    "Akut Böbrek Yetmezliği",
                                                                    "Hiperpotasemi",
                                                                    "Hiperfosfatemi",
                                                                    "Erken hipokalsemi",
                                                                    "Geç hiperkalsemi",
                                                                    "Metabolik Asidoz",
                                                                    "Fasyotomi endikasyonları",
                                                                    "Ampütasyon endikasyonları"
                                        ))
            if weight>0:                                    
                if st.button("Önerileri Al"):
                    st.warning("Sıvı miktarını hastanın dehidratasyon belirtilerini, göçük altında geçirdiği süreyi, kan basıncını ve idrar çıkışını göz önüne alarak düzenleyin. Bu hesaplamalar size fikir sunmak amaçlıdır.")
                    st.warning("İdrar miktarı izleyin. Hastanın bilinci açıksa idrar yapıp yapmadığını sorun, kıyafetlerinde idrar kaçırdığına dair izler olup olmadığına bakın, idrar çıkışı yoksa mesane sondası takın")
                    st.warning("Serum üre, kreatinin, sodyum, potasyum, klor, kalsiyum, fosfor, ürik asit, kreatinin kinaz, kan gazı ve tam kan sayımı isteyin")
                    st.error("Sıvıya potasyum koymayın !!!")
                    if weight>0:
                        st.info(f"Total mayi: {totalmayi} mL/24sa")
                    st.warning("Rabdomiyoliz: serum kreatinfosfokinaz (CK) seviyelerinin 1000 U/’den fazla olması veya bazal degerinin beş katı yükselmesi ")
                    st.error("Crush sendromunda olası komplikasyonlar; ")
                    if "Rabdomiyoliz" in komplikasyonlar:
                        st.warning("Önleme ve tedavi")
                        st.write("CK <5000 unit/L olan hastalarda agresif sıvı tedavisine gerek yoktur, ancak daha yüksek olan hastalarda ABH’yı önlemek için CK <5000 ünit/L’nin altına inene kadar serum fizyolojik ile agresif sıvı tedavisi uygulanmalıdır.")
                        st.warning("Bikarbonat tedavisi şu durumda verilmelidir;")
                        st.write("CK >5000 unit/L ise")
                        st.write("Hipokalsemi yoksa")
                        st.write("Arteryal pH <7.5")
                        st.write("Serum bikarbonat değeri <30 mEq/L ise uygulanabilir.")
                        st.write("Hemolizi olan hastalara uygulanması önerilmez.")
                        st.write("Uygulamadan 3-4 saat sonra idrar pH >6.5 yükselmez ise tedavi kesilmelidir. Ayrıca semptomatik hipokalsemi gelişirse, HCO3 >30 mEq/L aşarsa ve arteryal pH >7.5 olursa tedavi kesilmelidir.")
                    if "Akut Böbrek Yetmezliği" in komplikasyonlar:        
                        st.info("Diyaliz endikasyonları:")
                        st.write("- Ağır volüm yükü (diüretik tedavisine cevap vermeyen hipertansiyon ve/veya pulmoner ödem)")
                        st.write("- Medikal tedaviye cevap vermeyen hiperpotasemi")
                        st.write("- Düzeltilemeyen ağır metabolik asidoz")
                        st.write("- Üremik ensefalopati, perikardit, kanama diyatezi")
                        st.write("- Kesin olmayan endikasyonlar: hiperfosfatemi (P > 15 mg/dL) ve hiperürisemi (ürik asit > 10 mg/dL)")
                        st.warning("Akut böbrek hasarının iki dönemi vardır: Oligürik ve poliürik dönem. Hasta oligürik dönemi, atlattıktan sonra poliürik döneme girer. Poliürik dönemde sıvı, sodyum, potasyum, kalsiyum kaybı artar. Bu kayıpların yerine konması gerekir.")
                    if "Hiperpotasemi" in komplikasyonlar:
                        hiperk = pd.read_csv("./table/hiperk.csv")
                        st.table(hiperk)
                    if "Hiperfosfatemi" in komplikasyonlar:
                        st.warning("Yemekler sırasında 2-4 çay kaşığı toz kalsiyum karbonat (CaCO3) veya 2-4 tablet Antifosfat tablet kullanın")
                    if "Erken hipokalsemi" in komplikasyonlar:
                        st.info("İV tedavi:")
                        st.write("Elemental Ca:100-200 mg/kg (%10 Ca glukonat 1-2 ml/kg/doz, maksimum 10 ml/doz bire bir sulandırılarak kardiyak monitorizasyon ile verilir.")
                        st.write("6-8 saatte bir doz tekrarlanabilir")
                        st.write("100 mg/dk hızından daha hızlı verilmez")
                        st.write("iv Ca, bikarbonat ile karıştırılmaz")
                        st.info("Oral tedavi:") 
                        st.write("Semptomlar düzeldikten sonra oral tedaviye geçilir;")
                        st.write("Elemental Ca: 50-100 mg/kg/gün 3-4 dozda verilir")
                    if "Geç hiperkalsemi" in komplikasyonlar:
                        st.info("1. Hiperkalsemi tedavisinde 4 ana strateji vardir;")
                        st.write("İntestinal Ca emilimini azaltmak")
                        st.write("İdrarla Ca atılımını arttırmak")
                        st.write("Kemik rezorbsiyonunu azaltmak")
                        st.write("Aşırı Ca’yı vücuttan temizlemek (diyaliz)")
                        st.warning("2. Hidrasyon: 3000 ml/m²/gün izotonik salin (böbrek fonksiyonları normal ise)")
                        st.warning("3. Loop diüretikleri: Furosemid 1 mg/kg/doz, 4 dozda")
                        st.warning("4. Hidrokortizon: 1 mg/kg/doz, 4 dozda veya glukokortikoidlerin ekivalan dozları.")
                        st.warning("5. Bifosfonatlar;")
                        st.write("Pamidronat: Hafif hiperkalsemide; 0.5-1 mg/kg/doz iv, Şiddetli hiperkalsemide; 1.5-2 mg/kg/doz iv")
                        st.write("Pamidronat başlangıçta suda dilüe edilir, fakat salin ya da dextrozda infüzyonu yapılır. 12 mg/100 ml’den daha fazla konsantre olmamalıdır.İlk infüzyon 4 saatte verilir sonraki günler 2-4 saatte verilir. Tedavi 3 gün üst üste verilir, sonraki kür 2-3 hafta veya 2-3 ay sonra verilir (hiperkalseminin şiddetine göre karar verilir).")
                        st.warning("6. Kalsitonin: başlangıç dozu; 4 IU/kg, 1-2 doz/gün, im veya sc  devamında; 8 IU/kg, 2-4 doz/gün")
                        st.error("7. Diyaliz: Düşük kalsiyumlu diyaliz")
                    if "Metabolik asidoz" in komplikasyonlar:
                        st.warning("İntravenöz veya oral sodyum bikarbonat (NaHCO3) kullanın, dirençli olduğu durumda hemodiyalizi hatırla!")
                    if "Fasyotomi endikasyonları" in komplikasyonlar:
                        st.write("Kompartman sendromunun en basit ve etkili tedavisi cerrahi olarak fasyaların açılmasıdır.")
                        st.write("Ekstremitesinde ezilme yaralanması olan tüm hastalarda kompartman sendromu gelişmemesi için profilaktik fasyotomi onerilmemektedir, kapalı ezilme yaralarında enfeksiyon, sepsis ve kronik sinir disfonksiyonu riski olduğundan kontrendikedir.")
                        st.write("Fasyotomi, ozellikledistal nabızların yoklugu veya kompartman basınçlarının dogrulanmış yükselmesiyle ilişkili akut kompartman sendromunun ilerleyen klinik belirtileri varsa yapılabilir.")
                    if "Ampütasyon endikasyonları" in komplikasyonlar:
                        st.error("Uzuvdaki yaralanmaların sepsis, sistemik enflamasyon veya kontrol edilemeyen kanamaya neden oldugu durumlarla onerilmektedir.")
                        st.warning("Bir çocuk ve ergen ruh sağlığı uzmanı eşliğinde hastaya bilgilendirme yapılması önerilir.")
                    if "Hiperbarik oksijen tedavisi" in komplikasyonlar:
                        st.warning("Hiperbarik oksijen tedavisinin (HBOT); Yara iyileşmesini iyileştirebilecegi ve ezilme yaralanmasında cerrahi girişimleri azaltabilecegi konusunda teorik ve sınırlı deneysel kanıtlar vardır.")
    st.markdown(""" <style> .font {
    font-size:15px ; font-family: 'Cooper Black'; color: #FFFF;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<a href= "http://cayd.org.tr/files/depremde-cocuk-hastaya-yaklasim-5q.pdf" ><p class="font" align="center">Çocuk Acil Tıp ve Yoğun Bakım Derneği Depremde Çocuk Hastaya Yaklaşım</p></a>', unsafe_allow_html=True)
    st.markdown('<a href= "https://ato.org.tr/files/documents/0820419001675761898.pdf" ><p class="font" align="center">CRUSH (EZİLME) SENDROMU: ÇOCUKLARDA TEDAVİ</p></a>', unsafe_allow_html=True)
    st.markdown('<a href= "https://www.cocuknefroloji.org/site//kitap/detail/1/cocUk-nefroloji-el-kitabi-%E2%80%93-klinik-pratik-yaklasimlar.html" ><p class="font" align="center">ÇOCUK NEFROLOJİ EL KİTABI – Klinik Pratik yaklaşımlar</p></a>', unsafe_allow_html=True)
if choose == "Hipotermi ve Yönetimi":
    st.title("Hipotermi ve Yönetimi")
    st.subheader("Çocuk Acil ve Yoğun Bakım Derneğinin kılavuzundan hazırlanmıştır")
    with st.container():
        yasamsal_bulgu = st.selectbox("Yasamsal bulgu var mı", options=["","Evet", "Hayır"],index=0)
        tedavi_onerileri = st.selectbox("Tedavi önerilerini göster", options=["","Evet", "Hayır"],index=0)
        if yasamsal_bulgu!="":
            st.info("Hastane öncesi tedavi")
            st.write("Hastane önc esi tedavide öncelikler hastanın dikkatle değerlendirilmesi, temel ve ileri yaşam desteği prensipleri doğrultusunda müdahale edilmesi,\
                      pasif ve aktif eksternal ısıtma uygulanması, ve hastanın uygun bir merkeze naklinin sağlanmasıdır. Hipotermik bir hastada nabzın alınması zor olabilir,\
                      yaşamsal bulgular ve nabız en az 60 saniye kontrol edilmelidir. Kardiopulmoner resüsitasyonu ve nakli geciktirmeyecek şekilde her hasta ısıtılmaya başlanmalıdır.\
                      Hastalara verilecek tüm sıvılar ısıtılmalı, sıvılar hastaların elektrolit ve pH Hastanın Nakli değerleri dikkate alınarak uygulanmalıdır.")
            if yasamsal_bulgu == "Evet":                                
                col1,col2 =st.columns(2)
                bilinc_degisikligi = col1.selectbox("Bilinc Değişikliği",options=["Bilinç Değişikliği","Evet", "Hayır"],index=0)
                yaralanma_bulgusu = col2.selectbox("Yaralanma Bulgusu", ("Yaralanma Bulgusu","Evet", "Hayır"),index=0)                              
                if bilinc_degisikligi == "Evet":
                    klinik = st.multiselect("Kliniğini seç", options=["Hiç biri yok","Hastane öncesi kardiak instabilite", "Sistolik kan basıncı yaşa göre hipertansiyon ile uyumlu", "Ventriküler aritmiler  ", "Kor sıcaklık < 28°C"])                            
                    if "Hiç biri yok" not in klinik:
                        st.error("ECMO ya da kardiopulmoner bypass ile hastaneye nakil") 
                        st.warning("Evre II veya III")
                        st.warning("Aritmileri engellemek için hareketleri kısıtla")
                        st.warning("Daha fazla ısı kaybını engelle")
                        st.warning("Aktif ekstarnal ve minimal invaziv ısıtma uygula")
                        st.warning("Havayolu güvenliğini sağla")
                        st.warning("Çevre ısısını arttır ve kıyafet giydir")                
                    elif klinik == ["Hiç biri yok"]:
                        st.error("En yakın hastaneye götür!")
                        st.warning("Evre II veya III")
                        st.warning("Aritmileri engellemek için hareketleri kısıtla")
                        st.warning("Daha fazla ısı kaybını engelle")
                        st.warning("Aktif ekstarnal ve minimal invaziv ısıtma uygula")
                        st.warning("Havayolu güvenliğini sağla")
                        st.warning("Çevre ısısını arttır ve kıyafet giydir")                                    
                    else:
                        st.write("Hiç biri yok seçeneği yalnız seçilmelidir!")
                if bilinc_degisikligi == "Hayır":                                                                      
                    if yaralanma_bulgusu == "Evet":
                        st.error("En yakın hastaneye nakil")
                        st.warning("Evre I Hipotermi")
                        st.warning("Çevreyi ısıt ve giydir")
                        st.warning("Islak giysilerini çıkart")
                        st.warning("Sıcak tatlı içecekler içir")
                        st.warning("Aktif hareket için cesaretlendir")                    
                    if yaralanma_bulgusu == "Hayır":
                        st.error("Alanda veya hastanede tedaviyi değerlendir")
                        st.warning("Evre I Hipotermi")
                        st.warning("Çevreyi ısıt ve giydir")
                        st.warning("Islak giysilerini çıkart")
                        st.warning("Sıcak tatlı içecekler içir")
                        st.warning("Aktif hareket için cesaretlendir")
            if yasamsal_bulgu == "Hayır":
                    klinik = st.multiselect("Klinik durumu seç", options=["Hiç biri yok","Açıkça ölüm olduğunu gösteren bulgular mevcut", "Kurtarıcı için güvensiz koşullar", "Karın altında kalma süresi >= 35 dk, havayolu karla kapanmış ve asistoli mevcut"])                    
                    if klinik:
                        if klinik==["Hiç biri yok"]:                            
                            st.error("Pediatrik ileri yaşam desteği prensiplerine uygun şekilde KPR'ye başla, nakli erteleme")
                            st.error("Daha fazla ısı kaybını önle")   
                            klinik2 = st.multiselect("Kilinik durumu seç", options=["Hiç biri yok","Soğumadan önce kardiyak arrest olmuş ise","Major travma", "Tanıklı normotermik arrest", "Karın altında kalma süresi < 35 dk"])                            
                            if klinik2:
                                if klinik2==["Hiç biri yok"]:
                                    st.error("ECMO veya Kardiopulmoner(KP) by-pass ihtiyacını belirlemek için hastayı değerlendir")                                    
                                    klinik3 = st.multiselect("Klinik durumu seç", options=["Vücut sıcaklığı <32°C", "Serum potasyum < 12 mEq/L"])                                    
                                    if klinik3:                                        
                                        if klinik3==["Vücut sıcaklığı <32°C", "Serum potasyum < 12 mEq/L"]:
                                            st.error("Evre IV Hipotermi")
                                            st.error("Ecmo veya kardiyopulumoner by-pass ile hastaneye nakil")
                                            st.error("KPR'yi sonlandırmayın")
                                            st.error("ECMO veya KP bypass ile yeniden ısıtın, ECMO veya KP bypass yoksa, aktif harici ve alternatif internal ısıtma ile KPR sağlayın")
                                            st.error("32°C derece sıcaklığa ulaştığında yeniden değerlendirin")
                                            klinik4 = st.selectbox("Dolaşımı değerlendirin", ("Dolaşımı değerlendirin","Kardiyak instabilite","Spontan dolaşım yok"),index=0)
                                            if klinik4:
                                                if klinik4 == "Spontan dolaşım yok":
                                                    st.error("KPR'yi sonlandırmayı düşün")
                                                if klinik4 == "Kardiyak instabilite":
                                                    st.error("Çoklu organ yetmezliği, ECMO ve solunum desteği ihtiyacı için hazırlanın")
                                                    st.error("Post-arrest yönetimi sağlayın")
                                                    st.error("Terapötik hipotermiyi düşünün")                                             
                                        else:
                                            st.error("KPR'yi sonlandırmayı düşün")                                       
                                else:
                                    st.error("KPR'yi sonlandırmayı düşün")
                        else:
                            st.error("KPR'yi sonlandırmayı düşün")    
        if tedavi_onerileri=="Evet":            
            st.warning("Havayolu, solunum ve dolaşım desteği (A,B,C)")
            st.write("● Servikalstabilizasyon sağlanarak havayolu açılmalı, O2 desteği verilmeli ")
            st.write("● Gerektiğinde ileri havayolu sağlanmalı ")
            st.write("● Sürekli EKG monitorizasyonu ve sıcaklık monitorizasyonu yapılmalı ")
            st.write("● Resüsitasyon yapılan hastalarda hasta yeterince ısıtılana kadar eksternal kardiyak masaja ara vermeden devam edilmeli Sıvı resüsitasyonu ")
            st.write("● Hafif hipotermik, bilinci yerinde, perfüzyonu yeterli olan hastalarda oral sıcak sıvılar verilmesi ile uygun hidrasyon sağlanabilir. Özellikle 24 saatten uzun sürmüş hipotermide ısınmayla birlikte artan sıvı ihtiyacı yakın izleme alınmalı")
            st.write("● Verilen tüm sıvılar ve kan ürünleri 38-42oC’ye kadar ısıtılarak verilmeli")
            st.write("● Pıhtılaşma bozukluğu belirgin olan hastalarda ısıtılmış taze donmuş plazma (10-15 ml/kg) volum replasmanında kullanılabilir.  ")
            st.write("● İzlemde hastanın kan basıncı ve kan biyokimyası (Na, K, Ca vb.) monitorize edilerek sıvı içeriği ve miktarı yönetilmelidir. ")
            st.write("● Santral venözkateterizasyon yapılabilir")
            st.write("● İdrar kateterizasyonu yapılmalı ve aldığı-çıkardığı yakın izlenmeli ")
            st.write("● Vazopressörler kullanılabilir, ancak aritmi riski ve soğuk ısırması olan hastalarda periferik doku perfüzyonunun bozulması nedeniyle dikkatli olunması gerekir. ")
            st.warning("KardiopulmonerResüsitasyon ")
            st.write("● Asfiksiden önce derin hipotermi gelişirse, uzun süreli kalp durmasından sonra bile bozulmamış tam nörolojik iyileşme mümkün olabilir. Hipotermi çok yavaş, küçük hacimli, düzensiz bir nabız ve hipotansiyona neden olacağı için hipotermik bir hastada ölüm teşhisi koyma konusunda dikkatli olunmalıdır. Hasta kardiyak monitorize edilmeli ve yaşamsal bulguları çok yakın gözlenmelidir. Hasta arrest ise standart kardiopulmoner resüsitasyon algoritması uygulanmalıdır. ")
            st.write("● Avrupa Resüsitasyon Birliği önerilerine göre vücut sıcaklığı 300C üzerine çıkana kadar epinefrin ve üç defaya kadar defibrilasyon yapılması önerilmektedir. Daha sonrasında pediatrik kardiopulmoner resüsitasyon rehberi doğrultusunda devam edilmelidir. ")
            st.warning("Yeniden ısınma / ısıtma ")
            st.write("● Kurtarılan hipotermik hastanın varsa ıslak giysileri çıkarılarak kurulanır. Asla cilt masajı, ovuşturulması, herhangi bir cisimle (kar vb.) ovulması gibi ikincil zararı arttıracak girişimler yapılmamalı")
            st.write("● Hafif hipotermide (≥32oC); özellikle titreme refleksinin olduğu bilincin ve perfüzyonun ileri derecede bozulmadığı hastalarda, kuru giysiler ve battaniye gibi örtülerle sararak pasif ısıtma yapılmalı")
            st.write("● Akut gelişen orta-ağır hipotermide (<32oC, 24 saatten kısa süreli); eksternal ve santral aktif ısıtma yapılır.  Aktif eksternal ısıtma için; rezistans telli elektrikli ısıtıcı, ısıtma lambaları, sıcak hava üflemeli ısıtıcılar, sıcak su torbaları, sıcak pedler kullanılabilir. Aktif santral ısıtma için; ")
            st.write("● Entübe hastada inhalasyon (sıcaklığı 44 oC’e ayarlanmış sulu-ısıtıcılı ventilatörle), 40-44 oC arasında ısıtılmış sıvılarla IV infüzyon, gastrik, rektal, peritoneal, torakostomi yapılarak mediastinal lavaj, periton diyalizi, hemodiyaliz, sürekli renal replasman tedavisi, modifiye ekstrakorporeyal kan ısıtma yapılarak kardiyopulmonerby-pass yöntemleri kullanılabilir. Isıtma sırasında santral sıcaklığın saatte 1-2 oC arttırılması hedeflenir. ")
            st.write("● Yeniden ısınma şoku, “after drop hipotermi” ve ısınma sonrası ventrikülerfibrilasyonu önlemek için önce santral ısınma sağlanıp sonra periferik ısıtma yapılmalıdır.  ")
            st.write("● Aktif eksternal ısıtma için seçici olarak baş ve gövde bölgesine uygulama yapılması da işe yarar bir önlemdir.  ")
            st.write("● Kronik orta-ağır hipotermide (<32oC, 24 saatten uzun süreli); santral aktif ısıtma yapılır. ")                        
            st.error("Aktif eksternal ısıtma için; rezistans telli elektrikli ısıtıcı, ısıtma lambaları, sıcak hava üflemeli ısıtıcılar, sıcak su torbaları, sıcak pedler kullanılabilir. ")
            st.warning("Aktif santral ısıtma için; ")
            st.write("● Entübe hastada inhalasyon (sıcaklığı 44 oC’e ayarlanmış sulu-ısıtıcılı ventilatörle), 40-44 oC arasında ısıtılmış sıvılarla IV infüzyon, gastrik, rektal, peritoneal, torakostomi yapılarak mediastinal lavaj, periton diyalizi, hemodiyaliz, sürekli renal replasman tedavisi, modifiye ekstrakorporeyal kan ısıtma yapılarak kardiyopulmonerby-pass yöntemleri kullanılabilir. Isıtma sırasında santral sıcaklığın saatte 1-2 oC arttırılması hedeflenir. ")
            st.write("● Yeniden ısınma şoku, “after drop hipotermi” ve ısınma sonrası ventrikülerfibrilasyonu önlemek için önce santral ısınma sağlanıp sonra periferik ısıtma yapılmalıdır.  ")
            st.write("● Aktif eksternal ısıtma için seçici olarak baş ve gövde bölgesine uygulama yapılması da işe yarar bir önlemdir.  ")
            st.error("Kronik orta-ağır hipotermide (<32oC, 24 saatten uzun süreli); santral aktif ısıtma yapılır.")
            st.warning("Lokal donma bakımı ")
            st.write("● Donmuş bölgenin tedavisinde dokudaki buz kristallerini eritmek, bölgeye kan dolaşımını sağlamak, re-perfüzyon hasarı yaratacak inflamasyonu kontrol altına almak ve ikincil trombotik hasarlanmayı önlemek hedeflenir.  ")
            st.write("● Donmuş organın 40-42 oC sıcak su banyosuna sokularak 15-30 dakika içinde hızla ısıtılması en uygun yaklaşımdır.  ")
            st.write("● Düşük sıcaklıkta yavaş yavaş ısınmayı beklemek ikincil hasarlanmayı arttırmaktadır. ")
            st.write("● Çözülen bölgenin tekrar donmasını önlemek ve çözülmenin ikincil sistemik etkilerinden korunmak için öncelikle hastanın sistemik hipotermi durumu düzeltilmiş olmalıdır. ")
            st.write("● Lokal ısınma tipik hiperemi şeklinde başlar ve olguların %75’inde narkotik analjezik gerektirecek kadar şiddetli ağrı eşlik eder.  ")
            st.write("● Çözülme sonrası canlı dokular enfeksiyon ve inflamatuar hasardan korunmalıdır.  ")
            st.write("● Lokal antiseptik sabunlu suya daldırma banyosu, bölgenin atele alınıp hareketsizleştirilmesi ve elevasyonu, narkotik analjezik, antiinflamatuar etki için oral ibuprofen, tetanoz proflaksisi, çözülmeyi izleyen 24 saat içinde başlayıp ödem gerileyene kadar antibiyotik proflaksisi önerilmektedir.  ")
            st.write("● Çözülen alandaki vezikül ve büllerin patlatılması, aspire edilmesi ya da olduğu gibi bırakılması, üzerinde uzlaşının olmadığı uygulamalardır.  ")
            st.write("● Donmalardan sonra ortalama %30 lokal enfeksiyon gelişimi gözlenir.             ")
    st.markdown(""" <style> .font {
    font-size:15px ; font-family: 'Cooper Black'; color: #FFFF;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<a href= "http://cayd.org.tr/files/depremde-cocuk-hastaya-yaklasim-5q.pdf" ><p class="font" align="center">Çocuk Acil Tıp ve Yoğun Bakım Derneği Depremde Çocuk Hastaya Yaklaşım ;</p></a>', unsafe_allow_html=True)
if choose == "ChatGPT":
    gptimg = Image.open(r'./images/gpt.jpg')
    st.image(gptimg)    
    st.error("OpenAI API'nin ücretsiz davinci-3 sürümü kullanılmaktadır. Ücretsiz olması nedeniyle günlük belirli kota aşıldığında yanıt alınamayacaktır :(")
    st.warning("Amazon Web Servislerinden Lambda Fonksiyonu kullanılarak sorgular oluşturulmaktadır, bu nedenle uzun sorgular tamamlanamayabilmektedir (güncel harf sınırı: 250)")
    st.info("Geliştirilecektir...")
    key_prompt = st.text_input("Sorgulamak istenen")
    if st.button("Sorgula.."):
        if len(key_prompt)>250:
            st.error("Daha kısa bir sorgu deneyiniz")
        else:
            with st.spinner("Tahmin oluşturuluyor..."):
                time.sleep(30)
                url = "API_URL_BY_LAMBDA"
            st.success(responsegpt.json())    
if choose == "Uygulama geliştiricileri":    
    profile = Image.open(r'./images/ai_med.jpg')    
    st.markdown(""" <style> .font {font-size:15px ; font-family: 'Cooper Black'; color: #FFFF;} </style> """, unsafe_allow_html=True)
    st.info("Proje yöneticisi")
    st.markdown('<a href= "https://github.com/turkalpmd" ><p class="font" align="center">TurkalpMD</p></a>', unsafe_allow_html=True)
    st.info("Geliştirici grup üyeleri")
    st.markdown('<a href= "https://lsc.hacettepe.edu.tr/ai_med.html" ><p class="font" align="center">AI_MED</p></a>', unsafe_allow_html=True)
    st.image(profile, width=700)
    st.info("Proje grubu destek verenler;")
    st.markdown('<a href= "https://github.com/KaganHanCatan" ><p class="font" align="center">Kağan Han Çatan</p></a>', unsafe_allow_html=True)
    st.markdown('<a href= "https://www.linkedin.com/in/zekakgun/" ><p class="font" align="center">Zekeriya Akgün</p></a>', unsafe_allow_html=True)
    st.markdown('<a href= "https://github.com/kaanozbudak" ><p class="font" align="center">Kaan Özbudak</p></a>', unsafe_allow_html=True)
    sponsor = Image.open(r'./images/aws.png')
    st.image(sponsor, width=700)
    st.success("AWS projemizi geliştirmemiz için 1500 dolarlık kredi tanımlamıştır")