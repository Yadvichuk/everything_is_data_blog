import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as mpcol
import numpy as np

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def subs(cmapnames, image):
    cmaps = [plt.colormaps.get_cmap(cmapname) for cmapname in cmapnames]
    fig, axes = plt.subplots(1, len(cmaps), figsize=(15, 5))
    for cmap, ax in zip(cmaps, axes):
        ax.axis("off")
        im = ax.imshow(image, cmap=cmap)
        ax.set_title(cmap.name)
    plt.show()


image = mpimg.imread("lenna.png")
subs(['jet', 'gray', 'viridis'], rgb2gray(image) )

