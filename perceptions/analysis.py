from skimage import io, color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import pdb
from scipy.optimize import curve_fit

mpl.rcParams.update({'font.size': 14})
mpl.rcParams['font.sans-serif'] = 'Arev Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Helvetica, Avant Garde, sans-serif'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal'] = 'cursive'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.tt'] = 'monospace'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.bf'] = 'sans:bold'
mpl.rcParams['mathtext.sf'] = 'sans'
mpl.rcParams['mathtext.fallback_to_cm'] = 'True'


## Get colormaps, from http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html

# Get a list of the colormaps in matplotlib.  Ignore the ones that end with
# '_r' because these are simply reversed versions of ones that don't end
# with '_r'
maps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))
nmaps = len(maps) + 1

# OR, to have colormaps separated into categories: http://matplotlib.org/examples/color/colormaps_reference.html

cmaps = [('Sequential',     ['binary', 'Blues', 'BuGn', 'BuPu', 'gist_yarg',
                             'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
                             'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
                             'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']),
         ('Sequential (2)', ['afmhot', 'autumn', 'bone', 'cool', 'copper',
                             'gist_gray', 'gist_heat', 'gray', 'hot', 'pink',
                             'spring', 'summer', 'winter']),
         ('Diverging',      ['BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
                             'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'seismic']),
         ('Qualitative',    ['Accent', 'Dark2', 'hsv', 'Paired', 'Pastel1',
                             'Pastel2', 'Set1', 'Set2', 'Set3', 'spectral']),
         ('Miscellaneous',  ['gist_earth', 'gist_ncar', 'gist_rainbow',
                             'gist_stern', 'jet', 'brg', 'CMRmap', 'cubehelix',
                             'gnuplot', 'gnuplot2', 'ocean', 'rainbow',
                             'terrain', 'flag', 'prism'])]

ncmaps = len(cmaps)
        
x = np.linspace(0.0, 1.0, 100)

## Sequential colormaps

fig = plt.figure(figsize=(18,8))

# loop through maps
# for i,m in enumerate(maps):
i = 1
for cmap_category, cmap_list in cmaps:

    if 'Sequential' not in cmap_category:
        continue

    flag = True

    ax = fig.add_subplot(2, 1, i)
    if i==1:
        ax.set_title('Lightness $L^*$ along colormap index', fontsize=18)
    
    for j, cmap in enumerate(cmap_list):

        # Get rgb values for colormap
        rgb = cm.get_cmap(cmap)(x)[np.newaxis,:,:3]
        # hsv = matplotlib.colors.rgb_to_hsv(rgb).squeeze()

        # Get colormap in CIE LAB. We want the L here.
        lab = color.rgb2lab(rgb)

        # if cmap=='binary':
            # pdb.set_trace()

        # Plot colormap L values
        if '(2)' in cmap_category:
            ax.scatter(x+j*0.83, lab[0,:,0], c=x, cmap=cmap, s=300, linewidths=0.1)
            ax.set_ylabel('Sequential MatLab', fontsize=18)
            ax.axis([0,11,0,100])
        else:
            ax.scatter(x+j*0.5, lab[0,::-1,0], c=x, cmap=cmap + '_r', s=300, linewidths=0.1)
            ax.set_ylabel('Sequential', fontsize=18)
            ax.axis([0,10.5,0,100])
    
        ax.get_xaxis().set_ticks([])

    i += 1

fig.subplots_adjust(left=0.04, right=0.99, bottom=0.05, top=0.93, hspace=0.1)
fig.show()

fig.savefig('figures/lightness-sequential.png')


## Non-sequential colormaps

fig = plt.figure(figsize=(18,10))

# loop through maps
# for i,m in enumerate(maps):
i = 1
for cmap_category, cmap_list in cmaps:

    if 'Sequential' in cmap_category:
        continue

    flag = True

    ax = fig.add_subplot(3, 1, i)
    if i==1:
        ax.set_title('Lightness $L^*$ along colormap index', fontsize=18)
    
    for j, cmap in enumerate(cmap_list):

        # Get rgb values for colormap
        rgb = cm.get_cmap(cmap)(x)[np.newaxis,:,:3]
        # hsv = matplotlib.colors.rgb_to_hsv(rgb).squeeze()

        # Get colormap in CIE LAB. We want the L here.
        lab = color.rgb2lab(rgb)

        # Plot colormap L values
        if 'Qualitative' in cmap_category:
            ax.scatter(x+j*1.3, lab[0,:,0], c=x, cmap=cmap, s=300, linewidths=0.1)
            ax.axis([0,13,0,100])
        elif 'Diverging' in cmap_category:
            ax.scatter(x+j*1.2, lab[0,::-1,0], c=x, cmap=cmap + '_r', s=300, linewidths=0.1)
            ax.axis([0,13,0,100])
        elif 'Miscellaneous' in cmap_category:
            ax.scatter(x+j*1.5, lab[0,::-1,0], c=x, cmap=cmap + '_r', s=300, linewidths=0.1)
            ax.axis([0,22,0,100])

        ax.get_xaxis().set_ticks([])
        ax.set_ylabel(cmap_category, fontsize=18)

    i += 1

fig.subplots_adjust(left=0.04, right=0.99, bottom=0.03, top=0.95, hspace=0.1)
fig.show()
fig.savefig('figures/lightness-rest.png')

# can't figure out this part. Curve fitting isn't looking right.

# ## Sequential colormap L* curve fitting

# def func(x, a, b, c):
#     return c + a * x ** b

# # xdata = np.linspace(0, 4, 50)

# # Loop through sequential colormaps and calculate the curve fit
# # Then paste the exponent on the plot for each.
# for j, cmap in enumerate(cmaps[0][1]): # Sequential colormaps

#     # Get rgb values for colormap
#     rgb = cm.get_cmap(cmap + '_r')(x)[np.newaxis,:,:3]

#     # Get colormap in CIE LAB. We want the L here.
#     lab = color.rgb2lab(rgb)

#     popt, pcov = curve_fit(func, x, lab[0,:,0])

#     print cmap, popt[1]

#     # pdb.set_trace()
