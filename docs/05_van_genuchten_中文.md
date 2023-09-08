# Water Retention Curve

### 簡介

* 繪製 "**未飽和曲線**"

* 輸入參數:
    * `particle_types`
        > 岩層屬性，例如礫石層、砂層或泥層
    * `saturation_capacity` [無因次/無量綱]
        > 飽和含水量，一般設為 1
    * `residual_saturation` [無因次/無量綱]
        > 殘餘含水量，定義為水分含量的變化梯度 (dθ /dh) 為零的時候，此時的水分含量即為殘餘水分含量
    * `air_entry_value` [1/m]
        > 與空氣陷入值有關，a 越大曲線越陡
    * `pore_size_distribution` [無因次/無量綱]
        > 與土壤孔徑分布有關，土壤孔徑分布越均勻n越小，曲線越圓滑、平緩，n值越大

---

### 範例

* 岩層與其未飽和參數如下表:
    |岩層|礫石層|砂層|泥層|
    | -- | -- | -- | -- |
    | Sr | 0.0311 | 0.045 | 0.068 |
    | a  | 493. | 14.5 | 0.068 |
    | n  | 2.4476 | 2.68 | 2. |

* 模擬結果圖:
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
