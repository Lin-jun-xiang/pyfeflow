# Optimization-by-BAS
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)
### Introduction
* Using Beetle Antennae Search algorithm (`BAS`) to solve the unknow parameter problem from groundwater simulation (Reduce simulation error).

* Tools
    * Numerical groundwater simulation tool : FEFLOW7.3

    * Script : Python 3.8.6

* Function and Purpose

    * Establishing a groundwater flow model requires **fitting** simulated values to observed values, which may be difficult due to lack of data.
    * **Optimization algorithms** can **automatically adjust parameters** to achieve the fitting goal.
    * This function can use optimization algorithms to find missing data parameters and fit simulated values to observed values.

* **Optimization** algorithms vs. `FePEST` calibration:

   * Optimization algorithms can customize the objective function, making it faster and easier to fit the simulation results.
   * Optimization algorithms are not limited to specific parameters and can be applied to any unknown parameter optimization (e.g. `FePEST` can only calibrate `element` properties and cannot calibrate pumping well parameters).

* `BAS` is a type of optimization algorithm developed by Jiang and Li in 2017. The algorithm is as follows:

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159463464-716ea7a1-7af6-491e-aebd-db98ea735cd2.png" width=50%/>
</p>

* Context
In our research area, there are many private wells for which we cannot obtain detailed information (such as well location and pumping rates). Therefore, we uniformly set up some virtual wells in the study area, and all pumping rates are system parameters. These system parameters will be adjusted through `BAS` to match the simulated and observed values.
(Note: unknown parameters can be considered hydraulic conductivity, porosity, saturation, etc.)

* :warning: `Important Note`: This application scenario is referenced from the paper - <a href="https://hdl.handle.net/11296/tq3m78" target="_blank">Numerical simulation of groundwater development and evaluation - A case study of Kaoping River</a>

---
### Algorithm Flow

* Define the following:
    * **Unknown parameters** (parameters to be optimized): pumping rates of each well
    * **Objective function**: Root Mean Square Error (RMSE) between simulated hydraulic head and observed water level
    * Beetle step length
    * Spacing between whiskers

* Algorithm:

    1. Randomly initialize unknown parameters (pumping rates)
    2. Perform simulation
    3. Calculate the objective function using simulated hydraulic head and observed water level (the goal is to minimize the objective function, i.e., minimize the error)
    4. Adjust parameters using BAS, iterate repeatedly until the objective function is less than the threshold

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/168416976-8bc62e63-a839-44ba-9dec-d194c9b0ad56.png" widht=50%/>
</p>

---
### Part1 - Study area

Roughly explain:
1. The study area is Pingtung in Taiwan.
2. The following image is the groundwater table of observation.

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640237-e52cecde-67de-4818-94fc-4c3c03219a4f.png" width=50%/>
</p>

---
### Part2 - Groundwater Simulation

Roughly explain:
1. We use the **FEFLOW7.3** to build our flow model.
2. Setting the boundary condition. (ex: Dirichlet, Neumann...)
3. Setting the hydraulic conductivity and inflow of study area.

---
### Part3 - Before Optimization

As we can see, the result is not good without well setting.
(gray line : observation ; color line : simulation result)

And compare to the observation data, the

> **absolute error**: `6.87`
>
> **root mean square**: `7.83`
>
> **standard deviation**: `8`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159640520-910c0a10-67a5-45de-b03b-93d0be45e868.png" width=200px/>
</p>

---
### Part4 - After Optimization

We set well in the study area uniformly, and then use BAS.

> **absolute error** : `0.988`
>
> **root mean square**: `1.3`
>
> **standard deviation**: `1.3`

<p align="center">
<img src="https://user-images.githubusercontent.com/63782903/159641259-042c74c8-3028-4253-a7b8-249b46966bc5.png" width=60%/>
</p>

---
### Part5 - Results

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178942962-eb72864d-f97b-45e6-b571-ab54cf841cc3.png" width=50% />

<p align="center">
<image src="https://user-images.githubusercontent.com/63782903/178094741-34584c0d-b9a9-44c4-8386-3b2c3005522c.png" width=50%/>

<a href="#top">Back to top</a>

### Examples

```python
# BAS_algorithm.py
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
```
