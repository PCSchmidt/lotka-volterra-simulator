from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from scipy.integrate import odeint
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Mount static files (if you have any CSS or JS files)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class SimulationParams(BaseModel):
    """
    Pydantic model for validating and describing simulation parameters.
    All parameters must be positive. Simulation time is capped at 1000 units.
    """
    x0: float = Field(..., gt=0, description="Initial prey population")
    y0: float = Field(..., gt=0, description="Initial predator population")
    alpha: float = Field(..., gt=0, description="Prey birth rate")
    beta: float = Field(..., gt=0, description="Predation rate")
    gamma: float = Field(..., gt=0, description="Predator death rate")
    delta: float = Field(..., gt=0, description="Predator growth rate")
    T: int = Field(..., gt=0, le=1000, description="Simulation time")

def lotka_volterra(init_conditions, t, alpha, beta, gamma, delta):
    """
    Defines the Lotka-Volterra predator-prey model equations.

    Args:
    init_conditions (list): Initial populations [x, y]
    t (float): Time point (not used explicitly but required for odeint)
    alpha (float): Prey birth rate
    beta (float): Predation rate
    gamma (float): Predator death rate
    delta (float): Predator growth rate

    Returns:
    list: Rate of change for prey and predator populations [dx/dt, dy/dt]
    """
    x, y = init_conditions
    dxdt = alpha * x - beta * x * y  # Change in prey population
    dydt = delta * x * y - gamma * y  # Change in predator population
    return [dxdt, dydt]

@app.get("/")
async def read_root(request: Request):
    """
    Root endpoint that serves the HTML template.

    Args:
    request (Request): The incoming request object

    Returns:
    TemplateResponse: Rendered HTML template
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/simulate/")
def simulate_lotka_volterra(params: SimulationParams):
    """
    Endpoint to run a Lotka-Volterra simulation with given parameters.

    Args:
    params (SimulationParams): Input parameters for the simulation

    Returns:
    dict: Simulation results containing time series for prey and predator populations

    Raises:
    HTTPException: If the simulation fails for any reason
    """
    try:
        # Create time points for the simulation
        t = np.linspace(0, params.T, 500)
        
        # Set up initial conditions and parameters
        init_conditions = [params.x0, params.y0]
        model_params = (params.alpha, params.beta, params.gamma, params.delta)
        
        # Run the simulation
        solution = odeint(lotka_volterra, init_conditions, t, args=model_params)
        
        # Prepare and return the results
        return {
            "time": t.tolist(),
            "prey": solution[:, 0].tolist(),
            "predator": solution[:, 1].tolist()
        }
    except Exception as e:
        # If any error occurs during simulation, raise an HTTP exception
        raise HTTPException(status_code=400, detail=f"Simulation failed: {str(e)}")

@app.get("/info/")
def get_model_info():
    """
    Endpoint to provide information about the Lotka-Volterra model and its parameters.

    Returns:
    dict: Model name, description, and parameter explanations
    """
    return {
        "name": "Lotka-Volterra Predator-Prey Model",
        "description": "A mathematical model that describes the dynamics of biological systems in which two species interact, one as a predator and the other as prey.",
        "parameters": {
            "x0": "Initial prey population",
            "y0": "Initial predator population",
            "alpha": "Prey birth rate",
            "beta": "Predation rate",
            "gamma": "Predator death rate",
            "delta": "Predator growth rate",
            "T": "Simulation time"
        }
    }

# Additional comments can be added here to explain the overall structure or purpose of the file
