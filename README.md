# 🏙️ Previsão de Expansão Urbana

Ferramenta interativa para previsão de crescimento urbano com base em imagens históricas de satélite.  
Desenvolvido em Python com **Streamlit**, **OpenCV** e **Scikit-learn**.

## 🚀 Execução

```bash
pip install streamlit opencv-python scikit-learn numpy
streamlit run app.py
```

## 📂 Estrutura do Projeto

```
📁 dataset/        # Imagens de satélite (.png)
📄 app.py          # Código principal
📄 DOCUMENTATION.md
📄 README.md
```

## ⚙️ Configuração

- Adicione imagens nomeadas por ano, como `2000.png`, `2010.png`, `2020.png`.
- O sistema analisará automaticamente as imagens e projetará o crescimento urbano para 2030.

## 📊 Saídas

- Imagem final com marcação da expansão urbana.
- Percentual estimado de aumento da área.
- Centro geométrico da expansão.

---

### 📘 Tecnologias Utilizadas
- Python 3.10+  
- Streamlit  
- OpenCV  
- NumPy  
- Scikit-learn

---

### 🧠 Autor
Desenvolvido por Andre Pontes Vaz de Medeiros Filho  
[andrepontesvazdemedeiros@gmail.com](mailto:andrepontesvazdemedeiros@gmail.com)
