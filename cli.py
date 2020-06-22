from tricorder import scan
import click
from colour import Color
from TricorderGUI import TricorderGUI
from TricorderNotifier import CLINotifier

@click.command()
@click.argument('infile', type=click.File('r'))
@click.option('-o', type=click.File('w'), default='-', help="The output srt file", show_default=True)
@click.option('--color', default="#fff", help="The color of the subtitles in a html5-compliant format", show_default=True)
@click.option('--tleft', type=(float, float), default=(0, .8), help="Top left position of the rectangle where subtitles are located, in [0, 1] range", show_default=True)
@click.option('--bright', type=(float, float), default=(1, 1), help="Bottom right position of the rectangle where subtitles are located, in [0, 1] range", show_default=True)
@click.option('--tolerance', default=25, help="Value in range [0, 255] on how tolerant should the code be on the color of the subtitle", show_default=True)
@click.option('--sensitivity', default=25, help="How many pixels should change in order for us to try reading new subtitles. Should propably not be changed", show_default=True)
@click.option('--gui', is_flag=True, help="Display a GUI dialogue showing progress", show_default=True)
@click.option('--frameskip', default=2, help="Number of frames to skip before analyzing a frame", show_default=True)
def main(infile, o, color, tleft, bright, tolerance, sensitivity, gui, frameskip):
    color = tuple(map(lambda v: int(v*255), Color(color).rgb))

    if gui:
        app = TricorderGUI(infile, o, color, tleft, bright, tolerance, sensitivity, frameskip)
        app.exec()
    else:
        scan(infile, o, color, tleft, bright, tolerance, sensitivity, frameskip, CLINotifier())

if __name__ == '__main__':
    main()
