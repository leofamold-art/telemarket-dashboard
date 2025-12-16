import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Настройка заголовка страницы
st.set_page_config(page_title="Telemarket Dashboard", layout="wide")

st.title("📊 Дашборд Telemarket")

# Создание защищенного соединения
conn = st.connection("gsheets", type=GSheetsConnection)

# Ссылка на вашу таблицу (вы её уже давали, я вставил её сюда)
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1VRsEGCe2f1Iz2Q-GO6noqiPKVyyvjDukk1Epr3frLlo/edit?usp=sharing"

try:
    # Чтение данных
    # Мы используем первый лист, данные начинаются с первой строки
    df = conn.read(spreadsheet=SPREADSHEET_URL, ttl="10m")
    
    # Убираем пустые строки, если они есть
    df = df.dropna(how='all')

    # ВЫВОД ДАННЫХ
    st.success("Данные успешно загружены!")
    
    # Боковая панель для простых фильтров
    st.sidebar.header("Фильтры")
    
    # Здесь мы берем названия колонок. Если в таблице колонки называются иначе,
    # мы поправим это на следующем шаге.
    columns = df.columns.tolist()
    filter_col = st.sidebar.selectbox("Фильтровать по колонке:", columns)
    unique_vals = df[filter_col].unique()
    selected_val = st.sidebar.multiselect("Выберите значения:", unique_vals, default=unique_vals)

    # Фильтрация
    df_filtered = df[df[filter_col].isin(selected_val)]

    # Отображение таблицы
    st.subheader("Таблица данных")
    st.dataframe(df_filtered, use_container_width=True)

except Exception as e:
    st.error(f"Произошла ошибка при подключении: {e}")
    st.info("Скорее всего, нам нужно настроить секретные ключи на следующем шаге.")
