import pandas as pd

# CSV dosyalarını yükle
musteriler_guncel = pd.read_csv('musteriler_guncel_v3.csv')
kredi_karti_harcamalar_v2 = pd.read_csv('kredi_karti_harcamalar_v2.csv')
transaction_updated_v2 = pd.read_csv('transaction_updated_v2.csv')

# Tarih sütunlarını datetime formatına çevir
kredi_karti_harcamalar_v2['transaction_date'] = pd.to_datetime(kredi_karti_harcamalar_v2['transaction_date'])
transaction_updated_v2['TransactionDate'] = pd.to_datetime(transaction_updated_v2['TransactionDate'])

# Aylık sütun isimleri
months = ['Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran', 'Temmuz']

# En sık yapılan işlemi ve toplam harcama miktarını hesapla
def calculate_most_frequent(df, group_by_col, value_col):
    freq_df = df.groupby([group_by_col, value_col]).size().reset_index(name='counts')
    most_freq_df = freq_df.loc[freq_df.groupby(group_by_col)['counts'].idxmax()].reset_index(drop=True)
    most_freq_df.columns = [group_by_col, f'{value_col}_most_freq', 'counts']
    return most_freq_df

# Toplam harcama miktarını ve en yüksek miktarı hesapla
def calculate_max_amount(df, group_by_col, value_col, amount_col):
    sum_df = df.groupby([group_by_col, value_col])[amount_col].sum().reset_index()
    max_amount_df = sum_df.loc[sum_df.groupby(group_by_col)[amount_col].idxmax()].reset_index(drop=True)
    max_amount_df.columns = [group_by_col, f'{value_col}_max_amount', 'total_amount']
    return max_amount_df

# Kredi kartı harcamaları için toplam ve aylık en çok harcama yapılan kategoriler ve açıklamalar
for month in range(1, 8):
    kredi_karti_harcamalar_v2[f'month_{month}'] = kredi_karti_harcamalar_v2['transaction_date'].dt.month == month

most_freq_expense_type = calculate_most_frequent(kredi_karti_harcamalar_v2, 'customer_id', 'expense_type')
max_expense_type_amount = calculate_max_amount(kredi_karti_harcamalar_v2, 'customer_id', 'expense_type', 'spending_amount')
most_freq_expense_desc = calculate_most_frequent(kredi_karti_harcamalar_v2, 'customer_id', 'expense_description')
max_expense_desc_amount = calculate_max_amount(kredi_karti_harcamalar_v2, 'customer_id', 'expense_description', 'spending_amount')

# Aylık veriler
monthly_freq_expense_type = []
monthly_max_expense_type_amount = []
monthly_freq_expense_desc = []
monthly_max_expense_desc_amount = []

for month in range(1, 8):
    monthly_data = kredi_karti_harcamalar_v2[kredi_karti_harcamalar_v2[f'month_{month}']]
    monthly_freq_expense_type.append(calculate_most_frequent(monthly_data, 'customer_id', 'expense_type'))
    monthly_max_expense_type_amount.append(calculate_max_amount(monthly_data, 'customer_id', 'expense_type', 'spending_amount'))
    monthly_freq_expense_desc.append(calculate_most_frequent(monthly_data, 'customer_id', 'expense_description'))
    monthly_max_expense_desc_amount.append(calculate_max_amount(monthly_data, 'customer_id', 'expense_description', 'spending_amount'))

# Transaction verileri için aynı hesaplamaları yap
most_freq_trans_type = calculate_most_frequent(transaction_updated_v2, 'CustomerID', 'TransactionType')
max_trans_type_amount = calculate_max_amount(transaction_updated_v2, 'CustomerID', 'TransactionType', 'Amount')
most_freq_trans_desc = calculate_most_frequent(transaction_updated_v2, 'CustomerID', 'Description')
max_trans_desc_amount = calculate_max_amount(transaction_updated_v2, 'CustomerID', 'Description', 'Amount')

# Aylık veriler
monthly_freq_trans_type = []
monthly_max_trans_type_amount = []
monthly_freq_trans_desc = []
monthly_max_trans_desc_amount = []

for month in range(1, 8):
    monthly_data = transaction_updated_v2[transaction_updated_v2['TransactionDate'].dt.month == month]
    monthly_freq_trans_type.append(calculate_most_frequent(monthly_data, 'CustomerID', 'TransactionType'))
    monthly_max_trans_type_amount.append(calculate_max_amount(monthly_data, 'CustomerID', 'TransactionType', 'Amount'))
    monthly_freq_trans_desc.append(calculate_most_frequent(monthly_data, 'CustomerID', 'Description'))
    monthly_max_trans_desc_amount.append(calculate_max_amount(monthly_data, 'CustomerID', 'Description', 'Amount'))

# Son transaction verisindeki UpdatedBalance'ı ekle
last_transaction = transaction_updated_v2.sort_values('TransactionDate').groupby('CustomerID').last().reset_index()
last_transaction_balance = last_transaction[['CustomerID', 'UpdatedBalance']]
last_transaction_balance.columns = ['CustomerID', 'Güncel_hesap_bakiyesi']

# Verileri birleştir
merged_data = musteriler_guncel.merge(most_freq_expense_type, left_on='CustomerID', right_on='customer_id', how='left').drop(columns='customer_id')
merged_data = merged_data.merge(max_expense_type_amount, left_on='CustomerID', right_on='customer_id', how='left').drop(columns='customer_id')
merged_data = merged_data.merge(most_freq_expense_desc, left_on='CustomerID', right_on='customer_id', how='left').drop(columns='customer_id')
merged_data = merged_data.merge(max_expense_desc_amount, left_on='CustomerID', right_on='customer_id', how='left').drop(columns='customer_id')

for i, month in enumerate(months):
    merged_data = merged_data.merge(monthly_freq_expense_type[i], left_on='CustomerID', right_on='customer_id', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_max_expense_type_amount[i], left_on='CustomerID', right_on='customer_id', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_freq_expense_desc[i], left_on='CustomerID', right_on='customer_id', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_max_expense_desc_amount[i], left_on='CustomerID', right_on='customer_id', how='left', suffixes=('', f'_{month}'))

merged_data = merged_data.merge(most_freq_trans_type, on='CustomerID', how='left')
merged_data = merged_data.merge(max_trans_type_amount, on='CustomerID', how='left')
merged_data = merged_data.merge(most_freq_trans_desc, on='CustomerID', how='left')
merged_data = merged_data.merge(max_trans_desc_amount, on='CustomerID', how='left')

for i, month in enumerate(months):
    merged_data = merged_data.merge(monthly_freq_trans_type[i], on='CustomerID', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_max_trans_type_amount[i], on='CustomerID', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_freq_trans_desc[i], on='CustomerID', how='left', suffixes=('', f'_{month}'))
    merged_data = merged_data.merge(monthly_max_trans_desc_amount[i], on='CustomerID', how='left', suffixes=('', f'_{month}'))

merged_data = merged_data.merge(last_transaction_balance, on='CustomerID', how='left')

# Sütun isimlerini düzenle
def rename_columns(df):
    new_columns = {}
    for col in df.columns:
        if 'most_freq_' in col:
            new_columns[col] = col.replace('most_freq_', '').replace('counts', 'counts_x')
        elif 'max_' in col:
            new_columns[col] = col.replace('max_', '').replace('total_amount', 'total_x')
        elif 'counts' in col:
            new_columns[col] = col.replace('counts', 'counts_x')
        elif 'total_amount' in col:
            new_columns[col] = col.replace('total_amount', 'total_x')
        else:
            new_columns[col] = col
    return df.rename(columns=new_columns)

merged_data = rename_columns(merged_data)

# Sonuçları kaydet veya görüntüle
merged_data.to_csv('musteriler_guncel_v4.csv', index=False)
print(merged_data.head())