# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 04:20:59 2024

@author: kerim
"""
import pandas as pd

# CSV dosyalarını yükle
musteriler = pd.read_csv('F_musteriler_guncel_v4.csv')
transactions = pd.read_csv('transaction_updated_v2.csv')

# TransactionDate sütununu datetime formatına çevir
transactions['TransactionDate'] = pd.to_datetime(transactions['TransactionDate'], format='%m-%d-%y %H:%M')

# Her müşteri ve ay için son günün UpdatedBalance değerini almak için işlemler
# Ay ve yıl sütunları ekleyin
transactions['YearMonth'] = transactions['TransactionDate'].dt.to_period('M')

# Her müşteri ve ay için son günün UpdatedBalance değerini almak için işlemler
latest_balance_per_month = transactions.groupby(['CustomerID', 'YearMonth'])['UpdatedBalance'].last().reset_index()

# Pivot tablo oluşturun: CustomerID'ye göre YearMonth'i sütun olarak kullanın
latest_balance_pivot = latest_balance_per_month.pivot(index='CustomerID', columns='YearMonth', values='UpdatedBalance').reset_index()

# Pivot tablodaki sütunları uygun şekilde yeniden adlandırın (Ocak hesap bakiyesi, Şubat hesap bakiyesi, vb.)
latest_balance_pivot.columns = ['CustomerID'] + [f"{period.strftime('%b')}_hesap_bakiyesi" for period in latest_balance_pivot.columns[1:]]

# Müşteriler datasına yeni hesap bakiyesi sütunlarını ekleyin
musteriler = musteriler.merge(latest_balance_pivot, on='CustomerID', how='left')

# Sonuçları kaydet veya görüntüle
musteriler.to_csv('F_musteriler_guncel_v5.csv', index=False)
print(musteriler.head())