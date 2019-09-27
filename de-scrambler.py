import math, os
from PIL import Image

"""
A dumb program inspired by Gmask, a program popular quite a few years ago that would de-scramble
parts of an image. Gmask had multiple different types of ways to de-scramble an image, where as
this program focussed only on the rotation of a ring of pixels that make up an image.
"""

def rotate(inner, outer):
    #dtheta necessary for non-perfect-square images AKA rectangles
    dtheta = 90 if width == height else 180
    angle = 0
    comparisons = []
    (owidth, oheight) = outer.size
    (iwidth, iheight) = inner.size
    #Hollows out the two images and breaks them into components to compare pixel to pixel
    #Frame: [top, rign, bottom, left]
    oframes = [outer.crop((pixelsize - 1, pixelsize - 1, owidth, pixelsize)),
               outer.crop((owidth - pixelsize, pixelsize - 1, owidth, oheight)),
               outer.crop((pixelsize - 1, oheight - pixelsize, owidth, oheight)),
               outer.crop((pixelsize - 1, pixelsize - 1, pixelsize, oheight))]
    iframes = [inner.crop((0, 0, iwidth, 1)),
               inner.crop((iwidth - 1, 0, iwidth, iheight)),
               inner.crop((0, iheight - 1, iwidth, iheight)),
               inner.crop((0, 0, 1, iheight))]
    
    while angle % 360 != 0 or angle == 0:
        likeness = []
        #Confusing logic to rearrange iframe depending on angle and dtheta
        #"Simulates" rotation without actually applying it
        order = [(x + ((angle*(dtheta//90))//dtheta)%4)%4 for x in range(4)]
        newiframes = [iframes[x] for x in order]
        #Sends each component of the two frames to be compared
        for x in range(4):
            likeness.append(compare(newiframes[x], oframes[x]))
        comparisons.append(sum(likeness))
        angle += dtheta

    #The smallest difference, in theory, should be the correct angle of rotation
    return inner.rotate(comparisons.index(min(comparisons)) * dtheta)

def compare(iline, oline):
    #Convert pixel data to a list of RGB values
    iline = iline.getdata()
    oline = oline.getdata()
    totaldiff = 0
    for i, x in enumerate(iline):
        difference = 0
        for y in range(3):
            #Literally using the distance formula to find the color difference between RGB values
            #One inner pixel is being compared to three surrounding outer pixels
            difference += ((((iline[i][0] - oline[i + y][0]) ** 2) + ((iline[i][1] - oline[i + y][1]) ** 2)+((iline[i][2] - oline[i + y][2]) ** 2)) ** .5)
        #Divided by 3 to average the difference
        totaldiff += difference / 3
    return totaldiff

#Sometimes it won't get it on the first try, or at all for that matter, so it keeps trying
#Eventually gets to the point where no changes are made anymore, be it correct or not
count = 0
while(1):
    base = Image.open(os.path.dirname(__file__) + "/Pictures/De-scramble/" + str(count) +  ".png")
    outer = base.copy();
    output = Image.new('RGB', base.size)
    pixelsize = 8

    #Some math to calculate how many rings of width pixelsize you can make out of a 2D image
    for i in range(math.ceil(min(outer.size) * pixelsize / 2)):
        (width, height) = outer.size
        box = (pixelsize, pixelsize, width - pixelsize, height - pixelsize)
        inner = outer.crop(box)
        inner = rotate(inner, outer)
        #Destination.paste(object, position)
        outer.paste(inner, (pixelsize, pixelsize))
        output.paste(outer, (pixelsize * i, pixelsize * i))
        output.save(os.path.dirname(__file__) + "/Pictures/De-scramble/z" + str(i) +  ".png")
        outer = inner

    count += 1
    base.close()
    print(count)
    #output.save(os.path.dirname(__file__) + "/Pictures/De-scramble/" + str(count) +  ".png")
