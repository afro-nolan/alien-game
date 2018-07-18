
import pygame
from pygame.locals import *
import math
import random 

#initialise
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False, False, False, False]
playerpos=[100,100]
acc = [0,0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
pygame.display.set_caption("Aliens")
kill_score = 0

#load images
player = pygame.image.load("resources/images/alien1.png")
grass = pygame.image.load("resources/images/space.png")
castle = pygame.image.load("resources/images/planet.png")
arrow = pygame.image.load("resources/images/bullet2.png")
badguyimg1 = pygame.image.load("resources/images/missile.png")
badguyimg=badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

#loop
running = 1
exitcode = 0

#Start Screen
black=(0,0,0)
end_it=False
while (end_it==False):
    screen.fill(black)
    myfont2 = pygame.font.SysFont("Britannic Bold", 64)
    myfont=pygame.font.SysFont("Comic Sans MS", 40)
    myfont1 = pygame.font.SysFont("Comic Sans MS", 24)
    name = myfont2.render("Defeat The Aliens", 1, (255,0,0))
    play_label = myfont1.render("Click to play!", 1, (255, 0, 0))
    rule1 = myfont1.render("W: Up", 24, (255,0,0))
    rule2 = myfont1.render("D: Right", 24, (255,0,0))
    rule3 = myfont1.render("S: Down", 24, (255,0,0))
    rule4 = myfont1.render("A: Left", 24, (255,0,0))
    rule5 = myfont1.render("Right Click: Shoot", 24, (255,0,0))
    
    for event in pygame.event.get():
        if event.type==MOUSEBUTTONDOWN:
            end_it=True
    screen.blit(name, (200, 100))
    screen.blit(play_label,(200,200))
    screen.blit(rule1, (200, 240))
    screen.blit(rule2, (200, 260))
    screen.blit(rule3, (200, 280))
    screen.blit(rule4, (200, 300))
    screen.blit(rule5, (200, 320))
    pygame.display.flip()
while running:
    badtimer -= 1
    
    #clear screen
    screen.fill(0)
    
    #draw elements
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345 ))
    
    #player position + rotation
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    
    #Draw bullets
    for bullet in arrows:
        index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
            
    #draw bad guys
    if badtimer==0:
            badguys.append([640, random.randint(50,430)])
            badtimer=100-(badtimer1*2)
            if badtimer1>=35:
                badtimer1=35
            else:
                badtimer1+=5
    index = 0
    for badguy in badguys:
        if badguy[0]<-64:
            badguys.pop(index)
        badguy[0]-=7
        #Attack planets
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left=badguy[0]
        if badrect.left<64:
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        #Check for collisions
        index1=0
        for bullet in arrows:
            bullrect=pygame.Rect(arrow.get_rect())
            bullrect.left=bullet[1]
            bullrect.top=bullet[2]
            if badrect.colliderect(bullrect):
                acc[0]+=1
                kill_score += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        #Next bad guy
        index+=1
    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    #Draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+str((90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (200,000,000))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)
    
    #Draw health bar
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))
        
    #Draw kill Score
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    text = "Kill Score: " + str(kill_score)
    textsurface = myfont.render(text, False, (200,000,000))
    screen.blit(textsurface,(500, 450))
        
    #update screen
    pygame.display.flip()
    #loop events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        if event.type==pygame.MOUSEBUTTONDOWN:
            position=pygame.mouse.get_pos()
            acc[1]+=1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
            
    #move player
    if keys[0]:
        playerpos[1]-=5
    elif keys[2]:
        playerpos[1]+=5
    if keys[1]:
        playerpos[0]-=5
    elif keys[3]:
        playerpos[0]+=5
    #Win/lose check
    if pygame.time.get_ticks()>=90000:
               running = 0
               exitcode = 1
    if healthvalue<=0:
        running = 0
        exitcode = 0
    if acc[1]!=0:
        accuracy=acc[0]*1.0/acc[1]*100
    else:
        accuracy=0

#Win/lose display
if exitcode==0:
     pygame.font.init()
     font = pygame.font.Font(None, 24)
     output_accuracy = "{:.2f}".format(accuracy)
     text = font.render("Accuracy: "+str(output_accuracy)+"%", True, (255,0,0))
     textRect = text.get_rect()
     textRect.centerx = screen.get_rect().centerx
     textRect.centery = screen.get_rect().centery+24
     screen.blit(gameover, (0,0))
     screen.blit(text, textRect)
        
else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    output_accuracy = "{:.2f}".format(accuracy)
    text = font.render("Accuracy: "+str(output_accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
        
    
        
                

                    
                
            
    
