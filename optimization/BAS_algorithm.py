import math
import sys
from functools import lru_cache

import ifm
import numpy as np
import pandas as pd


# Adding FEFLOW directory to system path
sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
# Loading FEFLOW project document
doc = ifm.loadDocument('Your_FEM_FILE')
# Define the parameter which want to be calibrated
CALIBRATION_PARA = 'Head'


class ObservationData:
    def __init__(self, observation_data: pd.DataFrame):
        self.obs_data = observation_data

    @property
    def get_node_data(self):
        """Returns a dictionary of observation head values with node IDs as keys"""
        obs_heads = {}
        for i in self.obs_data.index:
            obs_heads[i+1] = self.obs_data[CALIBRATION_PARA][i]

        return obs_heads

    @property
    def get_node_coordinates(self):
        """Returns dictionaries of observation point X and Y coordinates with node IDs as keys"""
        obs_x, obs_y = {}, {}
        for i in self.obs_data.index:
            obs_x[i+1] = self.obs_data["X"][i]
            obs_y[i+1] = self.obs_data["Y"][i]

        return obs_x, obs_y


class FeflowAPI:
    @staticmethod
    def get_simulation_result(node_id: int):
        if CALIBRATION_PARA == 'Head':
            return doc.getResultsFlowHeadValue(node_id)
                                                      
    @staticmethod
    def get_well_effect_region(
        well_id: int,
        obs_x: dict,
        obs_y: dict,
        effect_radius: float=1000
    ) -> list:
        """Returns a list of node IDs within the effective radius of a given well"""
        well_node = doc.getMultiLayerWellTopNode(well_id)
        well_x, well_y = obs_x[well_node], obs_y[well_node]

        effected_nodes = []
        for node in obs_x:
            distance = ((well_x - obs_x[node])**2 + (well_y - obs_y[node])**2)**0.5

            if distance <= effect_radius:
                effected_nodes.append(node)
        return effected_nodes

    @staticmethod
    def get_well_info() -> None:
        """Prints the number of multi-layer wells in the project and their respective pump rates"""
        well_n = int(doc.getNumberOfMultiLayerWells())
        print("well number= ", well_n)
        
        for i in range(well_n):
            print(f"doc.setMultiLayerWellAttrValue({i}, 0, {int(doc.getMultiLayerWellAttrValue(i, 0))})")


@lru_cache(maxsize=50)
def optimizing_function(
    obs_heads: dict,
    effected_nodes: list,
    well_ids: int,
    well_pumps_rate: np.ndarray
) -> float:
    """Calculates the objective function for a given set of well pump rates"""
    for well_id in range(well_ids):
        doc.setMultiLayerWellAttrValue(well_id, 0, well_pumps_rate[well_id])

    loss = 0
    N = len(effected_nodes)
    doc.startSimulator()

    for node in effected_nodes:
        sim_head = feflow_api.get_simulation_result(node-1)
        loss += (obs_heads[node] - sim_head)**2/N # MSE
    doc.stopSimulator()

    return loss


class BeetleSearch:
    def normalize(self, x: np.ndarray) -> np.ndarray:
        """Normalizes a given vector"""
        norm = math.sqrt(sum(e**2 for e in x))
        return x / norm

    def sign(self, a):
        """Returns the sign of a given number"""
        if a > 0: return 1
        elif a < 0: return -1
        else: return 0
    
    def run_bas(
        self,
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
        well_ids = doc.getNumberOfMultiLayerWells()

        # Initialize the well pump rates and corresponding variables
        # The unknown parameters, i.e., the pumping rates of n wells (n-dimensional problem)
        well_pumps_rate = np.array([0 for _ in range(well_ids)])
        xl = well_pumps_rate
        xr = well_pumps_rate

        # Determine the nodes influenced by each well and store in a list
        effected_nodes = []
        for well_id in range(well_ids):
            effected_nodes.extend(feflow_api.get_well_effect_region(well_id, obs_x, obs_y))

        i = 0
        # Run the optimization algorithm
        # 2 is the threshold, acceptable loss value (total head error)
        while step/100 >= 2 or i <= iter:
            dir = np.random.randn(well_ids)
            dir = self.normalize(dir)

            xl = well_pumps_rate + d0*dir/2
            xr = well_pumps_rate - d0*dir/2

            fl = optimizing_function(obs_heads, effected_nodes, well_ids, xl)
            fr = optimizing_function(obs_heads, effected_nodes, well_ids, xr)

            well_pumps_rate = well_pumps_rate - step*dir*self.sign(fl-fr)

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

    obs_data = ObservationData(data)
    obs_heads = obs_data.get_node_data
    obs_x, obs_y = obs_data.get_node_coordinates

    feflow_api = FeflowAPI()

    bas = BeetleSearch()
    bas.run_bas()

    feflow_api.get_well_info()
