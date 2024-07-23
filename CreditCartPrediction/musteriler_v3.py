# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 04:30:09 2024

@author: kerim
"""

'''
import pandas as pd

# CSV dosyalarını yükle
musteriler_guncel = pd.read_csv('musteriler_guncel_v2.csv')
kredi_karti_harcamalar_v2 = pd.read_csv('kredi_karti_harcamalar_v2.csv')

# Tarih sütununu datetime formatına çevir
kredi_karti_harcamalar_v2['transaction_date'] = pd.to_datetime(kredi_karti_harcamalar_v2['transaction_date'])

# Müşteriler bazında toplam kredi kartı harcama sayısı ve miktarını hesapla
total_tran_ct = kredi_karti_harcamalar_v2.groupby('customer_id')['transaction_id'].count().reset_index()
total_tran_ct.columns = ['CustomerID', 'credit_card_tran_ct']

total_tran_amt = kredi_karti_harcamalar_v2.groupby('customer_id')['spending_amount'].sum().reset_index()
total_tran_amt.columns = ['CustomerID', 'credit_card_tran_Amt']

# Aylık bazda toplam kredi kartı harcama sayısı ve miktarını hesapla
kredi_karti_harcamalar_v2['month'] = kredi_karti_harcamalar_v2['transaction_date'].dt.month

monthly_tran_ct = kredi_karti_harcamalar_v2.groupby(['customer_id', 'month'])['transaction_id'].count().unstack(fill_value=0).reset_index()
monthly_tran_ct.columns = ['CustomerID'] + ['credit_card_tran_ct_{}'.format(i) for i in range(1, 8)]

monthly_tran_amt = kredi_karti_harcamalar_v2.groupby(['customer_id', 'month'])['spending_amount'].sum().unstack(fill_value=0).reset_index()
monthly_tran_amt.columns = ['CustomerID'] + ['credit_card_tran_Amt_{}'.format(i) for i in range(1, 8)]

# Verileri birleştir
merged_data = musteriler_guncel.merge(total_tran_ct, on='CustomerID', how='left')
merged_data = merged_data.merge(total_tran_amt, on='CustomerID', how='left')
merged_data = merged_data.merge(monthly_tran_ct, on='CustomerID', how='left')
merged_data = merged_data.merge(monthly_tran_amt, on='CustomerID', how='left')

# Avg_Utilization_Ratio sütununu güncelle
merged_data['Avg_Utilization_Ratio'] = ((merged_data['credit_card_tran_Amt'] / 12) / merged_data['Credit_Limit'])

# Sonuçları kaydet veya görüntüle
merged_data.to_csv('musteriler_guncel_v3.csv', index=False)
print(merged_data.head())
'''

# Haziran ve Temmuz Hariç:

    
import pandas as pd

# CSV dosyalarını yükle
musteriler_guncel = pd.read_csv('F_musteriler_guncel_v2.csv')
kredi_karti_harcamalar_v2 = pd.read_csv('kredi_karti_harcamalar_v2.csv')

# Tarih sütununu datetime formatına çevir
kredi_karti_harcamalar_v2['transaction_date'] = pd.to_datetime(kredi_karti_harcamalar_v2['transaction_date'])

# Haziran ve Temmuz aylarını hariç tut
kredi_karti_harcamalar_v2 = kredi_karti_harcamalar_v2[~kredi_karti_harcamalar_v2['transaction_date'].dt.month.isin([6, 7])]

# Müşteriler bazında toplam kredi kartı harcama sayısı ve miktarını hesapla
total_tran_ct = kredi_karti_harcamalar_v2.groupby('customer_id')['transaction_id'].count().reset_index()
total_tran_ct.columns = ['CustomerID', 'credit_card_tran_ct']

total_tran_amt = kredi_karti_harcamalar_v2.groupby('customer_id')['spending_amount'].sum().reset_index()
total_tran_amt.columns = ['CustomerID', 'credit_card_tran_Amt']

# Aylık bazda toplam kredi kartı harcama sayısı ve miktarını hesapla
kredi_karti_harcamalar_v2['month'] = kredi_karti_harcamalar_v2['transaction_date'].dt.month

monthly_tran_ct = kredi_karti_harcamalar_v2.groupby(['customer_id', 'month'])['transaction_id'].count().unstack(fill_value=0).reset_index()
monthly_tran_ct.columns = ['CustomerID'] + ['credit_card_tran_ct_{}'.format(i) for i in range(1, 6)]  # 5 ay

monthly_tran_amt = kredi_karti_harcamalar_v2.groupby(['customer_id', 'month'])['spending_amount'].sum().unstack(fill_value=0).reset_index()
monthly_tran_amt.columns = ['CustomerID'] + ['credit_card_tran_Amt_{}'.format(i) for i in range(1, 6)]  # 5 ay

# Verileri birleştir
merged_data = musteriler_guncel.merge(total_tran_ct, on='CustomerID', how='left')
merged_data = merged_data.merge(total_tran_amt, on='CustomerID', how='left')
merged_data = merged_data.merge(monthly_tran_ct, on='CustomerID', how='left')
merged_data = merged_data.merge(monthly_tran_amt, on='CustomerID', how='left')

# Avg_Utilization_Ratio sütununu güncelle
merged_data['Avg_Utilization_Ratio'] = ((merged_data['credit_card_tran_Amt'] / 10) / merged_data['Credit_Limit'])

# Sonuçları kaydet veya görüntüle
merged_data.to_csv('F_musteriler_guncel_v3.csv', index=False)
print(merged_data.head())