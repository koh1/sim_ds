import pymongo
import pandas as pd
import numpy as np


import matplotlib as mpl
mpl.use('Agg')
import pylab


def show_plot(xdf, ydf, path):
    fig, ax = mpl.pyplot.subplots()
    ax.plot(xdf, ydf)
    mpl.pyplot.savefig(path)

def show_bar(df):
    width = 1
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    ax.bar(ind, df['mean'], width, color='r')
    ax.set_ylabel('mean traffic on sw [bps]')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(df['name'])

    mpl.pyplot.savefig("sample.png", dpi=300)

def show_bar(df, out_file):
    width = 1
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    ax.bar(ind, df['mean'], width, color='r')
    ax.set_ylabel('mean traffic on sw [bps]')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(df['name'])

    mpl.pyplot.savefig(out_file, dpi=300)

def show_bar_by_layer(df, out_file, ylim):
    width = 0.8
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
#    rects1 = ax.bar(ind, df['mean'], color='b', align="center")
    rects1 = ax.bar(ind, df['mean'], width, color='b', align="center")
    ax.set_ylabel('mean traffic by layer [bps]')
    ax.set_xticks(ind)
    ax.set_xticklabels(df['layer'])
    ax.grid(True)
    if not ylim == None:
        ax.set_ylim(0, int(ylim))
    autolabel(rects1, ax)
#    mpl.pyplot.savefig(out_file, dpi=300)    
    mpl.pyplot.savefig(out_file, bbox_inches='tight')    

def show_bar_peak_by_layer(df, out_file, ylim):
    width = 0.8
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    rects1 = ax.bar(ind, df['max'], width, color='g', align="center")
    ax.set_ylabel('peak traffic by layer [bps]')
    ax.set_xticks(ind)
    ax.set_xticklabels(df['layer'])
    ax.grid(True)
    if not ylim == None:
        ax.set_ylim(0, int(ylim))
    autolabel(rects1, ax)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')    

def show_bar_planning_time(df, out_file):
    width = 0.25
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    rects1 = ax.bar(ind, df['step1_mean_ms'], width, color='b')
    rects2 = ax.bar(ind+width, df['step2_mean_ms'], width, color='y')
    rects3 = ax.bar(ind+width*2, (df['step1_mean_ms'] + df['step2_mean_ms']), width, color='r')
    ax.set_ylabel('planning time [ms]')
    ax.set_xticks(ind+0.35)
    ax.set_xticklabels(df['time'])
    ax.set_xlabel('time [sim_step]')
    ax.grid(True)
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('step1', 'step2', 'total'), loc='best' )
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')

def show_bar_pacing_delay(df, out_file):
    width = 0.25
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    rects1 = ax.bar(ind, df['pacing_delay_min_ms'], width, color='y')
    rects2 = ax.bar(ind+width, df['pacing_delay_max_ms'], width, color='r')
    rects3 = ax.bar(ind+width*2, df['pacing_delay_mean_ms'], width, color='c')
    ax.set_ylabel('pacing delay [ms]')
    ax.set_xticks(ind+0.35)
    ax.set_xticklabels(df['time'])
    ax.set_xlabel('time [sim_step]')
    ax.grid(True)
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('min', 'max', 'mean'), loc='best' )
    autolabel(rects1, ax)
    autolabel(rects2, ax)
    autolabel(rects3, ax)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if height > ax.get_ylim()[1]:
            ax.text(rect.get_x()+rect.get_width()/2., ax.get_ylim()[1], '%d'%int(height), 
                    ha='center', va='bottom', fontsize='smaller')
        else:
            ax.text(rect.get_x()+rect.get_width()/2., int(height), '%d'%int(height), 
                    ha='center', va='bottom', fontsize='smaller')
            # ax.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height), 
            #         ha='center', va='bottom', fontsize='smaller')

def show_plot(df, out_file):
    fig,ax = mpl.pyplot.subplots()
    for i in range(len(df)):
        ax.plot(df.ix[i]['data'], label=str(df.ix[i]['layer']))
    ax.set_ylabel('traffic by layer [bps]')
    ax.set_xlabel('time [sec]')
    ax.legend(loc='best')
    ax.grid(True)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')

def show_plot_by_layer(df, out_file):
    fig,axarr = mpl.pyplot.subplots(len(df), sharex=True)
    axarr[len(df) - 1].set_xlabel('time [sec]')
    for i in range(len(df)):
        axarr[i].plot(df.ix[i]['data'])
        axarr[i].set_ylabel(str(df.ix[i]['layer']) + ' [bps]')
#        axarr[i].legend(loc='best')
        axarr[i].grid(True)
    mpl.pyplot.tight_layout()  # prevent the overburden of title
    mpl.pyplot.savefig(out_file, figsize=(8, 18), bbox_inches='tight')

def show_plot_for_node_log(df, log_name, out_file):
    fig,ax = mpl.pyplot.subplots()
    ax.plot(df[log_name])
    ax.plot(pd.stats.moments.rolling_mean(df[log_name], 60), 'k')
    ax.set_ylabel(log_name)
    ax.set_xlabel('time [sec]')
#    ax.legend(loc='best')
    ax.grid(True)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')

def show_barh(df):
    width = 1
    ind = np.arange(len(df))
    fig,ax = mpl.pyplot.subplots()
    ax.barh(ind, df['mean'], height=1, left=None, color='r', linewidth=0)
    ax.set_xlabel('mean traffic on sw [bps]')
    ax.set_yticks(ind+width)
    ax.set_yticklabels(df['name'], fontsize=1)

    mpl.pyplot.savefig("sample.png", dpi=800)
    
def show_bubble(x, y, z, xlabel, ylabel, title, out_file, scale):
    vmin = z.min()
    vmax = z.max()
    cm = mpl.pyplot.cm.get_cmap('jet')
    fig, ax = mpl.pyplot.subplots()

#    sc = ax.scatter(x, y, s=z*scale, c=z, linewidth=0, alpha=0.5, vmin=vmin, vmax=vmax)
    sc = ax.scatter(x, y, s=z*scale, c=z, linewidth=0, alpha=0.5, vmin=0, vmax=5e8)
    ax.grid()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.invert_yaxis()
    fig.colorbar(sc)

#    mpl.pyplot.savefig(out_file)
    mpl.pyplot.savefig(out_file, bbox_inches='tight')
