import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify, sin, cos, exp
from sympy.solvers import solve

# Titre de l'application
st.title("Étude et visualisation des fonctions réelles à deux paramètres")

# Description
st.write(
    "Cette application permet de visualiser et d'étudier des fonctions réelles \(f(x, y)\) "
    "en fournissant des graphiques et une analyse mathématique (extrema, dérivées, etc.)."
)

# Sélection de la fonction
fonction_str = st.selectbox(
    "Choisissez une fonction à étudier :",
    ["x**2 + y**2", "sin(x) * cos(y)", "exp(-x**2 - y**2)"]
)

# Définir un contexte sûr pour `eval`
safe_dict = {"x": symbols("x"), "y": symbols("y"), "sin": sin, "cos": cos, "exp": exp}
x, y = safe_dict["x"], safe_dict["y"]

try:
    fonction = eval(fonction_str, {"__builtins__": None}, safe_dict)
except Exception as e:
    st.error(f"Erreur lors de l'interprétation de la fonction : {e}")
    st.stop()

# Calcul des dérivées partielles
df_dx = diff(fonction, x)
df_dy = diff(fonction, y)

# Points critiques : Résolution des équations df/dx = 0 et df/dy = 0
crit_points = st.checkbox("Afficher les points critiques ?")
if crit_points:
    st.write("### Points critiques :")
    try:
        # Résolution
        solutions = solve([df_dx, df_dy], (x, y), dict=True)
        st.write(f"Solutions brutes (pour débogage) : {solutions}")

        if solutions:
            for point in solutions:
                # Vérification des types et évaluation
                x_val = point.get(x, None)
                y_val = point.get(y, None)

                # Évaluation numérique si possible
                if x_val is not None and y_val is not None:
                    try:
                        x_val = x_val.evalf() if hasattr(x_val, "evalf") else x_val
                        y_val = y_val.evalf() if hasattr(y_val, "evalf") else y_val
                        st.write(f"Point critique : (x = {x_val}, y = {y_val})")
                    except Exception as eval_error:
                        st.error(f"Erreur lors de l'évaluation du point critique : {eval_error}")
                else:
                    st.error("Impossible d'évaluer un ou plusieurs points critiques.")
        else:
            st.write("Aucun point critique trouvé.")
    except Exception as solve_error:
        st.error(f"Erreur lors du calcul des points critiques : {solve_error}")

# Définition des bornes pour x et y
x_min = st.slider("x minimum", -10, 0, -5)
x_max = st.slider("x maximum", 0, 10, 5)
y_min = st.slider("y minimum", -10, 0, -5)
y_max = st.slider("y maximum", 0, 10, 5)

# Génération des données pour x et y
x_vals = np.linspace(x_min, x_max, 100)
y_vals = np.linspace(y_min, y_max, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Conversion de la fonction en fonction numérique
fonction_numeric = lambdify((x, y), fonction, "numpy")
Z = fonction_numeric(X, Y)

# Tracé du graphique 3D
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="k", alpha=0.8)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
ax.set_title(f"Graphique de {fonction_str}")
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

# Affichage dans Streamlit
st.pyplot(fig)

# Analyse mathématique
st.header("Analyse mathématique")
st.write(f"Fonction choisie : \( f(x, y) = {fonction_str} \)")
st.write("### Dérivées partielles :")
st.latex(f"\\frac{{\\partial f}}{{\\partial x}} = {df_dx}")
st.latex(f"\\frac{{\\partial f}}{{\\partial y}} = {df_dy}")
