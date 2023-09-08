# MonteCarlo-Cache

### 簡介

* 優化蒙地卡羅模擬:
    * 在[蒙地卡羅章節中](../mc/)，我們知道會進行上千、上萬次的模擬，假設今天每一次模擬都需要花費1分鐘(這在暫態模擬很常見)，若要進行一萬次模擬，我們需要花費近7天時間...

    * 但你是否想過，這一萬次模擬中，重複抽樣到的模擬參數高達百次、千次，也就是說我們這一萬次模擬其實重複模擬同樣參數百次、千次，我們要避免這樣的情況，來達到**模擬時長的縮短**。

* **Cache** 概念:
    * 在 python 中可以使用 `@lru_cache` 記下每次呼叫 function 時所傳入的參數與計算結果
    * 我們每次模擬時，透過快取記下模擬參數與模擬結果，如果下次呼叫模擬 function 時，我們會判斷該模擬參數是否有出現過，如果有的話就不用再次模擬，而是直接從快取記憶中取得計算結果
    * 如下範例，由於模擬參數出現兩次1、2，因此透過快取可以省下兩次模擬次數
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

### 範例

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
