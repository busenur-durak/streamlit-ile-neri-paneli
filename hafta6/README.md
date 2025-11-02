# 🛒 Market Sepeti Analizi - Basit Versiyon

Bu proje, öğrencilerin **Market Basket Analysis** konusunu kolayca öğrenmesi için tasarlanmıştır.

## 📊 Kullanılan Veri

- **Dosya**: `data/basket_analysis.csv`
- **Format**: 999 satır (sepet) x 16 sütun (ürün)
- **İçerik**: Her hücre True/False - ürünün sepette olup olmadığını gösterir
- **Ürünler**: Apple, Bread, Butter, Cheese, Corn, Dill, Eggs, Ice cream, Kidney Beans, Milk, Nutmeg, Onion, Sugar, Unicorn, Yogurt, chocolate

## 🎯 Öğrenme Hedefleri

Bu proje ile öğrenciler şunları öğrenecek:

1. **Market Basket Analysis nedir?**
2. **Support, Confidence, Lift kavramları**
3. **Ürün birlikteliklerini nasıl bulabiliriz?**
4. **Association Rules nasıl oluşturulur?**
5. **Sonuçları nasıl yorumlarız?**

## 🚀 Nasıl Çalıştırılır?

### 1. Python ile Konsol Uygulaması

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Basit analizi çalıştır
python basit_market_analizi.py
```

### 2. Web Arayüzü (Streamlit)

```bash
# Virtual environment'ı aktifleştir
source venv/bin/activate

# Web uygulamasını başlat
streamlit run basit_streamlit_app.py
```

Tarayıcınızda açılan sayfada:
- 🏠 **Ana Sayfa**: Teorik bilgiler
- 📊 **Veri Görüntüleme**: Ham verileri inceleyin
- 🔍 **Popüler Ürünler**: En çok satılan ürünler
- 🔗 **Birliktelik Analizi**: Hangi ürünler birlikte alınıyor?
- 📋 **Kural Analizi**: "X alan Y'yi de alır" kuralları
- 🎯 **Ürün Önerileri**: Müşterilere ne önerebiliriz?

## 📖 Temel Kavramlar

### Support (Destek)
- Bir ürün veya ürün çiftinin ne kadar sık alındığı
- **Formül**: Support(A) = A içeren sepet sayısı / Toplam sepet sayısı
- **Örnek**: Milk %40 support → Sepetlerin %40'ında milk var

### Confidence (Güven)
- A ürününü alan müşterilerin kaçta kaçının B ürününü de aldığı
- **Formül**: Confidence(A→B) = Support(A,B) / Support(A)
- **Örnek**: Milk→Bread %60 confidence → Milk alan müşterilerin %60'ı bread da alıyor

### Lift
- İki ürünün birlikte alınma olasılığının tesadüfi duruma göre ne kadar güçlü olduğu
- **Formül**: Lift(A→B) = Confidence(A→B) / Support(B)
- **Yorum**:
  - Lift = 1: Tesadüfi birliktelik
  - Lift > 1: Pozitif birliktelik (birlikte alınma eğilimi var)
  - Lift < 1: Negatif birliktelik (birlikte alınma eğilimi yok)

## 🔍 Örnek Analiz Sonuçları

### En Popüler Ürünler
1. **chocolate**: 421 sepet (%42.1)
2. **Butter**: 420 sepet (%42.0)
3. **Yogurt**: 420 sepet (%42.0)

### En Güçlü Birliktelikler
- **Milk + chocolate**: 89 sepet (%8.9 support)
- **Bread + Butter**: 85 sepet (%8.5 support)
- **Yogurt + chocolate**: 83 sepet (%8.3 support)

### En İyi Association Rules
1. **Milk → chocolate**: %68 confidence, 1.6 lift
   - "Milk alan müşterilerin %68'i chocolate da alıyor"
2. **Bread → Butter**: %65 confidence, 1.5 lift
   - "Bread alan müşterilerin %65'i butter da alıyor"

## 💡 İş Uygulamaları

### Cross-Selling (Çapraz Satış)
- Milk alan müşterilere chocolate önerin
- Bread alan müşterilere butter önerin

### Mağaza Düzeni
- İlgili ürünleri yakın raflara koyun
- Milk ve chocolate'ı aynı bölümde bulundurun

### Kampanya Planlama
- Birlikte alınan ürünlerde "2. ürün %50 indirim" kampanyası
- Milk + chocolate paketi oluşturun

### Stok Yönetimi
- Birlikte alınan ürünlerin stoklarını birlikte planlayın
- Milk bitiyorsa chocolate da bitebilir

## 🎓 Öğrenci Egzersizleri

### Seviye 1: Başlangıç
1. En popüler 5 ürünü bulun
2. En az popüler 5 ürünü bulun
3. Ortalama sepet büyüklüğünü hesaplayın

### Seviye 2: Orta
1. Support > %10 olan ürün çiftlerini bulun
2. Confidence > %50 olan kuralları listeleyin
3. Lift > 1.5 olan birliktelikleri analiz edin

### Seviye 3: İleri
1. Farklı support/confidence threshold'ları deneyin
2. 3'lü ürün kombinasyonlarını araştırın
3. Özel ürün önerisi algoritması geliştirin

## 📊 Beklenen Çıktılar

### Konsol Uygulaması Çıktısı:
```
🛒 MARKET SEPETİ ANALİZİ
==========================================

📁 Veri yükleniyor...
✅ Veri yüklendi: 999 sepet, 16 ürün
✅ 999 sepet hazırlandı

📊 TEMEL İSTATİSTİKLER
==========================================
Toplam sepet sayısı: 999
Ortalama ürün/sepet: 8.2
En fazla ürün/sepet: 16
En az ürün/sepet: 1

En popüler 5 ürün:
  chocolate: 421 sepet (%42.1)
  Butter: 420 sepet (%42.0)
  Yogurt: 420 sepet (%42.0)
  ...
```

### Web Arayüzü Özellikleri:
- 📊 İnteraktif grafikler
- 🔧 Parametreleri değiştirme
- 🎯 Gerçek zamanlı öneri sistemi
- 📋 Detaylı açıklamalar

## ⚙️ Teknik Detaylar

### Gereksinimler
```
pandas>=1.5.0
numpy>=1.21.0
streamlit>=1.28.0
plotly>=5.15.0
matplotlib>=3.6.0
seaborn>=0.12.0
```

### Dosya Yapısı
```
hafta6/
├── data/
│   └── basket_analysis.csv          # Ana veri dosyası
├── basit_market_analizi.py          # Konsol uygulaması
├── basit_streamlit_app.py           # Web uygulaması
├── README_BASIT.md                  # Bu dosya
└── requirements.txt                 # Python gereksinimleri
```

## 🔧 Troubleshooting

### Problem: CSV dosyası bulunamıyor
**Çözüm**: `data/basket_analysis.csv` dosyasının doğru konumda olduğundan emin olun

### Problem: Streamlit açılmıyor
**Çözüm**: 
```bash
source venv/bin/activate
pip install streamlit
streamlit run basit_streamlit_app.py
```

### Problem: Grafikler görünmüyor
**Çözüm**: Plotly ve matplotlib yüklü olduğundan emin olun

## 📚 Ek Kaynaklar

- [Market Basket Analysis Nedir? (Türkçe)](https://example.com)
- [Association Rules Tutorial](https://example.com)
- [Streamlit Dokümantasyonu](https://docs.streamlit.io)

## 👨‍🏫 Eğitmenler İçin Notlar

### Ders Planı (2 saat)
1. **0-30 dk**: Teorik anlatım (Support, Confidence, Lift)
2. **30-60 dk**: Konsol uygulaması ile hands-on
3. **60-90 dk**: Web arayüzü ile etkileşimli analiz
4. **90-120 dk**: Öğrenci egzersizleri ve grup çalışması

### Değerlendirme Kriterleri
- Market Basket Analysis kavramlarını anlama
- Support/Confidence/Lift hesaplama
- Sonuçları doğru yorumlama
- İş uygulamalarını kavrama

### Ekstra Aktiviteler
- Farklı sector verisiyle analiz (online retail, e-commerce)
- Kendi veri seti oluşturma
- Gerçek business case çalışması

---

📧 **İletişim**: Bu proje hakkında sorularınız için...
🎓 **Seviye**: Başlangıç-Orta seviye veri bilimi öğrencileri
⏱️ **Süre**: 2-3 saat
🎯 **Hedef**: Market Basket Analysis temellerini öğrenmek