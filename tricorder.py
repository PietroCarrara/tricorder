from PIL import Image
from datetime import timedelta
from VideoFrames import VideoFrames
from FrameDeltaIterator import FrameDeltaIterator
from SubtitleStateMachine import SubtitleStateMachine
from hypercube import tesse_fix
import pytesseract


def scan(infile, out, color, tleft, bright, tolerance, sensitivity, notifier):

    with infile as video, VideoFrames(video) as frames, out:
        # Crop the images and scan them for changes
        changes = FrameDeltaIterator(map(lambda frame: crop_img(
            frame, tleft, bright), frames), color, sensitivity)

        subs = SubtitleStateMachine(out, notifier)

        for change in changes:
            # For each change...

            # Filter only pixels that have subtitle colors
            img = filter_pixels(
                change[0], color, tolerance)

            notifier.notify_frame(img, change[1]/frames.total_frames)

            s = tesse_fix(pytesseract.image_to_string(img, lang='eng'))
            time = frames.duration * (change[1] / frames.total_frames)

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

    x = 0
    y = 0
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            p = img.getpixel((x, y))
            if near(p, color, deviation):
                res.putpixel((x, y), p)

    return res


def near(color1, color2, deviation):
    color = (
        abs(color1[0] - color2[0]),
        abs(color1[0] - color2[1]),
        abs(color1[0] - color2[2]),
        abs(color1[1] - color2[0]),
        abs(color1[1] - color2[1]),
        abs(color1[1] - color2[2]),
        abs(color1[2] - color2[0]),
        abs(color1[2] - color2[1]),
        abs(color1[2] - color2[2]),
    )
    return max(color) <= deviation