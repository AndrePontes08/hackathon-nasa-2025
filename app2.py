import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.linear_model import LinearRegression
import math
import os
import time
import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES ---
IMAGE_FOLDER = 'dataset2'
N_CLUSTERS = 4
URBAN_REFERENCE_COLOR = np.array([120, 110, 100])
YEAR_TO_PREDICT = 2030
RESIZE_PERCENT_FOR_ANALYSIS = 30
ANIMATION_IMAGE_WIDTH = 600
FINAL_IMAGE_DISPLAY_WIDTH = 500
CSV_PATH = "populacao_municipios.csv"

# --- FUNÇÕES DE ANÁLISE ---

def find_urban_cluster_index(kmeans_model, reference_color):
    cluster_centers = kmeans_model.cluster_centers_
    distances = np.linalg.norm(cluster_centers - reference_color, axis=1)
    return np.argmin(distances)

def calculate_metrics(mask):
    area = np.sum(mask) / 255
    moments = cv2.moments(mask)
    centroid = None
    if moments["m00"] != 0:
        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])
        centroid = (cx, cy)
    return area, centroid

# --- FUNÇÃO PRINCIPAL DE ANÁLISE URBANA ---

def run_analysis_and_prediction(image_placeholder, status_placeholder):
    try:
        image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith('.png')])
        if not image_files:
            st.error(f"A pasta '{IMAGE_FOLDER}' não foi encontrada ou não contém arquivos .png.")
            return None, None
    except FileNotFoundError:
        st.error(f"A pasta '{IMAGE_FOLDER}' não foi encontrada.")
        return None, None

    historical_data = []
    resized_w, resized_h = 0, 0
    original_w, original_h = 0, 0

    for image_file in image_files:
        year_str = "".join(filter(str.isdigit, os.path.splitext(image_file)[0]))
        if not year_str:
            continue
        year = int(year_str)

        image_path = os.path.join(IMAGE_FOLDER, image_file)
        status_placeholder.info(f"Processando imagem do ano {year}...")
        image_placeholder.image(image_path, caption=f"Analisando: {year}", width=ANIMATION_IMAGE_WIDTH)
        time.sleep(0.6)

        image = cv2.imread(image_path)
        if image is None:
            continue

        if original_w == 0:
            original_h, original_w, _ = image.shape
            resized_w = int(original_w * RESIZE_PERCENT_FOR_ANALYSIS / 100)
            resized_h = int(original_h * RESIZE_PERCENT_FOR_ANALYSIS / 100)
        
        resized_image = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), (resized_w, resized_h))
        pixel_data = resized_image.reshape((-1, 3))
        
        kmeans = MiniBatchKMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10).fit(pixel_data)
        urban_cluster_label = find_urban_cluster_index(kmeans, URBAN_REFERENCE_COLOR)
        urban_mask = (kmeans.labels_ == urban_cluster_label).reshape(resized_image.shape[:2]).astype(np.uint8) * 255
        area, centroid = calculate_metrics(urban_mask)

        if centroid and area > 0:
            historical_data.append({
                'year': year,
                'area': area,
                'cx': centroid[0],
                'cy': centroid[1],
                'filename': image_file
            })

    if len(historical_data) < 2:
        st.error("Dados insuficientes para o modelo. São necessárias pelo menos 2 imagens.")
        return None, None

    status_placeholder.info("Treinando modelo de previsão...")
    time.sleep(1)
    
    historical_data.sort(key=lambda x: x['year'])
    X = np.array([d['year'] for d in historical_data]).reshape(-1, 1)
    model_area = LinearRegression().fit(X, np.array([d['area'] for d in historical_data]))
    model_cx = LinearRegression().fit(X, np.array([d['cx'] for d in historical_data]))
    model_cy = LinearRegression().fit(X, np.array([d['cy'] for d in historical_data]))

    status_placeholder.info(f"Calculando previsão para {YEAR_TO_PREDICT}...")
    time.sleep(1)

    year_future = np.array([[YEAR_TO_PREDICT]])
    predicted_area = model_area.predict(year_future)[0]
    predicted_cx_resized = model_cx.predict(year_future)[0]
    predicted_cy_resized = model_cy.predict(year_future)[0]

    last_data = historical_data[-1]
    area_increase_resized = predicted_area - last_data['area']
    last_image_path = os.path.join(IMAGE_FOLDER, last_data['filename'])
    final_image_hr = cv2.imread(last_image_path)

    scale_factor = original_w / resized_w
    final_cx = int(predicted_cx_resized * scale_factor)
    final_cy = int(predicted_cy_resized * scale_factor)
    last_cx_hr = int(last_data['cx'] * scale_factor)
    last_cy_hr = int(last_data['cy'] * scale_factor)
    area_increase_hr = area_increase_resized * (scale_factor ** 2)
    radius_of_growth_hr = int(math.sqrt(max(0, area_increase_hr) / math.pi))

    overlay = final_image_hr.copy()
    cv2.circle(overlay, (final_cx, final_cy), radius_of_growth_hr, (0, 255, 255), -1)
    final_image_hr = cv2.addWeighted(overlay, 0.5, final_image_hr, 0.5, 0)
    cv2.arrowedLine(final_image_hr, (last_cx_hr, last_cy_hr), (final_cx, final_cy), (0, 0, 255), 6, tipLength=0.03)
    cv2.circle(final_image_hr, (last_cx_hr, last_cy_hr), 12, (255, 0, 0), -1)
    cv2.circle(final_image_hr, (final_cx, final_cy), 12, (0, 0, 255), -1)

    final_h, final_w, _ = final_image_hr.shape
    display_h = int(final_h * (FINAL_IMAGE_DISPLAY_WIDTH / final_w))
    display_image = cv2.resize(final_image_hr, (FINAL_IMAGE_DISPLAY_WIDTH, display_h))
    final_image_rgb = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
    
    results = {
        "last_year": last_data['year'],
        "predicted_year": YEAR_TO_PREDICT,
        "area_increase_percent": (predicted_area / last_data['area'] - 1) * 100
    }
    
    return final_image_rgb, results

# --- INTERFACE STREAMLIT ---

st.set_page_config(layout="wide", page_title="Previsão de Expansão Urbana")
st.title("📈 Previsão de Expansão Urbana - João Pessoa")

st.markdown("""
Este aplicativo analisa imagens históricas de satélite e estima a expansão urbana até o ano de 2030.
""")

if st.button('Iniciar Análise e Previsão'):
    st.info("Processando... Aguarde alguns instantes.")
    
    image_placeholder = st.empty()
    status_placeholder = st.empty()

    with st.spinner('Executando análise...'):
        final_prediction_image, results = run_analysis_and_prediction(image_placeholder, status_placeholder)
    
    if final_prediction_image is not None and results is not None:
        status_placeholder.empty()
        image_placeholder.empty()
        st.success("✅ Análise concluída com sucesso!")
        st.image(final_prediction_image, caption=f"Previsão para {results['predicted_year']}", use_container_width=True)
        
        st.subheader("📊 Resultados da Previsão")
        col1, col2 = st.columns(2)
        col1.metric(label="Ano Base", value=results['last_year'])
        col2.metric(label="Aumento Estimado de Área", value=f"{results['area_increase_percent']:.2f} %")

        # --- EXIBE O GRÁFICO DO CSV ---
        if os.path.exists(CSV_PATH):
            st.divider()
            st.header("📈 Variação Populacional das Capitais (2010–2022)")

            df = pd.read_csv(CSV_PATH)
            df_sorted = df.sort_values(by="Variacao", ascending=False)

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(df_sorted["Municipio"], df_sorted["Variacao"], color='skyblue')
            ax.set_xlabel("Variação Populacional (%)")
            ax.set_ylabel("Município")
            ax.set_title("Variação Populacional entre 2010 e 2022")
            ax.grid(axis='x', linestyle='--', alpha=0.6)
            ax.invert_yaxis()

            st.pyplot(fig)
        else:
            st.warning("Arquivo CSV 'populacao_municipios.csv' não encontrado no diretório.")
else:
    st.warning("Clique no botão acima para iniciar.")
