# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:16:55 2024

@author: kerim
"""

import pandas as pd
import numpy as np

# CSV dosyasından veri setini yükle
df = pd.read_csv('BankChurners_segment.csv')  # 'veri.csv' dosya yolunu kendi dosya yolunuzla değiştirin

# Tüm veri seti için genel metrikleri hesaplayın
metrics = df.describe(include='all').T  # Betimsel istatistikleri hesaplayın

# Genel veri setine en yakın segmenti bulun
en_yakin_segment = None
en_yakin_mesafe = np.inf

# Veriyi rastgele 10 eşit parçaya bölün
np.random.seed(42)
df['segment'] = np.random.randint(0, 2, size=len(df))

# Her segmenti yineleyin
for i in range(2):
    segment_df = df[df['segment'] == i]  # Mevcut segment için satırları seçin
    
    # Mevcut segment için metrikleri hesaplayın
    metrics_segment = segment_df.describe(include='all').T
    
    # Genel metriklerden olan uzaklığı ölçün (kendi mesafe metrinizi tanımlayabilirsiniz)
    mesafe = np.sum(np.abs(metrics['mean'] - metrics_segment['mean']))
    
    # Eğer bu segment daha yakınsa en yakın segmenti güncelleyin
    if mesafe < en_yakin_mesafe:
        en_yakin_mesafe = mesafe
        en_yakin_segment = segment_df.copy()  # En yakın segment DataFrame'inin bir kopyasını alın

# Metrikleri ve en yakın segmenti yazdırın
print("Genel Metrikler:")
print(metrics)
print("\nEn Yakın Segment:")
print(en_yakin_segment.head())  # En yakın segment DataFrame'ini gösterin

# En yakın segmenti CSV dosyasına kaydet
en_yakin_segment.to_csv('BankChurners_segment2.csv', index=False)