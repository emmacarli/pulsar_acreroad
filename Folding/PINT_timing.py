
from pint import models, toa, residuals, fitter
from astropy import units
import matplotlib.pyplot as plt
from astropy.visualization import quantity_support
import numpy as np

#%%Generate model
model = models.model_builder.get_model('B0329+54.par')
#this parameter file's data was obtained from ATNF

#%%Load in TOAs
SNR_cutoff=5
TOAs = toa.get_TOAs('TEMPO_TOAs.txt', planets=True)
FFTFIT_results = np.genfromtxt('FFTFIT_results.txt')
SNRs = FFTFIT_results[:,2] #load the folded profiles' SNRs
SNRs = np.ma.masked_where(SNRs<SNR_cutoff, SNRs)

#selection =  TOAs.get_errors() < 650 * units.us

TOAs.select(~SNRs.mask)
TOAs.print_summary()

#%%Pre-fit residuals

#Calculate them
prefit_residuals = residuals.Residuals(TOAs, model)

#can plot different correction delays added here


# Plot them
fig1 = plt.figure()
ax1 = plt.gca()
ax1.errorbar(
    TOAs.get_mjds().value,
    prefit_residuals.time_resids.to(units.us),
    yerr=TOAs.get_errors().to(units.us),
    fmt=".", color='black')
ax1.set_title("%s Pre-fit Timing Residuals" % model.PSR.value)
ax1.set_xlabel("MJD")
ax1.set_ylabel("Residual ($\mu$s)")
plt.savefig('Pre_fit_residuals.pdf') 
plt.close()


#%%Post-fit residuals

#Perform the fit
WLS_fit = fitter.WLSFitter(TOAs, model)
WLS_fit.set_fitparams('F0','F1','F2')
WLS_fit.fit_toas()






fig2 = plt.figure()
ax2 = plt.gca()
#Plot the post-fit residuals
ax2.errorbar(TOAs.get_mjds().value, WLS_fit.resids.time_resids.to(units.us), yerr=TOAs.get_errors().to(units.us), fmt='.', color='black')
ax2.set_title("%s Post-Fit Timing Residuals" % model.PSR.value)
ax2.set_xlabel("MJD")
ax2.set_ylabel("Residual ($\mu$s)")
plt.savefig('Post_fit_residuals.pdf') 
plt.close()

