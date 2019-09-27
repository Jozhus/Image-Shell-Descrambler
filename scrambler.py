import random, math, os
from PIL import Image

base = Image.open(os.path.dirname(__file__) + "/Pictures/De-scramble/0.png")
outer = base.copy();
output = Image.new('RGB', base.size)
pixelsize = 1
dtheta = 90 if base.width == base.height else 180 

for i in range(math.ceil(min(outer.size) * pixelsize / 2)):
        (width, height) = outer.size
        box = (pixelsize, pixelsize, width - pixelsize, height - pixelsize)
        inner = outer.crop(box)
        inner = inner.rotate((random.randrange(100)%3)*dtheta)
        #Destination.paste(object, position)
        outer.paste(inner, (pixelsize, pixelsize))
        output.paste(outer, (pixelsize * i, pixelsize * i))
        outer = inner

output.save(os.path.dirname(__file__) + "/Pictures/De-scramble/0.png")
