# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 01:23:45 2024

@author: kerim
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Verileri okuma
customers_df = pd.read_csv('musteriler_guncel.csv')

# Expense types and descriptions
expense_types = ['Groceries', 'Restaurant', 'Entertainment', 'Health', 'Clothing', 'Transportation', 'Technology', 'Miscellaneous']
expense_descriptions = {
    'Groceries': ['Supermarket shopping', 'Grocery store shopping', 'Organic food store', 'Farmer\'s market'],
    'Restaurant': ['Dinner', 'Lunch', 'Breakfast', 'Brunch', 'Fast food', 'Cafe'],
    'Entertainment': ['Cinema ticket', 'Theater ticket', 'Concert ticket', 'Amusement park', 'Museum entry', 'Sport event ticket'],
    'Health': ['Pharmacy', 'Doctor appointment', 'Dental care', 'Optometrist visit', 'Therapy session'],
    'Clothing': ['Retail store shopping', 'Online clothing shopping', 'Boutique shopping', 'Thrift store', 'Footwear store'],
    'Transportation': ['Taxi', 'Bus ticket', 'Train ticket', 'Flight ticket', 'Car rental', 'Gas station'],
    'Technology': ['Electronics shopping', 'Online tech shopping', 'Gadget store', 'Software purchase', 'Hardware purchase'],
    'Miscellaneous': ['Other expenses', 'Gifts', 'Donations', 'Home supplies', 'Pet supplies', 'Hobbies']
}


# Harcama miktarını belirlemek için yardımcı fonksiyonlar
def get_random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def get_spending_amount(card_category, credit_limit):
    # Harcama seviyeleri için aralıklar
    spending_ranges = {
        'Blue': {
            'small': (5, 100),
            'medium': (100, 500),
            'large': (500, 1000)
        },
        'Silver': {
            'small': (5, 150),
            'medium': (150, 700),
            'large': (700, 1500)
        },
        'Gold': {
            'small': (20, 200),
            'medium': (200, 1000),
            'large': (1000, 2000)
        },
        'Platinum': {
            'small': (20, 300),
            'medium': (300, 1500),
            'large': (1500, 3000)
        }
    }
    
    # Harcama seviyeleri için ağırlıklar
    spending_weights = {
        'Blue': [0.7, 0.2, 0.1],
        'Silver': [0.6, 0.3, 0.1],
        'Gold': [0.5, 0.3, 0.2],
        'Platinum': [0.4, 0.4, 0.2]
    }
    
    # Kart tipine göre uygun aralık ve ağırlıkları al
    ranges = spending_ranges.get(card_category, spending_ranges['Blue'])
    weights = spending_weights.get(card_category, spending_weights['Blue'])
    
    # Harcama seviyesi seçimi
    level_choice = random.choices(
        ['small', 'medium', 'large'],
        weights=weights,
        k=1
    )[0]
    
    # Seçilen seviyeye göre harcama miktarını belirleme
    spending_amount = np.random.uniform(ranges[level_choice][0], ranges[level_choice][1])
    
    return spending_amount



# Kredi kartı harcama verilerini oluşturma
transaction_data = []

for index, customer in customers_df.iterrows():
    customer_id = customer['CLIENTNUM']
    card_category = customer['Card_Category']
    credit_limit = customer['Credit_Limit']
    total_revolving_bal = customer['Total_Revolving_Bal']
    avg_open_to_buy = customer['Avg_Open_To_Buy']
    
    # Son 6 ay için veri oluşturma
    for month_offset in range(6):
        start_date = datetime.now() - timedelta(days=30 * (month_offset + 1))
        end_date = datetime.now() - timedelta(days=30 * month_offset)
        
        # Her ay için rastgele işlem sayısı belirleme
        num_transactions = random.randint(5, 25)
        
        # Aylık toplam harcama miktarını total_revolving_bal sütunundan sapmalarla belirleme
        monthly_total_spending = total_revolving_bal * (1 + np.random.uniform(-0.3, 0.3))
        
        for _ in range(num_transactions):
            transaction_id = random.randint(100000, 999999)
            transaction_date = get_random_date(start_date, end_date)
            spending_amount = get_spending_amount(card_category, credit_limit)
            expense_type = random.choice(expense_types)
            expense_description = random.choice(expense_descriptions[expense_type])
            
            # Toplam harcama miktarını aşmamak için her işlemde harcama miktarını ayarlama
            if spending_amount > monthly_total_spending:
                spending_amount = monthly_total_spending / num_transactions
            
            transaction_data.append([
                transaction_id, customer_id, transaction_date, spending_amount, expense_type, expense_description
            ])

# DataFrame oluşturma
transactions_df = pd.DataFrame(transaction_data, columns=[
    'transaction_id', 'customer_id', 'transaction_date', 'spending_amount', 'expense_type', 'expense_description'
])



# Müşteri ID ve tarih sütunlarına göre sıralama
transactions_df.sort_values(by=['customer_id', 'transaction_date'], ascending=[True, True], inplace=True)

# Transaction ID indeksini resetleyerek 1'den başlatma
transactions_df.reset_index(drop=True, inplace=True)
transactions_df.index += 1
transactions_df.reset_index(inplace=True)
transactions_df.rename(columns={'index': 'transaction_id'}, inplace=True)


# Verileri CSV dosyasına kaydetme
transactions_df.to_csv('kredi_karti_harcamalar.csv', index=False)

print("Kredi kartı harcama verileri başarıyla oluşturuldu ve kredi_karti_harcamalar.csv dosyasına kaydedildi.")
