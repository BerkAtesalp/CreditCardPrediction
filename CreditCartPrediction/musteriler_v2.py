# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 03:28:52 2024

@author: kerim
"""

'''
import pandas as pd

# CSV dosyalarını yükle
musteriler_guncel = pd.read_csv('musteriler_guncel.csv')
transaction_updated_v2 = pd.read_csv('transaction_updated_v2.csv')

# TransactionDate sütununu datetime tipine çevir
transaction_updated_v2['TransactionDate'] = pd.to_datetime(transaction_updated_v2['TransactionDate'], format='%m-%d-%y %H:%M')

# Toplam işlem sayısını ve toplam işlem tutarını hesapla
transaction_summary = transaction_updated_v2.groupby('CustomerID').agg(
    Total_Trans_Ct=('TransactionID', 'count'),
    Total_Trans_Amt=('Amount', 'sum')
).reset_index()

# Ay bazında işlem sayısı ve toplam işlem tutarını hesapla
transaction_updated_v2['Month'] = transaction_updated_v2['TransactionDate'].dt.month

monthly_summary = transaction_updated_v2.groupby(['CustomerID', 'Month']).agg(
    Trans_Ct=('TransactionID', 'count'),
    Trans_Amt=('Amount', 'sum')
).unstack(fill_value=0).reset_index()

# Sütun isimlerini düzenle
monthly_summary.columns = ['CustomerID'] + [f"{month}_{col}" for col in ['Trans_Ct', 'Trans_Amt'] for month in ['Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran', 'Temmuz']]

# CustomerID'yi CLIENTNUM'a dönüştürme işlemi
musteriler_guncel = musteriler_guncel.rename(columns={'CLIENTNUM': 'CustomerID'})

# İki veri setini birleştirmek için
merged_df = pd.merge(musteriler_guncel, transaction_summary, on='CustomerID', how='left')
merged_df = pd.merge(merged_df, monthly_summary, on='CustomerID', how='left')

# Yeni güncellenmiş veriyi CSV'ye kaydet
merged_df.to_csv('musteriler_guncel_v2.csv', index=False)

print("Veriler güncellendi ve 'musteriler_guncel_v2.csv' dosyasına kaydedildi.")

'''

# Haziran ve temmuz hariç :
    
import pandas as pd

# CSV dosyalarını yükle
musteriler_guncel = pd.read_csv('musteriler_guncel.csv')
transaction_updated_v2 = pd.read_csv('transaction_updated_v2.csv')

# TransactionDate sütununu datetime tipine çevir
transaction_updated_v2['TransactionDate'] = pd.to_datetime(transaction_updated_v2['TransactionDate'], format='%m-%d-%y %H:%M')

# Haziran ve Temmuz aylarını hariç tutarak veri filtresi yap
transaction_updated_v2 = transaction_updated_v2[~transaction_updated_v2['TransactionDate'].dt.month.isin([6, 7])]

# Toplam işlem sayısını ve toplam işlem tutarını hesapla
transaction_summary = transaction_updated_v2.groupby('CustomerID').agg(
    Total_Trans_Ct=('TransactionID', 'count'),
    Total_Trans_Amt=('Amount', 'sum')
).reset_index()

# Ay bazında işlem sayısı ve toplam işlem tutarını hesapla
transaction_updated_v2['Month'] = transaction_updated_v2['TransactionDate'].dt.month

monthly_summary = transaction_updated_v2.groupby(['CustomerID', 'Month']).agg(
    Trans_Ct=('TransactionID', 'count'),
    Trans_Amt=('Amount', 'sum')
).unstack(fill_value=0).reset_index()

# Sütun isimlerini düzenle (Haziran ve Temmuz hariç)
monthly_summary.columns = ['CustomerID'] + [f"{month}_{col}" for col in ['Trans_Ct', 'Trans_Amt'] for month in ['Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis']]

# CustomerID'yi CLIENTNUM'a dönüştürme işlemi
musteriler_guncel = musteriler_guncel.rename(columns={'CLIENTNUM': 'CustomerID'})

# İki veri setini birleştirmek için
merged_df = pd.merge(musteriler_guncel, transaction_summary, on='CustomerID', how='left')
merged_df = pd.merge(merged_df, monthly_summary, on='CustomerID', how='left')

# Yeni güncellenmiş veriyi CSV'ye kaydet
merged_df.to_csv('F_musteriler_guncel_v2.csv', index=False)

print("Veriler güncellendi ve 'musteriler_guncel_v2.csv' dosyasına kaydedildi.")