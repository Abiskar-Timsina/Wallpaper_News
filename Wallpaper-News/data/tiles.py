from data.scraper import DataScraper
from PIL import Image,ImageFont,ImageDraw
import time

class GenerateTiles:
	def __init__(self,FONT,FONT_SIZE,FONT_COLOR,TILE_SIZE,TILE_BG_COLOR):
		self.FONT = FONT
		self.FONT_COLOR = FONT_COLOR
		self.FONT_SIZE = FONT_SIZE
		self.TILE_SIZE = TILE_SIZE
		self.TILE_BG_COLOR = TILE_BG_COLOR

		#for the logo and title
		self.LOGO_SIZE = (50,50)
		self.TITLE_FONT_SIZE = int(sum(self.TILE_SIZE) / 40)
		self.TITLE_FONT_COLOR = (255,255,255,255)
		self.LOGO_TITLE_FONT = ImageFont.truetype(font="arial.ttf",size=self.TITLE_FONT_SIZE)

		#last updated field
		self.LU_FONT_SIZE = 12
		self.LU_FONT_COLOR = (255,255,255,255)
		self.LU_FONT = ImageFont.truetype(font="arial.ttf",size=self.LU_FONT_SIZE)

		#Titles
		self.LOCAL_NEWS_TITLE = "My Republica"
		self.INT_NEWS_TITLE = "New York Times"



	# News parser is needed to make sure that the text doesn't render out of the screen
	def news_parser(self,NEWS):
		#The "breadth" of the canvas
		render_limit = self.TILE_SIZE[1]

		#check for each article in the list.
		for artice_no,news_articles in enumerate(NEWS):
			length_of_article = len(news_articles)
			no_of_chars = 0
			index = 0

			#for each character consider a certain no of pixels are used up. So, if the text is long it takes up more pixels than the render_limit,
			#in which case we add a break line in the article
			
			for characters in news_articles:
				# The multiplication factor can be changed if needed, but 0.5 seems to work the best; the 0.5 essentially means a line break is added
				# after a certain no of characters have been printed
				no_of_chars += 0.50 * self.FONT_SIZE # this cannot be 1 because different characters seem to take up different amont of pixels to render
				index += 1
				if no_of_chars > render_limit:
					news_articles = news_articles[:index] + "-\n" + news_articles[index:]
					no_of_chars = 0
					NEWS[artice_no] = news_articles

		return NEWS

	def generate_localnews_tile(self):
		with Image.open("./images/local_logo.png") as logo:
			logo = logo.convert(mode="RGBA",colors=(0,0,0,0))
			logo = logo.resize(self.LOGO_SIZE)
			logo = logo.copy()

		# A blank image where the text is rendered; 
		canvas = Image.new("RGBA",size=self.TILE_SIZE,color=self.TILE_BG_COLOR)
		# Rendering the actual text
		drawing = ImageDraw.Draw(canvas)

		'''Text Rendering Settings'''
		'''Starting posn for drawing text; certain % times size of the canvas '''
		# Changing the multiplication factor is enough to change the position
		__TEXT_POSN_X = 0 * self.TILE_SIZE[0] 
		__TEXT_POSN_Y = 0.1 * self.TILE_SIZE[1]

		# Spacing between each line; changing the multiplication factor is enough 
		__SPACING_BETN_LINES = int(1.4 * self.FONT_SIZE) 

		# keeps track of the lines printed on the screen
		_lines = 0

		# Scrapes the data required
		__LOCAL_NEWS = self.news_parser(DataScraper().localnews())

		#draw the logo
		canvas.paste(im=logo,box=(0,0))
		drawing.text(xy=(__TEXT_POSN_X+200,__TEXT_POSN_Y-40),text=self.LOCAL_NEWS_TITLE,font=self.LOGO_TITLE_FONT,fill=self.TITLE_FONT_COLOR)
		_lines+=1

		#draw updated time
		last_updated = time.strftime("Last Updated: %x At %X %p")
		drawing.text(xy=(self.TILE_SIZE[0]-225,self.TILE_SIZE[1]-15),text=last_updated,font=self.LU_FONT,fill=self.LU_FONT_COLOR)

		for news_article in __LOCAL_NEWS:
			drawing.multiline_text(xy=(__TEXT_POSN_X,__TEXT_POSN_Y+(__SPACING_BETN_LINES*_lines)),text=news_article,font=self.FONT,fill=self.FONT_COLOR)
			_lines += 1
			if "\n" in news_article:
				_lines += news_article.count("\n")

		return canvas
		# canvas.save("local_news.png")

	def generate_int_news_tile(self):
		with Image.open("./images/int_logo.png") as logo:
			logo = logo.convert(mode="RGBA",colors=(0,0,0,0))
			logo = logo.resize(self.LOGO_SIZE)
			logo = logo.copy()

		# A blank image where the text is rendered; 
		canvas = Image.new("RGBA",size=self.TILE_SIZE,color=self.TILE_BG_COLOR)
		# Rendering the actual text
		drawing = ImageDraw.Draw(canvas)
		
		'''Text Rendering Settings'''
		'''Starting posn for drawing text; certain % times size of the canvas '''
		# Changing the multiplication factor is enough to change the position
		__TEXT_POSN_X = 0 * self.TILE_SIZE[0] 
		__TEXT_POSN_Y = 0.1 * self.TILE_SIZE[1]

		# Spacing between each line; changing the multiplication factor is enough 
		__SPACING_BETN_LINES = int(1.4 * self.FONT_SIZE) 

		# keeps track of the lines printed on the screen
		_lines = 0

		# Scrapes the data required
		__LOCAL_NEWS = self.news_parser(DataScraper().int_news())

		#draw the logo
		canvas.paste(im=logo,box=(0,0))
		drawing.text(xy=(__TEXT_POSN_X+200,__TEXT_POSN_Y-40),text=self.INT_NEWS_TITLE,font=self.LOGO_TITLE_FONT,fill=self.TITLE_FONT_COLOR )
		_lines+=1

		#draw updated time
		last_updated = time.strftime("Last Updated: %x At %X %p")
		drawing.text(xy=(self.TILE_SIZE[0]-225,self.TILE_SIZE[1]-15),text=last_updated,font=self.LU_FONT,fill=self.LU_FONT_COLOR)

		for news_article in __LOCAL_NEWS:
			drawing.multiline_text(xy=(__TEXT_POSN_X,__TEXT_POSN_Y+(__SPACING_BETN_LINES*_lines)),text=news_article,font=self.FONT,fill=self.FONT_COLOR)
			_lines += 1
			if "\n" in news_article:
				_lines += news_article.count("\n")
		
		return canvas
		# canvas.save("int_news.png")

