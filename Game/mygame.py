import pygame
import random
#import mysprites
pygame.init()
dis_w=700
dis_h=700

gameDisplay = pygame.display.set_mode((dis_w,dis_h))
pygame.display.set_caption('Space Shooter')

clock = pygame.time.Clock()
crashed = False

BGImg = pygame.image.load('BG2.jpg').convert()
BGImg1=pygame.image.load('BG2.jpg').convert()

####################

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('hmmm.png').convert_alpha()
        self.ship_h=125
        self.ship_w=120
        self.rect=self.image.get_rect()
        self.rect.x=350-65
        self.rect.y=585
        self.died=0
    def update(self):
        global move
        if self.died==0 :
            self.rect.x+=move

####################

class bullets(pygame.sprite.Sprite):
    def __init__(self,ship) :
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('bullet.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.x=ship.rect.x+ship.ship_w/2
        self.rect.y=dis_h-ship.ship_h
        self.speed=-10
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y+24<0:
            global score
            global scorestr
            score-=2
            scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))
            self.kill() 

####################

class asters(pygame.sprite.Sprite) :
    def __init__(self,image) :
        pygame.sprite.Sprite.__init__(self)
        self.image=image
        self.imageorig=image
        self.rect=self.image.get_rect()
        self.rect.y=random.randrange(-200,-100)
        self.rect.x=random.randrange(30,dis_w-self.image.get_rect()[3])
        self.speedy=random.randrange(2,4)
        self.center=self.rect.center
        self.rotsp=random.randrange(-2,2)
        self.rot=0
        self.last_time=pygame.time.get_ticks()

    def update(self) :
        self.rotate()
        self.rect.y+=self.speedy
        if self.rect.y>700:
            global score
            global scorestr
            score-=2
            scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))
            self.stagain()
    
    def rotate(self):
        now=pygame.time.get_ticks()
        if now>self.last_time+50:
            self.last_time=now
            self.rot+=self.rotsp
            self.rot%=360
            self.center=self.rect.center
            self.image=pygame.transform.rotate(self.imageorig,self.rot)
            self.rect=self.image.get_rect()
            self.rect.center=self.center
    
    def stagain(self):
        self.speedy=random.randrange(2,4)
        self.rotsp=random.randrange(-10,10)
        self.rot=0
        self.rect.y=random.randrange(-200,-100)
        self.rect.x=random.randrange(30,dis_w-self.image.get_rect()[3])

##########################

class explosion(pygame.sprite.Sprite) :
    def __init__(self,ast=None):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for i in range(1,6):
            img=pygame.image.load('exp{}.png'.format(i)).convert_alpha()
            img=pygame.transform.scale(img,ast.image.get_size())
            self.images.append(img)
        self.tct=0
        self.image=self.images[0]
        self.rect=self.image.get_rect()
        self.rect.center=ast.rect.center
        self.center=ast.rect.center
        self.aste=ast
        if type(ast).__name__ == 'asters' :
            ast.speedy=0
    def update(self):
        f=0
        self.image=self.images[self.tct//4]
        self.rect=self.image.get_rect()
        self.rect.center=self.center
        self.tct+=1
        if f==0 and self.tct>8 :
            if type(self.aste).__name__ == 'asters' :
                self.aste.stagain()
            else:
                global ship
                ship.kill()
            f=1
        if self.tct==20 :
            self.kill()


###########################
#Groups

Ast=pygame.sprite.Group()
mod1=pygame.image.load('med1.png').convert_alpha()
a1=asters(mod1)
mod2=pygame.image.load('meteorBrown_big.png').convert_alpha()
a2=asters(mod2)
mod3=pygame.image.load('meteorBrown_big1.png').convert_alpha()
a3=asters(mod3)
mod4=pygame.image.load('meteorBrown_med1.png').convert_alpha()
a4=asters(mod4)
mod5=pygame.image.load('meteorBrown_med2.png').convert_alpha()
a5=asters(mod5)
Ast.add(a1,a2,a3,a4,a5)

ship=player()
Ship=pygame.sprite.Group()
Ship.add(ship)

Bullets=pygame.sprite.Group()

Explosions=pygame.sprite.Group()

##############################
x=0
a=0
FPS=60
bul_time=0
smst=0
slowmo=0
move=0

fire=pygame.image.load('menu.png').convert_alpha()
font=pygame.font.Font('pac/Pacifico.ttf',40)
font1=pygame.font.Font('pac/Pacifico.ttf',20)
name=font.render('SPACE SHOOTER',True,(255,0,0))
Scorefont=pygame.font.Font('amatic/Amatic-Bold.ttf',30)
score=0
lives=5
scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))


#Pause menu
def pausemenu(Ast,Ship,Bullets,Explosions,scorestr):
    yet=True
    col=0
    while yet:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    yet=False
                elif event.key == pygame.K_q:
                    exit()
        col+=1
        if col//20 % 2 == 0:
            ins=font.render('Resume : Esc    Quit : Q',True,(255,255,0))
        else:
            ins=font.render('Resume : Esc    Quit : Q',True,(255,0,255))
        Ast.draw(gameDisplay)
        Ship.draw(gameDisplay)
        Bullets.draw(gameDisplay)
        Explosions.draw(gameDisplay)
        gameDisplay.blit(scorestr,(10,10))
        gameDisplay.blit(ins,(130,330))
        pygame.display.update()
        clock.tick(FPS)

#Gameover
def gameover(BGImg,scorestr):
    ft=pygame.time.get_ticks()
    nt=0
    yet=True
    font=pygame.font.Font('amatic/Amatic-Bold.ttf',80)
    st=font.render('GAME OVER',True,(255,255,255))
    while yet:
        nt=pygame.time.get_ticks()
        if nt-ft>3000:
            break
        
        gameDisplay.blit(BGImg,(0,0))
        gameDisplay.blit(scorestr,(230,250))
        gameDisplay.blit(st,(220,310))
        pygame.display.update()
        clock.tick(FPS)
    startmenu()



#Start menu
def startmenu():
    col=0
    yet=True
    while yet:
        a=0
        gameDisplay.blit(BGImg,(0,a))
        gameDisplay.blit(BGImg1,(0,a-dis_h))
        a+=1
        a%=dis_h
        gameDisplay.blit(fire,(50,70))
        gameDisplay.blit(name,(170,230))
        col+=1
        if col//20 % 2 == 0:
            ins=font1.render('Click Enter to play',True,(255,255,0))
            ins1=font1.render('A,D : Move    SPACE : Shoot',True,(255,0,255))
            ins2=font1.render('Esc : Pause',True,(255,255,0))
        else:
            ins=font1.render('Click Enter to play',True,(255,0,255))
            ins1=font1.render('A,D : Move    SPACE : Shoot',True,(255,255,0))
            ins2=font1.render('Esc : Pause',True,(255,0,255))
        gameDisplay.blit(ins,(280,500))
        gameDisplay.blit(ins1,(220,560))
        gameDisplay.blit(ins2,(300,620))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN :
                if event.key==pygame.K_RETURN:
                    yet=False
        clock.tick(FPS)

###################################
startmenu()
while not crashed:

#moving background
    gameDisplay.blit(BGImg,(0,a))
    gameDisplay.blit(BGImg1,(0,a-dis_h))
    a+=1
    a%=dis_h
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
#ship movement and bullet creation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a :
                move=-7
            elif event.key == pygame.K_d :
                move=7
            elif event.key == pygame.K_SPACE:
                nw=pygame.time.get_ticks()
                if nw>bul_time+50 :
                    bul_time=nw
                    bul=bullets(ship)
                    Bullets.add(bul)
            elif event.key == pygame.K_ESCAPE :
                pausemenu(Ast,Ship,Bullets,Explosions,scorestr)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and move==-7 :
                move=0
            elif event.key == pygame.K_d and move==7 :
                move=0
    if ship.rect.x+move<=dis_w-ship.ship_w and ship.rect.x+move>=0 :
        Ship.update()

#slowmo
    if slowmo>0 :
        if slowmo==1:
            smst=pygame.time.get_ticks()
            slowmo=2
            FPS=20
        if slowmo==2:
            smet=pygame.time.get_ticks()
            if smet>smst+300:
                for i in Ast:
                    expl=explosion(i)
                    Explosions.add(expl)
                    slowmo=3
        if slowmo==3:
            smet=pygame.time.get_ticks()
            if smet>smst+1000:
                FPS=60
                slowmo=0
                if lives==0:
                    Bullets.empty()
                    for i in Ast:
                        i.stagain()
                    Explosions.empty()
                    gameover(BGImg,scorestr)
                    startmenu()
                    lives=5
                    score=0
                    scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))
                ship=player()
                Ship.add(ship)


#Blasts
    blasts=pygame.sprite.groupcollide(Ast,Bullets,False,True)
    for rock in blasts:
        if len(blasts[rock])>0:
            expl=explosion(rock)
            Explosions.add(expl)
            score+=1
            scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))

    blasts=pygame.sprite.spritecollide(ship,Ast,False,pygame.sprite.collide_rect_ratio(0.7))
    if len(blasts)>0:
        for i in blasts:
            if type(i).__name__=='asters':
                expl=explosion(i)
                Explosions.add(expl)
        expl=explosion(ship)
        Explosions.add(expl)
        if ship.died == 0:
            lives-=1
        scorestr=Scorefont.render('SCORE : {}  Lives left : {}'.format(score,lives),True,(255,255,255))
        ship.died=1
        slowmo=1


#Display updates
    Ast.update()
    Bullets.update()
    Explosions.update()
    Ast.draw(gameDisplay)
    Ship.draw(gameDisplay)
    Bullets.draw(gameDisplay)
    Explosions.draw(gameDisplay)
    gameDisplay.blit(scorestr,(10,10))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()