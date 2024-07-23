import pandas as pd
import numpy as np

# CSV dosyasını yükle
df = pd.read_csv('BankChurners_segment2.csv')

meslekler = ['student','retired', 'management', 'technician', 'admin.', 'self-employed','blue-collar','engineer', 
             'housemaid','services','sales', 'consultant',
             'unemployed','entrepreneur',
              
              ]

meslek_olasiliklari = {
    'blue-collar': {'age': [28, 55], 'income': ['Less than $40K'], 'gender': ['M', 'F'],
                    'education': ['High School', 'Uneducated']},
    'management': {'age': [30, 60], 'income': ['$60K - $80K','$80K - $120K', '$120K +'], 'gender': ['M', 'F'],
                   'education': ['Graduate', 'Post-Graduate', 'Doctorate']},
    'technician': {'age': [25, 50], 'income': ['$40K - $60K'], 'gender': ['M', 'F'],
                   'education': ['High School', 'College']},
    'admin.': {'age': [35, 55], 'income': ['$40K - $60K', '$60K - $80K'], 'gender': ['M', 'F'],
               'education': ['High School', 'College','Graduate']},
    'services': {'age': [20, 50], 'income': ['Less than $40K'], 'gender': ['M', 'F'],
                 'education': ['High School', 'Uneducated','Unknown']},
    'entrepreneur': {'age': [30, 60], 'income': ['$60K - $80K','$80K - $120K', '$120K +'], 'gender': ['M', 'F'],
                     'education': ['College','Graduate', 'Post-Graduate', 'Doctorate']},
    'retired': {'age': [60, 100], 'income': ['Less than $40K','$40K - $60K', '$60K - $80K','Unknown'], 'gender': ['M', 'F'],
                'education': ['Unknown','High School','Uneducated','Graduate', 'Post-Graduate']},
    'self-employed': {'age': [25, 60], 'income': ['$60K - $80K', '$80K - $120K'], 'gender': ['M', 'F'],
                      'education': ['Unknown','High School','College', 'Graduate', 'Post-Graduate']},
    'unemployed': {'age': [18, 65], 'income': ['Less than $40K'], 'gender': ['M', 'F'],
                   'education': ['High School', 'Uneducated']},
    'housemaid': {'age': [35, 45], 'income': ['Less than $40K'], 'gender': ['F'],
                  'education': ['High School', 'Uneducated','Unknown']},
    'student': {'age': [18, 30], 'income': ['Less than $40K'], 'gender': ['M', 'F'],
                'education': ['College', 'Graduate']},
    'sales': {'age': [25, 50], 'income': ['$40K - $60K','$60K - $80K'], 'gender': ['M', 'F'],
              'education': ['High School', 'College','Unknown']},
    'consultant': {'age': [35, 60], 'income': ['$60K - $80K','$80K - $120K', '$120K +'], 'gender': ['M', 'F'],
                   'education': ['Graduate', 'Post-Graduate', 'Doctorate']},
    'engineer': {'age': [30, 55], 'income': ['$60K - $80K', '$80K - $120K', '$120K +'], 'gender': ['M', 'F'],
                 'education': ['College','Graduate', 'Post-Graduate', 'Doctorate']}
}

# Meslek sütunu ekleyin ve ilk olarak 'unknown' olarak işaretleyin
df['jobs'] = 'unknown'

# Her satır için meslek ataması yapın
for idx, row in df.iterrows():
    customer_age = row['Customer_Age']
    gender = row['Gender']
    income_category = row['Income_Category']
    education = row['Education_Level']
    
    selected_job = 'unknown'  # Başlangıçta 'unknown'
    
    # Meslek seçimi için uygunluk kontrolü
    for meslek in meslekler:
        criteria = meslek_olasiliklari[meslek]
        age_criteria = criteria['age']
        income_criteria = criteria['income']
        gender_criteria = criteria['gender']
        education_criteria = criteria['education']
        
        # Tüm kriterleri kontrol et
        if ((income_category in income_criteria or 'Unknown' in income_criteria) and 
            (education in education_criteria or 'Unknown' in education_criteria) and 
            age_criteria[0] <= customer_age <= age_criteria[1] and 
            gender in gender_criteria):
            selected_job = meslek
            break
    
    # Dataframe'e meslek ataması yap
    df.at[idx, 'jobs'] = selected_job

# Sonuçları kontrol edin
print(df[['Customer_Age', 'Gender', 'Income_Category', 'jobs']].head(20))

# 'unknown' sütununun value_counts sonuçlarını göster
print("\njobs Sütunu Dağılımları:")
print(df['jobs'].value_counts())

# Yeni veri setini kaydedin
df.to_csv('musteriler_guncel.csv', index=False)