from typing import List, Union

import numpy as np
import seaborn as sns
from pydantic import BaseModel
from scipy import stats


class SimulatedParam(BaseModel):
    name: str
    values: Union[List, np.ndarray]
    domain_elements: List


class MonteCarloSimulator:
    """Homogeneous case
    
    Examples
    --------
    A random hydraulic conductivity case.
    * suppose the area_1 (elementId 1~1000) are gravel type
    * suppose the area_2 (elementId 1001~2000) are clay type

    Collect nodeId 13, the hydraulic head values obtained
    in each Monte Carlo simulation.
    (can collect any result base on `ifm`)

    ```python
    import ifm
    from pyfeflow import MonteCarloSimulator

    # Loading FEFLOW project document
    doc = ifm.loadDocument('Your_FEM_FILE.fem')

    simulation_times = 100
    monte_carlo_simulator = MonteCarloSimulator(doc, simulation_times)

    # Hydraulic conductivity is setting on element
    elements = doc.getNumberOfElements()

    # Build the distribution for hydraulic conductivity
    hydraulic_samples_area1 = monte_carlo_simulator(
        domain_elements = elements[:1001], # elementId: 1~1000
        mu = 1e-3,
        sigma = 1e-4
    )
    hydraulic_samples_area2 = monte_carlo_simulator(
        domain_elements = elements[1000:2001], # elementId: 1000~2001
        mu = 1e-8,
        sigma = 1e-4
    )

    # Run MonteCarlo simulation
    hydraulic_heads = []
    for i in range(simulation_times):
        monte_carlo_simulator.run(
            [hyraulic_samples_area1, hydraulic_samples_area2], i
        )
        # collect data in each simulation
        hyraulic_heads.append(
            doc.getResultsFlowHeadValue(13)
        )

    # Plot the monteCarlo results
    monte_carlo_simulator.show(hydraulic_heads)
    ```
    """
    def __init__(self, doc, simulation_times: int = 100) -> None:
        self.doc = doc
        self.simulation_times = simulation_times

    def hydraulic_conductivity_samples(
        self,
        domain_elements: List = None,
        mu: float = 1e-3,
        sigma: float = 1e-4
    ) -> SimulatedParam:
        """
        Hydraulic conductivity (K) ~ log-normal-distribution
        (https://en.wikipedia.org/wiki/Log-normal_distribution)

        Parameters
        ----------
        domain_elements: list
            the simulated area (elements), default is all elements
        num_samples: int
            the samples of distribution
        mu: float
            mean of K (m/s)
        sigma: float
            standard deviation of K (m/s)
        """
        conductivity_distr = stats.norm.rvs(
            loc=np.math.log(mu**2/(mu**2+sigma**2)**0.5),
            scale=np.math.log((sigma/mu)**2+1)**0.5,
            size=self.simulation_times
        )
        return SimulatedParam(
            name='h_conductivity',
            values=conductivity_distr,
            domain_elements=domain_elements
        )

    def thermal_conductivity_samples(self):
        pass

    def _setup_parameters(
        self, simulated_param: SimulatedParam, ith: int
    ) -> None:
        param_name = simulated_param.name
        # the ith sample from distribution
        param_value = simulated_param.values[ith]
        simulated_area = simulated_param.domain_elements

        if param_name == 'h_conductivity':
            param_value = np.math.exp(param_value)
            param_value *= 24 * 3600
            for element in simulated_area:
                self.doc.setMatXConductivityValue3D(element, param_value)
                self.doc.setMatYConductivityValue3D(element, param_value)
                self.doc.setMatZConductivityValue3D(element, 0.1*param_value)
            return

    def run(self, simulated_params: List[SimulatedParam], ith: int) -> None:
        """
        Parameters
        ----------
        simulated_params: List[SimulatedParam]

        Examples
        --------
        ```python
        simulated_params = [
            hydraulic_conductivity_for_area1,
            hydraulic_conductivity_for_area2,
            thermal_conductivity_for_area1,
        ]
        ```
        """
        for simulated_param in simulated_params:
            self._setup_parameters(simulated_param, ith)
            
        self.doc.startSimulator()
        self.doc.stopSimulator()

    def show(self, data) -> None:
        sns.distplot(data)
