# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 03:20:37 2024

@author: kerim
"""

import pandas as pd
import numpy as np

# CSV dosyasını oku
df = pd.read_csv('musteriler_guncel_v4.csv')

# Fonksiyon: Ardışık aylar arasındaki yüzdesel değişimi hesapla
def calculate_percentage_change(df, col_prefix, new_col_prefix):
    for i in range(1, 7):
        current_col = f'{col_prefix}_{i}'
        next_col = f'{col_prefix}_{i+1}'
        new_col = f'{new_col_prefix}_{i}to{i+1}'
        # Sıfır olmayan değerlere sahip olup olmadığını kontrol et
        df[new_col] = np.where(df[current_col] != 0, (df[next_col] - df[current_col]) / df[current_col], np.nan)

# İşlem sayıları için yüzdesel değişim
transaction_cols = ['Ocak_Trans_Ct', 'Subat_Trans_Ct', 'Mart_Trans_Ct', 'Nisan_Trans_Ct', 'Mayis_Trans_Ct', 'Haziran_Trans_Ct', 'Temmuz_Trans_Ct']
for i in range(len(transaction_cols)-1):
    col1 = transaction_cols[i]
    col2 = transaction_cols[i+1]
    new_col = f'{transaction_cols[i].split("_")[0].lower()}_to_{transaction_cols[i+1].split("_")[0].lower()}_tran_ct_degisim'
    df[new_col] = np.where(df[col1] != 0, (df[col2] - df[col1]) / df[col1], np.nan)

# İşlem miktarları için yüzdesel değişim
transaction_amt_cols = ['Ocak_Trans_Amt', 'Subat_Trans_Amt', 'Mart_Trans_Amt', 'Nisan_Trans_Amt', 'Mayis_Trans_Amt', 'Haziran_Trans_Amt', 'Temmuz_Trans_Amt']
for i in range(len(transaction_amt_cols)-1):
    col1 = transaction_amt_cols[i]
    col2 = transaction_amt_cols[i+1]
    new_col = f'{transaction_amt_cols[i].split("_")[0].lower()}_to_{transaction_amt_cols[i+1].split("_")[0].lower()}_tran_amt_degisim'
    df[new_col] = np.where(df[col1] != 0, (df[col2] - df[col1]) / df[col1], np.nan)

# Kredi kartı işlem sayıları için yüzdesel değişim
calculate_percentage_change(df, 'credit_card_tran_ct', 'credit_cart_tran_ct_degisim')

# Kredi kartı işlem miktarları için yüzdesel değişim
calculate_percentage_change(df, 'credit_card_tran_Amt', 'credit_cart_tran_Amt_degisim')

# Yeni veriyi kaydet
df.to_csv('musteriler_guncel_v5.csv', index=False)

print("Veriler başarıyla 'musteriler_guncel_v5.csv' dosyasına kaydedildi.")