import streamlit as st
import folium
from streamlit_folium import st_folium

# Título da Aplicação e configuração da página
st.set_page_config(page_title="Análise Geoespacial de João Pessoa", layout="wide")
st.title("Análise de Cobertura e Uso da Terra em João Pessoa")
st.write("Mapa base de satélite (ESRI World Imagery) com camadas do IBGE e IBAMA.")


st.image("mapbiomasevolution.gif", caption="Minha animação local")
# Dicionário com as camadas WMS que você precisa
CAMADAS_WMS = {
    "Áreas Embargadas (IBAMA)": {
        "url": "http://siscom.ibama.gov.br/geoserver/publica/wms",
        "layer_name": "publica:vw_brasil_adm_embargo_a"
    },
    "Cobertura e Uso da Terra 2014 (IBGE)": {
        "url": "https://geoservicos.ibge.gov.br/geoserver/wms",
        "layer_name": "CREN:Uso_Brasil_2014"
    },
    "Cobertura e Uso da Terra 2000 (IBGE)": {
        "url": "https://geoservicos.ibge.gov.br/geoserver/wms",
        "layer_name": "CREN:Uso_Brasil_2000"
    }
}

# Coordenadas do centro de João Pessoa
LAT_JP, LON_JP = -7.1195, -34.8451

# NOVO: Coordenadas da "cerca" geográfica (bounding box) para a Grande João Pessoa
# Formato: [[sul, oeste], [norte, leste]]
GRANDE_JP_BOUNDS = [
    [-7.30, -35.00],  # Canto Sudoeste (aprox. Conde/Santa Rita)
    [-6.95, -34.78]   # Canto Nordeste (aprox. Cabedelo)
]

try:
    # --- Criação do Mapa Base ---
    # ALTERADO: Adicionados parâmetros para limitar zoom e área de navegação
    m = folium.Map(
        location=[LAT_JP, LON_JP],
        zoom_start=12,
        tiles='Esri.WorldImagery',
        attr='Tiles &copy; Esri &mdash; Source: Esri',
        min_zoom=11.8, # Impede de dar zoom out para além deste nível
        max_zoom=18, # Impede de dar zoom in excessivo
        max_bounds=True, # Ativa a restrição de área
        max_lat=GRANDE_JP_BOUNDS[1][0], # Limite Norte
        min_lat=GRANDE_JP_BOUNDS[0][0], # Limite Sul
        max_lon=GRANDE_JP_BOUNDS[1][0], # Limite Leste
        min_lon=GRANDE_JP_BOUNDS[0][1]  # Limite Oeste
    )


    # --- Seletor de Múltiplas Camadas ---
    titulos_camadas = list(CAMADAS_WMS.keys())
    camadas_selecionadas = st.multiselect(
        "Selecione as camadas de dados para sobrepor:",
        titulos_camadas,
        default=[]
    )

    # Adiciona as camadas WMS que foram selecionadas
    for titulo in camadas_selecionadas:
        info_camada = CAMADAS_WMS[titulo]
        folium.WmsTileLayer(
            url=info_camada["url"],
            layers=info_camada["layer_name"],
            transparent=True,
            control=True,
            fmt='image/png',
            name=titulo
        ).add_to(m)

    # --- Adicionar seus Dados de Análise/Previsão ---
    st.sidebar.header("Área de Simulação")
    show_prediction = st.sidebar.checkbox("Mostrar área de análise/previsão no mapa")

    if show_prediction:
        coordenadas_previsao = [
            [-7.172, -34.835], [-7.185, -34.845],
            [-7.195, -34.830], [-7.180, -34.820],
        ]

        folium.Polygon(
            locations=coordenadas_previsao,
            popup='<b>Área de Análise 1</b>',
            color='#E32227', fill=True, fill_color='#E32227', fill_opacity=0.3,
            tooltip="Clique para ver detalhes", name="Previsão de Crescimento"
        ).add_to(m)

    # Adiciona controle de camadas ao mapa
    if camadas_selecionadas or show_prediction:
        folium.LayerControl().add_to(m)

    # Exibe o mapa no Streamlit
    st_folium(m, width=1200, height=700)

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o mapa: {e}")