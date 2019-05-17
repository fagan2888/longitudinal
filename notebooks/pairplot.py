#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 21:35:35 2019

@author: max
"""
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# aggregates multiple labs for every patient into a single 
# dataframe by an aggregation function of choice, such as median, mean, etc...
# takes in the name of the simulation files, reads the corresponding normal and 
# '_long' versions of the file, as well as the name of the aggregating function
#, which must be a function implemented by a pandas series object. Returns a 
# stationary dataframe containing patient demographic info as well as aggregated
# lab specific information.
def generate_stationary_dataframe(name, func_name):
    df = pd.read_csv(name + ".csv")
    df_long = pd.read_csv(name + "_long.csv")
    groups = df_long.groupby("id")

    exec("bmi_aggregate = [d[(d.name == 'bmi')]." + func_name + "()[-1] for _,d in groups]")
    exec("age_aggregate = [d[(d.name == 'age')]." + func_name + "()[-1] for _,d in groups]")
    exec("lab_aggregate = [d[(d.name == 'lab')]." + func_name + "()[-1] for _,d in groups]")
    
    df['bmi_aggregate'] = bmi_aggregate;
    df['age_aggregate'] = age_aggregate;
    df['lab_aggregate'] = lab_aggregate;
    df.drop(columns = ['id'], inplace=True)
    
    return df


# this function generates heatmap pairplots between previously computed lab 
# and demographic values (see last function) and the resulting classification
# from a provided simulation number. It takes in a dataframe containing information
# for each patient, as well as their classifier results. It also takes in a simulation
# number, used to identify the relevant simulation dataset, and the name of the aggregating
# function. It then generates the plots and saves them to an easy to navigate
# filepath. 
def generate_and_save_plots(data, sim_num, func_name):
    d = data
    f, ax = plt.subplots(figsize=(6, 6))
    cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
    sns.kdeplot(d.classification, d.bmi_aggregate, cmap=cmap, n_levels=60, shade=True)
    plt.savefig("figures/simulation" + str(sim_num) + "/bmi_aggregate=" + func_name + ".png")
    sns.kdeplot(d.classification, d.age_aggregate, cmap=cmap, n_levels=60, shade=True)
    plt.savefig("figures/simulation" + str(sim_num) + "/age_aggregate=" + func_name + ".png")
    sns.kdeplot(d.classification, d.lab_aggregate, cmap=cmap, n_levels=60, shade=True)
    plt.savefig("figures/simulation" + str(sim_num) + "/lab_aggregate=" + func_name + ".png")


#%%
filenames = ['d_lr_example_patients_bmi_slope-lab_max',
'd_lr_example_patients_bmi_slope-lab_median-age_max',
'd_lr_example_patients_bmi_slope-lab_slope',
'd_lr_example_patients_bmi_slope-lab_var',
'd_lr_example_patients_bmi_slope',
'd_lr_example_patients_lab_max',
'd_lr_example_patients_lab_min',
'd_lr_example_patients_lab_var']

func_name = "median"
for sim_num in range(len(filenames)):
    name = filenames[sim_num]
    
    data = generate_stationary_dataframe(name, func_name)
    generate_and_save_plots(data, sim_num, func_name)





#%%
#df = pd.concat([df, df_long], axis = 1)
#df.drop(columns = ['id'], inplace=True)
#print(df)
#plot = sns.pairplot(data = df[['classification, race, sex']])
#plot = sns.pairplot(data = df)
#%%
d = data
f, ax = plt.subplots(figsize=(6, 6))
cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
sns.kdeplot(d.classification, d.bmi_aggregate, cmap=cmap, n_levels=60, shade=True)
plt.savefig("figures/simulation" + str(sim_num) + "/bmi_aggregate=" + func_name + ".png")
sns.kdeplot(d.classification, d.age_aggregate, cmap=cmap, n_levels=60, shade=True)
plt.savefig("figures/simulation" + str(sim_num) + "/age_aggregate=" + func_name + ".png")
sns.kdeplot(d.classification, d.lab_aggregate, cmap=cmap, n_levels=60, shade=True)
plt.savefig("figures/simulation" + str(sim_num) + "/lab_aggregate=" + func_name + ".png")



#%%
g = sns.PairGrid(df)
g = g.map_upper(plt.scatter)
g = g.map_lower(sns.kdeplot, cmap="hot",shade=True)
g = g.map_diag(plt.hist)
sns.plt.show()