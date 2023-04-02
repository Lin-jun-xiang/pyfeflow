import gstools as gs
import numpy as np
from scipy import stats

class RandomFieldGenerator:
    """
    Geostatistical Model for "sand"
    """
    @staticmethod
    def gs_meanDistr(mean : float = np.log(2e-5),
                     var : float = 0.3):
        """
        Geostatistical Model parameter - "mean"
        The "mean" follow normal distribution.

        Returns
        -------
        rd_mean : Random sampling "mean" from its distribution
        p_mean : pdf(x)

        """
        rd_mean = stats.norm.rvs(loc=mean, scale=var)

        p_mean = stats.norm.pdf(rd_mean, loc=mean, scale=var)

        return rd_mean, p_mean

    @staticmethod
    def gs_varDistr(upper : float = 5.,
                    down : float = 0.2):
        """
        Geostatistical Model parameter - "variance"
        The "variance" follow uniform distribution.

        In the standard form, the distribution is uniform on ``[0, 1]``. Using
        the parameters ``loc`` and ``scale``, one obtains the uniform distribution
        on ``[loc, loc + scale]``.

        Returns
        -------
        rd_var : Random sampling "variance" from its distribution
        """
        rd_var = stats.uniform.rvs(loc=down, scale=upper-down)

        return rd_var

    @staticmethod
    def gs_lenScaleDistr(down : list = [8., 8., 1.],
                         upper : list = [50., 50., 4.]):
        """
        Geostatistical Model parameter - "len scale"
        The "len scale" follow uniform distribution.

        In the standard form, the distribution is uniform on ``[0, 1]``. Using
        the parameters ``loc`` and ``scale``, one obtains the uniform distribution
        on ``[loc, loc + scale]``.

        Parameters
        ----------
        down : downer in uniform distribution for x, y, z
        upper : upper in uiform distribution for x, y, z

        Returns
        -------
        rd_ls (ndarray->x_ls, y_ls, z_ls): Random sampling "len_scale" from its distribution
        """ 
        rd_ls = stats.uniform.rvs(loc=down, scale=np.array(upper)-np.array(down))

        return rd_ls

    @staticmethod
    def uncondFieldGenerator(pos,
                             mean,
                             var,
                             len_scale):
        """
        After sampling gs parameters (eg:mean, var, len_scale), we
        can generate a hydraulic conductivity field now.
        """
        model = gs.Gaussian(dim=3, var=var, len_scale=len_scale)
        field = gs.SRF(model, mean=mean)

        realization = np.exp(field(pos, seed=np.random.randint(10000)))

        return realization
