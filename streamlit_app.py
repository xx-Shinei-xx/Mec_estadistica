import numpy as np
import streamlit as st
import plotly.graph_objects as go

def initialize_system(num_particles, box_length):
    # posiciones de las partículas de forma aleatoria en la caja
    positions = np.random.uniform(0, box_length, size=num_particles)
    return positions
def monte_carlo_step(positions, box_length, temperature):
    # prediccion de una particula
    selected_particle = np.random.randint(0, len(positions))
    move = np.random.normal(loc=0.0, scale=0.5)
    
    # cambio de energía potencial  
    old_position = positions[selected_particle]
    new_position = old_position + move
    potential_energy_change = 0.5 * (new_position**2 - old_position**2)
    if np.random.uniform(0, 1) < np.exp(-potential_energy_change / temperature):
        positions[selected_particle] = new_position  
    return positions
def run_simulation(num_particles, box_length, temperature, num_steps):
    positions = initialize_system(num_particles, box_length)
    for step in range(num_steps):
        positions = monte_carlo_step(positions, box_length, temperature)
    return positions
st.title("El algoritmo del demonio")

#Streamlit
num_particles = st.sidebar.slider("Número de partículas", min_value=10, max_value=100, value=50, step=10)
box_length = st.sidebar.slider("Longitud de la celda", min_value=5.0, max_value=20.0, value=10.0, step=1.0)
temperature = st.sidebar.slider("Temperatura", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
num_steps = st.sidebar.slider("Número de pasos", min_value=500, max_value=5000, value=1000, step=500)

# Ejecuta la simulación
final_positions = run_simulation(num_particles, box_length, temperature, num_steps)

#Histograma de las posiciones finales de las partículas
histogram_data = np.histogram(final_positions, bins=30, density=True)
color_scale = 'Reds'  

fig = go.Figure(data=[go.Bar(
    x=histogram_data[1][:-1],
    y=histogram_data[0],
    marker=dict(color=histogram_data[0], colorbar=dict(title='Densidad', tickvals=[], ticktext=[]), colorscale=color_scale),
    hoverinfo='x+y',
)])

fig.update_layout(
    title='Distribución de partículas en equilibrio',
    xaxis_title='Posición',
    yaxis_title='Densidad',
)

st.plotly_chart(fig)
