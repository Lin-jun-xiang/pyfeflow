import ifm
import sys
from scipy import stats
import numpy as np
import seaborn as sns

sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
doc = ifm.loadDocument('YOUR_FEM_FILE')

# Hydraulic conductivity (K)
# K ~ log-normal-distribution
# mu: mean of K (m/s)
# sigma: standard deviation of K (m/s)
# Ref: https://en.wikipedia.org/wiki/Log-normal_distribution
mu, sigma = 1e-3, 1e-4
conductivity = stats.norm.rvs(loc=np.math.log(mu**2/(mu**2+sigma**2)**0.5), scale=np.math.log((sigma/mu)**2+1)**0.5, size=100)
sns.distplot(conductivity)

# Ifm getter : number of elements
elements = doc.getNumberOfElements()

velocityX = []
for c in conductivity:
    c = np.math.exp(c)
    c *= 24 * 3600

    for element in range(elements):
        # Ifm setter : set the random sample of K
        doc.setMatXConductivityValue3D(element, c)
        doc.setMatYConductivityValue3D(element, c)
        doc.setMatZConductivityValue3D(element, 0.1*c)

    doc.startSimulator()

    # Ifm getter : get the velocity value
    velocityX.append(doc.getResultsXVelocityValue(300))

    doc.stopSimulator()

# Visualization the monte carlo simulatiuon
sns.distplot(velocityX)
