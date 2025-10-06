# 📘 Documentação Técnica

## Descrição Geral
Este sistema realiza a **análise e previsão de expansão urbana** com base em imagens históricas de satélite.  
Emprega **clusterização de cores (KMeans)** para identificar áreas urbanizadas e **regressão linear** para projetar o crescimento até o ano de previsão.

## 📑 Módulos Principais

| Módulo | Função |
|--------|---------|
| `cv2` | Processamento e manipulação de imagens |
| `numpy` | Cálculos numéricos e vetoriais |
| `MiniBatchKMeans` | Clusterização eficiente de pixels |
| `LinearRegression` | Modelagem de tendência temporal |
| `streamlit` | Interface interativa e visualização de resultados |

## 🧩 Processo de Execução

1. Carrega imagens PNG de uma pasta (`dataset/`).
2. Redimensiona e analisa cada imagem para identificar a mancha urbana.
3. Calcula área e posição do centróide ao longo do tempo.
4. Treina modelos lineares com os dados históricos.
5. Gera uma previsão visual da expansão urbana futura.

## ⚙️ Parâmetros Configuráveis

| Parâmetro | Descrição |
|------------|------------|
| `IMAGE_FOLDER` | Caminho para o conjunto de imagens |
| `N_CLUSTERS` | Número de clusters para segmentação |
| `YEAR_TO_PREDICT` | Ano alvo da previsão |
| `FINAL_IMAGE_DISPLAY_WIDTH` | Largura da imagem exibida |
| `RESIZE_PERCENT_FOR_ANALYSIS` | Percentual de redução para análise |

## 📈 Saídas do Sistema

- **Imagem final** com sobreposição de áreas projetadas.
- **Métricas de previsão** exibidas na interface Streamlit:
  - Ano base
  - Percentual estimado de aumento da área urbana

## 🧠 Considerações Técnicas

O sistema depende de imagens nomeadas com o ano (ex: `2010.png`, `2020.png`) e localizadas dentro da pasta `dataset/`.  
É recomendado que todas as imagens possuam resolução semelhante e ângulo de captura equivalente para manter a consistência da análise.

## 🧩 Possíveis Extensões Futuras

- Suporte a formatos adicionais (JPG, TIFF).
- Implementação de modelos não lineares para previsão.
- Integração com APIs de satélite (Google Earth Engine, Sentinel).

---

### 📧 Contato
**Autor:** Andre Pontes Vaz de Medeiros Filho  
**E-mail:** [andrepontesvazdemedeiros@gmail.com](mailto:andrepontesvazdemedeiros@gmail.com)
