import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color
import pdb
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, colors


mpl.rcParams.update({'font.size': 20})
mpl.rcParams['font.sans-serif'] = 'Arev Sans, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Helvetica, Avant Garde, sans-serif'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal'] = 'cursive'
mpl.rcParams['mathtext.rm'] = 'sans'
mpl.rcParams['mathtext.tt'] = 'monospace'
mpl.rcParams['mathtext.it'] = 'sans:italic'
mpl.rcParams['mathtext.bf'] = 'sans:bold'
mpl.rcParams['mathtext.sf'] = 'sans'
mpl.rcParams['mathtext.fallback_to_cm'] = 'True'


### Red, original Albers plot

nrows = 5

# Start with red
red = np.array([np.hstack([np.ones((nrows,1)), np.zeros((nrows,2))])])

# Get basic red in LAB
lab_add = color.rgb2lab(red)
lab_geometric = lab_add.copy()

# Alter successive rows with more black
k = 1
for i in xrange(red.shape[1]):
    # more blackness is closer to 0 than one, and in first column of LAB
    lab_add[0,i,0] = lab_add[0,i,0] - 10*i
    print i,k
    if i != 0:
        lab_geometric[0,i,0] = lab_geometric[0,i,0] - 10*k
        k *= 2

# Change LAB back to RGB for plotting
rgb_add = red.copy() # only change red values
temp = color.lab2rgb(lab_add)
rgb_add[0,:,0] = temp[0,:,0]
rgb_geometric = red.copy() # only change red values
temp = color.lab2rgb(lab_geometric)
rgb_geometric[0,:,0] = temp[0,:,0]

fig = plt.figure()
k = 1
for i in xrange(red.shape[1]):

    # LHS: additive
    ax1 = fig.add_subplot(nrows,2,i*2+1, axisbg=tuple(rgb_add[0,i,:]))
    print tuple(lab_add[0,i,:])#, tuple(rgb_add[0,i,:])

    # RHS: multiplicative
    ax2 = fig.add_subplot(nrows,2,i*2+2, axisbg=tuple(rgb_geometric[0,i,:]))
    print tuple(lab_geometric[0,i,:])#, tuple(rgb_geometric[0,i,:])

    # ylabels
    if i!=0:
        ax1.set_ylabel(str(1*i))
        ax2.set_ylabel(str(k))
        k *= 2

    # Turn off ticks
    ax1.get_xaxis().set_ticks([])
    ax2.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])

    # Turn off black edges
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)


# common ylabel
ax1.text(-0.3, 3.8, 'Additional Parts Black', 
            rotation=90, transform=ax1.transAxes)


fig.subplots_adjust(hspace=0.0)
plt.show()

fig.savefig('figures/albers.pdf')
fig.savefig('figures/albers.png')



### Albers plot with linear scale black and white

nrows = 5
ncols = 2#3

x = np.linspace(0.0, 1.0, 100)
cmap = 'binary'

# Get binary colormap entries for full 100 entries
rgb = cm.get_cmap(cmap)(x)[np.newaxis,:,:3]

# Sample 100-entry rgb additively and geometrically
rgb_add = np.empty((1,nrows,3))
rgb_geometric = np.empty((1,nrows,3))
# rgb_cubic = np.empty((1,nrows,3))
k = 1
di = 8
I0 = 5
for i in xrange(nrows):
    # Do more blackness via increasing indices
    rgb_add[:,i,:] = rgb[:,i*di+I0,:]
    # rgb_cubic[:,i,:] = rgb[:,(I0**(1./3)+i*di**(1./3))**3,:]
    if i != 0:
        print i*di+I0, di*k+I0, (I0**(1./3)+i*di**(1./3))**3
        rgb_geometric[:,i,:] = rgb[:,I0+di*k,:]
        k *= 2
    elif i==0:
        print i*di+I0, I0, (I0**(1./3)+i*di**(1./3))**3
        rgb_geometric[:,i,:] = rgb[:,I0,:]

lab_add = color.rgb2lab(rgb_add)
lab_geometric = color.rgb2lab(rgb_geometric)
# lab_cubic = color.rgb2lab(rgb_cubic)

fig = plt.figure()
k = 1
for i in xrange(nrows):

    # LHS: additive
    ax1 = fig.add_subplot(nrows,ncols,i*2+1, axisbg=tuple(rgb_add[0,i,:]))
    print tuple(lab_add[0,i,:])#, tuple(rgb_add[0,i,:])

    # middle: multiplicative
    ax2 = fig.add_subplot(nrows,ncols,i*2+2, axisbg=tuple(rgb_geometric[0,i,:]))
    print tuple(lab_geometric[0,i,:])#, tuple(rgb_geometric[0,i,:])

    # # RHS: cubic
    # ax3 = fig.add_subplot(nrows,ncols,i*2+3, axisbg=tuple(rgb_cubic[0,i,:]))

    # ylabels
    if i!=0:
        ax1.set_ylabel(str(1*i))
        ax2.set_ylabel(str(k))
        k *= 2

    # Turn off ticks
    ax1.get_xaxis().set_ticks([])
    ax2.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])

    # Turn off black edges
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.spines['left'].set_visible(False)


# common ylabel
ax1.text(-0.3, 4.0, 'Steps through map indices', 
            rotation=90, transform=ax1.transAxes)


fig.subplots_adjust(hspace=0.0)
plt.show()

fig.savefig('figures/albers-bw.pdf')
fig.savefig('figures/albers-bw.png')


## Make a binary colormap with geometric relationship

# x = np.arange(100)
x = np.linspace(0.0, 7.64, 100)
# x = np.linspace(0.0, 6.15, 100)
di = -1. #1e-20
I0 = 100.
L = np.zeros(100)
L[0] = I0
L[1:] = I0 + 2**(x[:-1])*di
# L -= di
# L[L>100] = 100.
# L = 100-L
# L = L[::-1] #flip L

lab_geometric2 = lab.copy()
lab_geometric2[0,:,0] = L[::-1]
rgb_geometric2 = color.lab2rgb(lab_geometric2)


# Get binary colormap entries for full 100 entries
cmap = 'binary'
rgb = cm.get_cmap(cmap)(np.linspace(0.0, 1.0, 100))[np.newaxis,:,:3]
lab = color.rgb2lab(rgb)

# Make my new colormap
ind = rgb_geometric2>1.
rgb_geometric2[ind] = 1.
ind = rgb_geometric2<0.
rgb_geometric2[ind] = 0.
# red = rgb_geometric2[:,:,0]; red[0,0] = 1. # numbers aren't exactly 1
# red = tuple(map(tuple, red))
# green = rgb_geometric2[:,:,1]; green[0,0] = 1.
# green = tuple(map(tuple, green))
# blue = rgb_geometric2[:,:,2]; blue[0,0] = 1.
# blue = tuple(map(tuple, blue))
# cdict = {'red':red, 'green':green, 'blue':blue}
# my_cmap = colors.LinearSegmentedColormap('my_colormap', cdict, 100)
my_cmap = colors.ListedColormap(rgb_geometric2[0,::-1,:])#, name='my_name')

# plot colormaps with pyramid to test
giza = np.loadtxt('giza.txt')
x = np.linspace(1, 756, giza.shape[0]);
y = x.copy()
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(1,2,1, projection='3d')
ax.plot_surface(X, Y, giza, cmap='binary_r', linewidth=0)
ax = fig.add_subplot(1,2,2, projection='3d')
ax.plot_surface(X, Y, giza, cmap=my_cmap, linewidth=0)
