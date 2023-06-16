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
