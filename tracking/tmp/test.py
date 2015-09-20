# http://stackoverflow.com/questions/29718238/how-to-read-mp4-video-to-be-processed-by-scikit-image
import pylab
import imageio
filename = '/home/tor/jamu/xprmnt/cell/input/cell.mp4'
vid = imageio.get_reader(filename,  'ffmpeg')
nums = [10, 287]
for num in nums:
    image = vid.get_data(num)
    fig = pylab.figure()
    fig.suptitle('image #{}'.format(num), fontsize=20)
    pylab.imshow(image)
pylab.show()