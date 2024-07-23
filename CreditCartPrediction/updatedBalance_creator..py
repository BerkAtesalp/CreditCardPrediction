import pandas as pd
import random

# transactions.csv dosyasını okuma
transactions = pd.read_csv('transactions.csv')

# Müşteriler verisini içeren CSV dosyasını okuma
customers_df = pd.read_csv('musteriler_guncel.csv')


# Müşteri ID'sine, TransactionDate'e ve TransactionID'ye göre sıralama
sorted_transactions = transactions.sort_values(by=['CustomerID', 'TransactionDate', 'TransactionID'])

# Güncellenen bakiye sütununu eklemek için başlangıç değeri belirleme
updated_balances = {}
previous_customer_id = None

# Müşteri verilerinden Total_Revolving_Bal değerlerini alarak güncelleme
for index, customer in customers_df.iterrows():
    updated_balances[customer['CLIENTNUM']] = customer['Total_Revolving_Bal'] * random.uniform(0.5, 0.9)

# Güncellenmiş bakiye hesaplama ve sütunu ekleyerek DataFrame'i güncelleme
updated_balance = 0
for index, row in sorted_transactions.iterrows():
    if row['CustomerID'] != previous_customer_id:
        updated_balance = updated_balances[row['CustomerID']]
    # Bakiyeyi güncelleme işlemi
    if row['TransactionType'] in ['Deposit', 'Return', 'IncomingTransfer']:
        updated_balance += row['Amount']
    else:
        updated_balance -= row['Amount']
    # Güncellenen bakiyeyi DataFrame'e eklemek
    sorted_transactions.at[index, 'UpdatedBalance'] = updated_balance
    previous_customer_id = row['CustomerID']

# TransactionID'yi sıralı hale getirme ve DataFrame'i yeniden sıralama
sorted_transactions = sorted_transactions.reset_index(drop=True)

# TransactionID'yi yeniden oluşturma
sorted_transactions['TransactionID'] = sorted_transactions.index + 1

# TransactionDate sütununu datetime formatına çevirme
sorted_transactions['TransactionDate'] = pd.to_datetime(sorted_transactions['TransactionDate'], format='%Y-%m-%d %H:%M:%S')


# Güncellenmiş DataFrame'i CSV dosyasına kaydetme
sorted_transactions.to_csv('transaction_updated.csv', index=False)
print("transaction_updated.csv dosyası başarıyla oluşturuldu.")