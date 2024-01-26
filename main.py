import pygame
import random

class MatrixSign(pygame.Rect):
    def __init__(self, pos_x, pos_y):
        self.lifetime = random.randint(0, 255)
        #self.lifetime = 255
        #self.lifetimeDecreaseRate = random.randint(5, 20)
        self.lifetimeDecreaseRate = 17
        #self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.color = (0,0,0)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = 40
        self.brightness = 0
        pygame.Rect.__init__(self, self.pos_x, self.pos_y, self.width,self.width)
    def getCurrentColor(self):
        return self.color
    def getBrightness(self):
        return self.brightness
    def setBrightness(self, brightness):
        if brightness == 255:
            self.color = (brightness, brightness, brightness)
            self.brightness = 255
        #brightness cannot be negative:
        elif self.brightness - abs(brightness) < 0:
            self.color = (0, 0, 0)
            self.brightness = 0
        else:
            c = self.brightness - abs(brightness)
            self.color = (c, c, c)
            self.brightness = c

def createObjectsToDraw():
    # Create a rectangle object
    listOfObjectsToDraw = []

    #for row in range(0,800,40):
        #for col in range(0,600,40):
            #listOfObjectsToDraw.append(MatrixSign(row, col))

    for row in range(0,40,40):
        for col in range(0,600,40):
            listOfObjectsToDraw.append(MatrixSign(row, col))

    return listOfObjectsToDraw

def update(listOfObjectsToDraw):
    brightestElementIndex = -1
    brightestPresent = False

    # go through column and find the brightest element index or mark, if no element is set to 255:
    for index, sign in enumerate(listOfObjectsToDraw):
        #print(sign.getBrightness())
        if sign.getBrightness() == 255:
            brightestElementIndex = index
            brightestPresent = True
            print("brightest sign is present at index: ", brightestElementIndex)
    # if no element has brightness set to 255, set te first element to 255
    if brightestPresent == False:
        listOfObjectsToDraw[0].setBrightness(255)
        print("no element has brightness set to 255, set te first element to 255")
        # nothing to dim so return:
        return

    #now make the sign below the brightest (but dont go further than the last element in column):
    if brightestElementIndex + 1 < len(listOfObjectsToDraw):
        listOfObjectsToDraw[brightestElementIndex].setBrightness(-10)
        listOfObjectsToDraw[brightestElementIndex+ 1].setBrightness(255)
        print("setting a lower sign as brightest")
        # if element's brightness is more than 0 and it's not 255, dim its brightness:

    for index2, sign2 in enumerate(listOfObjectsToDraw):
        if sign2.getBrightness() > 0 and (sign2.getBrightness() != 255 or int(index2 == screen.get_height()/40-1)):
            sign2.setBrightness(-20)  # dim every element with brightness more than 0
            print("dim every element with brightness more than 0")



def drawObjects(listOfObjectsToDraw):
    for sign in listOfObjectsToDraw:
         #sign.decreaseLifetime()
         pygame.draw.rect(screen, sign.getCurrentColor(), sign)


def drawControlableObject(player):
    pygame.draw.rect(screen, (255,10,10), player)

# Initialize pygame
pygame.init()
# Create a display surface
screen = pygame.display.set_mode((800, 600))
# Set the caption of the window
pygame.display.set_caption("Moving Rectangle")
# Create a clock object
clock = pygame.time.Clock()

#Create objects to draw:
listOfObjectsToDraw = createObjectsToDraw()

# Create a color object
color = pygame.Color(255, 0, 0)

# Create a variable for the game loop
running = True

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

    #update listOfObjectsToDraw
    update(listOfObjectsToDraw)
    #draw signs
    drawObjects(listOfObjectsToDraw)

    #drawControlableObject(player)


    # Update the display
    pygame.display.update()
    # Control the frame rate
    clock.tick(2)

# Quit pygame
pygame.quit()
