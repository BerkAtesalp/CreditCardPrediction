import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt


# Modelleri ve preprocessing araçlarını yükleme
def load_model(file_path):
    return joblib.load(file_path)

@st.cache(allow_output_mutation=True)

def load_models_and_scaler():
    models = {}
    scaler = None
    
    try:
        models['credit_card_tran_Amt_6'] = load_model('credit_card_tran_Amt_6_model.pkl')
    except Exception:
        models['credit_card_tran_Amt_6'] = None

    try:
        models['Haziran_Trans_Amt'] = load_model('Haziran_Trans_Amt_model.pkl')
    except Exception:
        models['Haziran_Trans_Amt'] = None

    try:
        models['Jun_hesap_bakiyesi'] = load_model('Jun_hesap_bakiyesi_model.pkl')
    except Exception:
        models['Jun_hesap_bakiyesi'] = None

    try:
        scaler = load_model('scaler.pkl')
    except Exception:
        scaler = None
    
    return models, scaler

# Modelleri ve scaler'ı yükle
models, scaler = load_models_and_scaler()

# CSV dosyalarını okuma
transaction_df = pd.read_csv('transaction10.csv')
musteriler_df = pd.read_csv('musteriler_ml_10.csv')
kredi_karti_df = pd.read_csv('kredi_karti_harcamalar_10.csv')
gercek_degerler_df = pd.read_csv('musteriler_ml_10_gercekler.csv')

musteriler_df = musteriler_df.iloc[:, :-1]

musteriler_df_copy = musteriler_df.copy()

# Eğer preprocessing pipeline, scaler ve modeller varsa tahmin yapma
if scaler and \
   models['credit_card_tran_Amt_6'] and \
   models['Haziran_Trans_Amt'] and \
   models['Jun_hesap_bakiyesi']:
    
    # Ön işleme adımları
    # Gender sütunu için Gender_M oluştur
    musteriler_df['Gender_M'] = musteriler_df['Gender'].apply(lambda x: 1 if x == 'M' else 0)
    musteriler_df = musteriler_df.drop(columns=['Gender'])

    # Eğitim Seviyesi (Education_Level) için Ordinal Encoding
    education_mapping = joblib.load('education_mapping.pkl')
    musteriler_df['Education_Level'] = musteriler_df['Education_Level'].map(education_mapping)

    # Gelir Kategorisi (Income_Category) için Ordinal Encoding
    income_mapping = joblib.load('income_mapping.pkl')
    musteriler_df['Income_Category'] = musteriler_df['Income_Category'].map(income_mapping)

    # Kart Kategorisi (Card_Category) için Ordinal Encoding
    card_mapping = joblib.load('card_mapping.pkl')
    musteriler_df['Card_Category'] = musteriler_df['Card_Category'].map(card_mapping)

    # Meslek (jobs) için Label Encoding
    job_mapping = joblib.load('job_mapping.pkl')
    musteriler_df['jobs'] = musteriler_df['jobs'].map(job_mapping)

    # Medeni Durum (Marital_Status) için One-Hot Encoding
    encoder_marital_status = joblib.load('encoder_marital_status.pkl')
    marital_status_encoded = encoder_marital_status.transform(musteriler_df[['Marital_Status']])
    marital_status_encoded_df = pd.DataFrame(marital_status_encoded, columns=encoder_marital_status.get_feature_names_out(['Marital_Status']))
    marital_status_encoded_df['Marital_Status_Divorced'] = 0
    musteriler_df = pd.concat([musteriler_df, marital_status_encoded_df], axis=1)
    musteriler_df = musteriler_df.drop(columns=['Marital_Status'])

    # Object tipindeki sütunları sil
    object_columns = musteriler_df.select_dtypes(include=['object']).columns
    musteriler_df = musteriler_df.drop(columns=object_columns)

    # Sütun sıralamasını kontrol edin ve eşitlenmesini sağlayın
    musteriler_df = musteriler_df[scaler.feature_names_in_]

    # Eğer scaler varsa verileri ölçekleme
    musteriler_scaled = scaler.transform(musteriler_df)
    
    # Tahminler yapma
    credit_card_tran_Amt_6_pred = models['credit_card_tran_Amt_6'].predict(musteriler_scaled)
    Haziran_Trans_Amt_pred = models['Haziran_Trans_Amt'].predict(musteriler_scaled)
    Jun_hesap_bakiyesi_pred = models['Jun_hesap_bakiyesi'].predict(musteriler_scaled)

    # Sonuçları bir DataFrame'de toplama
    tahminler_df = pd.DataFrame({
        'CustomerID': musteriler_df['CustomerID'],
        'credit_card_tran_Amt_6_prediction': credit_card_tran_Amt_6_pred,
        'Haziran_Trans_Amt_prediction': Haziran_Trans_Amt_pred,
        'Jun_hesap_bakiyesi_prediction': Jun_hesap_bakiyesi_pred
    })
    






# Streamlit başlatma
st.title('Müşteri Bilgileri Görüntüleme')


# Müşteri ID'lerini seçmek için selectbox ekleme
customer_ids = musteriler_df['CustomerID'].unique()
selected_customer_id = st.selectbox('Müşteri ID seçin', customer_ids)


 
# Seçilen müşterinin bilgilerini gösterme
selected_customer_info = musteriler_df_copy[musteriler_df_copy['CustomerID'] == selected_customer_id]

st.write('Seçilen Müşterinin Bilgileri:')
st.dataframe(selected_customer_info)



# Gerçek değerlerle tahminleri karşılaştırma
real_values = gercek_degerler_df[gercek_degerler_df['CustomerID'] == selected_customer_id]
    
if not real_values.empty:
    real_credit_card_tran_Amt_6 = real_values['credit_card_tran_Amt_6'].values[0]
    predicted_credit_card_tran_Amt_6 = tahminler_df.loc[tahminler_df['CustomerID'] == selected_customer_id, 'credit_card_tran_Amt_6_prediction'].iloc[0]

    if real_credit_card_tran_Amt_6 > predicted_credit_card_tran_Amt_6:
        # Gerçek harcama tahmin edilen harcamadan fazlaysa
        difference = real_credit_card_tran_Amt_6 - predicted_credit_card_tran_Amt_6
        percentage = (difference / predicted_credit_card_tran_Amt_6) * 100
        st.write(f"Gerçek harcamanız tahmin edilen harcamadan %{percentage:.2f} daha fazla.")
        
        if percentage > 50:
            st.write("Harcamalarınız çok yüksek! Bütçenizi gözden geçirmenizde fayda var.")
        elif percentage > 20:
            st.write("Harcamalarınız tahmin edilen miktardan biraz yüksek. Bütçenizi kontrol edin.")
        else:
            st.write("Harcamalarınız tahmin edilen miktardan biraz fazla, dikkat edin.")

    elif real_credit_card_tran_Amt_6 < predicted_credit_card_tran_Amt_6:
        # Gerçek harcama tahmin edilen harcamadan azsa
        difference = predicted_credit_card_tran_Amt_6 - real_credit_card_tran_Amt_6
        percentage = (difference / real_credit_card_tran_Amt_6) * 100
        st.write(f"Harcamalarınız tahmin edilen miktarın %{percentage:.2f} altında kaldı.")
        
        if percentage > 50:
            st.write("Harika iş çıkardınız! Bütçenize daha fazla katkı sağladınız.")
        elif percentage > 20:
            st.write("Bütçeniz tahmin edilenden daha iyi. İyi bir yönetim gösterdiniz!")
        else:
            st.write("Harcamalarınız tahmin edilenden biraz düşük. Başarılı bir bütçe yönetimi!")
               
               
# Jun_hesap_bakiyesi için gerçek ve tahmin edilen değerleri karşılaştırma
real_Jun_hesap_bakiyesi = real_values['Jun_hesap_bakiyesi'].values[0]
predicted_Jun_hesap_bakiyesi = tahminler_df.loc[tahminler_df['CustomerID'] == selected_customer_id, 'Jun_hesap_bakiyesi_prediction'].iloc[0]

if real_Jun_hesap_bakiyesi > predicted_Jun_hesap_bakiyesi:
    # Gerçek hesap bakiyesi tahmin edilen hesap bakiyesinden fazlaysa
    difference = real_Jun_hesap_bakiyesi - predicted_Jun_hesap_bakiyesi
    percentage = (difference / real_Jun_hesap_bakiyesi) * 100
    st.write(f"Gerçek hesap bakiyeniz tahmin edilen bakiyeden %{percentage:.2f} daha fazla.")
    
    if percentage > 50:
        st.write("Hesap bakiyeniz oldukça yüksek! Finansal durumunuzu gözden geçirin.")
    elif percentage > 20:
        st.write("Hesap bakiyeniz tahmin edilenden biraz yüksek. Harcamalarınızı dikkatle takip edin.")
    else:
        st.write("Hesap bakiyeniz tahmin edilenden biraz fazla, dikkatli olun.")

elif real_Jun_hesap_bakiyesi < predicted_Jun_hesap_bakiyesi:
    # Gerçek hesap bakiyesi tahmin edilen hesap bakiyesinden azsa
    difference = predicted_Jun_hesap_bakiyesi - real_Jun_hesap_bakiyesi
    percentage = (difference / real_Jun_hesap_bakiyesi) * 100
    st.write(f"Hesap bakiyeniz tahmin edilen miktarın %{percentage:.2f} altında kaldı.")
    
    if percentage > 50:
        st.write("Hesap bakiyeniz tahmin edilenden çok düşük. Tasarruf yapmanız gerekebilir.")
    elif percentage > 20:
        st.write("Hesap bakiyeniz tahmin edilenden biraz düşük. Harcamalarınızı gözden geçirin.")
    else:
        st.write("Hesap bakiyeniz tahmin edilenden biraz düşük. Tasarruf etme fırsatını değerlendirin.")

# Geçmiş bakiye ve gelecek ay tahmini bakiye ile analiz yapma
gecmis_bakiyeler = musteriler_df_copy.loc[musteriler_df_copy['CustomerID'] == selected_customer_id, ['Jan_hesap_bakiyesi', 'Feb_hesap_bakiyesi', 'Mar_hesap_bakiyesi', 'Apr_hesap_bakiyesi', 'May_hesap_bakiyesi']]
gecmis_bakiyeler_mean = gecmis_bakiyeler.mean(axis=1).values[0]
gelecek_ay_bakiye = predicted_Jun_hesap_bakiyesi

# Yüzdesel değişim hesaplama
artis_orani = ((gelecek_ay_bakiye - gecmis_bakiyeler_mean) / gecmis_bakiyeler_mean) * 100
azalis_orani = -artis_orani

if gelecek_ay_bakiye > gecmis_bakiyeler_mean:
    if artis_orani >= 20:
        st.write(f"Gelecek ay hesap bakiyenizin geçmiş aylardan % {artis_orani:.2f} oranında artması bekleniyor. Tasarruf yapma fırsatını değerlendirin!")
    elif artis_orani >= 10:
        st.write(f"Gelecek ay hesap bakiyenizde geçmiş aylardan % {artis_orani:.2f} oranında bir artış bekleniyor. Tasarruflarınızı planlayın.")
    else:
        st.write("Gelecek ay hesap bakiyenizde geçmiş aylardan biraz artış olacak. Giderlerinizi gözden geçirin.")
elif gelecek_ay_bakiye < gecmis_bakiyeler_mean:
    if azalis_orani >= 20:
        st.write(f"Gelecek ay hesap bakiyenizin geçmiş aylardan % {azalis_orani:.2f} oranında azalması bekleniyor. Harcamalarınızı kısmanız gerekebilir.")
    elif azalis_orani >= 10:
        st.write(f"Gelecek ay hesap bakiyenizde geçmiş aylardan % {azalis_orani:.2f} oranında bir azalma bekleniyor. Tasarruf etme yollarını araştırın.")
    else:
        st.write("Gelecek ay hesap bakiyenizde geçmiş aylardan biraz azalma olacak. Bütçenizi gözden geçirin.")





# Öneriler için credit_card_tran_Amt_degisim_4to5 ve diğer sütunlara bakma
credit_card_tran_Amt_degisim_4to5 = selected_customer_info['credit_cart_tran_Amt_degisim_4to5'].values[0]
credit_card_tran_ct_degisim_4to5 = selected_customer_info['credit_cart_tran_ct_degisim_4to5'].values[0]
nisan_to_mayis_tran_amt_degisim = selected_customer_info['nisan_to_mayis_tran_amt_degisim'].values[0]
nisan_to_mayis_tran_ct_degisim = selected_customer_info['nisan_to_mayis_tran_ct_degisim'].values[0]
# Kredi kartı harcama değişimi
if credit_card_tran_Amt_degisim_4to5 > 0.4:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {credit_card_tran_Amt_degisim_4to5:.2f} oranında büyük bir artış gösterdi. Harcamalarınızı ciddi şekilde gözden geçirmeniz gerekebilir.")
elif credit_card_tran_Amt_degisim_4to5 > 0.2:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {credit_card_tran_Amt_degisim_4to5:.2f} oranında arttı. Harcamalarınızı planlamada dikkatli olmalısınız.")
elif credit_card_tran_Amt_degisim_4to5 > 0:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {credit_card_tran_Amt_degisim_4to5:.2f} oranında bir artış gösterdi. Harcamalarınıza dikkat etmenizde fayda var.")
elif credit_card_tran_Amt_degisim_4to5 < -0.4:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {-credit_card_tran_Amt_degisim_4to5:.2f} oranında büyük bir azalma yaşandı. Harcamalarınızı iyi yönettiğiniz için tebrikler!")
elif credit_card_tran_Amt_degisim_4to5 < -0.2:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {-credit_card_tran_Amt_degisim_4to5:.2f} oranında azaldı. Tasarruf etme konusunda başarılısınız.")
elif credit_card_tran_Amt_degisim_4to5 < 0:
    st.write(f"Kredi kartı harcamalarınız 4. aydan 5. aya % {-credit_card_tran_Amt_degisim_4to5:.2f} oranında azaldı. Bu durum tasarruf etme konusunda olumlu bir işaret.")
    
# Kredi kartı işlem sayısı değişimi
if credit_card_tran_ct_degisim_4to5 > 0.4:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {credit_card_tran_ct_degisim_4to5:.2f} oranında büyük bir artış gösterdi. İşlem sayınızı dikkatlice gözden geçirmeniz gerekebilir.")
elif credit_card_tran_ct_degisim_4to5 > 0.2:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {credit_card_tran_ct_degisim_4to5:.2f} oranında arttı. İşlemlerinizin artışıyla ilgili dikkatli olmalısınız.")
elif credit_card_tran_ct_degisim_4to5 > 0:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {credit_card_tran_ct_degisim_4to5:.2f} oranında arttı. İşlem sayınızı kontrol etmenizde fayda var.")
elif credit_card_tran_ct_degisim_4to5 < -0.4:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {-credit_card_tran_ct_degisim_4to5:.2f} oranında büyük bir azalma gösterdi. İşlem sayınızı başarılı bir şekilde yönettiğiniz için tebrikler!")
elif credit_card_tran_ct_degisim_4to5 < -0.2:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {-credit_card_tran_ct_degisim_4to5:.2f} oranında azaldı. Bu durum harcamalarınızı iyi yönettiğinizin bir işareti.")
elif credit_card_tran_ct_degisim_4to5 < 0:
    st.write(f"Kredi kartı işlem sayınız 4. aydan 5. aya % {-credit_card_tran_ct_degisim_4to5:.2f} oranında azaldı. İşlemlerdeki bu azalma tasarruf sağladığınızı gösteriyor.")
    
# Nisan'dan Mayıs'a kadar işlem tutar değişimi
if nisan_to_mayis_tran_amt_degisim > 0.4:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {nisan_to_mayis_tran_amt_degisim:.2f} oranında büyük bir artış gösterdi. Harcamalarınızı dikkatlice gözden geçirmeniz gerekebilir.")
elif nisan_to_mayis_tran_amt_degisim > 0.2:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {nisan_to_mayis_tran_amt_degisim:.2f} oranında arttı. Harcamalarınızı planlamada dikkatli olmalısınız.")
elif nisan_to_mayis_tran_amt_degisim > 0:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {nisan_to_mayis_tran_amt_degisim:.2f} oranında bir artış gösterdi. Harcamalarınıza dikkat etmenizde fayda var.")
elif nisan_to_mayis_tran_amt_degisim < -0.4:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {-nisan_to_mayis_tran_amt_degisim:.2f} oranında büyük bir azalma yaşandı. Tasarruf etme konusunda başarılısınız!")
elif nisan_to_mayis_tran_amt_degisim < -0.2:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {-nisan_to_mayis_tran_amt_degisim:.2f} oranında azaldı. Harcamalarınızı başarılı bir şekilde yönettiğiniz için tebrikler!")
elif nisan_to_mayis_tran_amt_degisim < 0:
    st.write(f"Nisan'dan Mayıs'a kadar işlem tutarınız % {-nisan_to_mayis_tran_amt_degisim:.2f} oranında azaldı. Bu durum tasarruf sağladığınızı gösteriyor.")
    
# Nisan'dan Mayıs'a kadar işlem sayısı değişimi
if nisan_to_mayis_tran_ct_degisim > 0.4:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {nisan_to_mayis_tran_ct_degisim:.2f} oranında büyük bir artış gösterdi. İşlem sayınızı dikkatlice gözden geçirmeniz gerekebilir.")
elif nisan_to_mayis_tran_ct_degisim > 0.2:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {nisan_to_mayis_tran_ct_degisim:.2f} oranında arttı. İşlem sayınızı planlamada dikkatli olmalısınız.")
elif nisan_to_mayis_tran_ct_degisim > 0:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {nisan_to_mayis_tran_ct_degisim:.2f} oranında bir artış gösterdi. İşlem sayınızı kontrol etmenizde fayda var.")
elif nisan_to_mayis_tran_ct_degisim < -0.4:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {-nisan_to_mayis_tran_ct_degisim:.2f} oranında büyük bir azalma yaşandı. İşlem sayınızı başarılı bir şekilde yönettiğiniz için tebrikler!")
elif nisan_to_mayis_tran_ct_degisim < -0.2:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {-nisan_to_mayis_tran_ct_degisim:.2f} oranında azaldı. Harcamalarınızı başarılı bir şekilde yönettiğiniz için tebrikler!")
elif nisan_to_mayis_tran_ct_degisim < 0:
    st.write(f"Nisan'dan Mayıs'a kadar işlem sayınız % {-nisan_to_mayis_tran_ct_degisim:.2f} oranında azaldı. Bu durum işlemlerinizin azaldığını ve tasarruf sağladığınızı gösteriyor.")
    
    
       

       
# Müşteri işlemlerini al
customer_transactions = transaction_df[transaction_df['CustomerID'] == selected_customer_id]

# Kategorilere göre işlem sayısını hesapla ve en çok işlem yapılan 5 kategoriyi seç
top5_categories = customer_transactions['Description'].value_counts().nlargest(5)

# Eğer en çok işlem yapılan 5 kategori varsa, pasta grafiği oluştur
if not top5_categories.empty:
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(top5_categories, labels=top5_categories.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(5)))
    ax.set_title('En Çok İşlem Yapılan 5 Kategori Açıklaması')
    
    # Streamlit'te grafiği göster
    st.pyplot(fig)
else:
    st.write("Seçilen müşteri için işlem bulunamadı.")
    

# Zaman içinde toplam kredi kartı harcamasını hesapla
transactions_amount_over_time = customer_transactions.groupby('TransactionDate')['Amount'].sum()

# Grafik oluştur
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(transactions_amount_over_time, label='Toplam Hesap Hareketi Miktarı', color='blue')
ax.set_title('Zaman İçinde Hesap Hareketleri Miktarları')
ax.set_xlabel('Tarih')
ax.set_ylabel('Miktar')
ax.legend()

# Streamlit'te grafiği göster
st.pyplot(fig)
    



# Zaman içinde hesap bakiyesinin değişimini hesapla
balance_over_time = customer_transactions.groupby('TransactionDate')['UpdatedBalance'].last()

# Grafik oluştur
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(balance_over_time, label='Hesap Bakiyesi', color='purple')
ax.set_title('Zaman İçinde Hesap Bakiyesi')
ax.set_xlabel('Tarih')
ax.set_ylabel('Güncellenmiş Bakiye')
ax.legend()

# Streamlit'te grafiği göster
st.pyplot(fig)
    
    
# Tarih sütununu datetime formatına dönüştür
customer_transactions['TransactionDate'] = pd.to_datetime(customer_transactions['TransactionDate'])
  
    
# Son 3 ay ve son ayın en çok harcama yapılan kategorilerini hesapla
last_three_months = customer_transactions[customer_transactions['TransactionDate'] >= (customer_transactions['TransactionDate'].max() - pd.DateOffset(months=3))]
last_month = customer_transactions[customer_transactions['TransactionDate'] >= (customer_transactions['TransactionDate'].max() - pd.DateOffset(months=1))]

top5_categories_last_three_months = last_three_months['Description'].value_counts().nlargest(5)
top5_categories_last_month = last_month['Description'].value_counts().nlargest(5)

# Son 3 ayın en çok harcama yapılan kategorileri grafiği
fig1, ax1 = plt.subplots(figsize=(10, 8))
ax1.pie(top5_categories_last_three_months, labels=top5_categories_last_three_months.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(5)))
ax1.set_title('Son 3 Ayın En Çok Sayıda Harcama Yapılan 5 Kategorisi')

# Son ayın en çok harcama yapılan kategorileri grafiği
fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.pie(top5_categories_last_month, labels=top5_categories_last_month.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(5)))
ax2.set_title('Son Ayın En Çok Sayıda Harcama Yapılan 5 Kategorisi')

# Streamlit'te grafikleri göster
st.pyplot(fig1)
st.pyplot(fig2)
    
        
     
# Tarih sütununu datetime formatına dönüştür
kredi_karti_df['transaction_date'] = pd.to_datetime(kredi_karti_df['transaction_date'])


# Seçilen müşteri için işlemleri filtrele
customer_transactions = kredi_karti_df[kredi_karti_df['customer_id'] == selected_customer_id]

# Kategorilere göre en çok harcama yapılan 5 expense type
top5_expenses = customer_transactions['expense_type'].value_counts().nlargest(5)

# Son 3 ay ve son ayın verilerini filtrele
last_three_months = customer_transactions[customer_transactions['transaction_date'] >= (customer_transactions['transaction_date'].max() - pd.DateOffset(months=3))]
last_month = customer_transactions[customer_transactions['transaction_date'] >= (customer_transactions['transaction_date'].max() - pd.DateOffset(months=1))]

# Son 3 ayın en çok harcama yapılan 5 expense type
top5_expenses_last_three_months = last_three_months['expense_type'].value_counts().nlargest(5)
top5_expenses_last_month = last_month['expense_type'].value_counts().nlargest(5)

# Son 3 ay ve son ay için pasta grafiği
fig1, ax1 = plt.subplots(figsize=(10, 8))
ax1.pie(top5_expenses_last_three_months, labels=top5_expenses_last_three_months.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(5)))
ax1.set_title('Son 3 Ayın En Çok Harcama Yapılan 5 Expense Type')

fig2, ax2 = plt.subplots(figsize=(10, 8))
ax2.pie(top5_expenses_last_month, labels=top5_expenses_last_month.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(5)))
ax2.set_title('Son Ayın En Çok Harcama Yapılan 5 Expense Type')

# Streamlit'te grafikleri göster
st.pyplot(fig1)
st.pyplot(fig2)

# En çok sayıda yapılan harcama türü için kutu grafiği
top_expense_descriptions = customer_transactions['expense_description'].value_counts().nlargest(10)
fig3, ax3 = plt.subplots(figsize=(12, 8))
top_expense_descriptions.plot(kind='bar', ax=ax3, color='orange')
ax3.set_title('En Çok Sayıda Yapılan Harcama Türleri')
ax3.set_xlabel('Expense Description')
ax3.set_ylabel('Count')

st.pyplot(fig3)

# Zaman içindeki harcamaları çizgi grafiği
spending_over_time = customer_transactions.groupby('transaction_date')['spending_amount'].sum()
fig4, ax4 = plt.subplots(figsize=(14, 8))
ax4.plot(spending_over_time.index, spending_over_time.values, label='Total Spending Amount', color='blue')
ax4.set_title('Harcama Miktarlarının Zaman İçindeki Değişimi')
ax4.set_xlabel('Tarih')
ax4.set_ylabel('Toplam Harcama Miktarı')
ax4.legend()

st.pyplot(fig4)
   




