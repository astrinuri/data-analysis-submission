import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df_day = pd.read_csv('day.csv')
df_hour = pd.read_csv('hour.csv')

st.title("🚲 Bike Rental Dashboard")

# Membuat tab navigasi di atas
tab_dashboard, tab_analysis = st.tabs(["📊 Dashboard", "📈 Analisis Lanjutan"])

with tab_dashboard:
    st.header("📌 Statistik Penyewaan Sepeda")

    # **Rata-rata Penyewaan Sepeda per Hari**
    df_day["weekday"] = df_day["weekday"].astype("category")
    df_day["weekday"] = df_day["weekday"].cat.rename_categories(
        ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    )
    weekday_rentals = df_day.groupby("weekday")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    palette = ["gray"] * len(weekday_rentals)
    palette[weekday_rentals["cnt"].idxmax()] = "blue"
    sns.barplot(x="weekday", y="cnt", data=weekday_rentals, palette=palette, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.text_area("📌 Insight:", 
    "• Sabtu memiliki jumlah penyewaan tertinggi. Hal ini menunjukkan bahwa akhir pekan, khususnya Sabtu, adalah hari yang paling populer untuk penyewaan sepeda. Mungkin karena banyak orang memiliki waktu luang dan lebih cenderung beraktivitas di luar ruangan.\n"
    "• Hari kerja memiliki tren penyewaan yang relatif stabil. Penyewaan sepeda di hari kerja (Senin-Jumat) tidak memiliki perbedaan signifikan satu sama lain. Ini bisa mengindikasikan bahwa banyak orang menggunakan sepeda sebagai sarana transportasi rutin, seperti untuk bekerja atau sekolah.\n"
    "• Minggu tidak menjadi hari dengan penyewaan tertinggi. Meskipun masih termasuk akhir pekan, jumlah penyewaan di hari Minggu tampaknya sedikit lebih rendah dibandingkan Sabtu. Mungkin karena orang lebih memilih untuk beristirahat atau melakukan aktivitas lain selain bersepeda.",
    key="interp1")


    # **Rata-rata Penyewaan Sepeda Berdasarkan Jam**
    fig, ax = plt.subplots(figsize=(6, 4))
    hr_rentals = df_hour.groupby('hr')["cnt"].mean()
    sns.lineplot(x=hr_rentals.index, y=hr_rentals.values, marker='o', color="gray", ax=ax)
    sns.scatterplot(x=[hr_rentals.idxmax()], y=[hr_rentals.max()], color="blue", s=100, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid()
    st.pyplot(fig)
    st.text_area("📌 Insight:", 
    "• Dua Puncak Penyewaan (Peak Hours) Terlihat Jelas. Puncak pertama terjadi pada pagi hari sekitar pukul 8 pagi, yang kemungkinan besar terkait dengan jam berangkat kerja atau sekolah. Puncak kedua terjadi pada sore hingga malam sekitar pukul 17-18 (ditandai dengan titik biru pada grafik). Ini kemungkinan berhubungan dengan jam pulang kerja atau aktivitas rekreasi setelah jam kerja/sekolah.\n"
    "• Dari pukul 0 hingga 5 pagi, jumlah penyewaan sangat rendah, menunjukkan bahwa sebagian besar orang tidak menggunakan sepeda pada jam tersebut.\n",
    key="interp2")

    # **Rata-rata Penyewaan Berdasarkan Kecepatan Angin**
    df_day["wind_category"] = pd.cut(df_day["windspeed"], bins=[0, 0.1, 0.2, 0.3, 1], 
                                        labels=["Tenang", "Sedang", "Kencang", "Sangat Kencang"])
    wind_rentals = df_day.groupby("wind_category")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    palette = ["gray"] * len(wind_rentals)
    palette[wind_rentals["cnt"].idxmax()] = "blue"
    sns.barplot(x="wind_category", y="cnt", data=wind_rentals, palette=palette, ax=ax)
    ax.set_title("Rata-rata Penyewaan Berdasarkan Kecepatan Angin")
    ax.set_xlabel("Kategori Kecepatan Angin")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.text_area("📌 Insight:", 
    "• Jumlah penyewaan tertinggi terjadi saat angin dalam kondisi Tenang (ditandai dengan warna biru). Seiring meningkatnya kecepatan angin, jumlah penyewaan mengalami penurunan bertahap.\n"
    "• Saat kecepatan angin mencapai kategori Sangat Kencang, jumlah penyewaan sepeda turun drastis, yang menunjukkan bahwa angin kencang menjadi hambatan besar bagi pengguna sepeda.\n",
    key="interp3")

    # **Rata-rata Penyewaan Sepeda Berdasarkan Musim**
    df_day["season"] = df_day["season"].astype("category")
    df_day["season"] = df_day["season"].cat.rename_categories(["Semi", "Panas", "Gugur", "Dingin"])
    season_rentals = df_day.groupby("season")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(6, 4))
    palette = ["gray"] * len(season_rentals)
    palette[season_rentals["cnt"].idxmax()] = "blue"
    sns.barplot(x="season", y="cnt", data=season_rentals, palette=palette, ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig)
    st.text_area("📌 Insight:", 
    "• Musim gugur memiliki rata-rata penyewaan sepeda tertinggi, yang ditandai dengan batang berwarna biru. Ini menunjukkan bahwa musim gugur adalah waktu yang paling populer bagi orang-orang untuk menyewa sepeda.\n"
    "• Musim semi memiliki jumlah penyewaan terendah, mungkin karena cuaca masih tidak menentu atau karena lebih banyak hujan. Musim dingin memiliki lebih banyak penyewaan dibandingkan musim semi, tetapi masih lebih rendah dibandingkan musim panas dan gugur.\n",
    key="interp4")

with tab_analysis:
    st.header("🔹 Clustering Penyewaan Sepeda")

    # **Clustering Penyewaan Sepeda**
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    bins = [0, 2000, 4000, 6000, 8000, 10000]
    labels = ['Sangat Rendah', 'Rendah', 'Sedang', 'Tinggi', 'Sangat Tinggi']
    df_day['Rental_Category'] = pd.cut(df_day['cnt'], bins=bins, labels=labels)

    category_counts = df_day['Rental_Category'].value_counts()
    
    st.write("Jumlah total tanggal per kategori penyewaan:")
    st.bar_chart(category_counts)
    st.text_area("📌 Insight:", 
    "• Sebanyak 272 hari (sekitar 45% dari total hari) masuk dalam kategori Sedang, menunjukkan bahwa pola penyewaan sepeda relatif stabil di level menengah. Ini menandakan bahwa sebagian besar waktu, jumlah penyewaan berada di sekitar rata-rata, tanpa fluktuasi ekstrem.\n"
    "• Sebanyak 98 hari berada dalam kategori Sangat Rendah, yang bisa disebabkan oleh kondisi cuaca buruk, musim dingin, atau faktor lain yang mengurangi minat bersepeda. Sementara itu, hanya 12 hari masuk dalam kategori Sangat Tinggi, menandakan bahwa lonjakan ekstrem dalam penyewaan sangat jarang terjadi. Ini bisa mengindikasikan bahwa faktor khusus seperti event besar, promosi, atau liburan sangat memengaruhi kenaikan drastis dalam penyewaan.\n",
    key="interp5")
