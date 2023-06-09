import math
import sys

import ifm
import numpy as np
import pandas as pd


# Adding FEFLOW directory to system path
sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
# Loading FEFLOW project document
doc = ifm.loadDocument('Your_FEM_FILE')


def normalize(x: np.ndarray) -> np.ndarray:
    """Normalizes a given vector"""
    norm = math.sqrt(sum(e**2 for e in x))
    return x / norm


def set_obs_heads(data) -> dict:
    """Returns a dictionary of observation head values with node IDs as keys"""
    obs_heads = {}
    for i in data.index:
        obs_heads[i+1] = data["Head"][i]

    return obs_heads


def set_obs_coordinates(data: pd.DataFrame):
    """Returns dictionaries of observation point X and Y coordinates with node IDs as keys"""
    obs_x, obs_y = {}, {}
    for i in data.index:
        obs_x[i+1] = data["X"][i]
        obs_y[i+1] = data["Y"][i]

    return obs_x, obs_y


def get_well_effect_region(
    well_number: int,
    obs_x: dict,
    obs_y: dict,
    effect_radius: float=1000
) -> list:
    """Returns a list of node IDs within the effective radius of a given well"""
    well_node = doc.getMultiLayerWellTopNode(well_number)
    well_x, well_y = obs_x[well_node], obs_y[well_node]

    effected_nodes = []
    for node in obs_x:
        distance = ((well_x - obs_x[node])**2 + (well_y - obs_y[node])**2)**0.5

        if distance <= effect_radius:
            effected_nodes.append(node)
    return effected_nodes


def sign(a):
    """Returns the sign of a given number"""
    if a > 0: return 1
    elif a < 0: return -1
    else: return 0


def optimizing_function(
    obs_heads: dict,
    effected_nodes: list,
    well_numbers: int,
    well_pumps_rate: np.ndarray
) -> float:
    """Calculates the objective function for a given set of well pump rates"""
    for well_number in range(well_numbers):
        doc.setMultiLayerWellAttrValue(well_number, 0, well_pumps_rate[well_number])

    loss = 0
    N = len(effected_nodes)
    doc.startSimulator()

    for node in effected_nodes:
        sim_head = doc.getResultsFlowHeadValue(node-1)
        loss += (obs_heads[node] - sim_head)**2/N # MSE
    doc.stopSimulator()

    return loss


def get_well_info() -> None:
    """Prints the number of multi-layer wells in the project and their respective pump rates"""
    well_n = int(doc.getNumberOfMultiLayerWells())
    print("well number= ", well_n)
    for i in range(well_n):
        print(f"doc.setMultiLayerWellAttrValue({i}, 0, {int(doc.getMultiLayerWellAttrValue(i, 0))})")


def run_bas(
    iter: int = 500,
    step: int = 250,
    d0: int = 5000,
) -> None:
    """

    Parameters
    ----------
    iter (int, optional)
        Number of iteration. Defaults to 500.
    step (int, optional)
        Beetle step length. Defaults to 250.
    d0 (int, optional)
        Spacing between whiskers. Defaults to 5000.
    """    
    # Get number of multi-layer-wells in the document
    well_numbers = doc.getNumberOfMultiLayerWells()

    # Initialize the well pump rates and corresponding variables
    # The unknown parameters, i.e., the pumping rates of n wells (n-dimensional problem)
    well_pumps_rate = np.array([0 for _ in range(well_numbers)])
    xl = well_pumps_rate
    xr = well_pumps_rate

    # Determine the nodes influenced by each well and store in a list
    effected_nodes = []
    for well_number in range(well_numbers):
        effected_nodes.extend(get_well_effect_region(well_number, obs_x, obs_y))

    i = 0
    # Run the optimization algorithm
    # 2 is the threshold, acceptable loss value (total head error)
    while step/100 >= 2 or i <= iter:
        dir = np.random.randn(well_numbers)
        dir = normalize(dir)

        xl = well_pumps_rate + d0*dir/2
        xr = well_pumps_rate - d0*dir/2

        fl = optimizing_function(obs_heads, effected_nodes, well_numbers, xl)
        fr = optimizing_function(obs_heads, effected_nodes, well_numbers, xr)

        well_pumps_rate = well_pumps_rate - step*dir*sign(fl-fr)

        # Adjust the pumping rate based on the magnitude of the head error
        step = 100 * 0.5 * (abs(fl) + abs(fr))

        i += 1
        print('epoch=', i+1, 'loss=', fl, fr, 'step=', step)


if __name__ == "__main__":
    # Reading observation head data from an Excel file
    # | Node_ID |  Head  |
    # |    0    |   25   |
    # |    10   |  12.2  |
    data = pd.read_excel("THE_OBSERVATION_HEAD.xlsx")

    obs_heads = set_obs_heads(data)
    obs_x, obs_y = set_obs_coordinates(data)[0], set_obs_coordinates(data)[1]

    run_bas()
    get_well_info()

    print("Finished")
