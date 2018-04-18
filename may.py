import pygame
import pygame.gfxdraw
import random
import math
import time
pygame.init()

StateMainScreen=1
StateRotateWheel=2
StateStopWheel=3
StateInflateBubble=4
StateWinScreen=5
StateBlink=6
display_width = 1300
display_height = 770
gameState=StateMainScreen
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Çark-ı Şark')

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
spacing=50
rect=(100+spacing, 0+spacing, 600-2*spacing, 600-2*spacing)
cols= ((247,231,28),(66,165,245),(246,166,34),(208,30,28),(73,144,226),(6,176,55),(142,45,162),(126,211,33))
radi=150
clock = pygame.time.Clock()
chosenColor=0
crashed = False
wheelImg = pygame.image.load('cark_dolu.png').convert_alpha()
bg = pygame.image.load('bg.png')
bg2 =pygame.image.load('bg2.png')
prizePic = pygame.image.load('Prize.png')
x =  (display_width * 0.45)
y = (display_height * 0.8)
pi=3.141592
i=0
stopTime=0
speed=0
blinkTimer=0

inSpeed=speed
acc=0

result=1
def draw1cark(screen, color, rect, a1,a2, radi ):
    if a2<a1:
        a2+=pi
    r=a2-a1
    for i in range(10):
        for j in range((i)):
            pygame.draw.arc(screen, color, rect,a1+ (j)*r/i,a1+(j+1)*r/i, radi)


def create_background(width, height):
        colors = [(255, 255, 255), (212, 212, 212)]
        background = pygame.Surface((width, height))
        tile_width = 20
        y = 0
        while y < height:
                x = 0
                while x < width:
                        row = y // tile_width
                        col = x // tile_width
                        pygame.draw.rect(
                                background, 
                                colors[(row + col) % 2],
                                pygame.Rect(x, y, tile_width, tile_width))
                        x += tile_width
                y += tile_width
        return background
def drawRText(text,angle,x,y):
    font = pygame.font.SysFont('Calibri', 25, True, False)
    textW = font.render(text, True, black)
    textW = pygame.transform.rotate(textW, angle*180/pi)
    gameDisplay.blit(textW, [x, y])
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def drawResult(i,x,y):
    global chosenColor
    chosenColor=(int((i/(pi/4))+.5)%8)
    pygame.draw.rect(gameDisplay, cols[chosenColor],(x,y,100,50))
    smallText = pygame.font.SysFont("comicsansms",50)
    textSurf, textRect = text_objects("Color:"+ str(chosenColor), smallText)
    textRect.center = ( (x+(100/2)), (y+(50/2)) )
    gameDisplay.blit(textSurf, textRect)
    drawTriangle(cols[chosenColor])
def drawTriangle(color):
    pygame.draw.polygon(gameDisplay,color,((1120,250),(1140,210),(1170,250)))

def drawCark(i):
    pygame.draw.arc(gameDisplay, cols[0], rect, i-0.03,pi/2+i, radi)
    pygame.draw.arc(gameDisplay, cols[1],rect, i+pi/2-0.03,pi+i, radi)
    pygame.draw.arc(gameDisplay, cols[2], rect, i+pi-0.03,3*pi/2+i, radi)
    pygame.gfxdraw.pie(gameDisplay,rect[1]+200,rect[2]+200,radi, int((i+3*pi/2-0.03)*57.3),int((2*pi+i)*57.3),cols[3])
   # pygame.gfxdraw.arc(gameDisplay, cols[3], rect, i+3*pi/2-0.03,2*pi+i, radi)

def rotateCark():
    global speed,inSpeed,acc,gameState
    speed=0.02*random.randint(10, 20)
    inSpeed=speed
    acc=0.0013*random.randint(10, 20)
    gameState=StateRotateWheel


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()  
                 
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)
def wheel(x,y,i):
    newIm=rot_center(wheelImg,i)
    #gameDisplay.blit(newIm, (x,y))
    #newIm=wheelImg
    blit_alpha(gameDisplay,newIm,(x,y),256)
def drawPrize(x,y,r):
    r2=int(r*402/340)
    scaledPrize=pygame.transform.scale(prizePic,(int(r),int(r2)))
    blit_alpha(gameDisplay,scaledPrize,(x-int(r/2),y-int(r2/2)),256)
def drawGoodCircle(surface,color,center_x,center_y,radius):
    iterations = 150
    for i in range(iterations):
        ang = i * 3.14159 * 2 / iterations
        dx = int(math.cos(ang) * radius/2)
        dy = int(math.sin(ang) * radius/2)
        x = center_x + dx
        y = center_y + dy
        pygame.draw.circle(surface, color, (x, y), int(radius*0.5))
def rotateWheel():
    global i,speed,gameState
    gameDisplay.blit(bg,(0,0))
    #gameDisplay.fill(white)
    if i>pi*2:
        i=0
    i=i-speed
    if speed >inSpeed/100:
        speed=speed*(1-acc)
    else:
        speed=0
        gameState=StateStopWheel
    drawResult(i,370,350)
    #drawCark(i)
    button("Start",0,0,100,50,cols[2],cols[1],rotateCark)
    wheel(810-320,385-320,i*180/pi)
    #drawCark(i)
def stopWheel():
    global gameState, stopTime
    if stopTime<20:
        stopTime+=1
    else:
        stopTime=0
        gameState=StateBlink
def inflateBubble():
    global gameState, stopTime,i
    if stopTime<400:  
        gameDisplay.blit(bg,(0,0))
        wheel(810-320,385-320,i*180/pi)
        drawGoodCircle(gameDisplay,cols[chosenColor],810,385,int(stopTime)+88)
        drawPrize(810,385,(int((stopTime+50)/1.3)))
        stopTime+=80/(stopTime/10+2)
    else:
        stopTime=0
    
        gameState=StateWinScreen
def winScreen():
    button("Start",0,0,100,50,cols[2],cols[1],rotateCark)
    a=0
def blink():
    global gameState,i,blinkTimer
    gameDisplay.blit(bg,(0,0))
    wheel(810-320,385-320,i*180/pi)
    if blinkTimer%16>8:
        drawGoodCircle(gameDisplay,cols[chosenColor],810,385,20+blinkTimer)
    blinkTimer+=1
    if blinkTimer>54:
        gameState=StateInflateBubble
        blinkTimer=0
def mainScreen():
    global i
    gameDisplay.blit(bg,(0,0))
    button("Start",0,0,100,50,cols[2],cols[1],rotateCark)
    wheel(810-320,385-320,i*180/pi)
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    if(gameState==StateMainScreen):
        mainScreen()
    elif(gameState==StateRotateWheel):
        rotateWheel()
    elif(gameState==StateStopWheel):
        stopWheel()
    elif(gameState==StateInflateBubble):
        inflateBubble()
    elif(gameState==StateWinScreen):
        winScreen()
    elif(gameState==StateBlink):
        blink()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()