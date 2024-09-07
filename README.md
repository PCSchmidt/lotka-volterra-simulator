# Lotka-Volterra Simulator

This project is a FastAPI-based web application that simulates the Lotka-Volterra predator-prey model. Users can adjust the parameters and see the population dynamics over time.

## Features

- Simulate predator-prey dynamics with customizable parameters
- API endpoint for performing simulations
- Optional HTML frontend (extendable)

## Endpoints

### `/`

Returns a welcome message.

### `/simulate/`

Perform a simulation of the Lotka-Volterra model.

**Parameters**:

- `x0` (float): Initial prey population
- `y0` (float): Initial predator population
- `alpha` (float): Prey birth rate
- `beta` (float): Predation rate
- `gamma` (float): Predator death rate
- `delta` (float): Predator growth rate
- `T` (int): Time period for simulation

**Response**:
Returns a JSON object with time, prey population, and predator population arrays.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/lotka-volterra-simulator.git
   ```
