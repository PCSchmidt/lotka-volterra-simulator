from fastapi import FastAPI
from scipy.integrate import odeint
import numpy as np

app = FastAPI()

def lotka_volterra(init_conditions, t, alpha, beta, gamma, delta):
    x, y = init_conditions
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lotka-Volterra Simulator!"}

@app.post("/simulate/")
def simulate_lotka_volterra(x0: float, y0: float, alpha: float, beta: float, gamma: float, delta: float, T: int):
    t = np.linspace(0, T, 500)
    init_conditions = [x0, y0]
    params = (alpha, beta, gamma, delta)
    solution = odeint(lotka_volterra, init_conditions, t, args=params)
    return {"time": t.tolist(), "prey": solution[:, 0].tolist(), "predator": solution[:, 1].tolist()}
