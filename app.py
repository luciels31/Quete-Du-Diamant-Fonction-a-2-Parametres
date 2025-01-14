import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sympy import symbols, diff, lambdify
from scipy.optimize import minimize

# Set page configuration
st.set_page_config(page_title="Étude de fonctions à deux variables", layout="wide")

# Title and description
st.title("Étude et Visualisation de Fonctions à Deux Variables")
st.markdown(
    """Bienvenue dans cette application ! Vous pouvez entrer une fonction de deux variables (x, y), spécifier les bornes, 
    et visualiser ses propriétés. Vous obtiendrez également les extrema locaux et globaux.
    """
)

# Input fields for function and ranges
function_input = st.text_input("Entrez une fonction en x et y (ex: x**2 + y**2 - x*y)", "x**2 + y**2")
x_min = st.number_input("Borne inférieure pour x", value=-10.0)
x_max = st.number_input("Borne supérieure pour x", value=10.0)
y_min = st.number_input("Borne inférieure pour y", value=-10.0)
y_max = st.number_input("Borne supérieure pour y", value=10.0)

# Parse the input function
x, y = symbols("x y")
try:
    function = eval(function_input)
    f_lambdified = lambdify((x, y), function, "numpy")
except Exception as e:
    st.error(f"Erreur lors de l'analyse de la fonction : {e}")
    st.stop()

# Create meshgrid
x_vals = np.linspace(x_min, x_max, 100)
y_vals = np.linspace(y_min, y_max, 100)
X, Y = np.meshgrid(x_vals, y_vals)
Z = f_lambdified(X, Y)

# Plotting 3D surface
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="none")
ax.set_title("Surface de la fonction")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("f(x, y)")
st.pyplot(fig)

# Plotting contour
fig2, ax2 = plt.subplots(figsize=(8, 6))
contour = ax2.contourf(X, Y, Z, cmap="viridis")
plt.colorbar(contour)
ax2.set_title("Courbes de niveau de la fonction")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
st.pyplot(fig2)

# Extrema calculation
def find_extrema(f, bounds):
    def f_numpy(coords):
        return f(coords[0], coords[1])

    x_bounds, y_bounds = bounds
    results = []
    for x0 in np.linspace(x_bounds[0], x_bounds[1], 10):
        for y0 in np.linspace(y_bounds[0], y_bounds[1], 10):
            res = minimize(f_numpy, [x0, y0], bounds=[x_bounds, y_bounds])
            if res.success:
                results.append((res.fun, res.x))
    return results

try:
    bounds = [(x_min, x_max), (y_min, y_max)]
    extrema = find_extrema(f_lambdified, bounds)
    extrema_sorted = sorted(extrema, key=lambda x: x[0])

    st.subheader("Extrema trouvés")
    for i, (value, coords) in enumerate(extrema_sorted[:5]):
        st.write(f"Extremum {i + 1} : f({coords[0]:.3f}, {coords[1]:.3f}) = {value:.3f}")
except Exception as e:
    st.error(f"Erreur lors du calcul des extrema : {e}")