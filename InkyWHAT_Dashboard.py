#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from inky.auto import auto
from PIL import Image, ImageDraw, ImageFont
from font_fredoka_one import FredokaOne

import textwrap

# Colours for the InkyWHAT
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
orange = (255, 140, 0)

font = ImageFont.truetype(FredokaOne, 20)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/freefont/Piboto-BoldItalic.ttf", 20)

outOfStockPhrases = ["Sold out",
			"Out of Stock"]
inStockPhrases = ["In stock, ready to be shipped",
		 "In stock and ready to ship!"]

# Initialise the inkyPhat as a red display, create background image
display=auto()
img = Image.open("Background2.jpg", "r")
drawnImg = ImageDraw.Draw(img)

# Initialise Selenium
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# Function to get the stock levels.  Needs a product URL and element
def checkStock(url, element):
	driver.get(url)
	stockLevel = driver.find_element(by=By.CSS_SELECTOR, value=element).text
	if stockLevel in inStockPhrases:
		return "In stock"
	elif stockLevel in outOfStockPhrases:
		return "Out of stock"
	else:
		return stockLevel

# Function to set text colour according to stock level
def checkFont(message):
	if message == "Out of stock":
		return(red)
	elif message == "In stock":
		return(green)
	else:
		return(orange)

# Get the stock levels
pimoroniURL = "https://shop.pimoroni.com/products/raspberry-pi-zero-2-w?variant=39493046075475"
pimoroniElement = "div.stock-message"
pimoroniStockLevel = checkStock(pimoroniURL, pimoroniElement)

pihutURL = "https://thepihut.com/products/raspberry-pi-zero-2"
pihutElement = "span.product-form__inventory"
pihutStockLevel = checkStock(pihutURL, pihutElement)

pimoroniPicoURL = "https://shop.pimoroni.com/products/raspberry-pi-pico?variant=39410491621459"
pimoroniPicoElement = "div.stock-message"
pimoroniPicoStockLevel = checkStock(pimoroniPicoURL, pimoroniPicoElement)

pihutPicoURL = "https://thepihut.com/products/raspberry-pi-pico"
pihutPicoElement = "span.product-form__inventory"
pihutPicoStockLevel = checkStock(pihutPicoURL, pihutPicoElement)

# Get the weather
driver.get("https://www.bbc.co.uk/weather/2655984")
weather = driver.find_element(by=By.CLASS_NAME, value="wr-day__details__weather-type-description").get_attribute("innerHTML")
highTemp = (driver.find_element(by=By.CSS_SELECTOR,
                                value="div.wr-day-temperature__high")).text.replace("\n", ": ") + "C"
lowTemp = (driver.find_element(by=By.CSS_SELECTOR,
                               value="div.wr-day-temperature__low")).text.replace("\n", ": ") + "C"

# Get rain data
rainRawData = list(driver.find_elements(by=By.CLASS_NAME, value="wr-u-font-weight-500"))
# Convert rain data to plaintext.  It does funky stuff otherwise
plainTextRainData = []
for item in rainRawData:
    plainTextRainData.append(item.text)
# Last two values aren't rain data, remove them
del(plainTextRainData[-2:-1])

rainChances = []

parsing = True
while parsing == True:
    for x in range (0, len(plainTextRainData), 2):
        if int(plainTextRainData[x]) > 00:
            numberEnd = plainTextRainData[x+1].find("%")
            rainChances.append(int(plainTextRainData[x+1][:numberEnd]))
        else:
            parsing = False
            break
maxRainChance = str(max(rainChances))

driver.quit()

# Draw the image
drawnImg = ImageDraw.Draw(img)
pimoroniLogo = Image.open("PimoroniSmall.jpg", "r")
pihutLogo = Image.open("PiHutSmall.jpg", "r")
# Pi Zero W 2 Stock
drawnImg.text((20,50), "Pi Zero 2 Stock", blue, font)

img.paste(pimoroniLogo, (20, 80))
drawnImg.text((80, 90),
	pimoroniStockLevel,
	checkFont(pimoroniStockLevel),
	font)

img.paste(pihutLogo, (20, 120))
drawnImg.text((80, 130),
	pihutStockLevel,
	checkFont(pihutStockLevel),
	font)

# Pi Pico stock
drawnImg.text((20,170), "Pi Pico Stock", blue, font)

img.paste(pimoroniLogo, (20, 200))
#drawnImg.text((20, 200), "Pimoroni:", black, font)
drawnImg.text((80, 210),
	pimoroniPicoStockLevel,
	checkFont(pimoroniPicoStockLevel),
	font)

img.paste(pihutLogo, (20, 240))
#drawnImg.text((20, 230), "PiHut:", black, font)
drawnImg.text((80, 250),
	pihutPicoStockLevel,
	checkFont(pihutPicoStockLevel),
	font)

# Draw weather
drawnImg.text((310, 50), "Weather for today:", black, font)

weather = textwrap.wrap(weather, 28)
Ycursor =80

for line in weather:
	drawnImg.text((310, Ycursor), line, black, font2)
	Ycursor += 30

drawnImg.text((310, Ycursor), highTemp, red, font)
Ycursor += 30
drawnImg.text((310, Ycursor), lowTemp, blue, font)
Ycursor += 30
drawnImg.text((310, Ycursor), "Max. chance of rain:", black, font)
Ycursor +=30
drawnImg.text((310, Ycursor), maxRainChance + "%", blue, font) 

display.set_image(img)
display.show()
