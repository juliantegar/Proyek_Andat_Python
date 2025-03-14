# -*- coding: utf-8 -*-
"""dashboardandat

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MAtXQLwmTXrV_gOtlDfCPubABM5IuWJO
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

st.title("Proyek Analisis Data")
st.sidebar.header("Bike Sharing")
st.subheader("Visualisasi Data")

st.write("Performa Pengguna Sepeda per Bulan pada Tahun 2011-2012")
plt.figure(figsize=(24,5))
monthly_means=day_df['cnt'].groupby(day_df['dteday']).mean()
plt.scatter(monthly_means.index, monthly_means.values, c="#72BCD4", s=10, marker='o')
plt.plot(monthly_means.index, monthly_means.values)
plt.xlabel('Bulan')
plt.ylabel('Jumlah')
plt.title('Grafik Jumlah Pengguna Sepeda per Bulan pada Tahun 2011-2012')
st.pyplot(plt)

st.write('Performa Penggunaan Sepeda berdasarkan Jam')
jam_sewa=hour_df.groupby(by='hr').agg({
    'cnt': ['min', 'mean', 'max'],
}).reset_index()
plt.figure(figsize=(10,5))
plt.plot(jam_sewa['hr'], jam_sewa[('cnt','mean')], marker='o',linewidth=2, color='green')
plt.title('Penggunaan sepeda berdasarkan jam')
plt.xlabel('Jam')
plt.xticks(jam_sewa['hr'])
plt.ylabel('Jumlah Penyewaan')
plt.grid(True)
st.pyplot(plt)

st.write('Perbandingan Penggunaan Sepeda berdasarkan Hari')
hari_sewa = day_df.groupby(['workingday', 'weekday'])['cnt'].mean().reset_index()
day_mapping = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
hari_sewa['weekday'] = hari_sewa['weekday'].map(day_mapping)
plt.figure(figsize=(10, 6))
sns.barplot(x='weekday', y='cnt', hue='workingday', data=hari_sewa, palette=['red', 'blue'])
plt.title('Perbandingan Rata-rata Penyewaan Sepeda: Hari Kerja vs Hari Libur')
plt.xlabel('Hari')
plt.ylabel('Rata-rata Penyewaan')
handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, ['Libur (0)', 'Hari Kerja (1)'], title="Workingday")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(plt)

st.write("Jumlah Pengguna Sepeda Berdasarkan Musim")
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
day_df['season'] = day_df['season'].replace(season_mapping)
season_usage = day_df.groupby('season')['cnt'].mean().reset_index()

plt.figure(figsize=(12, 5))
sns.barplot(x='season', y='cnt', data=season_usage, color='brown')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

st.write('Penggunaan Sepeda berdasarkan Kondisi Cuaca')
weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow', 4: 'Heavy Rain'}
day_df['weathersit'] = day_df['weathersit'].replace(weather_mapping)
all_weather = pd.DataFrame({'weathersit': ['Clear', 'Mist', 'Light Snow', 'Heavy Rain']})
weather_usage = day_df.groupby('weathersit')['cnt'].mean().reset_index()
weather_usage = all_weather.merge(weather_usage, on='weathersit', how='left').fillna(0)

plt.figure(figsize=(12, 5))
sns.barplot(x='weathersit', y='cnt', data=weather_usage, color='brown')
plt.title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
plt.xlabel('Kondisi Cuaca')
plt.ylabel('Rata-rata Penyewaan Sepeda')
plt.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(plt)

st.write('Kelompok Pengguna Sepeda Berdasarkan Jumlah Pengguna & Suhu')
X = day_df[['cnt', 'temp']]
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=42)
day_df['cluster'] = kmeans.fit_predict(X_scaled)


plt.figure(figsize=(8,6))
sns.scatterplot(x=day_df['cnt'], y=day_df['temp'], hue=day_df['cluster'], palette=['blue', 'red', 'green'], alpha=0.7)
plt.title('Clustering Penggunaan Sepeda berdasarkan Jumlah Penyewaan & Suhu')
plt.xlabel('Jumlah Penyewaan Sepeda')
plt.ylabel('Suhu')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

st.caption('Copyright © Dicoding 2023')
