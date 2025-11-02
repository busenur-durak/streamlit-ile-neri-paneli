# Hafta 6 - Association Rules & User Behavior Analysis

## Dataset Information

Bu projede market basket analysis ve association rules için aşağıdaki Kaggle dataset'lerini kullanacağız:

### Primary Dataset: Groceries Market Basket Dataset
- **Kaynak**: https://www.kaggle.com/datasets/irfanasrullah/groceries
- **Boyut**: 9,835 transaction
- **Ürün Sayısı**: 169 unique grocery items
- **Format**: CSV/ZIP
- **Kullanım**: Apriori ve FP-Growth algoritmaları için ideal

### Secondary Dataset: Market Basket Analysis Data
- **Kaynak**: https://www.kaggle.com/datasets/ahmtcnbs/datasets-for-appiori
- **Format**: CSV/ZIP  
- **Kullanım**: Apriori algorithm demonstration için tasarlanmış

## Dataset Download Instructions

1. Kaggle hesabınızla login olun
2. Yukarıdaki dataset linklerine gidin
3. "Download" butonuna tıklayın
4. ZIP dosyalarını bu klasöre extract edin

## Data Structure

Dataset'ler transaction-based format'ta olacak:
- Her satır bir transaction
- Her transaction multiple items içerebilir
- Market basket analysis için uygun format

## Usage

Bu dataset'ler şu konular için kullanılacak:
- Association Rules (Apriori, FP-Growth)
- User Behavior Analysis  
- Recommendation Systems
- Streamlit Dashboard Development