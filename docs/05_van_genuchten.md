# Water Retention Curve
* [中文版說明書](./README_%E4%B8%AD%E6%96%87.md)

### Introduction

* Plot the "**Unsaturated Curve**".

* Input parameters:
    * `particle_types`
        > Rock properties, such as gravel layer, sand layer, or mud layer.
    * `saturation_capacity` [dimensionless]
        > Saturation capacity, generally set to 1.
    * `residual_saturation` [dimensionless]
        > Residual saturation, defined as the water content when the change gradient of water content (dθ /dh) is zero.
    * `air_entry_value` [1/m]
        > Related to the air entry value, the larger "a" is, the steeper the curve.
    * `pore_size_distribution` [dimensionless]
        > lated to the distribution of soil pore size, the more uniform the distribution of soil pore size, the smaller n, the smoother and gentler the curve, and the larger the value of "n".

---

### Example

* The rock layers and their unsaturated parameters are shown in the following table:
    |Rock Layer|Gravel Layer|Sand Layer|Mud Layer|
    | -- | -- | -- | -- |
    | Sr | 0.0311 | 0.045 | 0.068 |
    | a  | 493. | 14.5 | 0.068 |
    | n  | 2.4476 | 2.68 | 2. |

* Simulation result plot:
    ![](../images/2023-04-08-20-58-01.png)

```python
#van_genuchten.py
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set()


def water_retention_curve(
    particle_types: List[str],
    saturation_capacity: List[float],
    residual_saturation: List[float],
    air_entry_value: List[float],
    pore_size_distribution: List[float],
    pore_shape_factor: List[float],
    pressure_head: np.ndarray
) -> None:
    """calculate water content based on Van Genuchten model

    Parameters:
    -----------
    particle_types : List[str]
        A list of names of the soil particle types.
    saturation_capacity : List[float]
        A list of the soil saturation capacity, which is the maximum amount of water the soil can hold.
    residual_saturation : List[float]
        A list of the soil residual saturation, which is the water content retained in the soil at very low pressures.
    air_entry_value : List[float]
        A list of the soil air entry value, which is the lowest pressure at which air can enter the soil and water starts to drain.
    pore_size_distribution : List[float]
        A list of the soil pore size distribution, which is the variability of the pore sizes in the soil.
    pore_shape_factor : List[float]
        A list of the soil pore shape factor, which is the shape of the pores in the soil.
    pressure_head : np.ndarray
        An array of the pressure head range for plotting.

    Returns:
    --------
    None

    """

    water_content = [[residual_saturation[i] + ((saturation_capacity[i]-residual_saturation[i])/(1.0+(air_entry_value[i]*h)**pore_size_distribution[i])**pore_shape_factor[i]) for h in pressure_head] for i in range(len(particle_types))]
    
    fig = plt.figure(figsize=(7, 7))
    ax1 = fig.add_subplot(111)
    color = ['dodgerblue', 'gold', 'orange', 'r']
    [ax1.plot(water_content[i], pressure_head, c=color[i], label=particle_types[i], linewidth=3) for i in range(len(particle_types))]
    plt.yscale("log")
    
    ax1.legend(loc='upper right')
    ax1.set(xlim=(0.0, 1),
            xlabel="${\Theta}$ (water content)",
            ylabel="-hp",
            title="Water retention curve")

    plt.xlabel("${\Theta}$ (water content)", fontsize=24)
    plt.ylabel("-hp", fontsize=24)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.title("Water retention curve", fontsize=28)
    plt.show()


if __name__ == "__main__":
    # define soil particle types and related parameters
    particle_types = ["Gravel", "Sand", "Clay"]
    saturation_capacity = [1., 1., 1.]
    residual_saturation = [0.0311, 0.045, 0.068]
    air_entry_value = [493., 14.5, 0.0008] # higher a : the low suction threshold of air entry(start to drain)
    pore_size_distribution = [2.4476, 2.68, 2.] # 1.0~5.0; higher n: free drain; n=1: not drain
    pore_shape_factor = [1-1/i for i in pore_size_distribution]

    # define pressure head range for plotting
    clay_pressure_head = np.linspace(1e1, 1e5, 10000) # clay scale
    sand_pressure_head = np.linspace(1e-4, 1e1, 100000) # sand, gravel scale
    pressure_head = np.append(sand_pressure_head, clay_pressure_head)

    water_retention_curve(
        particle_types,
        saturation_capacity,
        residual_saturation,
        air_entry_value,
        pore_size_distribution,
        pore_shape_factor,
        pressure_head
    )
```
