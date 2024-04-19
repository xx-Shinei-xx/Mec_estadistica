import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Function to initialize the particle system
def initialize_system(num_particles, box_length):
    positions = np.random.uniform(0, box_length, size=num_particles)
    return positions

# Function to perform a Monte Carlo step using the Demon Algorithm
def monte_carlo_step(positions, box_length, temperature):
    # Randomly select a particle
    selected_particle = np.random.randint(0, len(positions))
    
    # Choose a random move for the selected particle
    move = np.random.uniform(-0.5, 0.5)
    
    # Calculate potential change in energy if particle is moved
    old_position = positions[selected_particle]
    new_position = old_position + move
    potential_energy_change = 0.5 * (new_position**2 - old_position**2)
    
    # Accept or reject the move based on Metropolis criterion
    if np.random.uniform(0, 1) < np.exp(-potential_energy_change / temperature):
        positions[selected_particle] = new_position
        
    return positions

# Function to run the simulation for a given temperature
def run_simulation(num_particles, box_length, temperature, num_steps):
    positions = initialize_system(num_particles, box_length)
    
    for step in range(num_steps):
        positions = monte_carlo_step(positions, box_length, temperature)
        
    return positions

# Streamlit app
st.title("The demon algorithm")

# Sidebar for parameter inputs
num_particles = st.sidebar.slider("Número de partículas", min_value=10, max_value=100, value=50, step=10)
box_length = st.sidebar.slider("Longitud de la celda", min_value=5.0, max_value=20.0, value=10.0, step=1.0)
temperature = st.sidebar.slider("Temperatura", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
num_steps = st.sidebar.slider("Número de pasos", min_value=500, max_value=5000, value=1000, step=500)

# Run the simulation
final_positions = run_simulation(num_particles, box_length, temperature, num_steps)

# Create histogram data
histogram_data = np.histogram(final_positions, bins=30, density=True)

# Define colormap based on histogram data values
color_scale = 'Reds'  # Choose a colormap (e.g., 'Reds')

# Create a bar chart using plotly
fig = go.Figure(data=[go.Bar(
    x=histogram_data[1][:-1],
    y=histogram_data[0],
    marker=dict(color=histogram_data[0], colorbar=dict(title='Density', tickvals=[], ticktext=[]), colorscale=color_scale),
    hoverinfo='x+y',
)])

# Update layout of the plot
fig.update_layout(
    title='Distribución de partículas en equilibrio',
    xaxis_title='Posición',
    yaxis_title='Densidad',
)

# Display the plot using Streamlit
st.plotly_chart(fig)
