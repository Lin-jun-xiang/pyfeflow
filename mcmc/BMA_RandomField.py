# For Demo case (heterogeneous, random field)
import lib.Mc_module as MC
import numpy as np
import pandas as pd
import time
import lib.Voronoi_tessellation as Voronoi_tessellation
import lib.RandomField as RF
import xlsxwriter

def getPositiondata(eleFile):
    """
    Get coordinates of "elements" from fem file, then
    return the pos for random field generator
    """
    if dimensionalProb == 3:
        pos = (eleFile["X"], eleFile["Y"], eleFile["Z"])
    if dimensionalProb == 2:
        pos = (eleFile["X"], eleFile["Y"])

    return pos

def prior_ensemble():
    prior_gs_mean, prior_gs_var, prior_gs_ls = [], [], []
    realizations = []
    prior = {"concentraion":[], "mass_flux":[]}
    for i in range(nRealizations):
        # Only take rd_mean in prior
        prior_gs_mean.append(rfg.gs_meanDistr()[0])
        prior_gs_var.append(rfg.gs_varDistr())
        prior_gs_ls.append(rfg.gs_lenScaleDistr())
        realizations.append(rfg.uncondFieldGenerator(pos,
                                                     prior_gs_mean[i],
                                                     prior_gs_var[i],
                                                     prior_gs_ls[i]))

        MC.set_ifm_K(K_zone, realizations[i])
        sim_result = MC.get_sim_data(obs_nodes, area=voronoi_area)
        prior["concentraion"].append(sim_result["concentraion"])
        prior["mass_flux"].append(sim_result["mass_flux"])
        print('prior-', i+1)

    return prior

def create_markov_chain(n):
    chain = []
    # Initialize the uncertainty parameters by sampling from proposal distr
    # Notice the gs_var and gs_lenScale which itself is uniform distr (eg proposal distr)
    chain.append([MC.gs_mean_proposal_distribution(),
                 rfg.gs_varDistr(),
                 rfg.gs_lenScaleDistr()])

    rejection_rate = 0

    covMatrix = MC.covariance_matrix(n_obs=len(obs_data))

    posterior = {"concentraion":[], "mass_flux":[]}
    for t in range(n-1):
        theta_cur = chain[-1]
        realization_cur = rfg.uncondFieldGenerator(pos,
                                                   theta_cur[0],
                                                   theta_cur[1],
                                                   theta_cur[2])
        likelihood_cur = MC.likelihood_calculate(obs_data,
                                                 obs_nodes,
                                                 K_zone,
                                                 realization_cur,
                                                 covMatrix,
                                                 area=voronoi_area,
                                                 MultiSpecies=multiSpecies)

        theta_star = [MC.gs_mean_proposal_distribution(),
                      rfg.gs_varDistr(),
                      rfg.gs_lenScaleDistr()]
        realization_star = rfg.uncondFieldGenerator(pos,
                                                    theta_star[0],
                                                    theta_star[1],
                                                    theta_star[2])
        likelihood_star = MC.likelihood_calculate(obs_data,
                                                  obs_nodes,
                                                  K_zone,
                                                  realization_star,
                                                  covMatrix,
                                                  area=voronoi_area,
                                                  MultiSpecies=multiSpecies)

        u = np.random.uniform(size=1)[0]

        acceptance_rate = min(1, likelihood_star['likelihood']*MC.gs_parameters_target_distribution(theta_star)*MC.proposal_calculate(theta_cur, theta_star)/\
            MC.gs_parameters_target_distribution(theta_cur)/MC.proposal_calculate(theta_star, theta_cur)/likelihood_cur['likelihood'])

        if u <= acceptance_rate:
            chain.append(theta_star)
            posterior["concentraion"].append(likelihood_star['sim_data']["concentraion"])
            posterior["mass_flux"].append(likelihood_star['sim_data']["mass_flux"])
        else:
            chain.append(theta_cur)
            posterior["concentraion"].append(likelihood_cur['sim_data']["concentraion"])
            posterior["mass_flux"].append(likelihood_cur['sim_data']["mass_flux"])
            # If rejection_rate too big, can adjust the "u"
            rejection_rate += 1
        print('chain-', t+1)

    return {'chain':chain, 'posterior':posterior, 'rejection':rejection_rate/(n-1)}

def getFileName():
    fem_file = "..\\fem\\Virtual_3D_InitialRF.fem"
    ele_file = "..\\excel\\Virtual2D_RF.xlsx"
    obs_data = "..\\excel\\Obs_conc_Virtual2D_RandomField.xlsx"

    return fem_file, ele_file, obs_data

def conc_writter(conc_data, ensembleType, multiSpecies=True):
    """
    Write the concentration result for each observation node
    1. For MultiSpcecies: will create multiple worksheet
    2. For SingleSpecies: only create one worksheet
    """
    output_file = f"C:\\JunXiang\\Python\\Excel_py\\{ensembleType}_ConcResults.xlsx"

    if multiSpecies:
        writer = xlsxwriter.Workbook(output_file)
        multiSpecies_info = MC.get_MultiSpecies_Info()["species_id"]

        for species in multiSpecies_info:
            worksheet = writer.add_worksheet(species)
            worksheet.write(0, 0, "Realizations")

            for c, node in enumerate(conc_data[i][species]):
                worksheet.write(0, c+1, f"Obs_{node}")
                for i in range(len(conc_data)):
                    worksheet.write(i+1, c+1, conc_data[i][species][node])
        writer.close()
    else:
        df = pd.DataFrame(conc_data)
        df.to_excel(output_file, index=False)

def massFlux_writter(massFlux_data, ensembleType):
    """
    Write the mass flux result for each Species (Multi or Single)
    """
    output_file = f"C:\\JunXiang\\Python\\Excel_py\\{ensembleType}_MassFluxResults.xlsx"

    df = pd.DataFrame(massFlux_data)
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    time_start = time.time()

    dimensionalProb = 3

    # If multiSpecies:
    # 1. The FEFLOW should setting more than 1 species
    # 2. The algorithm will get the concentration and mass flux for each species
    # 3. But cannot consider the multispecies in the "calculate likelihood" (TO DO)
    multiSpecies = True

    filename = getFileName()

    # TO DO : Get the FEFLOW fem file
    MC.get_fem_file(filename[0])

    K_zone = [e+1 for e in range(MC.doc.getNumberOfElements())]

    # Get the coordinates of element from FEFLOW
    eleFile = pd.read_excel(filename[1])
    pos = getPositiondata(eleFile)

    # Get the concentration of observation data
    obs_data = MC.get_obs_data(filename[2])

    obs_nodes = list(obs_data.keys())

    voronoi_area = Voronoi_tessellation.voronoi(obs_data=pd.read_excel(filename[2]))
    control_plane_area = 1000

    nRealizations = 100

    # Get initialize concentration field, for monte carlo simulation
    MC.get_initialize_concField(multiSpecies)

    rfg = RF.RandomFieldGenerator()

    prior = prior_ensemble()

    markov_chain = create_markov_chain(n=nRealizations)
    burn_in_period = 0

    posterior = markov_chain['posterior'][burn_in_period-1:]

    time_end = time.time()

    print('rejection rate=', markov_chain['rejection'])
    print('time=', time_end-time_start)

    # Write concentration data
    conc_writter(prior["concentration"], ensembleType="Prior", multiSpecies=multiSpecies)
    conc_writter(posterior["concetraion"], ensembleType="Posterior", multiSpecies=multiSpecies)

    # Write mass flux data
    massFlux_writter(prior["mass_flu"], ensembleType="Prior")
    massFlux_writter(posterior["mass_flux"], ensembleType="Posterior")
    import winsound
    winsound.PlaySound('SystemHand', winsound.SND_ALIAS)
