import pandas as pd
import xml.etree.ElementTree as ET
import ifm
import sys
from scipy import stats
import numpy as np

def get_fem_file(file):
    sys.path.append("C:\\Program Files\\DHI\\2020\\FEFLOW 7.3\\bin64")
    global doc
    doc = ifm.loadDocument(file)

def get_well_index(xml_file):
    """
    get well sampling data index including K, head, qc from xml file
    return index of elements "or" nodes
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    obs_index = []
    for child in root:
        obs_index.append(child.attrib['end'])

    return obs_index

def get_obs_data(obs_data_filepath):
    """
    return "true" data on sampling(observation)
    """
    obs_data = {}

    well_data = pd.read_excel(obs_data_filepath)
    for i in range(len(well_data)):
        obs_data[well_data['Node'][i]] = well_data['MINIT'][i]

    return obs_data

def get_MultiSpecies_Info():
    """
    1. Get the MultiSpecies "name" and "id" in FEFLOW by IFM
    2. Initialize the concentraion hash table for multiSpecies
    """
    concentration = {}
    species_id = {}

    num_species = doc.getNumberOfSpecies()
    if num_species >= 2:
        # if not, cannot call doc.getSpeciesName
        species_name = [doc.getSpeciesName(i) for i in num_species]
        for i, name in enumerate(species_name):
            if name not in concentration:
                concentration[name] = {}
                species_id[name] = i

    return {"concentration" : concentration, "species_id" : species_id}

def get_sim_data(nodes, area, control_plane_area=1000, MultiSpecies=True):
    """
    Parameters
    ----------
    nodes : the nodes which located in the Observation point
    area : the voronoi area of each node

    Darcy flux - [m/d] to [m/yr] ; Concentration - [mg/l] to [kg/m^3] ; Area - [m^2]
    Mass discharge = [(Darcy flux)*365] * [(Concentration)*1e-3] * [(Area)] which unit is [kg/yr]
    return "simulated" data (mass concentration, darcy flux, mass discharge)
    """
    concentration = {}
    mass_flux = {}

    initialize_results(MultiSpecies)

    doc.startSimulator()

    if MultiSpecies:
        MultiSpecies_Info = get_MultiSpecies_Info()
        concentration = MultiSpecies_Info["concentration"]
        species_id = MultiSpecies_Info["species_id"]

        for species in species_id:
            doc.setMultiSpeciesId(species_id[species])
            mass_flux[species] = {}

            for node in nodes:
                concentration[species][int(node)] = doc.getResultsTransportMassValue(int(node)-1)
                darcy_flux = doc.getResultsXVelocityValue(int(node)-1)
                mass_flux[species][int(node)] = darcy_flux * concentration[species][int(node)] * area[int(node)] * 365 * 1e-3
            mass_flux[species] = sum([v for v in mass_flux[species].values()])
            mass_flux[species] = mass_flux[species] / control_plane_area
    else:
        for node in nodes:
            concentration[int(node)] = doc.getResultsTransportMassValue(int(node)-1)
            mass_flux[int(node)] = doc.getResultsXVelocityValue(int(node)-1) * concentration[int(node)] * area[int(node)] * 365 * 1e-3
        mass_flux = sum([v for v in mass_flux.values()])
        mass_flux = mass_flux / control_plane_area

    doc.stopSimulator()

    return {'concentration':concentration, 'mass_flux':mass_flux}

def set_ifm_K(zone_elements, theta_K):
    """
    Set conductivity(X=Y=10*Z) in each element; units - "m/d"
    Input conductivity units is "m/s", need to convert to "m/d"
    """
    if type(theta_K) == float:
        # Homogeneous case
        theta_K = theta_K * 24 * 3600

        for element in zone_elements:
            doc.setMatXConductivityValue3D(int(element)-1, theta_K)
            doc.setMatYConductivityValue3D(int(element)-1, theta_K)
            doc.setMatZConductivityValue3D(int(element)-1, theta_K*0.1)
    else:
        # Heterogeneou case
        for i in range(len(zone_elements)):
            doc.setMatXConductivityValue3D(int(zone_elements[i])-1, theta_K[i] * 24 * 3600)
            doc.setMatYConductivityValue3D(int(zone_elements[i])-1, theta_K[i] * 24 * 3600)
            doc.setMatZConductivityValue3D(int(zone_elements[i])-1, theta_K[i] * 24 * 3600 * 0.1)

def get_initialize_concField(MultiSpecies):
    """
    Get the initialization concentration field.
    """
    global init_concField

    if MultiSpecies:
        init_concField = {}
        for i in range(doc.getNumberOfSpecies()):
            # Convert the species type, then get the concentration fo species
            doc.setMultiSpeciesId(i)
            init_concField[i] = []
            for node in range(doc.getNumberOfNodes()):
                init_concField[i].append(doc.getResultsTransportMassValue(node))
    else:
        init_concField = []
        for node in range(doc.getNumberOfNodes()):
            init_concField.append(doc.getResultsTransportMassValue(node))

def initialize_results(MultiSpecies):
    """
    For transport simulation, need to initialize 'concentration' for avoid concentration accumulation.
    """
    if MultiSpecies:
        for i in range(doc.getNumberOfSpecies()):
            doc.setMultiSpeciesId(i)
            [doc.setResultsTransportMassValue(node, init_concField[i][node]) for node in range(doc.getNumberOfNodes())]
    else:
        [doc.setResultsTransportMassValue(node, init_concField[node]) for node in range(doc.getNumberOfNodes())]

def covariance_matrix(n_obs, r=0.8, sigma=0.01):
    """
    Hyper-parameters: r, sigma. (reference: Bodin et al.,2012； Zheng et al.,2016)
    return the covariance matrix of data noise.
    """
    covMatrix = np.array([[1.0]*n_obs]*n_obs) # initialize

    for i in range(len(covMatrix)):
        for j in range(len(covMatrix)):
            covMatrix[i][j] = r**(abs(i-j))

    return sigma*covMatrix

def likelihood_calculate(obs_data, nodes, K_zone, theta, covMatrix, area, target='concentration', MultiSpecies=True):
    """
    P(D|theta) = 1/((2π)^(N/2)*|C|^(1/2))*exp⁡((-1/2)*(d-f(θ))^T C^(-1) (d-f(θ))). (reference: Bodin et al.,2012； Zheng et al.,2016)
    left = 1/((2π)^(N/2)*|C|^(1/2))
    right = exp⁡((-1/2)*(d-f(θ))^T C^(-1) (d-f(θ)))
    return-1 P(D|theta) which is a value
    return-2 dictionary of simulate data(ex:concentration)
    """
    set_ifm_K(K_zone, theta)

    sim_data = get_sim_data(nodes, area, MultiSpecies=MultiSpecies)

    residual = []
    if MultiSpecies:
        for node in obs_data:
            # In this case, just take the major species (PCE) for likelihoode calculate
            residual.append(obs_data[node] - sim_data[target][doc.getSpeciesName(0)][node])
    else:
        for node in obs_data:
            residual.append(obs_data[node] - sim_data[target][node])

    likelihood_left =  1/((2*3.14159)**len(obs_data)*np.linalg.det(covMatrix))**0.5
    likelihood_right = np.math.exp(-0.5*np.array(residual).dot(np.linalg.inv(covMatrix)).dot(np.array(residual)))

    return {'likelihood':likelihood_left*likelihood_right, 'sim_data':sim_data}

def k_target_distribution(theta, mu=1e-3, sigma=1e-3):
    """
    Calculate the "p(theta)" of conductivity
    Then call the function "joint_distribution", get
    the joint distribution of conductivity

    Parameters
    ----------
    Prior conductivity distribution ~ N(mu, sigma)

    Returns
    -------
    return a value which belong to the distr
    """
    return joint_distribution([stats.norm.pdf(np.math.log(theta_i), loc=np.math.log(mu**2/(mu**2+sigma**2)**0.5), scale=(np.math.log((sigma/mu)**2+1))**0.5) for theta_i in theta])

def gs_parameters_target_distribution(theta, mu=np.log(2e-5), sigma=0.3):
    """
    Calculate the "p(theta)" of gs_parameters
    Then call the function "joint_distribution", get
    the joint distribution of gs_parameters

    Parameters
    ----------
    Prior gs_mean distribution ~ N(mu, sigma)

    Prior gs_var distribution ~ Uniform(0.2, 5.)
    -> see the "RandomField.py (down and upper)"

    Prior gs_lenScale distribution ~ Uniform([8., 8., 1.], [50., 50., 4.])
    -> see the "RandomField.py (down and upper)"

    Returns
    -------
    p(gs_mean)*p(gs_var)*p(gs_lenScale_x)*p(gs_lenScale_y)*p(gs_lenScale_z)
    """
    p_gs_mean = stats.norm.pdf(theta[0], mu, sigma)
    p_gs_var = stats.uniform.pdf(theta[1], 0.2, 5.)
    p_gs_ls = stats.uniform.pdf(theta[2], [8., 8., 1.], [50., 50., 4.])

    p_theta = [p_gs_mean, p_gs_var]
    [p_theta.append(v) for v in p_gs_ls]

    return joint_distribution(p_theta)

def k_proposal_distribution(theta, s=1):
    """
    Calculate the "q(theta)" of conductivity
    """
    # return abs(stats.norm.rvs(loc=theta, scale=1e-4, size=s))
    return np.random.uniform(1e-6, 1e-3, size=2)

def gs_mean_proposal_distribution(mean=np.log(2e-5), var=0.3):
    """
    Calculate the "q(theta)" of gs_mean
    gs_mean is follow normal distribution ~ N(mean, var)

    Returns
    -------
    sampling from proposal distribution (uniform)
    """
    return np.random.uniform(mean-var, mean+var)

def proposal_calculate(target, condition):
    """
    Calculate the "q(theta_star|theta_cur)" or "q(theta_cur|theta_star)"

    Notice : if the theta_star and theta_cur is very close, then
             return high probability.

    Parameters
    ------
    target : theta_cur
    condition : theta_star

    """
    pp_res = 1

    for para_index in range(len(target)):
        pp_res *= joint_distribution(stats.norm.pdf(target[para_index], condition[para_index]))

    return pp_res

def joint_distribution(dist):
    """
    Math trick:
    Because of p(theta) is very small value, so
    use ln(p(theta)) to calculate firstly, avoid
    small value product small value.

    ln(results) = ln(P(x1)) + ln(P(x2)) +...
    return a value of joint distribution : P(x1)*P(x2)*...P(xn)
    """
    res = 0
    if isinstance(dist, list) or isinstance(dist, np.ndarray):
        for v in dist:
            if v != 0:
                res += np.math.log(v)
    else:
        if dist != 0:
            res += np.math.log(dist)

    return np.math.exp(res)
