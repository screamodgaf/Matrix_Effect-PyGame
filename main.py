import pygame
import random
import time
import threading


class MatrixSign(pygame.Rect):
    def __init__(self, pos_x, pos_y, size, font):
        self.font = font
        self.lifetime = random.randint(0, 255)
        # self.lifetime = 255
        # self.lifetimeDecreaseRate = random.randint(5, 20)
        self.lifetimeDecreaseRate = 17
        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #self.color = (0, 0, 0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = size
        self.brightness = 0
        self.katakana = ['ア','イ','ウ','エ','オ','カ','キ','ク','ケ','コ','サ','シ','ス','セ','ソ','タ','チ','ツ','テ','ト',
                    'ナ','ニ','ヌ','ネ','ノ','ハ','ヒ','フ','ヘ','ホ','マ','ミ','ム','メ','モ','ヤ','ユ','ヨ','ラ','リ',
                    'ル','レ','ロ','ワ','ヰ','ヱ','ヲ','ン']
        self.katakanaSign = 'ウ'

    def getCurrentColor(self):
        return self.color
    def getBrightness(self):
        return self.brightness
    def getX(self):
        return self.pos_x
    def getY(self):
        return self.pos_y
    def changeSign(self):
        r = random.randrange(0, len(self.katakana))
        self.katakanaSign = self.katakana[r]
    def getSign(self):
        return self.katakanaSign
    def changeBrightness(self, brightness):
        # check if the brightness value is valid:
        if brightness == 255:
            # self.color = (0, brightness, 0)
            self.brightness = 255
        # brightness cannot be negative:
        elif self.brightness - abs(brightness) < 0:
            # self.color = (0, 0, 0)
            self.brightness = 0
        else:
            self.brightness = self.brightness - abs(brightness)

def createColumn(positionX, size, font):
    # Create a rectangle object
    columnList = []

    for row in range(positionX, positionX + size, size):  # positionX + size is sign's size
        for col in range(0, screenHeight, size):
            columnList.append(MatrixSign(row, col, size, font))
    return columnList


def createTableOfColumns(matrix, width, size, font):
    for row in range(0, width, size):
        matrix.append(createColumn(row, size, font))
    return matrix


def update(column, brightnessDecreaseRate):
    brightestElementIndex = -1
    brightestPresent = False
    # go through column and find the brightest element index or mark, if no element is set to 255:
    for index, sign in enumerate(column):
        # print(sign.getBrightness())
        if sign.getBrightness() == 255:
            brightestElementIndex = index
            brightestPresent = True
            # print("brightest sign is present at index: ", brightestElementIndex)

        #change sign - the speed of change is related to thread.sleep:
        if random.randrange(0,2): #change by chance - 50%
            sign.changeSign()
    # if no element has brightness set to 255, set te first element to 255
    if brightestPresent == False:
        # print(column[0])
        column[0].changeBrightness(255)
        # print("no element has brightness set to 255, set te first element to 255")
        # nothing to dim so return:
        return

    # now make the sign below the brightest (but dont go further than the last element in column):
    if brightestElementIndex + 1 < len(column):
        column[brightestElementIndex].changeBrightness(-brightnessDecreaseRate)
        column[brightestElementIndex + 1].changeBrightness(255)
        # print("setting a lower sign as brightest")
        # if element's brightness is more than 0 and it's not 255, dim its brightness:

    for index2, sign2 in enumerate(column):
        if sign2.getBrightness() > 0 and (
                sign2.getBrightness() != 255 or int(index2 == screenHeight / size - 1)):
            # dim every element with brightness more than 0:
            sign2.changeBrightness(-brightnessDecreaseRate)
            # print("dim every element with brightness more than 0")


def drawObjects(columnList):
    for sign in columnList:
        brightness = sign.getBrightness()
        katakanaSign = sign.getSign();
        katakanaSignSurface = None
        #make the brightest element white:
        if brightness == 255:
            katakanaSignSurface = font.render(katakanaSign, True, (brightness, brightness, 210))
        else: #if the current element isnt the brightest, make it a shade of green:
            katakanaSignSurface = font.render(katakanaSign,True, (0, brightness, 0))

        katakanaSign_rect =  katakanaSignSurface.get_rect()
        katakanaSign_rect.x = sign.getX()
        katakanaSign_rect.y = sign.getY()
        screen.blit(katakanaSignSurface, katakanaSign_rect)

def worker(column, is_running, sleep_time, brightnessDecreaseRate):
    while is_running:
        # pause the execution of the column thread for the sleep_time
        time.sleep(sleep_time)
        update(column, brightnessDecreaseRate)


# Initialize pygame
pygame.init()
# Create a display surface
screen = pygame.display.set_mode((1920, 1080))
# Set the caption of the window
pygame.display.set_caption("Matrix")
# Create a clock object
clock = pygame.time.Clock()

screenHeight = screen.get_height()
screenWidth = screen.get_width()
#screenWidth = 1
# Create a font object with the path to a Japanese font file and the desired size


# SIGN BEHAVIOUR SETTINGS:
size = 20  # set size of single sign rect:

font = pygame.font.Font('fonts/MSMINCHO.ttf', size)

# the max speed of single sign column disappearing - the bigger value the faster disappears (each iteration: 255 - brightnessDecreaseRateMax ):
brightnessDecreaseRateMax = 28
# slows down the speed the signs in a single column moves:
sleeptime = 0.7
# Create matrix table to draw:
matrix = []
matrix = createTableOfColumns(matrix, screenWidth, size, font)

# Create a variable for the game loop
running = True
threadList = []
for columnIndex in range(0, len(matrix)):
    sleep_time = random.uniform(0.1, sleeptime)
    brightnessDecreaseRate = random.randrange(2, brightnessDecreaseRateMax)
    t = threading.Thread(target=worker, args=(matrix[columnIndex], running, sleep_time, brightnessDecreaseRate))
    t.start()
    threadList.append(t)


fps = 17
# Start the game loop
while running:
    # Handle the events
    for event in pygame.event.get():
        # Check if the user clicked the close button
        if event.type == pygame.QUIT:
            # Exit the loop
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # draw signs
    for col in matrix:
        drawObjects(col)

    # Update the display
    pygame.display.update()
    # Control the frame rate
    clock.tick(fps)

# Quit pygame
pygame.quit()
