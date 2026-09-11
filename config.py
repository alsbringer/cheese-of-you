from utils import setSize_W, loadImage
from os.path import join

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BACKGROUND_IMG = loadImage(join("assets","amphoreus.png"))
BACKGROUND_IMG = setSize_W(BACKGROUND_IMG, 1000)
WIDTH_MARGIN = 20
HEIGHT_MARGIN = 34