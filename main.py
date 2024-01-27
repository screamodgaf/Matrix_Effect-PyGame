import pygame
import random
import time
import threading


class MatrixSign(pygame.Rect):
    def __init__(self, pos_x, pos_y):
        self.lifetime = random.randint(0, 255)
        # self.lifetime = 255
        # self.lifetimeDecreaseRate = random.randint(5, 20)
        self.lifetimeDecreaseRate = 17
        # self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = (0, 0, 0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = size
        self.brightness = 0
        pygame.Rect.__init__(self, self.pos_x, self.pos_y, self.width, self.width)

    def getCurrentColor(self):
        return self.color

    def getBrightness(self):
        return self.brightness

    def setBrightness(self, brightness):
        if brightness == 255:
            self.color = (brightness, brightness, brightness)
            self.brightness = 255
        # brightness cannot be negative:
        elif self.brightness - abs(brightness) < 0:
            self.color = (0, 0, 0)
            self.brightness = 0
        else:
            c = self.brightness - abs(brightness)
            self.color = (c, c, c)
            self.brightness = c


def createColumn(positionX):
    # Create a rectangle object
    columnList = []
    # for row in range(0,800,size):
    # for col in range(0,600,size):
    # listOfObjectsToDraw.append(MatrixSign(row, col))

    for row in range(positionX, positionX + size, size):  # positionX + size is sign's size
        for col in range(0, 600, size):
            columnList.append(MatrixSign(row, col))
    return columnList


def createTableOfColumns(matrix, width):
    for row in range(0, width, size):
        matrix.append(createColumn(row))
    return matrix


def update(column):
    brightestElementIndex = -1
    brightestPresent = False
    # go through column and find the brightest element index or mark, if no element is set to 255:
    for index, sign in enumerate(column):
        # print(sign.getBrightness())
        if sign.getBrightness() == 255:
            brightestElementIndex = index
            brightestPresent = True
            # print("brightest sign is present at index: ", brightestElementIndex)

    # if no element has brightness set to 255, set te first element to 255
    if brightestPresent == False:
        # print(column[0])
        column[0].setBrightness(255)
        # print("no element has brightness set to 255, set te first element to 255")
        # nothing to dim so return:
        return

    # now make the sign below the brightest (but dont go further than the last element in column):
    if brightestElementIndex + 1 < len(column):
        column[brightestElementIndex].setBrightness(brightnessDecreaseRate)
        column[brightestElementIndex + 1].setBrightness(255)
        # print("setting a lower sign as brightest")
        # if element's brightness is more than 0 and it's not 255, dim its brightness:

    for index2, sign2 in enumerate(column):
        if sign2.getBrightness() > 0 and (
                sign2.getBrightness() != 255 or int(index2 == screenHeight / size - 1)):
            sign2.setBrightness(brightnessDecreaseRate)  # dim every element with brightness more than 0
            # print("dim every element with brightness more than 0")


def drawObjects(columnList):
    for sign in columnList:
        # sign.decreaseLifetime()
        pygame.draw.rect(screen, sign.getCurrentColor(), sign)


def drawControlableObject(player):
    pygame.draw.rect(screen, (255, 10, 10), player)


def worker(column, is_running, sleep_time):
    while is_running:
        # pause the execution of the column thread for the sleep_time
        time.sleep(sleep_time)
        update(column)


# Initialize pygame
pygame.init()
# Create a display surface
screen = pygame.display.set_mode((800, 600))
# Set the caption of the window
pygame.display.set_caption("Matrix Screensaver")
# Create a clock object
clock = pygame.time.Clock()

#SIGN BEHAVIOUR SETTINGS:
# set size of single sign rect:
size = 20
brightnessDecreaseRate = -10
screenHeight = screen.get_height()
# Create matrix table to draw:
matrix = []
matrix = createTableOfColumns(matrix, 800)

# Create a variable for the game loop
running = True
threadList = []
for columnIndex in range(0, len(matrix)):
    sleep_time = random.uniform(0.1, 1)
    t = threading.Thread(target=worker, args=(matrix[columnIndex], running, sleep_time))
    t.start()
    threadList.append(t)

# Create a color object
color = pygame.Color(255, 0, 0)

fps = 10
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

    # update listOfObjectsToDraw
    # for col in matrix:
    # update(col)
    # draw signs
    for col in matrix:
        drawObjects(col)

    # drawControlableObject(player)

    # Update the display
    pygame.display.update()
    # Control the frame rate
    clock.tick(fps)




# Quit pygame
pygame.quit()
