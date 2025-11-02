"""
BASIT STREAMLIT UYGULAMASI
Kafe Sipariş Analizi için öğrenci dostu web arayüzü
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
import plotly.express as px
import plotly.graph_objects as go

# Sayfa ayarları
st.set_page_config(
    page_title="Kafe Menü Analizi",
    page_icon="☕",
    layout="wide"
)

# Ana başlık
st.title("☕ Kafe Menü Analizi")
st.markdown("---")
st.markdown("Bu uygulama, kafe siparişlerindeki ürün birlikteliklerini analiz eder.")

# Yan menü
st.sidebar.title("📋 Menü")
sayfa = st.sidebar.selectbox(
    "Analiz türünü seçin:",
    ["🏠 Ana Sayfa", "📊 Veri Görüntüleme", "🔍 Popüler Ürünler", "🔗 Birliktelik Analizi", "📋 Kural Analizi", "🎯 Ürün Önerileri"]
)

@st.cache_data
def veri_yukle():
    """CSV verisini yükler ve sepet formatına dönüştürür"""
    try:
        # 🔹 CSV dosyasını oku
        veri = pd.read_csv(r"C:\Users\Busenur Durak\Desktop\hafta6\data\groceries.csv")

        # 🔹 Sütun isimleri kontrolü
        if "Member_number" not in veri.columns or "itemDescription" not in veri.columns:
            st.error("❌ Veri setinde 'Member_number' veya 'itemDescription' sütunu bulunamadı!")
            st.stop()

        # 🔹 Her müşteri numarasına göre ürünleri grupla
        sepetler = veri.groupby("Member_number")["itemDescription"].apply(list).tolist()

        return veri, sepetler

    except FileNotFoundError:
        st.error("❌ groceries.csv dosyası bulunamadı! Dosya yolunu kontrol et.")
        return None, None


def urun_sayilarini_hesapla(sepetler):
    """Her ürünün kaç sepette olduğunu hesaplar"""
    urun_sayilari = {}
    for sepet in sepetler:
        for urun in sepet:
            urun_sayilari[urun] = urun_sayilari.get(urun, 0) + 1
    return urun_sayilari


def birliktelik_hesapla(sepetler, min_support=0.05):
    """Ürün birlikteliklerini hesaplar"""
    toplam_sepet = len(sepetler)
    min_sepet_sayisi = int(min_support * toplam_sepet)
    
    birliktelik_sayilari = {}
    
    for sepet in sepetler:
        if len(sepet) >= 2:
            for urun1, urun2 in combinations(sepet, 2):
                if urun1 > urun2:
                    urun1, urun2 = urun2, urun1
                
                cift = (urun1, urun2)
                birliktelik_sayilari[cift] = birliktelik_sayilari.get(cift, 0) + 1
    
    # Minimum desteği geçenleri filtrele
    onemli_birliktelikler = {}
    for cift, sayi in birliktelik_sayilari.items():
        if sayi >= min_sepet_sayisi:
            support = sayi / toplam_sepet
            onemli_birliktelikler[cift] = {
                'sepet_sayisi': sayi,
                'support': support
            }
    
    return onemli_birliktelikler


def kural_olustur(birliktelikler, urun_sayilari, toplam_sepet, min_confidence=0.3):
    """Association rules oluşturur"""
    kurallar = []
    
    for (urun1, urun2), bilgi in birliktelikler.items():
        birlikte_sayi = bilgi['sepet_sayisi']
        
        # Kural 1: urun1 → urun2
        confidence1 = birlikte_sayi / urun_sayilari[urun1]
        if confidence1 >= min_confidence:
            lift1 = confidence1 / (urun_sayilari[urun2] / toplam_sepet)
            kurallar.append({
                'antecedent': urun1,
                'consequent': urun2,
                'support': bilgi['support'],
                'confidence': confidence1,
                'lift': lift1
            })
        
        # Kural 2: urun2 → urun1
        confidence2 = birlikte_sayi / urun_sayilari[urun2]
        if confidence2 >= min_confidence:
            lift2 = confidence2 / (urun_sayilari[urun1] / toplam_sepet)
            kurallar.append({
                'antecedent': urun2,
                'consequent': urun1,
                'support': bilgi['support'],
                'confidence': confidence2,
                'lift': lift2
            })
    
    return sorted(kurallar, key=lambda x: x['confidence'], reverse=True)


# -----------------------------------------------------------------
# 🧠 SAYFALAR
# -----------------------------------------------------------------

veri, sepetler = veri_yukle()

if veri is not None and sepetler is not None:
    urun_sayilari = urun_sayilarini_hesapla(sepetler)

    if sayfa == "🏠 Ana Sayfa":
        st.header("Hoş Geldiniz ☕")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Toplam Sipariş Sayısı", len(sepetler))
        with col2:
            st.metric("Toplam Ürün Çeşidi", len(urun_sayilari))
        with col3:
            ortalama_urun = np.mean([len(sepet) for sepet in sepetler])
            st.metric("Ortalama Ürün/Sipariş", f"{ortalama_urun:.1f}")

        st.markdown("---")
        st.subheader("📖 Kafe Sipariş Analizi Nedir?")
        st.write("""
        Bu analiz, müşterilerin kafede hangi ürünleri birlikte sipariş ettiklerini 
        anlamak için kullanılır. Örneğin kahve ile tatlı mı, yoksa tost ile çay mı daha çok birlikte alınıyor?
        """)

    elif sayfa == "📊 Veri Görüntüleme":
        st.header("📊 Veri Görüntüleme")
        st.write("İlk 10 satır:")
        st.dataframe(veri.head(10))

        st.subheader("Örnek Siparişler")
        for i, sepet in enumerate(sepetler[:5], 1):
            st.write(f"**Sipariş {i}:** {', '.join(sepet)}")

    elif sayfa == "🔍 Popüler Ürünler":
        st.header("🔍 Popüler Ürünler")
        sorted_urunler = sorted(urun_sayilari.items(), key=lambda x: x[1], reverse=True)
        st.dataframe(pd.DataFrame(sorted_urunler, columns=["Ürün", "Sipariş Sayısı"]).head(10))

        fig = px.bar(
            x=[u for u, _ in sorted_urunler[:10]],
            y=[s for _, s in sorted_urunler[:10]],
            title="En Popüler Ürünler",
            color=[s for _, s in sorted_urunler[:10]],
            color_continuous_scale="viridis"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif sayfa == "🔗 Birliktelik Analizi":
        st.header("🔗 Ürün Birliktelikleri")
        min_support = st.slider("Minimum destek oranı", 0.01, 0.20, 0.05)
        if st.button("Birliktelik Analizi Yap"):
            birliktelikler = birliktelik_hesapla(sepetler, min_support)
            st.session_state["birliktelikler"] = birliktelikler
            st.success(f"{len(birliktelikler)} birliktelik bulundu!")
            st.dataframe(pd.DataFrame([
                {"Ürün 1": a, "Ürün 2": b, "Support": f"%{v['support']*100:.1f}"}
                for (a, b), v in birliktelikler.items()
            ]))

    elif sayfa == "📋 Kural Analizi":
        st.header("📋 Kural Analizi")
        if "birliktelikler" not in st.session_state:
            st.warning("⚠️ Önce 'Birliktelik Analizi' yapmalısınız.")
        else:
            min_conf = st.slider("Minimum Confidence", 0.1, 0.9, 0.3)
            if st.button("Kural Analizi Yap"):
                kurallar = kural_olustur(
                    st.session_state["birliktelikler"],
                    urun_sayilari, len(sepetler), min_conf
                )
                st.session_state["kurallar"] = kurallar
                st.dataframe(pd.DataFrame(kurallar).head(15))

    elif sayfa == "🎯 Ürün Önerileri":
        st.header("🎯 Ürün Önerileri")
        if "kurallar" not in st.session_state:
            st.warning("⚠️ Önce 'Kural Analizi' yapmalısınız.")
        else:
            kurallar = st.session_state["kurallar"]
            secilen_urun = st.selectbox("Bir ürün seçin:", sorted(urun_sayilari.keys()))
            oneri = [k for k in kurallar if k["antecedent"] == secilen_urun]
            if oneri:
                st.success(f"'{secilen_urun}' için {len(oneri)} öneri bulundu!")
                st.dataframe(pd.DataFrame(oneri).head(5))
            else:
                st.warning("Bu ürün için öneri bulunamadı.")

else:
    st.error("Veri yüklenemedi. Lütfen dosya yolunu kontrol et.")
