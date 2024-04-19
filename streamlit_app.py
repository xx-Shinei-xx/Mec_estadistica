import numpy as np
import streamlit as st
import plotly.graph_objects as go

# inicializar el sistema de partículas
def sis(n_particulas, box_length):
    posicion = np.random.uniform(0, box_length, size=n_particulas)
    return posicion

# Function to perform a Monte Carlo step using the Demon Algorithm
def monte_carlo(posicion, box_length, temperatura):
    # Randomly select a particle
    particula = np.random.randint(0, len(posicion))
    
    # Choose a random valor for the selected particle
    valor = np.random.uniform(-0.5, 0.5)
    
    # Calculate potential change in energy if particle is valord
    xi = posicion[particula]
    xf = xi + valor
    pe = 0.5 * (xf**2 - xi**2)
    
    # Accept or reject the valor based on Metropolis criterion
    if np.random.uniform(0, 1) < np.exp(-pe / temperatura):
        posicion[particula] = xf
        
    return posicion

# Function to run the simulation for a given temperatura
def simulacion(n_particulas, box_length, temperatura, n_pasos):
    posicion = sis(n_particulas, box_length)
    
    for step in range(n_pasos):
        posicion = monte_carlo(posicion, box_length, temperatura)
        
    return posicion

# Streamlit app
st.title("Demon Algorithm Simulation")

# Sidebar for parameter inputs
n_particulas = st.sidebar.slider("Número de partículas", valor_min=10, valor_max=100, value=50, step=10)
box_length = st.sidebar.slider(" longitud de la celda", valor_min=5.0, valor_max=20.0, value=10.0, step=1.0)
temperatura = st.sidebar.slider("temperatura", valor_min=0.1, valor_max=3.0, value=1.0, step=0.1)
n_pasos = st.sidebar.slider("Número de pasos", valor_min=500, valor_max=5000, value=1000, step=500)

# Run the simulation
xff = simulacion(n_particulas, box_length, temperatura, n_pasos)

# Create histogram data
histograma = np.histogram(xff, bins=30, density=True)

# Define colormap based on histogram data values
color = 'Reds'  # Choose a colormap (e.g., 'Reds')

# Create a bar chart using plotly
fig = go.Figure(data=[go.Bar(
    x=histograma[1][:-1],
    y=histograma[0],
    marker=dict(color=histograma[0], colorbar=dict(title='Density', tickvals=[], ticktext=[]), colorscale=color),
    hoverinfo='x+y',
)])

# Update layout of the plot
fig.update_layout(
    title='Distribución de partículas en equilibrio',
    titulo_x='pocisopm',
    titulo_y='densidad',
)

# Display the plot using Streamlit
st.plotly_chart(fig)
