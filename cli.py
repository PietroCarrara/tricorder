from tricorder import scan
import click
from colour import Color
from TricorderGUI import TricorderGUI
from TricorderNotifier import CLINotifier

@click.command()
@click.argument('infile', type=click.File('r'))
@click.option('-o', type=click.File('w'), default='-', help="The output srt file")
@click.option('--color', default="#fff", help="The color of the subtitles in a html5-compliant format")
@click.option('--tleft', type=(float, float), default=(0, .8), help="Top left position of the rectangle where subtitles are located, in [0, 1] range")
@click.option('--bright', type=(float, float), default=(1, 1), help="Bottom right position of the rectangle where subtitles are located, in [0, 1] range")
@click.option('--tolerance', default=25, help="Value in range [0, 255] on how tolerant should the code be on the color of the subtitle")
@click.option('--sensitivity', default=25, help="How many pixels should change in order for us to try reading new subtitles. Should propably not be changed")
@click.option('--gui', is_flag=True, help="Display a GUI dialogue showing progress")
def main(infile, o, color, tleft, bright, tolerance, sensitivity, gui):
    color = tuple(map(lambda v: int(v*255), Color(color).rgb))

    if gui:
        app = TricorderGUI(infile, o, color, tleft, bright, tolerance, sensitivity)
        app.exec()
    else:
        scan(infile, o, color, tleft, bright, tolerance, sensitivity, CLINotifier())

if __name__ == '__main__':
    main()
