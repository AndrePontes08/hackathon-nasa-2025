import streamlit as st
import folium
from streamlit_folium import st_folium
from owslib.wms import WebMapService

# Título da Aplicação
st.set_page_config(page_title="Mapa Interativo da INDE", layout="wide")
st.title("Visualizador de Mapas da Infraestrutura Nacional de Dados Espaciais (INDE)")

# URL do serviço WMS da INDE
wms_url = "http://www.geoservicos.inde.gov.br/geoserver/ows"

# Conecta ao serviço WMS para obter a lista de camadas
@st.cache_resource
def get_wms_layers(url):
    wms = WebMapService(url, version='1.3.0')
    return [(wms[layer].title, layer) for layer in list(wms.contents)]

try:
    # Obtém e exibe a lista de camadas em um selectbox
    available_layers = get_wms_layers(wms_url)
    layer_titles, layer_names = zip(*available_layers)
    selected_layer_title = st.selectbox("Selecione uma camada para visualizar:", layer_titles)
    selected_layer_name = layer_names[layer_titles.index(selected_layer_title)]

    # Cria o mapa base com Folium
    m = folium.Map(location=[-15.788, -47.882], zoom_start=4)

    # Adiciona a camada WMS selecionada ao mapa
    folium.WmsTileLayer(
        url=wms_url,
        layers=selected_layer_name,
        transparent=True,
        control=True,
        fmt='image/png',
        name=selected_layer_title
    ).add_to(m)

    # Adiciona controle de camadas ao mapa
    folium.LayerControl().add_to(m)

    # Exibe o mapa no Streamlit
    st_data = st_folium(m, width=1200, height=600)

except Exception as e:
    st.error(f"Ocorreu um erro ao tentar se conectar ao serviço WMS da INDE: {e}")