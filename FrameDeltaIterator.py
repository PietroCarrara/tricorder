from multiprocessing import Pool

class FrameDeltaIterator:

    def __init__(self, frames, color, delta):
        """
        :param frames: Sequence of frames to watch for changes
        :type frames: Iterable of PIL.Image
        :param color: Color to watch for changes
        :type color: (int, int, int)
        :param delta: Number of pixels that have to change in order to alert for a new frame
        :type delta: int
        """
        self.frames = frames
        self.color = color
        self.delta = delta

    def __iter__(self):
        prevCount = 0
        frameCount = 0

        for currFrame in self.frames:
            count = countPixels(currFrame, self.color)
            if abs(prevCount - count) >= self.delta:
                yield (currFrame, frameCount)

            frameCount += 1
            prevCount = count


def cmp(pixel):
    return pixel == (255, 255, 255)

def countPixels(img, color):
    i = 0
    for pixel in img.getdata():
        if pixel == color:
            i += 1
    return i
