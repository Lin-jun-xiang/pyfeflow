# MonteCarlo-Cache

### Introduction

* Optimizing Monte Carlo Simulation:
    * In the [Monte Carlo section](../mc/), we learned that thousands or even tens of thousands of simulations are often performed. Let's say each simulation takes 1 minute (which is common in transient simulations). If we want to perform 10,000 simulations, it would take nearly 7 days...

    * However, have you ever thought that among these 10,000 simulations, some simulation parameters are repeated hundreds or even thousands of times? In other words, we are repeating the same parameter simulations hundreds or thousands of times in these 10,000.

* Cache concept:
    * In Python, we can use `@lru_cache` to store the parameters and the corresponding results for each function call.
    
    * Every time we perform a simulation, we cache the simulation parameters and results. When we call the simulation function next time, we check if the simulation parameters have appeared before. If they have, instead of performing the simulation again, we directly retrieve the cached result.

    * In the following example, since the simulation parameters 1 and 2 appear twice, we can save two simulation runs using the cache.
        ```python
        
        @lru_cache(maxsize=None)
        def monte_carlo(a):
            print(a, 'simulating...') # suppose the time of simulation spend 1 min...

            return ...

        res = [monte_carlo(parameter) for parameter in [1, 2, 1, 2]]

        """
        1 simulating...
        2 simulating...
        """
        ```

### Demo

```python
# monteCarlo_cache.py
import sys
from functools import lru_cache

import ifm
import numpy as np
import seaborn as sns
from scipy import stats


sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
doc = ifm.loadDocument('YOUR_FEM_FILE')

mu, sigma = 1e-3, 1e-4
conductivity = stats.norm.rvs(
    loc = np.math.log(mu**2/(mu**2+sigma**2)**0.5),
    scale = np.math.log((sigma/mu)**2+1)**0.5,
    size = 10000
)
conductivity = np.round(conductivity, 4)
elements = doc.getNumberOfElements()


@lru_cache(maxsize=None)
def monte_carlo(conductivity):
    conductivity = np.math.exp(conductivity)
    conductivity *= 24 * 3600

    for element in range(elements):
        doc.setMatXConductivityValue3D(element, conductivity)
        doc.setMatYConductivityValue3D(element, conductivity)
        doc.setMatZConductivityValue3D(element, 0.1*conductivity)

    doc.startSimulator()

    velocityX = doc.getResultsXVelocityValue(300)

    doc.stopSimulator()

    return velocityX


velocityX = [monte_carlo(c) for c in conductivity]
sns.distplot(velocityX)

```
