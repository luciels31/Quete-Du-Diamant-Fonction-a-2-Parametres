import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, diff, solve, sin, cos, exp, lambdify

# Définition des symboles
x, y = symbols('x y')

# Dictionnaire des fonctions autorisées pour une évaluation sécurisée
allowed_functions = {
    "sin": sin,
    "cos": cos,
    "exp": exp,
    "x": x,
    "y": y
}

# Interface utilisateur
st.title("🔎 Étude et visualisation de fonctions à deux variables")

# Sélection de la fonction
options = {
    "x² + y²": x**2 + y**2,
    "sin(x) * cos(y)": sin(x) * cos(y),
    "exp(-x² - y²)": exp(-x**2 - y**2),
    "Entrer une fonction personnalisée": None
}

fonction_choisie = st.selectbox("📌 Choisissez une fonction prédéfinie ou entrez la vôtre :", list(options.keys()))

# Gestion de la fonction personnalisée
if fonction_choisie == "Entrer une fonction personnalisée":
    fonction_str = st.text_input("✏️ Entrez votre fonction en termes de x et y :", "x**2 + y**2")
    try:
        fonction = eval(fonction_str, {"__builtins__": None}, allowed_functions)
    except Exception as e:
        st.error(f"⚠️ Erreur dans la définition de la fonction : {e}")
        st.stop()
else:
    fonction = options[fonction_choisie]

# Calcul des dérivées partielles
df_dx = diff(fonction, x)
df_dy = diff(fonction, y)

# Affichage de la fonction
st.write("### ✅ Fonction sélectionnée :")
st.latex(f"f(x, y) = {fonction}")

# Affichage des dérivées
st.write("### 🔄 Dérivées partielles :")
st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {df_dx}")
st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {df_dy}")

# Calcul des points critiques
solutions = solve([df_dx, df_dy], (x, y), dict=True)

# Affichage des points critiques
st.write("### 📍 Points critiques :")
if solutions:
    for i, point in enumerate(solutions):
        x_val = point[x].evalf()
        y_val = point[y].evalf()
        st.write(f"Point critique {i + 1} : (x = {x_val}, y = {y_val})")
else:
    st.write("Aucun point critique trouvé.")

# Ajout de sliders pour x et y
st.write("### 🎚️ Modifier les valeurs de x et y")
x_slider = st.slider("📍 Valeur de x :", -5.0, 5.0, 0.0)
y_slider = st.slider("📍 Valeur de y :", -5.0, 5.0, 0.0)

# Génération des données pour le graphique
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Transformation de la fonction en fonction numérique utilisable
fonction_numeric = lambdify((x, y), fonction, modules=["numpy"])
Z = fonction_numeric(X, Y)

# Création du graphique interactif avec Plotly
fig = go.Figure()

# Ajout de la surface 3D
fig.add_trace(go.Surface(z=Z, x=X, y=Y, colorscale="viridis"))

# Ajout du point sélectionné par l'utilisateur
z_val = fonction_numeric(x_slider, y_slider)
fig.add_trace(go.Scatter3d(x=[x_slider], y=[y_slider], z=[z_val],
                           mode='markers', marker=dict(size=5, color='red'),
                           name="Point sélectionné"))

fig.update_layout(title="📊 Représentation interactive de f(x, y)",
                  scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'))

st.plotly_chart(fig)
