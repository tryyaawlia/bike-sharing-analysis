import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sns.set(style="dark")

# Konfigurasi dashboard
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Memuat berkas csv sebagai sebuah dataframe
@st.cache_data
def load_data():
    hour_df = pd.read_csv(BASE_DIR / "main_data.csv", parse_dates=["dteday"])

    day_df = pd.read_csv(BASE_DIR.parent / "data" / "day.csv", parse_dates=["dteday"])

    return hour_df, day_df

hour_df, day_df = load_data()

# Membuat header pada dashboard
st.header("Bike Sharing Dashboard 🚲")
st.subheader("Bike Sharing Data Analysis (2011–2012)")

st.write(
    "Dashboard ini menyajikan analisis pola penyewaan "
    "sepeda berdasarkan waktu, kondisi lingkungan, "
    "dan karakteristik pengguna."
)

# Filter data berdasarkan tanggal
min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

with st.sidebar:
    st.header("Bike Sharing Dashboard")
    st.subheader("Filter Data")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date)
    )

# Filter hourly dataset
main_hour_df = hour_df[
    (hour_df["dteday"].dt.date >= start_date) &
    (hour_df["dteday"].dt.date <= end_date)
]

# Filter daily dataset
main_day_df = day_df[
    (day_df["dteday"].dt.date >= start_date) &
    (day_df["dteday"].dt.date <= end_date)
]

# Membuat main dashboard metrics menggunakan metric() dan layout columns()
st.subheader("Bike Sharing Overview")

col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = main_day_df["cnt"].sum()
    st.metric(
        label="Total Bike Rentals",
        value=f"{total_rentals:,}"
    )

with col2:
    total_casual = main_day_df["casual"].sum()
    st.metric(
        label="Casual Users",
        value=f"{total_casual:,}"
    )

with col3:
    total_registered = main_day_df["registered"].sum()
    st.metric(
        label="Registered Users",
        value=f"{total_registered:,}"
    )

# Menampilkan rata-rata pola penyewaan berdasarkan jam dan jenis hari
st.subheader("Average Bike Rentals by Hour and Day Type")

hourly_rentals = main_hour_df.groupby(
    ["hr", "workingday"]
)["cnt"].mean().unstack()

fig, ax = plt.subplots(figsize=(12, 6))

hourly_rentals.plot(
    kind="line",
    marker="o",
    ax=ax
)

ax.set_title("Average Bike Rentals by Hour and Day Type")
ax.set_xlabel("Hour")
ax.set_ylabel("Average Bike Rentals")
ax.set_xticks(range(24))
ax.legend(
    ["Non-Working Day", "Working Day"],
    title="Day Type"
)
ax.grid(True)

st.pyplot(fig)
plt.close(fig)

# Menampilkan rata-rata penyewaan berdasarkan kondisi cuaca dan musim
st.subheader("Environmental Analysis")

col1, col2 = st.columns(2)

# rata-rata penyewaan berdasarkan cuaca
with col1:
    weather_rentals = main_day_df.groupby(
        "weathersit"
    )["cnt"].mean().reset_index()

    weather_labels = {
        1: "Clear",
        2: "Mist / Cloudy",
        3: "Light Rain / Snow",
        4: "Heavy Rain / Snow"
    }

    weather_rentals["weather_label"] = (
        weather_rentals["weathersit"].map(weather_labels)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=weather_rentals,
        x="weather_label",
        y="cnt",
        ax=ax
    )

    ax.set_title("Average Rentals by Weather")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Average Bike Rentals")
    ax.tick_params(axis="x", rotation=20)

    st.pyplot(fig)
    plt.close(fig)

# rata-rata penyewaan berdasarkan musim
with col2:
    season_rentals = main_day_df.groupby(
        "season"
    )["cnt"].mean().reset_index()

    season_labels = {
        1: "Spring",
        2: "Summer",
        3: "Fall",
        4: "Winter"
    }

    season_rentals["season_label"] = (
        season_rentals["season"].map(season_labels)
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        data=season_rentals,
        x="season_label",
        y="cnt",
        ax=ax
    )

    ax.set_title("Average Rentals by Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Average Bike Rentals")

    st.pyplot(fig)
    plt.close(fig)

# Menampilkan total penyewaan pengguna casual dan registered
st.subheader("User Behavior Analysis")

# Menghitung total penyewaan berdasarkan tipe pengguna
user_rentals = pd.DataFrame({
    "User Type": ["Casual", "Registered"],
    "Total Rentals": [
        main_day_df["casual"].sum(),
        main_day_df["registered"].sum()
    ]
})

# Menghitung persentase pengguna
total_rentals = user_rentals["Total Rentals"].sum()

user_rentals["Percentage"] = (
    user_rentals["Total Rentals"] / total_rentals * 100
)

col1, col2 = st.columns(2)

# Diagram batang
with col1:
    fig, ax = plt.subplots(figsize=(8, 5))

    sns.barplot(
        data=user_rentals,
        x="User Type",
        y="Total Rentals",
        ax=ax
    )

    ax.set_title("Total Rentals by User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Total Bike Rentals")

    st.pyplot(fig)
    plt.close(fig)

# Diagram lingkaran (pie chart)
with col2:
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.pie(
        user_rentals["Total Rentals"],
        labels=user_rentals["User Type"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Rental Contribution by User Type")

    st.pyplot(fig)
    plt.close(fig)

# Analisis lanjutan (Binning)
st.subheader("Advanced Analysis: Bike Rental Demand")

# Membuat kategori permintaan penyewaan
demand_df = main_day_df.copy()

demand_df["demand_category"] = pd.qcut(
    demand_df["cnt"],
    q=3,
    labels=["Low Demand", "Medium Demand", "High Demand"]
)

# Menghitung rata-rata penyewaan berdasarkan kategori
demand_analysis = demand_df.groupby(
    "demand_category",
    observed=True
)[["cnt", "casual", "registered"]].mean().reset_index()

# Menampilkan rata-rata jumlah penyewaan sepeda berdasarkan kategori permintaan
fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=demand_analysis,
    x="demand_category",
    y="cnt",
    ax=ax
)

ax.set_title("Average Bike Rentals by Demand Category")
ax.set_xlabel("Demand Category")
ax.set_ylabel("Average Bike Rentals")

st.pyplot(fig)
plt.close(fig)

# Menampilkan tabel analisis
st.subheader("Demand Category Details")

demand_analysis = demand_analysis.round(2)

st.dataframe(
    demand_analysis.rename(columns={
        "demand_category": "Demand Category",
        "cnt": "Average Rentals",
        "casual": "Average Casual Users",
        "registered": "Average Registered Users"
    }),
    use_container_width=True
)

st.info("""
**Key Insight**

Rata-rata penyewaan sepeda meningkat dari sekitar
2.312 pada kategori Low Demand menjadi 6.688
pada kategori High Demand.

Pengguna Registered mendominasi jumlah penyewaan
pada seluruh kategori permintaan.
""")

