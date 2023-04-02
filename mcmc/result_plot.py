import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import lib.Voronoi_tessellation as vt

prior_mass_flux = pd.read_excel('..\\excel\\Prior_qc_V3D_randomField.xlsx')['mass_flux']

posterior_v1 = pd.read_excel('..\\excel\\Posterior_qc_V3D_randomField.xlsx')['mass_flux']

posterior_v1_2 = pd.read_excel('..\\excel\\Posterior_qc_v2-2.xlsx')['mass_flux']

true_v1_file = pd.read_excel('..\\excel\\Obs_conc_V3D_RandomField.xlsx')
vor_area = vt.voronoi(true_v1_file)
c = true_v1_file['MINIT']
true_v1 = 0
doc.startSimulator()
for i, node in enumerate(vor_area):
    true_v1 += doc.getResultsXVelocityValue(int(node)-1)*c[i]*365*1e-3*vor_area[int(node)]
doc.stopSimulator()
import ifm
import sys
def get_fem_file(file):
    sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
    global doc
    doc = ifm.loadDocument(file)
get_fem_file('..\\fem\\Virtual_3D_InitialRF.fem')


true_v1 = true_v1/1000

sns.set()
plt.axvline(true_v1, color='red')
# plt.axvline(0.00966, color='blue')
sns.distplot(prior_mass_flux, label='prior', color='dodgerblue', hist=False, kde_kws={'linewidth':4})
sns.distplot(posterior_v1, label='posterior', color='coral', hist=False, kde_kws={'linewidth':4})
# sns.distplot(posterior_v1_2, label='15 sampling points', color='mediumorchid', hist=False, kde_kws={'linewidth':4})

plt.legend()
# plt.title('Case1-Mass flux')
plt.xlabel('mass flux(kg/(yr${⋅𝑚^2}$))', fontsize=15)
plt.show()
