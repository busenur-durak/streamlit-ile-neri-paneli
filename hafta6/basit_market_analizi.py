"""
BASIT MARKET SEPETİ ANALİZİ
Bu dosya öğrenciler için Market Basket Analysis'in temellerini öğretmek amacıyla yazılmıştır.
"""

import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns


class BasitMarketAnalizi:
    """
    Market Sepeti Analizi için basit ve anlaşılır sınıf
    """
    
    def __init__(self):
        self.veri = None
        self.sepetler = []
        self.urun_sayilari = {}
        self.birliktelikler = {}
        
    def veri_yukle(self, dosya_yolu):
        """
        Veriyi yükler ve sepet formatına çevirir
        """
        print("📁 Veri yükleniyor...")
        
        # CSV dosyasını oku
        self.veri = pd.read_csv(dosya_yolu, index_col=0)
        print(f"✅ Veri yüklendi: {self.veri.shape[0]} sepet, {self.veri.shape[1]} ürün")
        
        # Sepetleri oluştur (True olan ürünleri liste haline getir)
        for i, satir in self.veri.iterrows():
            sepet = []
            for urun in self.veri.columns:
                if satir[urun] == True or satir[urun] == 'True':
                    sepet.append(urun)
            if sepet:  # Boş sepetleri ekleme
                self.sepetler.append(sepet)
        
        print(f"✅ {len(self.sepetler)} sepet hazırlandı")
        return self.veri
    
    def temel_istatistikler(self):
        """
        Veri hakkında temel bilgileri gösterir
        """
        print("\n📊 TEMEL İSTATİSTİKLER")
        print("=" * 40)
        
        # Toplam sepet sayısı
        print(f"Toplam sepet sayısı: {len(self.sepetler)}")
        
        # Her sepetteki ortalama ürün sayısı
        sepet_boyutlari = [len(sepet) for sepet in self.sepetler]
        print(f"Ortalama ürün/sepet: {np.mean(sepet_boyutlari):.1f}")
        print(f"En fazla ürün/sepet: {max(sepet_boyutlari)}")
        print(f"En az ürün/sepet: {min(sepet_boyutlari)}")
        
        # Ürün popülaritesi
        self._urun_popularitesini_hesapla()
        
        print(f"\nEn popüler 5 ürün:")
        sorted_urunler = sorted(self.urun_sayilari.items(), key=lambda x: x[1], reverse=True)
        for urun, sayi in sorted_urunler[:5]:
            yuzde = (sayi / len(self.sepetler)) * 100
            print(f"  {urun}: {sayi} sepet (%{yuzde:.1f})")
    
    def _urun_popularitesini_hesapla(self):
        """
        Her ürünün kaç sepette olduğunu hesaplar
        """
        self.urun_sayilari = {}
        for sepet in self.sepetler:
            for urun in sepet:
                if urun in self.urun_sayilari:
                    self.urun_sayilari[urun] += 1
                else:
                    self.urun_sayilari[urun] = 1
    
    def popular_urunleri_goster(self, top_n=10):
        """
        En popüler ürünleri grafik olarak gösterir
        """
        if not self.urun_sayilari:
            self._urun_popularitesini_hesapla()
        
        # En popüler N ürünü al
        sorted_urunler = sorted(self.urun_sayilari.items(), key=lambda x: x[1], reverse=True)
        top_urunler = sorted_urunler[:top_n]
        
        # Grafik oluştur
        urunler = [item[0] for item in top_urunler]
        sayilar = [item[1] for item in top_urunler]
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar(urunler, sayilar, color='skyblue', alpha=0.7)
        plt.title(f'En Popüler {top_n} Ürün', fontsize=16, fontweight='bold')
        plt.xlabel('Ürünler', fontsize=12)
        plt.ylabel('Sepet Sayısı', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # Barların üzerine sayıları yaz
        for bar, sayi in zip(bars, sayilar):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    str(sayi), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
    
    def birliktelik_analizi(self, min_support=0.05):
        """
        İki ürün arasındaki birliktelikleri analiz eder
        min_support: Minimum destek oranı (varsayılan %5)
        """
        print(f"\n🔗 BİRLİKTELİK ANALİZİ (Min Support: %{min_support*100:.0f})")
        print("=" * 50)
        
        toplam_sepet = len(self.sepetler)
        min_sepet_sayisi = int(min_support * toplam_sepet)
        
        print(f"Minimum sepet sayısı: {min_sepet_sayisi}")
        
        # Tüm ürün çiftlerini kontrol et
        tum_urunler = list(self.urun_sayilari.keys())
        birliktelik_sayilari = {}
        
        for sepet in self.sepetler:
            if len(sepet) >= 2:
                # Bu sepetteki tüm ürün çiftleri
                for urun1, urun2 in combinations(sepet, 2):
                    # Alfabetik sıraya koy (Apple, Bread yerine her zaman aynı sıra)
                    if urun1 > urun2:
                        urun1, urun2 = urun2, urun1
                    
                    cift = (urun1, urun2)
                    if cift in birliktelik_sayilari:
                        birliktelik_sayilari[cift] += 1
                    else:
                        birliktelik_sayilari[cift] = 1
        
        # Minimum desteği geçen çiftleri filtrele
        onemli_birliktelikler = {}
        for cift, sayi in birliktelik_sayilari.items():
            if sayi >= min_sepet_sayisi:
                support = sayi / toplam_sepet
                onemli_birliktelikler[cift] = {
                    'sepet_sayisi': sayi,
                    'support': support
                }
        
        print(f"✅ {len(onemli_birliktelikler)} önemli birliktelik bulundu")
        
        # En güçlü birliktelikleri göster
        if onemli_birliktelikler:
            print(f"\nEn güçlü 10 birliktelik:")
            sorted_birliktelikler = sorted(onemli_birliktelikler.items(), 
                                         key=lambda x: x[1]['support'], reverse=True)
            
            for i, (cift, bilgi) in enumerate(sorted_birliktelikler[:10], 1):
                urun1, urun2 = cift
                print(f"{i:2d}. {urun1} + {urun2}: "
                      f"{bilgi['sepet_sayisi']} sepet "
                      f"(%{bilgi['support']*100:.1f})")
        
        self.birliktelikler = onemli_birliktelikler
        return onemli_birliktelikler
    
    def kural_analizi(self, min_confidence=0.3):
        """
        Association Rules (Birliktelik Kuralları) oluşturur
        min_confidence: Minimum güven oranı (varsayılan %30)
        """
        print(f"\n📋 KURAL ANALİZİ (Min Confidence: %{min_confidence*100:.0f})")
        print("=" * 50)
        
        if not self.birliktelikler:
            print("❌ Önce birliktelik analizi yapmalısınız!")
            return
        
        kurallar = []
        toplam_sepet = len(self.sepetler)
        
        for (urun1, urun2), bilgi in self.birliktelikler.items():
            birlikte_sayi = bilgi['sepet_sayisi']
            
            # Kural 1: urun1 → urun2
            urun1_sayi = self.urun_sayilari[urun1]
            confidence1 = birlikte_sayi / urun1_sayi
            
            if confidence1 >= min_confidence:
                lift1 = confidence1 / (self.urun_sayilari[urun2] / toplam_sepet)
                kurallar.append({
                    'antecedent': urun1,      # Öncül
                    'consequent': urun2,      # Sonuç
                    'support': bilgi['support'],
                    'confidence': confidence1,
                    'lift': lift1
                })
            
            # Kural 2: urun2 → urun1
            urun2_sayi = self.urun_sayilari[urun2]
            confidence2 = birlikte_sayi / urun2_sayi
            
            if confidence2 >= min_confidence:
                lift2 = confidence2 / (self.urun_sayilari[urun1] / toplam_sepet)
                kurallar.append({
                    'antecedent': urun2,
                    'consequent': urun1,
                    'support': bilgi['support'],
                    'confidence': confidence2,
                    'lift': lift2
                })
        
        print(f"✅ {len(kurallar)} kural bulundu")
        
        if kurallar:
            # Kuralları güvene göre sırala
            kurallar.sort(key=lambda x: x['confidence'], reverse=True)
            
            print(f"\nEn güçlü 10 kural:")
            print("-" * 80)
            print(f"{'No':<3} {'Öncül':<15} {'→':<2} {'Sonuç':<15} {'Güven':<8} {'Lift':<8}")
            print("-" * 80)
            
            for i, kural in enumerate(kurallar[:10], 1):
                print(f"{i:<3} {kural['antecedent']:<15} → {kural['consequent']:<15} "
                      f"{kural['confidence']:<8.1%} {kural['lift']:<8.2f}")
        
        return kurallar
    
    def onerileri_goster(self, secilen_urun, kurallar=None, top_n=5):
        """
        Belirli bir ürün için öneriler gösterir
        """
        print(f"\n🎯 '{secilen_urun}' ÜRÜNÜ İÇİN ÖNERİLER")
        print("=" * 50)
        
        if kurallar is None:
            print("❌ Önce kural analizi yapmalısınız!")
            return
        
        # Bu ürün için geçerli kuralları bul
        uygun_kurallar = [kural for kural in kurallar 
                         if kural['antecedent'] == secilen_urun]
        
        if not uygun_kurallar:
            print(f"❌ '{secilen_urun}' için öneri bulunamadı.")
            return
        
        # Güvene göre sırala
        uygun_kurallar.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"✅ {len(uygun_kurallar)} öneri bulundu:")
        print()
        
        for i, kural in enumerate(uygun_kurallar[:top_n], 1):
            print(f"{i}. {kural['consequent']}")
            print(f"   Güven: %{kural['confidence']*100:.1f}")
            print(f"   Lift: {kural['lift']:.2f}")
            print(f"   Açıklama: '{secilen_urun}' alan müşterilerin "
                  f"%{kural['confidence']*100:.0f}'i '{kural['consequent']}' da alıyor")
            print()
    
    def ozet_rapor(self):
        """
        Analiz sonuçlarının özetini verir
        """
        print("\n📝 ÖZET RAPOR")
        print("=" * 40)
        
        if not self.veri is None:
            print(f"🔸 Toplam sepet sayısı: {len(self.sepetler)}")
            print(f"🔸 Toplam ürün çeşidi: {len(self.urun_sayilari)}")
            
            if self.birliktelikler:
                print(f"🔸 Bulunan birliktelik sayısı: {len(self.birliktelikler)}")
                
                # En popüler ürün
                en_populer = max(self.urun_sayilari.items(), key=lambda x: x[1])
                print(f"🔸 En popüler ürün: {en_populer[0]} ({en_populer[1]} sepet)")
                
                # En güçlü birliktelik
                en_guclu = max(self.birliktelikler.items(), key=lambda x: x[1]['support'])
                urun1, urun2 = en_guclu[0]
                support = en_guclu[1]['support']
                print(f"🔸 En güçlü birliktelik: {urun1} + {urun2} (%{support*100:.1f})")


def main():
    """
    Ana program - adım adım Market Basket Analysis
    """
    print("🛒 MARKET SEPETİ ANALİZİ")
    print("=" * 50)
    print("Bu program market sepetlerindeki ürün birlikteliklerini analiz eder.")
    print()
    
    # 1. Analiz nesnesini oluştur
    analiz = BasitMarketAnalizi()
    
    # 2. Veriyi yükle
    veri = analiz.veri_yukle('data/cafe_orders.csv')

    # 3. Temel istatistikleri göster
    analiz.temel_istatistikler()
    
    # 4. Popüler ürünleri göster
    print("\n📊 En popüler ürünlerin grafiği çiziliyor...")
    analiz.popular_urunleri_goster(top_n=8)
    
    # 5. Birliktelik analizi
    birliktelikler = analiz.birliktelik_analizi(min_support=0.05)
    
    # 6. Kural analizi
    kurallar = analiz.kural_analizi(min_confidence=0.3)
    
    # 7. Örnek öneriler
    if kurallar:
        print("\n" + "="*50)
        print("ÖRNEK ÖNERİLER")
        analiz.onerileri_goster('Milk', kurallar, top_n=3)
        analiz.onerileri_goster('Bread', kurallar, top_n=3)
    
    # 8. Özet rapor
    analiz.ozet_rapor()
    
    print("\n✅ Analiz tamamlandı!")


if __name__ == "__main__":
    main()