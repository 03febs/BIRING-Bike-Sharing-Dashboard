import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='dark')

st.header(':bicyclist: BIRING : Bike Sharing Dashboard :bicyclist:')

# -------------------------------
# 1. Load Dataset (data_clean_day.csv dan data_clean_hour.csv)
# -------------------------------
df_day = pd.read_csv('dashboard/data_clean_day.csv')
df_hour = pd.read_csv('dashboard/data_clean_hour.csv')

# Konversi kolom tanggal di df_day dan df_hour
df_day['date'] = pd.to_datetime(df_day['date'])
df_hour['date'] = pd.to_datetime(df_hour['date'])

# -------------------------------
# 2. Sidebar: Rentang Waktu
# -------------------------------
min_date = df_day['date'].min()
max_date = df_day['date'].max()

with st.sidebar:
    st.image('..\icon\logo.png', width=200)
    start_date, end_date = st.date_input(
        label='Select a date range',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang tanggal pada dataset harian
filtered_day_df = df_day[
    (df_day['date'] >= pd.to_datetime(start_date)) &
    (df_day['date'] <= pd.to_datetime(end_date))
]

# -------------------------------
# 3. Metrik Utama: Total Casual, Registered, dan Total Sharing Rides
# -------------------------------
total_casual = filtered_day_df['casual'].sum()
total_registered = filtered_day_df['registered'].sum()
total_sharing = filtered_day_df['total_rentals'].sum()  # total_rentals = casual + registered

st.subheader('Daily Bike-Sharing Summary')

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Casual Users", value=total_casual)
with col2:
    st.metric("Total Registered Users", value=total_registered)
with col3:
    st.metric("Total Bike-Sharing", value=total_sharing)

# -------------------------------
# 4. Visualisasi: Tren Penyewaan Harian
# -------------------------------
st.subheader("Daily Bike-Sharing Trend")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(filtered_day_df['date'], filtered_day_df['total_rentals'], marker='o', linewidth=2, color="#90EE90")
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Total Rentals", fontsize=12)
ax.set_title("Daily Bike-Sharing Trend", fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)


# -------------------------------
# 5. Visualisasi: Total Bike-Sharing by Season
# -------------------------------
st.subheader("Total Bike-Sharing by Season")

# Mapping untuk nama musim (sesuai kode label: 1 = Spring, 2 = Summer, 3 = Fall, 4 = Winter)
season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}

# Kelompokkan data berdasarkan musim dan hitung total penyewaan per musim
season_group = filtered_day_df.groupby('season')['total_rentals'].sum().reset_index()
season_group['season_name'] = season_group['season'].map(season_names)

# Identifikasi nilai total penyewaan tertinggi
max_val = season_group['total_rentals'].max()

# Buat daftar warna: hijau jika nilainya sama dengan max_val, abu-abu untuk yang lain
colors = ['#90EE90' if val == max_val else '#D3D3D3' for val in season_group['total_rentals']]

# Plot bar chart dengan seaborn menggunakan list warna
fig2, ax2 = plt.subplots(figsize=(8,6))
sns.barplot(x='season_name', y='total_rentals', data=season_group, palette=colors, ax=ax2)
ax2.set_title("Total Bike-Sharing by Season", fontsize=14)
ax2.set_xlabel("Musim", fontsize=12)
ax2.set_ylabel("Total Penyewaan", fontsize=12)
ax2.ticklabel_format(style='plain', axis='y')
st.pyplot(fig2)


# -------------------------------
# 6. Visualisasi: Hourly Bicycle Usage Pattern (Casual vs Registered)
# -------------------------------
st.subheader("Hourly Bicycle Usage Pattern (Casual vs Registered)")


# Filter dataset df_hour berdasarkan rentang tanggal yang dipilih
filtered_df_hour = df_hour[
    (df_hour['date'] >= pd.to_datetime(start_date)) &
    (df_hour['date'] <= pd.to_datetime(end_date))
].copy()


if 'hour' in filtered_df_hour.columns:
    filtered_df_hour.rename(columns={'hour': 'hour'}, inplace=True)

# Kelompokkan data berdasarkan 'hour' dan hitung rata-rata penyewaan casual dan registered
hour_group = filtered_df_hour.groupby('hour')[['casual', 'registered']].mean().reset_index()

# Buat line plot untuk menunjukkan pola penggunaan
fig3, ax3 = plt.subplots(figsize=(10,6))
sns.lineplot(x='hour', y='casual', data=hour_group, label='Casual', marker='o', ax=ax3)
sns.lineplot(x='hour', y='registered', data=hour_group, label='Registered', marker='o', ax=ax3)

ax3.set_title("Hourly Bicycle Usage Pattern (Casual vs Registered)", fontsize=14)
ax3.set_xlabel("Jam (0-23)", fontsize=12)
ax3.set_ylabel("Rata-rata Pengguna", fontsize=12)
ax3.legend()

st.pyplot(fig3)


# -------------------------------
# 7. Visualisasi: Pada Jam Berapa Permintaan Penyewaan Sepeda Paling Tinggi?
# -------------------------------
st.subheader("Average Bike-Sharing by Hour")

# Kelompokkan data berdasarkan jam dan hitung rata-rata total penyewaan
hourly_stats = filtered_df_hour.groupby('hour')['total_rentals'].mean().reset_index()

# Identifikasi nilai tertinggi
max_val = hourly_stats['total_rentals'].max()

# Buat daftar warna: gunakan hijau untuk nilai tertinggi, dan abu muda untuk yang lainnya
colors = ['#90EE90' if val == max_val else '#D3D3D3' for val in hourly_stats['total_rentals']]

# Buat bar chart menggunakan seaborn
fig4, ax4 = plt.subplots(figsize=(10,6))
sns.barplot(x='hour', y='total_rentals', data=hourly_stats, palette=colors, ax=ax4)
ax4.set_title("Rata-rata Penyewaan Sepeda per Jam", fontsize=14)
ax4.set_xlabel("Jam (0-23)", fontsize=12)
ax4.set_ylabel("Rata-rata Total Penyewaan", fontsize=12)
ax4.set_xticks(range(0, 24))  # Pastikan semua jam tampil di sumbu x

st.pyplot(fig4)


# -------------------------------
# 8.Visualisasi: Correlation Matrix - Factors Influencing Bike-Sharing
# -------------------------------
st.subheader("Correlation Matrix - Factors Influencing Bike-Sharing")

# Hitung matriks korelasi dari dataset asli (df_day)
corr_matrix = df_day.corr()

# Buat figure dan heatmap menggunakan seaborn
fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax_corr)
ax_corr.set_title("Correlation Matrix - Factors Influencing Bike-Sharing", fontsize=16)

# Tampilkan heatmap dalam dashboard
st.pyplot(fig_corr)


# -------------------------------
# 9. Visualisasi: Holiday Impact on Bike-Sharing (Static)
# -------------------------------
st.subheader("Holiday Impact on Bike-Sharing")

# Gunakan dataset asli (df_day) agar visualisasi tidak berubah meskipun rentang tanggal berubah
holiday_stats_day = df_day.groupby('holiday')['total_rentals'].agg(['mean', 'sum', 'std', 'count']).reset_index()
holiday_stats_day['holiday_label'] = holiday_stats_day['holiday'].map({0: 'Non-Holiday', 1: 'Holiday'})

fig3, ax3 = plt.subplots(figsize=(8,6))
sns.barplot(x='holiday_label', y='mean', data=holiday_stats_day, palette=['#90EE90', '#D3D3D3'], ax=ax3)
ax3.set_title("Pengaruh Hari Libur terhadap Rata-rata Penyewaan Sepeda Harian", fontsize=14)
ax3.set_xlabel("Tipe Hari", fontsize=12)
ax3.set_ylabel("Rata-rata Penyewaan", fontsize=12)
ax3.ticklabel_format(style='plain', axis='y')
st.pyplot(fig3)


# ---------------------------------------RFM Analysis--------------------------------------------------------------
# ===============================
# RFM Analysis: Customer Rental Behavior
# ===============================
st.subheader("RFM Analysis: Customer Bike-Sharing Behavior")

# Gunakan filtered_day_df agar analisis RFM sesuai dengan rentang tanggal yang dipilih
# === Recency: Kapan terakhir kali pengguna casual dan registered menyewa sepeda? ===
last_date_casual = filtered_day_df[filtered_day_df['casual'] > 0]['date'].max()
last_date_registered = filtered_day_df[filtered_day_df['registered'] > 0]['date'].max()

casual_rentals_on_last = filtered_day_df.loc[filtered_day_df['date'] == last_date_casual, 'casual'].iloc[0]
registered_rentals_on_last = filtered_day_df.loc[filtered_day_df['date'] == last_date_registered, 'registered'].iloc[0]

recency_table = pd.DataFrame({
    'User_Type': ['Casual', 'Registered'],
    'Last_Rental_Date': [last_date_casual, last_date_registered],
    'Total_Rentals_on_Last_Date': [casual_rentals_on_last, registered_rentals_on_last]
})

# === Frequency: Rata-rata penyewaan per hari untuk masing-masing segmen ===
casual_frequency = filtered_day_df['casual'].mean()
registered_frequency = filtered_day_df['registered'].mean()

# === Monetary: Total jumlah penyewaan selama periode pengamatan untuk masing-masing segmen ===
casual_total = filtered_day_df['casual'].sum()
registered_total = filtered_day_df['registered'].sum()


# ===============================
# Visualisasi RFM Analysis: 3 Subplots
# ===============================
fig_rfm, axs = plt.subplots(1, 3, figsize=(18, 6))

# Subplot 1: Recency
axs[0].bar(recency_table['User_Type'], recency_table['Total_Rentals_on_Last_Date'],
           color=['lightgreen', 'lightgreen'])
axs[0].set_title("Recency: Tanggal Terakhir & Total Penyewaan", fontsize=14)
axs[0].set_ylabel("Total Penyewaan", fontsize=12)
max_height = recency_table['Total_Rentals_on_Last_Date'].max()
axs[0].set_ylim(0, max_height * 1.2)
for i, row in recency_table.iterrows():
    date_str = row['Last_Rental_Date'].strftime("%Y-%m-%d")
    bar_height = row['Total_Rentals_on_Last_Date']
    axs[0].text(i, bar_height + (max_height * 0.05), date_str,
                ha='center', va='bottom', fontsize=10)

# Subplot 2: Frequency
axs[1].bar(['Casual', 'Registered'], [casual_frequency, registered_frequency],
           color=['lightgreen', 'lightgreen'])
axs[1].set_title("Frequency: Rata-rata Penyewaan per Hari", fontsize=14)
axs[1].set_ylabel("Rata-rata Penyewaan", fontsize=12)

# Subplot 3: Monetary
axs[2].bar(['Casual', 'Registered'], [casual_total, registered_total],
           color=['lightgreen', 'lightgreen'])
axs[2].set_title("Monetary: Total Penyewaan", fontsize=14)
axs[2].set_ylabel("Total Penyewaan", fontsize=12)

plt.tight_layout()
st.pyplot(fig_rfm)




st.caption("Copyright (c) BIRING : Bike Sharing Dashboard 2025")
