import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sympy import symbols, diff, solve, sin, cos, exp, lambdify

# Définition des symboles
x, y = symbols('x y')

# Dictionnaire des fonctions autorisées pour l'évaluation sécurisée
allowed_functions = {
    "sin": sin,
    "cos": cos,
    "exp": exp,
    "x": x,
    "y": y
}

# Interface utilisateur
st.title("Étude et visualisation de fonctions à deux variables")

# Sélection de la fonction
options = {
    "x² + y²": x**2 + y**2,
    "sin(x) * cos(y)": sin(x) * cos(y),
    "exp(-x² - y²)": exp(-x**2 - y**2),
    "Entrer une fonction personnalisée": None
}

fonction_choisie = st.selectbox("Choisissez une fonction prédéfinie ou entrez la vôtre :", list(options.keys()))

# Gestion de la fonction personnalisée
if fonction_choisie == "Entrer une fonction personnalisée":
    fonction_str = st.text_input("Entrez votre fonction en termes de x et y :", "x**2 + y**2")
    try:
        fonction = eval(fonction_str, {"__builtins__": None}, allowed_functions)
    except Exception as e:
        st.error(f"Erreur dans la définition de la fonction : {e}")
        st.stop()
else:
    fonction = options[fonction_choisie]

# Calcul des dérivées partielles
df_dx = diff(fonction, x)
df_dy = diff(fonction, y)

# Calcul des points critiques
solutions = solve([df_dx, df_dy], (x, y), dict=True)

# Affichage de la fonction
st.write("### Fonction sélectionnée :")
st.latex(f"f(x, y) = {fonction}")

# Affichage des points critiques
st.write("### Points critiques :")
if solutions:
    for i, point in enumerate(solutions):
        x_val = point[x].evalf()
        y_val = point[y].evalf()
        st.write(f"Point critique {i + 1} : (x = {x_val}, y = {y_val})")
else:
    st.write("Aucun point critique trouvé.")

# Création du graphique interactif avec Plotly
st.write("### Visualisation interactive de la fonction")

# Génération des données pour le graphique
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Transformation de la fonction en fonction numérique utilisable
fonction_numeric = lambdify((x, y), fonction, modules=["numpy"])
Z = fonction_numeric(X, Y)

# Création du graphique Plotly
fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="viridis")])
fig.update_layout(title="Représentation 3D de f(x, y)", scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'))

st.plotly_chart(fig)
