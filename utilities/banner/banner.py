# The Clay World Project Banner Generator

# How it Works
# 
# The input is a full-resolution image of the banner "the clay world project"
# We then generate a sequence of images where each image has progressively more resolution.
# The resolution increases geometrically, meaning that the resolution of the next image is a constant multiple
# of the resolution of the image that preceeds it.
# 
# The algorithm simply downsamples each image to make it pixelated, and the upsamples to make it big enough to be seen
# This sequence of images is then combined into an animaged GIF. The sequence starts low-res and gets high-res, and then
# doubles back on itself to return to low-res. 


from PIL import Image

# PARAMETERS
filename = "banner-fullres.png"
minimumHeight = 5 #in pixels
imageFrames = 10 #total number of image frames in the gif output
finalWidth = 800 #final image width
endingIndex = 3 #this should be the minimum recognizable image


original = Image.open(filename)
original_bw = original.convert("1")

originalWidth, originalHeight = original_bw.size #vertical size in pixels
aspectRatio = float(originalWidth)/float(originalHeight)
finalHeight = int(round(float(finalWidth)/aspectRatio))

geometricSpacing = (float(originalHeight)/float(minimumHeight))**(1.0/float(imageFrames-1))

imageSequence = []
for index in range(imageFrames):
    newHeight = int(round(minimumHeight * geometricSpacing**index))
    newWidth = int(round(newHeight * aspectRatio))
    smallImage = original_bw.resize((newWidth,newHeight), resample = Image.NEAREST)
    fullImage = smallImage.resize((finalWidth, finalHeight), resample = Image.NEAREST).convert("L")
    imageSequence += [fullImage]

reverseSequence = imageSequence[endingIndex:-1]
reverseSequence.reverse()

imageSequence[0].save("banner.gif", save_all= True, append_images = imageSequence[1:]+[imageSequence[-1]]+reverseSequence, duration = 1000)