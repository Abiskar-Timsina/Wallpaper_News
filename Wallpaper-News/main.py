from PIL import Image,ImageFont,ImageDraw
from data.tiles import GenerateTiles

import os
import ctypes
import time


# in mins
UPDATE_INTERVAL = 90

SCREEN_RES_X = 1920
SCREEN_RES_Y = 1080

''' Tile Settings ''' 
# A tile here is a smaller picture that renders the scraped data; these are later merged.

TILE_X = 0.3 # in % 
TILE_Y = 0.5 # in %

# defining the tile size based on the resolution and tile x,y parameters
TILE_SIZE = (int(TILE_X*SCREEN_RES_X),int(TILE_Y*SCREEN_RES_Y)) 
TILE_BG_COLOR = (0,0,0,0) # (R,G,B,Alpha)

'''Font Settings'''
FONT_SIZE = int(sum(TILE_SIZE) / 60)
FONT_COLOR = (255,255,255,255) # (R,G,B,Alpha)
FONT = ImageFont.truetype(font="arial.ttf",size=FONT_SIZE)


# Tile posn in the screen:
POSN_X = 1 - TILE_X
POSN_Y = 1 - TILE_Y
TILE_POSN = (int(POSN_X*SCREEN_RES_X),int(POSN_Y*SCREEN_RES_Y))


def change_wallpaper(file_name):
	path_for_wallpaper = os.path.join(os.getcwd(),file_name)
	return True if ctypes.windll.user32.SystemParametersInfoW(20, 0,path_for_wallpaper, 0) else False


def main():
	local_news_tile = GenerateTiles(FONT, FONT_SIZE, FONT_COLOR, TILE_SIZE, TILE_BG_COLOR).generate_localnews_tile()
	int_news_tile = GenerateTiles(FONT, FONT_SIZE, FONT_COLOR, TILE_SIZE, TILE_BG_COLOR).generate_int_news_tile()

	#now that the files have been generated.
	tiles_on_screen = 0
	with Image.open("./images/wallpaper.png").convert("RGBA") as background:
		canvas = Image.new(mode="RGBA",size=background.size,color=(0,0,0,0))
		canvas.paste(local_news_tile,box=(TILE_POSN[0],TILE_POSN[1]*tiles_on_screen))
		tiles_on_screen += 1
		canvas.paste(int_news_tile,box=(TILE_POSN[0],TILE_POSN[1]*tiles_on_screen))
		tiles_on_screen += 1
		background.alpha_composite(canvas)
		background.save("./wallpaper.png")
	
	if change_wallpaper("wallpaper.png"):
		time.sleep(5)
		os.remove("./wallpaper.png")

if __name__ == "__main__":
	while True:
		main()
		time.sleep(UPDATE_INTERVAL * 60)



'''
SETTINGS:

To change the size of Tiles. Change TILE_X, TILE_Y in the main file. [These are based on the screen resolution]
To change the FONT SETTING. Main.py file
To change Tile settings, Spacing_Between_Lines -> data.tiles -> GenerateTiles().generate_localnews_tile()

Scraper Settings.
data.scraper -> DataScraper
'''

'''
TODO:

Determine constants
MAKE A GUI
'''
