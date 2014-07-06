'''
Compare black and white algorithms.
'''

from skimage import io, color
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import pdb
from scipy.optimize import curve_fit

# Use grey calculation from http://www.tannerhelland.com/3643/grayscale-image-algorithm-vb6/
# grey1 = rgb[0,:,0]*0.212671 + rgb[0,:,1]*0.715160 + rgb[0,:,2]*0.072169

# Also from http://www.tannerhelland.com/3643/grayscale-image-algorithm-vb6/ but gives different results from the matplotlib colors rgb2lab conversion
# y = rgb[0,:,0]*0.212671 + rgb[0,:,1]*0.715160 + rgb[0,:,2]*0.072169
# L = 116.*y**(1./3) - 16
# ind = y<= 0.008856
# L[ind] = 903.3*y[ind]

# Just use the rgb2lab conversion for lab




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



nrows = max(len(cmap_list) for cmap_category, cmap_list in cmaps)
gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))

def plot_color_gradients(cmap_category, cmap_list):
    fig, axes = plt.subplots(nrows=nrows, ncols=2)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99, wspace=0.05)
    fig.suptitle(cmap_category + ' colormaps', fontsize=14, y=1.0, x=0.6)
    # axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_list):

        # Get rgb values for colormap
        rgb = cm.get_cmap(plt.get_cmap(name))(x)[np.newaxis,:,:3]

        # Get colormap in CIE LAB. We want the L here.
        lab = color.rgb2lab(rgb)
        L = lab[0,:,0]
        L = np.float32(np.vstack((L, L, L)))

        # grey = rgb[0,:,0]*0.212671 + rgb[0,:,1]*0.715160 + rgb[0,:,2]*0.072169
        # grey = np.float32(np.vstack((grey, grey, grey)))
        # for scatter plot, in list
        # grey = [str(rgb[0,i,0]*0.212671 + rgb[0,i,1]*0.715160 + rgb[0,i,2]*0.072169) for i in xrange(rgb.shape[1])]

        # if name == 'jet':
        #     pdb.set_trace()
        
        # ax.plot(L[0,:], 'k', lw=3)
        # ax.plot(grey[0,:], 'r', lw=3)
        # pdb.set_trace()
        ax[0].imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        ax[1].imshow(L, aspect='auto', cmap='binary_r', vmin=0., vmax=100.)
        pos = list(ax[0].get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='right', fontsize=10)
        # pdb.set_trace()

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax[0].set_axis_off()
        ax[1].set_axis_off()
    # pdb.set_trace()
    fig.savefig('figures/bw' + cmap_category + '.png', dpi=150)
    plt.close(fig)



for cmap_category, cmap_list in cmaps:

    plot_color_gradients(cmap_category, cmap_list)

