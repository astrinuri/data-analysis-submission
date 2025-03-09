import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_day = pd.read_csv('dashboard/day.csv')
df_hour = pd.read_csv('dashboard/hour.csv')

df_day['dteday'] = pd.to_datetime(df_day['dteday'])

st.title("🚲 Bike Rental Dashboard")

# Sidebar untuk filtering
st.sidebar.header("📌 Filter Data")

# Filter berdasarkan tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", 
                                  [df_day['dteday'].min(), df_day['dteday'].max()], 
                                  min_value=df_day['dteday'].min(), max_value=df_day['dteday'].max())

# Filter berdasarkan musim (season)
season_options = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
df_day["season"] = df_day["season"].map(season_options)
selected_seasons = st.sidebar.multiselect("Pilih Musim", list(season_options.values()), default=list(season_options.values()))

# Filter berdasarkan cuaca (weathersit)
weather_options = {1: "Cerah", 2: "Mendung", 3: "Hujan", 4: "Salju"}
df_day["weathersit"] = df_day["weathersit"].map(weather_options)
selected_weather = st.sidebar.multiselect("Pilih Cuaca", list(weather_options.values()), default=list(weather_options.values()))

# Terapkan filter
df_filtered = df_day[(df_day['dteday'] >= pd.to_datetime(date_range[0])) & 
                     (df_day['dteday'] <= pd.to_datetime(date_range[1])) & 
                     (df_day['season'].isin(selected_seasons)) & 
                     (df_day['weathersit'].isin(selected_weather))]

# Tab navigasi
tab_dashboard, tab_analysis = st.tabs(["📊 Dashboard", "📈 Analisis Lanjutan"])

with tab_dashboard:
    st.header("📌 Statistik Penyewaan Sepeda")

    # **Rata-rata Penyewaan Sepeda per Hari**
    weekday_rentals = df_filtered.groupby(df_filtered['dteday'].dt.day_name())['cnt'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x='dteday', y='cnt', data=weekday_rentals, ax=ax, palette="Blues")
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # **Rata-rata Penyewaan Berdasarkan Musim**
    season_rentals = df_filtered.groupby("season")["cnt"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="season", y="cnt", data=season_rentals, palette="coolwarm", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

    # **Rata-rata Penyewaan Berdasarkan Cuaca**
    weather_rentals = df_filtered.groupby("weathersit")["cnt"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x="weathersit", y="cnt", data=weather_rentals, palette="viridis", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Cuaca")
    ax.set_xlabel("Cuaca")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)

with tab_analysis:
    st.header("🔹 Clustering Penyewaan Sepeda")

    st.write("""
    **Tujuan Analisis:**  
    Pengelompokan ini bertujuan untuk mengkategorikan jumlah penyewaan sepeda per hari ke dalam lima tingkat—Sangat Rendah, Rendah, Sedang, Tinggi, dan Sangat Tinggi—berdasarkan rentang tertentu.
    """)

    bins = [0, 2000, 4000, 6000, 8000, 10000]
    labels = ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    df_filtered['Rental_Category'] = pd.cut(df_filtered['cnt'], bins=bins, labels=labels)

    category_counts = df_filtered['Rental_Category'].value_counts()
    st.write("Jumlah total tanggal per kategori penyewaan:")
    st.bar_chart(category_counts)

    st.write("""
    **Insight Analisis:**  
    Dengan klasifikasi ini, kita dapat memahami distribusi penyewaan sepeda, mengidentifikasi pola penggunaan, serta membantu pengelola dalam merencanakan strategi operasional seperti pengadaan sepeda dan promosi pada periode dengan permintaan tinggi
    """)
    

st.sidebar.write("Mari mengeksplor! 🚀")
