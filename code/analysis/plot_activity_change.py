import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as pl
import matplotlib.cm as cm
import os
import pickle
import pdb
import sys
sys.path.append(os.path.join(os.path.dirname(
    __file__), '..', 'striatal_model/'))
import params as p
import json
import matplotlib.pyplot as pl
from itertools import combinations
import itertools
import yaml
from pylab import *
import colors
from plot_tools2 import *
import copy
import seaborn as sbn
import pandas

colors.seaborn.set_context('paper', font_scale=5.0,
                           rc={"lines.linewidth": 1.5})
colors.seaborn.set_style('whitegrid', {"axes.linewidth": 1.5})

num_trials = 5

spikes_left_fn = sys.argv[1:num_trials+1]
spikes_right_fn = sys.argv[num_trials+1:2*num_trials+1]
channels_left_fn = sys.argv[2*num_trials+1:3*num_trials+1]
channels_right_fn = sys.argv[3*num_trials+1:4*num_trials+1]
experiment_fn = sys.argv[4*num_trials+1]
chng_out_fn = sys.argv[4*num_trials+2]


fig2 = pl.figure(figsize=[13, 16])
fig2.subplots_adjust(left=0.2)
t1 = fig2.add_subplot(111)
t11 = t1.twinx()

t1.grid(False)
t11.grid(False)


for trial in range(num_trials):
    # spike data of the channels
    data_left = np.loadtxt(spikes_left_fn[trial])
    senders_left = data_left[:, 0]
    unique_senders_left = np.unique(senders_left)  # all active senders
    times_left = data_left[:, 1]
    
    with open(channels_left_fn[trial], "r+") as f:
        channels_left = json.load(f)
        channels_left = channels_left['channels']
    
    
    data_right = np.loadtxt(spikes_right_fn[trial])
    senders_right = data_right[:, 0]
    unique_senders_right = np.unique(senders_right)  # all active senders
    times_right = data_right[:, 1]
    
    with open(channels_right_fn[trial], "r+") as f:
        channels_right = json.load(f)
        channels_right = channels_right['channels']
    
    
    with open(experiment_fn, "r+") as f:
        cfg = yaml.load(f)
    
    
    stim_times_start_left, stim_times_stop_left = get_stim_times(
        cfg, "left", params, mask=False, scale=1.)
    stim_times_start_right, stim_times_stop_right = get_stim_times(
        cfg, "right", params, mask=False, scale=1.)
    stim_times_left = zip(stim_times_start_left / 1000.,
                          stim_times_stop_left / 1000.)
    stim_times_right = zip(stim_times_start_right / 1000.,
                           stim_times_stop_right / 1000.)
    
    
    d1ActLeftip = []
    d1ActLeftwoip = []
    d1ActRightip = []
    d1ActRightwoip = []
    
    d2ActLeftip = []
    d2ActLeftwoip = []
    d2ActRightip = []
    d2ActRightwoip = []
    
    global_activity_left_ip_D1 = []
    global_activity_left_ip_D2 = []
    global_activity_right_ip_D1 = []
    global_activity_right_ip_D2 = []

    global_activity_left_woip_D1 = []
    global_activity_left_woip_D2 = []
    global_activity_right_woip_D1 = []
    global_activity_right_woip_D2 = []
    
    hists = []
    binsize = 200.
    binning = np.arange(0, p.runtime, binsize)
    
    all_d1_spikes = np.array([])
    all_d2_spikes = np.array([])
    
    hemisphere_neuron_ids = dict()
    
    for hemis in ["left", "right"]:
        if hemis == "left":
            hemisphere_neuron_ids["channels"] = copy.deepcopy(channels_left)
        else:
            hemisphere_neuron_ids["channels"] = copy.deepcopy(channels_right)

        for i, channel in enumerate(hemisphere_neuron_ids['channels']):
            if hemis == "left" and channel["row"] == 3 and channel["col"] == 4:
                # D1
                channel_n_ids = channel['d1']
                channel_spike_data = np.array([])
    
                # get spikes for this channel
                mask = np.hstack([np.where(n_id == senders_left)[0]
                                  for n_id in channel_n_ids])
                channel_spike_senders = senders_left[mask]
                channel_spike_times = times_left[mask]
                currStart = 500. # 500 ms to remove transients
                for start, stop in zip(stim_times_start_left, stim_times_stop_left):
                    currStop = start - 500.
                    rated1ip = len(channel_spike_times[np.logical_and(channel_spike_times >= start,
                                                                      channel_spike_times <= stop)]) / (((stop - start) / 1000.) * len(channel_n_ids))
                    rated1woip = len(channel_spike_times[np.logical_and(channel_spike_times >= currStart,
                                                                        channel_spike_times <= currStop)]) / (((currStop - currStart) / 1000.) * len(channel_n_ids))
                    d1ActLeftip.append(rated1ip)
                    d1ActLeftwoip.append(rated1woip)
                    global_activity_left_ip_D1.append(rated1ip)
                    global_activity_left_woip_D1.append(rated1woip)
                    currStart = stop + 500.
    
                # D2
                channel_n_ids2 = channel['d2']
                channel_spike_data2 = np.array([])
    
                # get spikes for this channel
                mask = np.hstack([np.where(n_id == senders_left)[0]
                                  for n_id in channel_n_ids2])
                channel_spike_senders2 = senders_left[mask]
                channel_spike_times2 = times_left[mask]
                currStart = 500. # 500 ms to remove transients
                for start, stop in zip(stim_times_start_left, stim_times_stop_left):
                    currStop = start - 500.
                    rated2ip = len(channel_spike_times2[np.logical_and(channel_spike_times2 >= start,
                                                                       channel_spike_times2 <= stop)]) / (((stop - start) / 1000.) * len(channel_n_ids2))
                    rated2woip = len(channel_spike_times2[np.logical_and(channel_spike_times2 >= currStart,
                                                                         channel_spike_times2 <= currStop)]) / (((currStop - currStart) / 1000.) * len(channel_n_ids))
                    d2ActLeftip.append(rated2ip)
                    d2ActLeftwoip.append(rated2woip)
                    global_activity_left_ip_D2.append(rated2ip)
                    global_activity_left_woip_D2.append(rated2woip)
                    currStart = stop + 500.
    
            elif hemis == "right" and channel["row"] == 3 and channel["col"] == 3:
                # D1
                channel_n_ids = channel['d1']
                channel_spike_data = np.array([])
    
                # get spikes for this channel
                mask = np.hstack([np.where(n_id == senders_right)[0]
                                  for n_id in channel_n_ids])
                channel_spike_senders = senders_right[mask]
                channel_spike_times = times_right[mask]
                currStart = 500. # 500 ms to remove transients
                for start, stop in zip(stim_times_start_right, stim_times_stop_right):
                    currStop = start - 500.
                    rated1ip = len(channel_spike_times[np.logical_and(channel_spike_times >= start,
                                                                      channel_spike_times <= stop)]) / (((stop - start) / 1000.) * len(channel_n_ids))
                    rated1woip = len(channel_spike_times[np.logical_and(channel_spike_times >= currStart,
                                                                        channel_spike_times <= currStop)]) / (((currStop - currStart) / 1000.) * len(channel_n_ids))
                    d1ActRightip.append(rated1ip)
                    d1ActRightwoip.append(rated1woip)
                    global_activity_right_ip_D1.append(rated1ip)
                    global_activity_right_woip_D1.append(rated1woip)
                    currStart = stop + 500.
    
                # D2
                channel_n_ids2 = channel['d2']
                channel_spike_data2 = np.array([])
    
                # get spikes for this channel
                mask = np.hstack([np.where(n_id == senders_right)[0]
                                  for n_id in channel_n_ids2])
                channel_spike_senders2 = senders_right[mask]
                channel_spike_times2 = times_right[mask]
                currStart = 500. # 500 ms to remove transients
                for start, stop in zip(stim_times_start_right, stim_times_stop_right):
                    currStop = start - 500.
                    rated2ip = len(channel_spike_times2[np.logical_and(channel_spike_times2 >= start,
                                                                       channel_spike_times2 <= stop)]) / (((stop - start) / 1000.) * len(channel_n_ids2))
                    rated2woip = len(channel_spike_times2[np.logical_and(channel_spike_times2 >= currStart,
                                                                         channel_spike_times2 <= currStop)]) / (((currStop - currStart) / 1000.) * len(channel_n_ids))
                    d2ActRightip.append(rated2ip)
                    d2ActRightwoip.append(rated2woip)
                    global_activity_right_ip_D2.append(rated2ip)
                    global_activity_right_woip_D2.append(rated2woip)
                    currStart = stop + 500.
    
    
    t1.plot(np.ones(len(d1ActLeftwoip)) * 0.9, d1ActLeftwoip,
            'o', color=colors.colors[0], markersize=15)
    t1.plot(np.ones(len(d1ActRightwoip)) * 0.9, d1ActRightwoip,
            's', color=colors.colors[0], markersize=15)
    t1.plot(np.ones(len(d1ActLeftip)) * 1.9, d1ActLeftip,
            'o', color=colors.colors[0], markersize=15)
    t1.plot(np.ones(len(d1ActRightip)) * 1.9, d1ActRightip,
            's', color=colors.colors[0], markersize=15)
   
    for woip, ip in zip(d1ActLeftwoip, d1ActLeftip):
        t1.plot([0.9, 1.9], [woip, ip], '-', color=colors.colors[0], linewidth=3.0)
    for woip, ip in zip(d1ActRightwoip, d1ActRightip):
        t1.plot([0.9, 1.9], [woip, ip], '--', color=colors.colors[0], linewidth=3.0)

    
    t1.set_xticks([1, 2])
    t1.set_xticklabels(['No Stimulation', 'Stimulation'],
                       fontweight='bold')
    t1.set_ylabel("Firing rate (spks/s)", fontweight='bold')
    t1.set_xlim(0.5, 2.5)


    for x in t1.get_yticklabels():
        x.set_fontweight('bold')


    t11.plot(np.ones(len(d2ActLeftwoip)) * 1.1, d2ActLeftwoip,
            'o', color=colors.colors[1], markersize=15)
    t11.plot(np.ones(len(d2ActRightwoip)) * 1.1, d2ActRightwoip,
            's', color=colors.colors[1], markersize=15)
    t11.plot(np.ones(len(d2ActLeftip)) * 2.1, d2ActLeftip,
            'o', color=colors.colors[1], markersize=15)
    t11.plot(np.ones(len(d2ActRightip)) * 2.1, d2ActRightip,
            's', color=colors.colors[1], markersize=15)
     
   
    for woip, ip in zip(d2ActLeftwoip, d2ActLeftip):
        t11.plot([1.1, 2.1], [woip, ip], '-', color=colors.colors[1], linewidth=3.0)
    for woip, ip in zip(d2ActRightwoip, d2ActRightip):
        t11.plot([1.1, 2.1], [woip, ip], '--', color=colors.colors[1], linewidth=3.0)

    
    t11.set_xlim(0.5, 2.5)
    
    t11.tick_params(axis='y', colors=colors.colors[1])

    for x in t1.get_yticklabels():
        x.set_fontweight('bold')

fig2.savefig(chng_out_fn)


