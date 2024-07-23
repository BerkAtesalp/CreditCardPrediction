# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 10:42:00 2024
@author: kerim
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Müşteri verilerini içeren CSV dosyasını okuma
customers_df = pd.read_csv('musteriler_guncel.csv')

# Boş bir transactions DataFrame'i oluşturma
transactions_data = []

# Her müşteri için işlem oluşturma
for index, customer in customers_df.iterrows():
    customer_id = customer['CLIENTNUM']
    income_level = customer['Income_Category']
    total_transactions = customer['Total_Trans_Ct']
    credit_limit = customer['Credit_Limit']
    occupation = customer['jobs']
    
    # Her müşteri için maaş işlemi ekleme
    if occupation != 'unemployed':
        if income_level == 'Unknown':
            if credit_limit <= 5000:
                annual_income = random.uniform(20000, 30000)
            elif credit_limit <= 10000:
                annual_income = random.uniform(30000, 50000)
            elif credit_limit <= 20000:
                annual_income = random.uniform(50000, 70000)
            else:
                annual_income = random.uniform(70000, 100000)
        elif income_level == 'Less than $40K':
            annual_income = random.uniform(20000, 40000)
        elif income_level == '$40K - $60K':
            annual_income = random.uniform(40000, 60000)
        elif income_level == '$60K - $80K':
            annual_income = random.uniform(60000, 80000)
        elif income_level == '$80K - $120K':
            annual_income = random.uniform(80000, 120000)
        elif income_level == '$120K +':
            annual_income = random.uniform(120000, 200000)
        else:
            annual_income = random.uniform(20000, 100000)  # Default case

        # Aylık maaş hesaplaması ve 50'ye tam bölünen en yakın sayıya yuvarlama
        monthly_income = round(annual_income / 12 / 50) * 50
        
        # Son 6 ay için işlemleri ekleme
        current_date = datetime.now()
        rent_payment = random.random() < 0.65  # %65 olasılıkla kira ödemesi

        for month in range(6):
            transaction_date = current_date - relativedelta(months=month)
            transaction_date = transaction_date.replace(day=random.randint(1, 5))  # Ayın 1'i ile 5'i arasında
            
            # Maaş işlemi ekleme
            transactions_data.append({
                'TransactionID': len(transactions_data) + 1,
                'CustomerID': customer_id,
                'TransactionType': 'IncomingTransfer',
                'Amount': monthly_income,
                'TransactionDate': transaction_date,
                'Description': 'Salary',
            })
            
            # Kredi kartı ödemesi (maaş tarihinden 5 gün sonra)
            total_revolving_bal = customer['Total_Revolving_Bal']
            if total_revolving_bal > 0:
                payment_ratio = random.uniform(1, 1.5)
                payment_amount = round(total_revolving_bal * payment_ratio, -2)
                credit_card_payment_date = transaction_date + timedelta(days=5)
                transactions_data.append({
                    'TransactionID': len(transactions_data) + 1,
                    'CustomerID': customer_id,
                    'TransactionType': 'Payment',
                    'Amount': payment_amount,
                    'TransactionDate': credit_card_payment_date,
                    'Description': 'Credit Card Payment',
                })
            
            # Kira veya diğer ödemeler ekleme
            transaction_date = current_date - relativedelta(months=month)
            transaction_date = transaction_date.replace(day=random.randint(10, 18))  # Ayın 10'u ile 18'i arasında
            
            if rent_payment:
                rent_amount = round(monthly_income * random.uniform(0.25, 0.65), -2)
                transactions_data.append({
                    'TransactionID': len(transactions_data) + 1,
                    'CustomerID': customer_id,
                    'TransactionType': 'Payment',
                    'Amount': rent_amount,
                    'TransactionDate': transaction_date,
                    'Description': 'Rent Payment',
                })
            else:
                other_expense_amount = round(monthly_income * random.uniform(0.25, 0.45), -2)
                transactions_data.append({
                    'TransactionID': len(transactions_data) + 1,
                    'CustomerID': customer_id,
                    'TransactionType': 'Payment',
                    'Amount': other_expense_amount,
                    'TransactionDate': transaction_date,
                    'Description': random.choice(['Insurance Payment', 'Installment Payment', 'Subscription Payment']),
                })

    
    # Müşteriye ait işlem sayısı olarak Total_Trans_Ct sütununu kullanma
    num_transactions = int(total_transactions)
    
    # İşlemler için boş bir liste
    transaction_amounts = []
    for i in range(num_transactions):
        # Rastgele işlem türü seçimi
        transaction_type = random.choices(['Purchase', 'Withdrawal', 'OutgoingTransfer', 'Payment', 'Deposit', 'OnlineShopping', 'Return', 'IncomingTransfer'],
                                          weights=[0.2, 0.15, 0.1, 0.1, 0.2, 0.1, 0.1, 0.05], k=1)[0]
        
        # Rastgele işlem miktarı seçimi (müşteri gelir seviyesine göre)
        if income_level == 'Unknown':
            amount = round(random.uniform(10, 500), 2)
        elif income_level == 'Less than $40K':
            amount = round(random.uniform(10, 250), 2)
        elif income_level == '$40K - $60K':
            amount = round(random.uniform(20, 400), 2)
        elif income_level == '$60K - $80K':
            amount = round(random.uniform(50, 550), 2)
        elif income_level == '$80K - $120K':
            amount = round(random.uniform(100, 750), 2)
        elif income_level == '$120K +':
            amount = round(random.uniform(200, 950), 2)
        else:
            amount = round(random.uniform(10, 500), 2)  # Default case
        
        transaction_amounts.append(amount)
        
        # Rastgele işlem tarihi seçimi (son 6 ay içinde)
        start_date = current_date - timedelta(days=180)
        transaction_date = start_date + timedelta(days=random.randint(1, 180))
        
        # İşlem saatini rastgele seçelim (haftaiçi, haftasonu ve gündüz/gece ayarlaması)
        if transaction_date.weekday() < 5:  # Haftaiçi ise
            if random.random() < 0.6:  # Gündüz saatleri için
                transaction_date = transaction_date.replace(hour=random.randint(9, 17))
            else:  # Gece saatleri için
                transaction_date = transaction_date.replace(hour=random.randint(18, 23))
        else:  # Haftasonu ise
            transaction_date = transaction_date.replace(hour=random.randint(10, 22))
        
        # İşlem açıklaması oluşturma
        if transaction_type == 'Purchase':
            description = random.choice(['Grocery', 'Clothing', 'Electronics', 'Restaurant', 'Travel', 'Pharmacy', 'Gas', 'Furniture', 'Home Improvement', 'Entertainment'])
        elif transaction_type == 'Withdrawal':
            description = random.choice(['ATM Withdrawal', 'Branch Withdrawal', 'Mobile App Withdrawal'])
        elif transaction_type == 'Payment':
            description = random.choice(['Bill Payment', 'Loan Payment', 'Mortgage Payment'])
        elif transaction_type == 'Deposit':
            description = random.choice(['Cash Deposit', 'Check Deposit', 'Direct Deposit', 'Mobile Deposit'])
        elif transaction_type == 'OnlineShopping':
            description = random.choice(['Amazon', 'eBay', 'AliExpress', 'Etsy', 'Walmart', 'Best Buy', 'Target'])
        elif transaction_type == 'Return':
            description = random.choice(['Amazon Return', 'eBay Return', 'AliExpress Return', 'Etsy Return', 'Walmart Return', 'Best Buy Return', 'Target Return', 'Store Return'])
        elif transaction_type == 'IncomingTransfer':
            description = 'Freelance Payment'  # Değiştirilebilir
        else:
            description = random.choice(['Bank Transfer', 'Peer-to-Peer Transfer', 'Wire Transfer', 'International Transfer'])
        
        # İşlem bilgilerini transactions_data listesine ekleme
        transactions_data.append({
            'TransactionID': len(transactions_data) + 1,
            'CustomerID': customer_id,
            'TransactionType': transaction_type,
            'Amount': amount,
            'TransactionDate': transaction_date,
            'Description': description,
        })
        


# transactions_data listesini DataFrame'e çevirme
transactions = pd.DataFrame(transactions_data)

# TransactionDate sütununun format ayarı
transactions['TransactionDate'] = pd.to_datetime(transactions['TransactionDate'])

# DataFrame'i CSV dosyasına kaydetme
transactions.to_csv('transactions.csv', index=False)

print("transactions.csv dosyası başarıyla oluşturuldu.")
