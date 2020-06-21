from PIL import Image
from datetime import timedelta
import subprocess
import json


class VideoFrames:

    def __init__(self, stream, ffmpeg='ffmpeg', ffprobe='ffprobe'):
        """
        Creates a iterator of the video frames

        stream: A stream to the contents of a video file. Must seek() and read()
        ffmpeg: The command to use when invoking ffmpeg
        ffprobe: The command to use when invoking ffprobe
        """
        self.stream = stream
        self.ffmpeg = ffmpeg
        self._subprocess = None

        probe = subprocess.Popen([ffprobe, '-show_streams', '-of', 'json', '-'],
                                 stdin=stream, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
        info = json.load(probe.stdout)
        if probe.poll() is None:
            probe.kill()

        # Reset stream
        stream.seek(0)

        # Acqurie video information
        info = next(
            stream for stream in info['streams'] if stream['codec_type'] == 'video')

        self.width = int(info['width'])
        self.height = int(info['height'])

        self.total_frames = int(info['nb_frames'])
        self.duration = timedelta(seconds=float(info['duration']))

        self._bytes_per_frame = self.width * self.height * 3  # 3 Bytes for each pixel

    def __enter__(self):
        self._subprocess = subprocess.Popen([self.ffmpeg, '-i', '-', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                                            stdin=self.stream, stderr=subprocess.DEVNULL, stdout=subprocess.PIPE)
        return self

    def __exit__(self, type, value, traceback):
        self._subprocess.kill()
        self._subprocess = None

    def __iter__(self):
        while self._subprocess.poll() is None:
            frame = self._subprocess.stdout.read(self._bytes_per_frame)
            if len(frame) > 0:
                yield Image.frombytes('RGB', (self.width, self.height), frame)
