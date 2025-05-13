import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import joblib
import os

# --- Імпорти для завантаження даних з Інтернету ---
import requests
import zipfile

# --- Налаштування Сторінки ---
st.set_page_config(
    page_title="Кластеризація Країн Світу",
    page_icon="🌍",
    layout="wide", # Використовувати всю ширину
    initial_sidebar_state="expanded"
)

# --- Функції для Завантаження Даних ---
@st.cache_data # Використовуємо кешування Streamlit для пришвидшення завантаження
def load_csv_data(data_path, index_col=None):
    if os.path.exists(data_path):
        try:
            return pd.read_csv(data_path, index_col=index_col)
        except Exception as e:
            st.error(f"Помилка завантаження CSV файлу '{data_path}': {e}")
            return None
    else:
        st.error(f"Файл даних не знайдено за шляхом: {data_path}")
        return None

@st.cache_data
def load_joblib_data(data_path):
    if os.path.exists(data_path):
        try:
            return joblib.load(data_path)
        except Exception as e:
            st.error(f"Помилка завантаження joblib файлу '{data_path}': {e}")
            return None
    else:
        st.error(f"Файл joblib не знайдено за шляхом: {data_path}")
        return None

@st.cache_data # Кешуємо завантажені геодані
def load_geodata_manual(data_dir_streamlit="natural_earth_data_streamlit"):
    """Завантажує геодані країн світу з Natural Earth, розпаковує та повертає GeoDataFrame."""
    ZIP_URL_ST = "https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip"
    zip_filename_st = os.path.basename(ZIP_URL_ST)
    zip_filepath_st = os.path.join(data_dir_streamlit, zip_filename_st)
    shapefile_name_relative_st = "ne_110m_admin_0_countries.shp"
    shapefile_path_st = os.path.join(data_dir_streamlit, shapefile_name_relative_st)

    if not os.path.exists(shapefile_path_st):
        st.info(f"Shapefile для карти ({shapefile_name_relative_st}) не знайдено. Спроба завантаження...")
        os.makedirs(data_dir_streamlit, exist_ok=True)

        if not os.path.exists(zip_filepath_st):
            progress_bar = st.progress(0, text="Завантаження геоданих...")
            try:
                response = requests.get(ZIP_URL_ST, stream=True)
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                bytes_downloaded = 0
                with open(zip_filepath_st, 'wb') as f:
                    for i, chunk in enumerate(response.iter_content(chunk_size=8192)):
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        if total_size > 0:
                            progress_bar.progress(min(100, int(100 * bytes_downloaded / total_size)), text=f"Завантаження геоданих... ({bytes_downloaded // 1024}KB / {total_size // 1024}KB)")
                        else:
                            progress_bar.progress(min(100, i // 10), text=f"Завантаження геоданих... (блок {i})") # Fallback if no content-length
                progress_bar.progress(100, text="Завантаження геоданих завершено.")
                st.success("ZIP-архів геоданих завантажено.")
            except requests.exceptions.RequestException as e:
                st.error(f"Помилка завантаження геоданих: {e}")
                progress_bar.empty()
                return None
            progress_bar.empty()

        st.info(f"Розпакування {zip_filename_st}...")
        try:
            with zipfile.ZipFile(zip_filepath_st, 'r') as zip_ref:
                zip_ref.extractall(data_dir_streamlit)
            st.success("Геодані розпаковано.")
        except zipfile.BadZipFile:
            st.error(f"Помилка: Файл {zip_filename_st} пошкоджений. Видаліть його та спробуйте знову.")
            if os.path.exists(zip_filepath_st): os.remove(zip_filepath_st)
            return None
        except Exception as e:
            st.error(f"Помилка розпакування геоданих: {e}")
            return None
        
        if not os.path.exists(shapefile_path_st):
            st.error(f"Shapefile '{shapefile_name_relative_st}' не знайдено після розпакування.")
            return None
            
    try:
        world_gdf = gpd.read_file(shapefile_path_st)
        st.success("Геодані країн світу успішно завантажено.")
        return world_gdf
    except Exception as e:
        st.error(f"Помилка читання shapefile '{shapefile_path_st}': {e}")
        return None

# --- Шляхи до Збережених Артефактів ---
ARTIFACTS_DIR = 'output_artifacts'
DATA_FILE = os.path.join(ARTIFACTS_DIR, 'country_clusters_data.csv')
PROFILES_FILE = os.path.join(ARTIFACTS_DIR, 'cluster_profiles.csv')
CLUSTER_NAMES_FILE = os.path.join(ARTIFACTS_DIR, 'cluster_names.joblib')
PCA_DATA_FILE = os.path.join(ARTIFACTS_DIR, 'pca_data_2c.csv')
MAP_DATA_FILE = os.path.join(ARTIFACTS_DIR, 'world_merged_clusters.csv') # CSV з даними для карти

# --- Завантаження Даних ---
df_processed_st = load_csv_data(DATA_FILE) # Може мати 'Country Code' або 'Country Name'
cluster_profiles_st = load_csv_data(PROFILES_FILE, index_col=0)
cluster_names_st = load_joblib_data(CLUSTER_NAMES_FILE)
df_pca_st = load_csv_data(PCA_DATA_FILE) # Має містити 'Country Name'/'Code', 'PCA1', 'PCA2'
df_map_info_from_csv = load_csv_data(MAP_DATA_FILE) # Дані для карти з CSV, містить ISO код та кластери
world_geodata_st = load_geodata_manual() # Геометрії країн

# --- Перевірка Завантаження ---
data_load_success = True
if df_processed_st is None: st.error("Помилка завантаження df_processed_st"); data_load_success = False
if cluster_profiles_st is None: st.error("Помилка завантаження cluster_profiles_st"); data_load_success = False
if cluster_names_st is None: st.error("Помилка завантаження cluster_names_st"); data_load_success = False
if df_pca_st is None: st.error("Помилка завантаження df_pca_st"); data_load_success = False
if df_map_info_from_csv is None: st.error("Помилка завантаження df_map_info_from_csv"); data_load_success = False
if world_geodata_st is None: st.error("Помилка завантаження world_geodata_st"); data_load_success = False

if not data_load_success:
    st.warning("Не вдалося завантажити всі необхідні дані. Робота застосунку може бути некоректною.")
    st.stop()

# --- Об'єднання Даних для Карти ---
world_merged_st = None
if world_geodata_st is not None and df_map_info_from_csv is not None:
    # Визначаємо ISO колонку в завантажених геоданих (world_geodata_st)
    iso_col_in_geodata = None
    possible_iso_cols_geo = ['ADM0_A3', 'ISO_A3_EH', 'ISO_A3', 'GU_A3']
    for col in possible_iso_cols_geo:
        if col in world_geodata_st.columns:
            iso_col_in_geodata = col
            break
    
    # Визначаємо ISO колонку в df_map_info_from_csv (завантажено з CSV)
    # Цей CSV був створений з world_merged в ноутбуці, який використовував певну ISO колонку.
    iso_col_in_csv_data = None
    if iso_col_in_geodata and iso_col_in_geodata in df_map_info_from_csv.columns: # Якщо назви співпадають
        iso_col_in_csv_data = iso_col_in_geodata
    else: # Інакше, шукаємо серед можливих
        possible_iso_cols_csv = ['iso_a3', 'ADM0_A3', 'ISO_A3_EH', 'ISO_A3'] # 'iso_a3' з оригінального коду
        for col_csv in possible_iso_cols_csv:
            if col_csv in df_map_info_from_csv.columns:
                iso_col_in_csv_data = col_csv
                break
                
    if iso_col_in_geodata and iso_col_in_csv_data:
        st.info(f"Об'єднання геоданих (ключ: '{iso_col_in_geodata}') з даними з CSV (ключ: '{iso_col_in_csv_data}').")
        world_merged_st = world_geodata_st.merge(
            df_map_info_from_csv,
            left_on=iso_col_in_geodata,
            right_on=iso_col_in_csv_data,
            how='left',
            suffixes=('_geo', '_csv') # Додаємо суфікси, щоб уникнути конфліктів імен колонок
        )
        
        # Обробка колонок після мержу (пріоритет даним з CSV, якщо є суфікси)
        cols_to_map = {
            'Cluster_Name': 'Cluster_Name_csv', 'KMeans_Cluster': 'KMeans_Cluster_csv',
            'ВВП на душу населення': 'ВВП на душу населення_csv',
            'Тривалість життя': 'Тривалість життя_csv', 'Населення': 'Населення_csv'
        }
        for target_col, source_col_suffixed in cols_to_map.items():
            if source_col_suffixed in world_merged_st.columns:
                world_merged_st[target_col] = world_merged_st[source_col_suffixed]
            elif target_col not in world_merged_st.columns: # Якщо немає ні з _csv, ні оригінальної
                 world_merged_st[target_col] = pd.NA


        # Забезпечимо, що колонки для кольору та підказок існують
        world_merged_st['Cluster_Name'] = world_merged_st['Cluster_Name'].fillna('Немає даних')
        world_merged_st['KMeans_Cluster'] = pd.to_numeric(world_merged_st['KMeans_Cluster'], errors='coerce').fillna(-1).astype(int)
        
        # Колонка для локацій на карті - це ISO код з геоданих
        st.session_state.locations_col_map = iso_col_in_geodata
        # Колонка для назв країн
        hover_name_col_map = 'NAME_geo' # За замовчуванням з геоданих
        name_candidates_map = ['NAME_geo', 'ADMIN_geo', 'SOVEREIGNT_geo', 'NAME_csv', 'name_csv'] # Пріоритет з _geo
        for nc_map in name_candidates_map:
            if nc_map in world_merged_st.columns:
                hover_name_col_map = nc_map
                break
        st.session_state.hover_name_col_map = hover_name_col_map

    else:
        st.error("Не вдалося визначити ключові колонки ISO для об'єднання даних для карти.")
else:
    if world_geodata_st is None: st.warning("Геодані не завантажено.")
    if df_map_info_from_csv is None: st.warning("Дані для карти з CSV не завантажено.")


# --- Заголовок Застосунку ---
st.title("🌍 Інтерактивний Аналіз Кластерів Країн Світу")
# SELECTED_YEAR потрібно визначити або передати
SELECTED_YEAR_ST = 2019 # Визначимо тут, якщо не передаємо ззовні
st.markdown(f"Кластеризація на основі соціально-економічних індикаторів за **{SELECTED_YEAR_ST}** рік.")

# --- Інтерпретація Кластерів (Опис) ---
cluster_descriptions = {
    0: "**Високорозвинені країни:** Найвищий ВВП, тривалість життя, доступ до технологій та інфраструктури. Високі викиди CO2, низька частка с/г.",
    1: "**Країни із середнім рівнем розвитку:** Помірні показники розвитку за більшістю індикаторів. Найбільша група країн.",
    2: "**Демографічні гіганти, що розвиваються:** Дуже велике населення (Індія, Китай). Показники розвитку нижчі за середні, але вищі за найменш розвинені країни.",
    3: "**Найменш розвинені країни:** Найнижчі показники ВВП, тривалості життя, освіти, доступу до технологій та інфраструктури. Переважно в Африці."
}

# --- Візуалізації ---
st.header("🗺️ Розподіл Країн за Кластерами")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Карта Світу")
    if world_merged_st is not None and 'locations_col_map' in st.session_state:
        try:
            fig_map_st = px.choropleth(world_merged_st,
                                    locations=st.session_state.locations_col_map, # Колонка ISO кодів
                                    geojson=world_merged_st.geometry, # Передаємо геометрії
                                    color="Cluster_Name", # Колонка з назвами кластерів
                                    hover_name=st.session_state.hover_name_col_map, # Колонка з назвами країн
                                    hover_data={ 
                                        st.session_state.locations_col_map: False, # Не показувати код ISO двічі
                                        "Cluster_Name": True,
                                        "ВВП на душу населення": ":,.0f",
                                        "Тривалість життя": ":.1f",
                                        "Населення": ":,.0f"
                                     },
                                    title=f"Кластери Розвитку Країн ({SELECTED_YEAR_ST})",
                                    color_discrete_map={
                                         "Високорозвинені країни": "blue",
                                         "Країни із середнім рівнем розвитку": "green",
                                         "Демографічні гіганти, що розвиваються": "orange",
                                         "Найменш розвинені країни": "red",
                                         "Немає даних": "lightgrey"
                                     },
                                    category_orders={"Cluster_Name": list(cluster_names_st.values()) + ['Немає даних']}
                                    )
            fig_map_st.update_geos(fitbounds="locations", visible=False)
            fig_map_st.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, height=450, legend_title_text='Кластер')
            st.plotly_chart(fig_map_st, use_container_width=True)
        except Exception as e:
            st.error(f"Помилка створення карти: {e}")
            st.dataframe(world_merged_st.drop(columns=['geometry'], errors='ignore').head())
    else:
        st.warning("Не вдалося створити карту через проблеми з даними або відсутність ключових колонок.")

with col2:
    st.subheader("PCA Візуалізація")
    # Об'єднання df_pca_st з df_processed_st для отримання 'Country Name', 'KMeans_Cluster', 'Cluster_Name'
    df_pca_final = None
    if df_pca_st is not None and df_processed_st is not None:
        # df_processed_st може мати індекс 'Country Code' або 'Country Name'
        # df_pca_st має містити відповідний ідентифікатор
        df_processed_for_pca = df_processed_st.reset_index()
        
        merge_key_pca = None
        if 'Country Code' in df_pca_st.columns and 'Country Code' in df_processed_for_pca.columns:
            merge_key_pca = 'Country Code'
        elif 'Country Name' in df_pca_st.columns and 'Country Name' in df_processed_for_pca.columns:
             merge_key_pca = 'Country Name'
        # Якщо pca_data_2c.csv зберіг індекс як першу колонку без назви:
        elif df_pca_st.columns[0].startswith('Unnamed: 0') and 'Country Name' in df_processed_for_pca.columns:
             df_pca_st = df_pca_st.rename(columns={df_pca_st.columns[0]: 'Country Name'})
             merge_key_pca = 'Country Name'


        if merge_key_pca:
            cols_to_get = [merge_key_pca, 'KMeans_Cluster', 'Cluster_Name']
            # Додамо 'Country Name', якщо ключ 'Country Code', для hover_name
            if merge_key_pca == 'Country Code' and 'Country Name' in df_processed_for_pca.columns:
                cols_to_get.append('Country Name')
            
            # Перевірка наявності всіх колонок в df_processed_for_pca
            missing_cols = [c for c in cols_to_get if c not in df_processed_for_pca.columns]
            if not missing_cols:
                df_pca_final = pd.merge(df_pca_st, df_processed_for_pca[cols_to_get], on=merge_key_pca, how='left')
            else:
                st.warning(f"Відсутні колонки в df_processed для об'єднання з PCA: {missing_cols}")

        else: # Спроба прямого присвоєння, якщо довжини збігаються (менш надійно)
            st.warning("Не вдалося знайти спільний ключ для об'єднання PCA даних з інформацією про кластери. Спроба прямого присвоєння.")
            if len(df_pca_st) == len(df_processed_for_pca):
                df_pca_st['KMeans_Cluster'] = df_processed_for_pca['KMeans_Cluster'].values
                df_pca_st['Cluster_Name'] = df_processed_for_pca['Cluster_Name'].values
                if 'Country Name' not in df_pca_st.columns and 'Country Name' in df_processed_for_pca.columns:
                     df_pca_st['Country Name'] = df_processed_for_pca['Country Name'].values
                df_pca_final = df_pca_st
            else:
                 st.warning("Розміри PCA даних та оброблених даних не збігаються для прямого присвоєння.")
    
    if df_pca_final is not None and 'PCA1' in df_pca_final.columns and 'PCA2' in df_pca_final.columns and 'KMeans_Cluster' in df_pca_final.columns:
        hover_name_pca = 'Country Name' if 'Country Name' in df_pca_final.columns else (merge_key_pca if merge_key_pca else 'index')

        fig_pca_st = px.scatter(df_pca_final, x='PCA1', y='PCA2',
                             color='KMeans_Cluster', # Використовуємо числову колонку для кольору
                             hover_name=hover_name_pca,
                             hover_data={'KMeans_Cluster': False, 'Cluster_Name': True},
                             title='Кластери у Просторі PCA',
                             labels={'KMeans_Cluster': 'Кластер K-Means'},
                             category_orders={"KMeans_Cluster": sorted(df_pca_final['KMeans_Cluster'].dropna().unique())})
        fig_pca_st.update_layout(xaxis_title='PCA1', yaxis_title='PCA2', height=450, legend_title_text='Кластер')
        fig_pca_st.update_traces(marker=dict(size=8, opacity=0.8))
        st.plotly_chart(fig_pca_st, use_container_width=True)
    else:
        st.warning("Необхідні колонки ('PCA1', 'PCA2', 'KMeans_Cluster', 'Country Name'/'Code') відсутні для PCA графіка.")
        if df_pca_final is not None: st.dataframe(df_pca_final.head())
        elif df_pca_st is not None: st.dataframe(df_pca_st.head())


st.divider()

# --- Детальний Аналіз Кластерів ---
st.header("📊 Детальний Профіль Кластерів")

if cluster_names_st and cluster_profiles_st is not None:
    cluster_options = {i: f"Кластер {i}: {name}" for i, name in cluster_names_st.items() if i in cluster_profiles_st.index}
    if not cluster_options:
        st.warning("Немає доступних кластерів для вибору.")
    else:
        selected_cluster_label = st.selectbox(
            "Оберіть кластер для перегляду:",
            options=list(cluster_options.keys()),
            format_func=lambda x: cluster_options[x]
        )

        selected_cluster_name = cluster_names_st[selected_cluster_label]
        selected_cluster_desc = cluster_descriptions.get(selected_cluster_label, "Опис для цього кластера відсутній.")

        st.subheader(f"Профіль: {selected_cluster_name} (Кластер {selected_cluster_label})")
        st.markdown(selected_cluster_desc)

        profile_data = cluster_profiles_st.loc[selected_cluster_label]
        
        col_prof1, col_prof2 = st.columns([0.6, 0.4])

        with col_prof1:
            st.markdown("**Радарна діаграма профілю (нормалізовані значення):**")
            from sklearn.preprocessing import MinMaxScaler # Локальний імпорт
            scaler_profiles = MinMaxScaler()
            # Нормалізуємо тільки числові колонки, якщо є нечислові
            numeric_profile_cols = cluster_profiles_st.select_dtypes(include=np.number).columns
            if not numeric_profile_cols.empty:
                profiles_scaled_np = scaler_profiles.fit_transform(cluster_profiles_st[numeric_profile_cols])
                df_profiles_scaled = pd.DataFrame(profiles_scaled_np, index=cluster_profiles_st.index, columns=numeric_profile_cols)

                fig_radar_single = go.Figure()
                categories = df_profiles_scaled.columns
                fig_radar_single.add_trace(go.Scatterpolar(
                    r=df_profiles_scaled.loc[selected_cluster_label].values,
                    theta=categories,
                    fill='toself',
                    name=selected_cluster_name
                ))
                fig_radar_single.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    showlegend=False,
                    title=f"Нормалізований профіль: {selected_cluster_name}",
                    height=400
                )
                st.plotly_chart(fig_radar_single, use_container_width=True)
            else:
                st.warning("Не знайдено числових колонок у профілях кластерів для радарної діаграми.")

            st.markdown("**Точні середні значення:**")
            st.dataframe(profile_data.to_frame(name='Середнє Значення').style.format("{:,.2f}"))

        with col_prof2:
            st.markdown(f"**Країни, що входять до кластера {selected_cluster_label}:**")
            if df_processed_st is not None and 'KMeans_Cluster' in df_processed_st.columns:
                # Визначення колонки з назвою країни (може бути індексом або колонкою)
                country_name_col_for_list = 'Country Name' # За замовчуванням
                if 'Country Name' not in df_processed_st.columns:
                    if df_processed_st.index.name == 'Country Name':
                        countries_in_cluster = df_processed_st[df_processed_st['KMeans_Cluster'] == selected_cluster_label].index.tolist()
                    elif 'Country Code' in df_processed_st.columns: # Якщо є Country Code, а Country Name - ні
                         countries_in_cluster = df_processed_st[df_processed_st['KMeans_Cluster'] == selected_cluster_label]['Country Code'].tolist()
                         country_name_col_for_list = 'Country Code' # Показуємо коди, якщо немає назв
                    else: # Немає ні 'Country Name', ні 'Country Code' як колонки або індексу
                         countries_in_cluster = []
                         st.warning("Не вдалося знайти колонку з назвами/кодами країн у `df_processed_st`.")
                else: # 'Country Name' є колонкою
                    countries_in_cluster = df_processed_st[df_processed_st['KMeans_Cluster'] == selected_cluster_label][country_name_col_for_list].tolist()
                
                if countries_in_cluster:
                    st.dataframe(pd.DataFrame({f"Назви країн (або коди) у кластері {selected_cluster_label}": countries_in_cluster}), height=450, use_container_width=True)
                    st.caption(f"Всього країн у кластері: {len(countries_in_cluster)}")
                else:
                    st.info("Немає країн для відображення у цьому кластері (або не вдалося отримати їх назви).")
            else:
                st.warning("Дані `df_processed_st` або колонка 'KMeans_Cluster' не доступні.")
else:
    st.error("Не вдалося завантажити назви кластерів або їх профілі. Детальний аналіз неможливий.")


# --- Завершення ---
st.sidebar.info(
    f"""
    **Про проєкт:**
    Цей застосунок візуалізує результати кластеризації країн світу
    на основі соціально-економічних індикаторів WDI за {SELECTED_YEAR_ST} рік.
    Використано алгоритм K-Means (k=4).

    **Навігація:**
    - Переглядайте карту та PCA графік.
    - Виберіть кластер у випадаючому списку для детального аналізу профілю та списку країн.
    """
)
# ==============================================================================
# Кінець коду для файлу app.py
# ==============================================================================