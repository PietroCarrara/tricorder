from PIL import Image
from datetime import timedelta
from VideoFrames import VideoFrames
from FrameDeltaIterator import FrameDeltaIterator
from SubtitleStateMachine import SubtitleStateMachine
from hypercube import tesse_fix
import math
import pytesseract


def scan(infile, out, color, tleft, bright, tolerance, sensitivity, frameskip, notifier):

    with infile as video, VideoFrames(video) as frames, out:
        # Skip frames, crop the images and scan them for changes
        changes = FrameDeltaIterator(map(lambda frame: crop_img(
            frame, tleft, bright), skipper(frames, frameskip)), color, sensitivity)

        subs = SubtitleStateMachine(out, notifier)

        for change in changes:
            img = change[0]
            # Account for skipped frames
            imgIndex = change[1] * (frameskip+1) + frameskip

            # Filter only pixels that have subtitle colors
            filtered = filter_pixels(img, color, tolerance)

            s = tesse_fix(pytesseract.image_to_string(filtered, lang='eng'))
            time = frames.duration * (imgIndex / frames.total_frames)

            notifier.notify_frame(filtered, s)
            notifier.notify_progress(imgIndex, frames.total_frames)
            notifier.notify_time(time)

            subs.say(s, time)

        notifier.notify_done()


def crop_img(frame, top_left, bottom_right):
    """Crops a image

    :param frame: The image to slice
    :type frame: Image
    :param top_left: Top left of the rectangle to slice, in % of the frame size (ranging in [0, 1])
    :type top_left: (float, float)
    :param bottom_right: Bottom right of the rectangle to slice, in % of the frame size (ranging in [0, 1])
    :type bottom_right: (float, float)
    """
    top_left_coords = (
        int(top_left[0] * frame.width), int(top_left[1] * frame.height))
    bottom_right_coords = (
        int(bottom_right[0] * frame.width), int(bottom_right[1] * frame.height))

    return frame.crop((top_left_coords[0], top_left_coords[1], bottom_right_coords[0], bottom_right_coords[1]))


def filter_pixels(img, color, deviation):
    res = Image.new('RGB', img.size, (
        color[0] ^ 255,
        color[1] ^ 255,
        color[2] ^ 255,
    ))

    # Allocate each line of the mask
    mask = [None] * img.height

    areaRadius = 40

    spots = []
    x = 0
    y = 0

    # Search for pixels that match the target color,
    # and calculate the distance of each pixel to the target color
    for y in range(img.height):
        # Allocate each row of the mask
        mask[y] = [0] * img.width
        for x in range(img.width):
            p = img.getpixel((x, y))
            mask[y][x] = distance(p, color)
            if color == p:
                spots.append((x, y))

    # For each pixel that the color is not too different from the target,
    # if it is within the radius of a 100% match with the target,
    # put it on the resulting image
    for y in range(img.height):
        for x in range(img.width):
            if mask[y][x] <= deviation:
                for point in spots:
                    _x = x - point[0]
                    _y = y - point[1]
                    d = math.sqrt(_y*_y + _x*_x) # Euclidean distance
                    if d < areaRadius:
                        res.putpixel((x, y), img.getpixel((x, y)))
                        break

    return res

def distance(color1, color2):
    return int(abs(sum(color1) - sum(color2)) / 3)

class skipper:
    def __init__(self, iter, skips):
        self.iter = iter
        self.skips = skips

    def __iter__(self):
        i = 0
        for obj in self.iter:
            if i >= self.skips:
                i = 0
                yield obj
            else:
                i += 1
