import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px

# set streamlit page config and style seaborn
st.set_page_config(page_title="Bike Sharing Dashboard", layout='wide')
sns.set(style='dark')

# load data
df = pd.read_csv("data.csv")
df['dateday'] = pd.to_datetime(df['dateday'])

## SIDEBAR ------------------------------------------------
min_date = df['dateday'].min()
max_date = df['dateday'].max()

with st.sidebar:
    # Menambahkan logo
    st.image("delivery-bike.png")

    # Mengambil start_date dan end_date dari date_input
    start_date, end_date = st.date_input(
        label="Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dateday'] >= str(start_date)) &
             (df['dateday'] <= str(end_date))]

# MAIN PAGE -------------------------------------------------
st.title("Bike Sharing Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    total_user = main_df['count'].sum()
    st.metric("Total User", value=total_user)

with col2:
    casual_user = main_df['casual'].sum()
    st.metric("Casual User", value=casual_user)

with col3:
    reg_user = main_df['registered'].sum()
    st.metric("Registered User", value=reg_user)

# chart 1
workingday = main_df.iloc[:,[7,15]]
workingday_result = workingday.groupby(by='workingday').sum().reset_index().sort_values('count', ascending=False)

chart_1 = px.pie(workingday_result,
              names='workingday',
              values='count',
              color_discrete_sequence=['yellow', 'green'],
              title="Bike Users by Workday/Offday").update_layout(
                  xaxis_title='Workday/Offday',
                  yaxis_title='Total Users')

st.plotly_chart(chart_1, use_container_width=True)

# chart 2
fig6, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='workingday', y='count', data=main_df, hue='season', ax=ax)
ax.set_title("Klaster pengguna sepeda berdasarkan hari kerja/tidak dan kategori musim")
ax.set_xlabel("Hari kerja/tidak")
ax.set_ylabel("Jumlah pengguna")
ax.grid(True)

st.pyplot(fig6)

# chart 3
season_analysis = main_df.iloc[:,[1,15]]
season_result = season_analysis.groupby(by='season').sum().reset_index().sort_values('count', ascending=False)

chart_2 = px.bar(season_result,
                  x='season',
                  y='count',
                  color_discrete_sequence=['skyblue', 'green', 'red'],
                  title="Bike Sharing Users by Season").update_layout(
                      xaxis_title='Season',
                      yaxis_title='Total Users'
                  )

# chart 4
monthly_registered = main_df.resample(rule='M', on='dateday').agg({
    "registered": "sum"
})
monthly_casual = main_df.resample(rule='M', on='dateday').agg({
    "casual": "sum"
})

# Gabungkan kedua hasil agar mudah dipakai dalam satu lineplot
monthly_data = monthly_registered.join(monthly_casual)
monthly_data.reset_index(inplace=True)  # agar 'dateday' jadi kolom biasa

# Plot
fig4, ax = plt.subplots(figsize=(15, 5))
sns.lineplot(data=monthly_data, x="dateday", y="registered", marker="o", label="Registered", ax=ax)
sns.lineplot(data=monthly_data, x="dateday", y="casual", marker="d", label="Casual", ax=ax)
ax.set_title("Jumlah pengguna sepeda bulanan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah pengguna")
ax.grid(True)

st.pyplot(fig4)
