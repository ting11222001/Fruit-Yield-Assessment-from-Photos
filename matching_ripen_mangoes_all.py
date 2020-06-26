%matplotlib notebook
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import match_template
from PIL import Image

# convert image into an array and ndim: 3
ImagenTotal = np.asarray(Image.open('./redmangos.jpg'))

# print(ImagenTotal.ndim) 
#output: 3

# print(ImagenTotal.shape) 
#output: (480, 640, 3)

# print(len(ImagenTotal)) 
#output: 480

# print(ImagenTotal) 
#output: entire array

# print(ImagenTotal[0]) 
#output: the first [[255 255 255]…[38 51 41]]

# print(len(ImagenTotal[0])) 
#output: the first [[255 255 255]…[38 51 41]]'s length, 640

# print(ImagenTotal[0][0]) 
#output: [255 255 255]

# Interactive selection of points
# store all clicked coordinates here 
puntosinteres = []

# Create a new figure: width, height in inches
fig = plt.figure(figsize=(5, 4))

# position figure to 1st row, 1st column, index = 1
ax = fig.add_subplot(111)

# display image: ImagenTotal
ax.imshow(ImagenTotal)

# when mouse clicks on a mango, coordinates text will show here
# put outside of onclick function to have new blank text area each time before each clicks
text = ax.text(0,0, "", va="bottom", ha="left")

def onclick(event):
 tx = 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
 text.set_text(tx)
 puntosinteres.append([event.xdata, event.ydata])

# The FigureCanvas method mpl_connect() returns a connection id for button_press_event when a MouseEvent where mouse button is pressed
cid = fig.canvas.mpl_connect('button_press_event', onclick)

# print all coordinates: x-coor at i[0], y-coor at i[1]
for i in puntosinteres:
 print(i)

# amount of points clicked
len(puntosinteres)
# output: 6

# click on more mangos on the original picture
fig = plt.figure(figsize = (5, 4))
ax = fig.add_subplot(111)
ax.imshow(ImagenTotal)

# show points already clicked over the image
# x, y: positions (x-coor at i[0], y-coor at i[1])
# c: the marker colors, marker: marker style, s: marker size
ax.scatter([x[0] for x in puntosinteres], [y[1] for y in puntosinteres], c = 'red', marker = 'o', s = 8)

# when mouse clicks on a mango, coordinates text will show here
text = ax.text(0,0, "", va="bottom", ha="left")

def onclick(event):
 tx = 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' % (event.button, event.x, event.y, event.xdata, event.ydata)
 text.set_text(tx)
 puntosinteres.append([event.xdata, event.ydata])

cid = fig.canvas.mpl_connect('button_press_event', onclick)

# show all the points of interest's picture
# fig is one figure, ax is one list of subplots 
# .subplots(): x rows, y columns. 
# rows determined by length of clicked list
# in order to show 5 subplots per row, we need to have one extra row for remaining subplots
fig, ax = plt.subplots(len(puntosinteres)//5 + 1, 5)

# start to draw each selected pictures from top left ax[0,0] to the last
i = 0
for item in puntosinteres:
 # selected target's x-coor & y-coor
 xinteres = int(item[0])
 yinteres = int(item[1])
 # ax[x, y]: define subplot of nth row and nth column & display ImagenTotal i.e. original picture
 ax[i//5, i - i//5*5].imshow(ImagenTotal)
 # give specific coordinates to show each targeted area from original picture, also adding markers
 ax[i//5, i - i//5*5].plot(xinteres, yinteres, color = 'red', marker = '+', markersize = 8)
 # change subplots' x-axis and y-axis to resize the target's picture
 radio = 40
 # if radio value is higher, the target at the center will look smaller, vice versa.
 ax[i//5, i - i//5*5].set_xlim(xinteres-radio,xinteres+radio)
 ax[i//5, i - i//5*5].set_ylim(yinteres-radio,yinteres+radio)
 # remove each subplot's axes
 ax[i//5, i - i//5*5].axis('off')
 # add nth plot as title on each subplot
 ax[i//5, i - i//5*5].set_title(i)
 i += 1

# in case having a wrong point, delete it by specifying its index
# del puntosinteres[...]

# double check current list of clicks
len(puntosinteres) 
#output: 9

# Match the image to the template

listaresultados = []
for punto in puntosinteres:
    xinteres = int(punto[0])
    yinteres = int(punto[1])
    radio = 10
    # get the color pixel arrays of the entire picture
    # ndim: 3
    # choose the very first layer
    imagenband = ImagenTotal[:,:,0]
    # get the color array of each selected target parts
    # add buffer range for height and width
    # choose the very first layer
    # height & width are reversed before putting into match_template function
    templateband = ImagenTotal[yinteres - radio : yinteres + radio, xinteres - radio : xinteres + radio, 0]
    # take template to match image
    # match_template function uses fast, normalized cross-correlation to find instances of the template in the image. 
    result = match_template(imagenband, templateband) 
    # result will give us a matrix
    # set a threshold level of the match and store the matched coordinates result into an array
    # Note that the peaks in the output of match_template correspond to the origin (i.e. top-left corner) of the template.
    # print(result)
    loc = np.where(result > 0.8)
    # print(loc)
    # when threshold is higher i.e. 0.9, less pixels will be identified, vice versa.
    listaresultados.append(loc)
    
# print(listaresultados) 
#output: tuples of 2 arrays

print(len(listaresultados)) 
#used our clicks as template and get several closet points from our clicks on original picture 

# Plot interpreted points over the image

from itertools import cycle
# randomly generate colors
cycol = cycle('bgrcmk')

fig = plt.figure(figsize = (5, 4))
ax = fig.add_subplot(111)

i = 1
for lista in listaresultados:
    # x-cood's color array is at lista[1], y-cood's color array is at lista[0] 
    ax.plot(lista[1], lista[0], '.', markerfacecolor = next(cycol), label = i)
    i += 1

# raw scatter plot: place legends, style it    
ax.legend(loc='upper center', bbox_to_anchor = (0.5,-0.1), fancybox = True, shadow = True, ncol = 5)

# display original picture underneath
# raw scatter plot will be upside down and left & right reversed
# ImagenTotal moved left by 10 units on x axis, moved up by 10 units on y axis 
ax.imshow(ImagenTotal[radio : -radio, radio : -radio, :])

# Cluster analysis with Birch algorithm
# convert result into array and transpose
datalist = [np.asarray(pares).T for pares in listaresultados]
# print(datalist) 
# outout: 9 arrays of colors
# print(len(datalist))

# Stack arrays in sequence vertically (row wise)
datalist = np.vstack(datalist)
# print(datalist)  
# output: 9 arrays of colors are vertilcally stacked

from sklearn.cluster import Birch
brc = Birch(threshold = 10)
# Build a CF Tree for the input data
brc.fit(datalist)
# subcluster_centers: centroids of all subclusters read directly from the leaves.
puntosbirch = brc.subcluster_centers_
# print(puntosbirch) #output: 15 coordinate pairs in a 2 dimension array

# plot these clustered points on original picture
fig = plt.figure(figsize = (8, 4))
ax = fig.add_subplot(111)

# raw scatter plot: puntosbirch[:, [1]]: x-coor, puntosbirch[:, [0]]: y-coor
ax.scatter(puntosbirch[:, [1]], puntosbirch[:, [0]], marker = '+', color = 'red')

# display original picture underneath, 
# ImagenTotal moved left by 10 units on x axis, moved up by 10 units on y axis 
ax.imshow(ImagenTotal[radio: -radio, radio: -radio, :])

len(puntosbirch)
# can recognize 15 mangoes by clicking just 9