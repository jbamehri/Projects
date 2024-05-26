# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 20:10:36 2024

@author: Andrew Ross 
@editor: Joud Bamehriz
"""

# A hash-tag/number-sign is how we start a comment--everything after it on the
# line of text is ignored by Python and/or R.

# Any cell that doesn't start with %%R is using Python.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from numpy.random import Generator, PCG64
from numpy.random import default_rng


#%matplotlib inline

# from https://colab.research.google.com/drive/1wqIUyStkKbUc4MYPvJgIExPOFvC5cUs2
# Output in high quality.

# Set the figure format to 'retina'
#matplotlib.rcParams['figure.figsize'] = [8,8] # [width, height] in inches

plt.rcParams['figure.dpi'] = 200  # Set your desired DPI for retina display
plt.rcParams['figure.figsize'] = [15,15] # [width, height]
# Now, when you generate plots with matplotlib, they will be optimized for retina displays

#%config InlineBackend.figure_format='retina'

# https://stackoverflow.com/questions/36367986/how-to-make-inline-plots-in-jupyter-notebook-larger

# Whichever of these is last (and not commented out) is the one that determines
# what data gets used.

# MAVEN is a NASA satellite orbiting Mars, collecting data on ion densities in the upper atmosphere, and other things.
url = "https://lasp.colorado.edu/maven/sdc/public/data/sci/ngi/l2/2023/11/mvn_ngi_l2_csn-abund-53326_20231101T015946_v08_r03.csv"
url = "https://emunix.emich.edu/~aross15/math319/mars_maven_2017-11-28T07.txt"
dataname="Mars MAVEN"

# Actually read the data from the URL:
# Assuming 'url' contains the URL of the CSV file you want to read
df = pd.read_csv(url, comment='#', sep=None, engine='python')
#df = pd.read_csv(url,comment='#',sep=None) # df stands for dataframe.
# pd.read_csv means use the read_csv function from the pandas library,
# which we said above we would refer to as pd.
# We might say sep=',' or sep=';' for what separates the columns,
# but if we say sep=None it will try to figure out what the separator is
# automatically.

print("what 'type' is df?")
print(type(df))
print("that's what 'type' it is.")

df.head() # show the first few lines of the dataframe

if dataname=="Mars MAVEN":
  df['lnAbundance']=np.log(df['abundance']) # numpy's log is Ln; use log10 if you want base 10.
  df = df.replace({-np.inf: np.nan})
  df.plot(kind="scatter",x="alt",y="lnAbundance")

if dataname=="Mars MAVEN":
  print(df['lnAbundance'])
  
if dataname=="Mars MAVEN":
  df.plot(kind="scatter",x="alt",y="abundance")
'''
sm=pd.plotting.scatter_matrix(df,diagonal='hist')

import seaborn as sns

if dataname=="Mars MAVEN":
  sns.pairplot(df, hue="orbit")
  #sns.pairplot(df)

'''
import statsmodels.api as sm
from scipy import stats # used for stats.zscore
# The next line lets us use "formulas" in regression, like "y ~ x" or "Price ~ SquareFeet".
from statsmodels.formula.api import ols # "ols" stands for "Ordinary Least Squares"
import matplotlib.pyplot as plt

from numpy.random import Generator, PCG64
from numpy.random import default_rng

# MAVEN is a NASA satellite orbiting Mars, collecting data on ion densities in the upper atmosphere, and other things.
url = "https://lasp.colorado.edu/maven/sdc/public/data/sci/ngi/l2/2023/11/mvn_ngi_l2_csn-abund-53326_20231101T015946_v08_r03.csv"
url = "https://emunix.emich.edu/~aross15/math319/mars_maven_2017-11-28T07.txt"
dataname="Mars MAVEN"
regress_formula='lnAbundance ~ alt'
regress_formula2='lnAbundance ~ alt + lat'
regress_formula3='lnAbundance ~ alt + lat + long'
regress_formula4='lnAbundance ~ alt + lat + long + lst + sza'
regress_formula5='lnAbundance ~ alt + lat + long + sza'


# and here's where we actually read the data file from the URL:
mysep='\t' # tab as a separator
df = pd.read_csv(url,comment="#",sep=mysep)

if dataname=="Mars MAVEN":
  df['lnAbundance']=np.log(df['abundance']) # numpy's log is Ln; use log10 if you want base 10.
  df['delta_t'] = df['t_unix'].diff()
  df['prev1_abundance']=df['abundance'].shift(periods=1)
  df['prev2_abundance']=df['abundance'].shift(periods=2)
  df['prev1_lnAbundance']=df['lnAbundance'].shift(periods=1)
  df['prev2_lnAbundance']=df['lnAbundance'].shift(periods=2)

  df = df.replace({-np.inf: np.nan})
  print(df.columns)

#model only using altitude
print("Regression formula that we're using:")
print(regress_formula)
model1 = ols(formula=regress_formula, data=df)
results1 = model1.fit()
print(results1.summary())
RMSE = np.sqrt(results1.mse_resid)
print(f"RMSE is : {RMSE}" ) 


#model using alt and latitude 
print("Regression formula that we're using:")
print(regress_formula2)
model2 = ols(formula=regress_formula2, data=df)
results2 = model2.fit()
print(results2.summary())
RMSE = np.sqrt(results2.mse_resid)
print(f"RMSE is : {RMSE}" ) 


#model using alt and latitude and longitude
print("Regression formula that we're using:")
print(regress_formula3)
model3 = ols(formula=regress_formula3, data=df)
results3 = model3.fit()
print(results3.summary())
RMSE = np.sqrt(results3.mse_resid)
print(f"RMSE is : {RMSE}" ) 


#model using alt and latitude and longitude and sza
print("Regression formula that we're using:")
print(regress_formula4)
model4 = ols(formula=regress_formula4, data=df)
results4 = model4.fit()
print(results4.summary())
RMSE = np.sqrt(results4.mse_resid)
print(f"RMSE is : {RMSE}" ) 

 
# Write out the model explicitly using full-precision numbers.
# This is for human readability, not for use by later Python code.
def makemodelstring(results):
    modelstring = ""
    for ii in range(len(results.model.exog_names)):
      modelstring += f" + {results.params[ii]}"
      if results.model.exog_names[ii] != "Intercept":
        modelstring += " * " + results.model.exog_names[ii]
    return modelstring
tmp=np.array([results1.rsquared, results2.rsquared, results3.rsquared, results4.rsquared]).reshape(4,1)
print(f"R squared values array: {tmp}")
tmp=np.array([results1.rsquared_adj, results2.rsquared_adj, results3.rsquared_adj, results4.rsquared_adj]).reshape(4,1)
print(f"R squared adjusted values array: {tmp}")
modelstring = makemodelstring(results1)
print(f"model 1 equation is :{modelstring}") 
modelstring = makemodelstring(results2)
print(f"model 2 equation is :{modelstring}") 
modelstring = makemodelstring(results3)
print(f"model 3 equation is :{modelstring}") 
modelstring = makemodelstring(results4)
print(f"model 4 equation is :{modelstring}") 

# We'll define a function that will make a residual plot of whichever
# x variable we tell it. That way, we don't have to repeat all the
# plotting code each time.

def residplot(df,results,xvarnum, figsize=(4,3), marker="o", fillstyle="none", color="tab:blue", linestyle="none", label="Residuals"):
  # xvarnum should be in 1, 2, ... len(results.model.exog_names).
  # using xvarnum = 0 would usually try to use x=Intercept, but there probably isn't
  # a df["Intercept"], so you'll get an error.
  # Since a default is specified for figsize, marker, etc. you can leave them out
  # when you call the function.
  xname = results.model.exog_names[xvarnum]
  fig, ax = plt.subplots(figsize=figsize)
  ax.plot(df[xname], results1.resid, marker=marker,fillstyle=fillstyle,color=color, linestyle=linestyle, label=label)
  ax.set_xlabel(xname)
  ax.set_ylabel(results1.model.endog_names + " residuals")
  ax.set_title("residuals" )
  legend = ax.legend(loc="best")
  ax.axhline(color="k") # add a line at y=0 (by default) to be the x-axis
  return fig,ax

for ii in range(1,len(results4.model.exog_names)):
  fig, ax = residplot(df,results4,ii)
#plt.draw() # apparently we don't have to do this, it's already drawn.

whichvar = 1
sm.graphics.plot_regress_exog(results1, whichvar)


whichvar = 1
sm.graphics.plot_regress_exog(results2, whichvar)

whichvar = 1
sm.graphics.plot_regress_exog(results3, whichvar)

whichvar = 1
sm.graphics.plot_regress_exog(results4, whichvar)

def predvsresidplot(df,results,figsize=(4,3), marker="o", fillstyle="none", color="tab:blue", linestyle="none", label="residual"):
  # In other residual plots, we use just one of the x variables as the x axis.
  # It would be nice to combine all the x variables into one value, but how?
  # Actually, we have a way to do that: the model says the best way to combine
  # the x variables: using the coefficients, to get a predicted y value.
  # So, we plot x=predicted y value, y=actual y value.
  # We can look for things like: is there more variability at low vs high predicted values?
  # Since a default is specified for figsize, marker, etc. you can leave them out
  # when you call the function.
  fig, ax = plt.subplots(figsize=figsize)
  ax.plot(results.fittedvalues, results.resid, marker=marker,fillstyle=fillstyle,color=color, linestyle=linestyle, label=label)
  ax.set_xlabel("Predicted " + results.model.endog_names)
  ax.set_ylabel(results1.model.endog_names + " residual")
  ax.set_title(results4.model.formula)
  legend = ax.legend(loc="best")
  ax.axhline(color="k") # add a line at y=0 (by default) to be the x-axis
  return fig,ax

predvsresidplot(df,results4)

min_altitude_to_use = 0 # setting it to 0 will mean don't filter out anything.

# Write out the model info in a dictionary that will fit into a row of a dataframe.
def makemodeldict(results):
  modeldict = {'response':results.model.endog_names} # and then we'll add to that.
  for ii in range(len(results.model.exog_names)):
    modeldict[results.model.exog_names[ii]] = results.params[ii]
  modeldict['RMSE'] = np.sqrt(results.mse_resid)
  modeldict['nobs'] = results.nobs # number of observations
  modeldict['rsquared'] = results.rsquared
  modeldict['rsquared_adj'] = results.rsquared_adj
  return modeldict

orbit_list = list(df['orbit'].unique())
orbit_values = df['orbit'].values
alt_values = df['alt'].values

result_list = []
list_of_dicts = [] # for constructing our own dataframe
for orbit in orbit_list:
  print(f"orbit: {orbit}")
  mask = (orbit_values == orbit) & (alt_values >= min_altitude_to_use )
  df_one_orbit = df[mask]

  model_one_orbit = ols(formula=regress_formula4, data=df_one_orbit)
  results_one_orbit = model_one_orbit.fit()
  RMSE = np.sqrt(results_one_orbit.mse_resid)
  result_list.append(results_one_orbit)
  tmpdict=makemodeldict(results_one_orbit)
  tmpdict['orbit'] = orbit
  tmpdict['min_altitude_to_use'] = min_altitude_to_use
  list_of_dicts.append(tmpdict)
  print(results_one_orbit.summary())
  print(f"RMSE: {RMSE}") 
  modelstring = makemodelstring(results_one_orbit) 
  print(f"orbit {orbit} equation is :{modelstring}") 

