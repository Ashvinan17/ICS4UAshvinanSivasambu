import pygame
from pygame.locals import *


#side not I watched a lot of youtube videos and looked at a lot of websites and I didnt mark it down exactly which part
# I got from videos so I will do that but for no I will just put the titles and url for the websites and vieos i Wated


#Pygame in 90 Minutes - For Beginners This is probably the biggest most helpful one
#https://www.youtube.com/watch?v=jO6qQDNa2UY

# Creating a platformer in Pygame with a camera, collisions, animation states and particle effects
# #https://www.youtube.com/watch?v=YWN8GcmJ-jA
#https://coderslegacy.com/python/pygame-platformer-game-development/
# coders legacy
# https://www.youtube.com/watch?v=uWvb3QzA48c
# Pygame Platformer Part 1: Setting Up



# initializing pygame
pygame.init()
# I dont really understand this but it looks cool so im keeping it, all I heard about is it fixes the frame rate and
# gives some consistensy to the game
clock = pygame.time.Clock()
fps = 60

# this is too create the game window, when i am just on my laptop I use 800x 800 when im on my monitor I use 1000 x 1000
screen_width = 1000
screen_height = 800
# this is too display the actual screen and your using the width and heights from the previous lines
screen = pygame.display.set_mode((screen_width, screen_height))
# Giving the game its not using the the built in caption function
pygame.display.set_caption('Ashvinans crazy cool awesome never to be beat game')

# here we are loading in the images from the folders that have been important into the main code, you import the folders
# just by dragging them into the main.
# here I am just loading in too images that I want the background to have which are the sun and the sky
sun_img = pygame.image.load('plswork/sunnn.png')
bg_img = pygame.image.load('plswork/sky.jpg')

# define game variables
# this is gow big each tile is in the map
tile_size = 50

# game over = 0 means that the game is not over
game_over = 0


# this is just to break down the game into tiles so its easier for me to see the map properly and add things
# it is in range for 20 because 50 x 20 =1000
# this isnt very necessary anymore because all it did was break it down and give clear indication of each tile
def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


# *********************************PLAYER STUFF*********************************************8

# Class for the user player
# took insparation from Creating a platformer in Pygame with a camera, collisions, animation states and particle effects
#https://www.youtube.com/watch?v=YWN8GcmJ-jA

class Player():
    # x and y coordinates are necessary for the player
    def __init__(self, x, y):
        #initilazies objects atrributes
        #self.images_right = []
        self.index = 0
        # loading in the playable character
        img = pygame.image.load('imgpython/wreck.png')
        self.image = pygame.transform.scale(img, (40, 80))
        # this is just to create a rectangle, it will be 40 by 80 pixels
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # this is used to give the player a coordinate
        self.rect.x = x
        self.rect.y = y
        # this is used for the jumping, he is on the ground as a defult
        self.vel_y = 0
        # this will stop the player from continuously floating after pressing jump
        self.jumped = False
        # we need to add game over here or there will be an error

    def update(self, game_over):
        # base coordinates for the player, this is for when the user will move it and change dx and dy
        dx = 0
        dy = 0

        # everything to about line 205 will run when game_over =0 because thats when the player is alive
        if game_over == 0:
            # this lets us use keys to move the player
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                # how high they will jump
                self.vel_y = -12
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False

            # these are too move the player horizontally
            # how fast they will move
            if key[pygame.K_LEFT]:
                dx -= 7
            if key[pygame.K_RIGHT]:
                dx += 7
            # this is creating the gravity for the player
            self.vel_y += 1
            # the player will never go pass the value of 10
            if self.vel_y > 10:
                self.vel_y = 10
                # player will jump up by this number
            dy += self.vel_y


            # **************************COLLISION*******************************************************************

            # tiles apart of the world class
            for tile in world.tilelist:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    # once he collides he stops moving hence dx= 0
                    dx = 0
                # check for collision in y direction
                # we use colliderect because all of my images are rectangles already
                # self.rect.x and rect.y are just the x and y coordinates, it just takes the width and height of the
                # image
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping, this is just to add collision for when the user jumps
                    # and hits a block on top of them
                    if self.vel_y < 0:
                        # limits how far he moves, he moves intell he hits his head
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

                    # checking for collision with enemies
                    # we use the sprite command to see if they have collided
                    # using the group will check if any one the gingers have been collided
                if pygame.sprite.spritecollide(self, GingerGuyGroup, False):
                    game_over = -1
                    # -1 is for when player dies

                # checking for lava
                # this is basically the same thing as the enemy group
                if pygame.sprite.spritecollide(self, lavaGroup, False):
                    game_over = -1

            # this is where the player will change coordinates due to the key pressing
            self.rect.x += dx
            self.rect.y += dy

            # this draws the player
            screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        # the 2 creates a 2 pixel wide rectangle, it took the outline of the picture and drew a a rectangle around it

        return game_over


# class for the actualy world and terrain of the map
class World():
    def __init__(self, data):
        #we need this tilelist empty list so we can append the tiles that correlate to the specific position so that
        # if I called 1 it would print a dirt block
        self.tilelist = []
        # creating list for later
        # loading in dirt so it can be the border of the map aswell as being dirt on the map
        dirt_img = pygame.image.load('plswork2/dirtgood.jpg')
        # grass is at the top and where the player walks on
        grass_img = pygame.image.load('imgpython/goodgrass.jpg')

        rows = 0
        for row in data:
            # coloumn count
            col_count = 0
            for tile in row:
                # this directly correlates with the world data, if tile is 1 it will print a dirt image
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    # tile size and the transform scale will transform it so it fits the tile size that I want
                    # img,get.rect will basically just create a rectangle
                    img_rect = img.get_rect()
                    # coloumn is going horizontal so you multiply it by the tile size to get the x coordinate
                    img_rect.x = col_count * tile_size
                    # row is going vertical so you multiply it by the tile size to get the y coordinate
                    img_rect.y = rows * tile_size
                    tile = (img, img_rect)
                    # the tile list comes into use here letting you have the picture, and the rectangle in the list
                    self.tilelist.append(tile)
                if tile == 2:
                    # if tile is 2 it will print a grass block
                    # this transforms it to the size of the tile in width and height
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    # turning it into a rectangle
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = rows * tile_size
                    tile = (img, img_rect)
                    self.tilelist.append(tile)
                # this is for the enemy  x is dependant on col count and y is dependant on row count
                if tile == 3:
                    # we do +10 so it can stand normally on the block, I got this by trial and error
                    GingerGuy = Enemy(col_count * tile_size, rows * tile_size + 10)
                    # adding the sort of list
                    GingerGuyGroup.add(GingerGuy)
                # til ==4 will be lava
                if tile == 4:
                    # making the coordinates for lava
                    lava = Lava(col_count * tile_size, rows * tile_size + (tile_size // 2))
                    lavaGroup.add(lava)
                # every time you go through one of the tiles and you move onto the next one it goes up by one
                col_count += 1
                # when you go through all the coloumns in a row and move onto the next one row count goes up by 1
            rows += 1

    # the only purpose of this is too draw the dirt around the barriers and tile 0 is literally nothing
    def draw(self):
        for tile in self.tilelist:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
            # the 2 makes it not a white screen


# ***************************ADDING ENEMIES**********************************

# we want the enemies to have movement so I cant include them in my grass, dirt area so we need to make a class
# pygame has sprite which gives objects different properties like height colour and movement, I am specifically using
# this for movement since the player is not controlling the enemy. Sprite is built into pygame

# found out about sprite through this
#https://coderslegacy.com/python/pygame-platformer-game-development/
# coders legacy

class Enemy(pygame.sprite.Sprite):
    # x and y coordinates
    def __init__(self, x, y):
        # calling the constructor from the superclass
        pygame.sprite.Sprite.__init__(self)
        # loading in the enemy character
        self.image = pygame.image.load('ginger guy/ginger.jpg')
        self.image = pygame.transform.scale(self.image, (40, 40))
        # making the player a rectangle
        self.rect = self.image.get_rect()
        # coordinates for rectangle
        self.rect.x = x
        self.rect.y = y
        # creating a move function default for the enemy
        self.move_direction = 1
        # setting up a counter for when they flip
        self.move_counter = 0

    def update(self):
        # the base x coordinate will move witht the addition to the move direction now
        self.rect.x += self.move_direction
        self.move_counter += 1
        # if it goes above 50 it will flip
        # abs will make the value always positive
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


# **************************************ADDING LAVA*************************


# we are using the same things as enemy with the sprite except we are not using movements in this
class Lava(pygame.sprite.Sprite):
    # we use x and y coordinates
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # loading in the lava image
        img = pygame.image.load('LavasoHot/Lava.gif')
        # we scale the lava to the tilze size for width and half the size of a tile for height of lava
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        # turning it into a rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



# The world data is for the map and where blocks will be placed 0 is nothing 1 is dirt and 2 is grass
# I put dirt around the borders of the map
# This huge list is to decide where everything will be on the map in summary

# 5 is going to be coins
# 6 is going to be exiting to another level

# found out about what this thing below can do through this video
# https://www.youtube.com/watch?v=uWvb3QzA48c
# Pygame Platformer Part 1: Setting Up
world_data = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 5, 0, 0, 2, 2, 2, 0, 0, 2, 2, 4, 4, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 3, 0, 2, 0, 3, 0, 2, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 4, 2, 4, 2, 4, 2, 4, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 2, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
# the coordinates for the player is going to be 100 on the x and sincee pixels are 50 pixels tall and the player
# is 80 tiles tall it is screen_height - 130 pixels
player = Player(100, screen_height - 130)

# kind of like a list where you could add enemies into
GingerGuyGroup = pygame.sprite.Group()

lavaGroup = pygame.sprite.Group()
# this is just putting the world_ data apart of the World class
world = World(world_data)

# run= True this just shows that the game is running
run = True
# as long as its set to true the game code will work
while run:
    clock.tick(fps)
    # to show an image on the display you have to use the blit function, you first choose which display I only have one
    # which is screen then you have to choose the coordinates for where you want the images
    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    world.draw()
    # if the game over is 0 then when it is -1 the enemies will stop moving once the player dies
    if game_over == 0:
        GingerGuyGroup.update()

    # adding bad guy to display screen
    GingerGuyGroup.draw(screen)

    # adding lava to display screen
    lavaGroup.draw(screen)
    game_over = player.update(game_over)

    # event has a lot of different things you can do with it but pygame.QUIT lets you press the top right x to exit
    # the display then you also have to set run run to x so that the program will stop running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # the pygame. display update is basically telling us that it will use all the code that is given for the display
    # without it nothing would display
    pygame.display.update()

pygame.quit()

# April 18 2022 10:50 am We have failed at adding animations to my program
# I thought I was making progress but the game woudnt run and I didnt know why
# I wasted an hour of my weekend and now I am sad
