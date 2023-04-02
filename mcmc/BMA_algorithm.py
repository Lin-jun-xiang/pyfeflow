# For demo case (homogeneous conductivity)
import lib.Mc_module as MC
from scipy import stats
import numpy as np
import pandas as pd
import time
import lib.Voronoi_tessellation as Voronoi_tessellation

def prior_ensemble(mu=1e-3, sigma=1e-3):
    prior_theta_K1 = stats.norm.rvs(loc=np.math.log(mu**2/(mu**2+sigma**2)**0.5), scale=np.math.log((sigma/mu)**2+1)**0.5, size=1000)
    prior_theta_K2 = stats.norm.rvs(loc=np.math.log(mu**2/(mu**2+sigma**2)**0.5), scale=np.math.log((sigma/mu)**2+1)**0.5, size=1000)

    prior = []
    for i in range(len(prior_theta_K1)):
        MC.set_ifm_K(K1_zone_elements, np.math.exp(prior_theta_K1[i]))
        MC.set_ifm_K(K2_zone_elements, np.math.exp(prior_theta_K2[i]))
        prior.append(MC.get_sim_data(nodes, area=voronoi_area)[output_target])
        print('prior-', i+1)

    return prior

def create_markov_chain(n=1000):
    chain = []
    chain.append(MC.proposal_distribution(theta=1e-3, s=2))
    posterior = []
    rejection_rate = 0

    covMatrix = MC.covariance_matrix(n_obs=len(obs_data))

    for t in range(n-1):
        theta_cur = chain[-1]

        likelihood_cur = MC.likelihood_calculate(obs_data, nodes, K_zone, theta_cur, covMatrix, area=voronoi_area)

        theta_star = MC.proposal_distribution(theta=theta_cur, s=2)

        likelihood_star = MC.likelihood_calculate(obs_data, nodes, K_zone, theta_star, covMatrix, area=voronoi_area)

        u = np.random.uniform(size=1)[0]

        acceptance_rate = min(1, likelihood_star['likelihood']*MC.k_target_distribution(theta_star)*MC.proposal_calculate(theta_cur, theta_star)/\
            MC.k_target_distribution(theta_cur)/MC.proposal_calculate(theta_star, theta_cur)/likelihood_cur['likelihood'])
        # acceptance_rate = min(1, likelihood_star['likelihood']/likelihood_cur['likelihood'])

        if u <= acceptance_rate:
            chain.append(theta_star)
            posterior.append(likelihood_star['sim_data'][output_target])
        else:
            chain.append(theta_cur)
            posterior.append(likelihood_cur['sim_data'][output_target])
            rejection_rate += 1
        print('chain-', t+1)

    return {'chain':chain, 'posterior':posterior, 'rejection':rejection_rate/(n-1)}

if __name__ == "__main__":
    time_start = time.time()

    MC.get_fem_file('')

    K1_zone_elements = pd.read_excel('')['Element']
    K2_zone_elements = pd.read_excel('..\\excel\\K2_ele.xlsx')['Element']
    K_zone = [K1_zone_elements, K2_zone_elements]

    nodes = MC.get_well_index("..\\xml\\well_sampling2.xml")
    obs_data_file = '..\\excel\\Obs_conc_v1-2.xlsx'
    obs_data = MC.get_obs_data(obs_data_file)

    voronoi_area = Voronoi_tessellation.voronoi(obs_data=pd.read_excel(obs_data_file))
    control_plane_area = 1000

    output_target = 'mass_discharge'

    prior = prior_ensemble()

    markov_chain = create_markov_chain(1800)
    burn_in_period = 800

    posterior = markov_chain['posterior'][burn_in_period-1:]

    time_end = time.time()

    print('rejection rate=', markov_chain['rejection'])
    print('time=', time_end-time_start)
    pd.DataFrame(prior).to_excel('..\\excel\\Prior_qc_v1-2.xlsx')
    pd.DataFrame(posterior).to_excel('..\\excel\\Posterior_qc_v1-2.xlsx')
    
    import winsound
    winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
