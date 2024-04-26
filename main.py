import pygame
pygame.init()
import os 
import random


# constants


FPS=60

WHITE=(255,255,255)
BLACK=(0,0,0)
WIDTH,HEIGHT=800,400
GROUND=pygame.image.load(os.path.join('resorce','ground.png'))
SKY=pygame.image.load(os.path.join('resorce','Sky.png'))
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
STATIC_IMAGE=pygame.image.load(os.path.join('resorce','Player','player_stand.png'))
STATIC_IMAGE=pygame.transform.rotozoom(STATIC_IMAGE,0,2)
STATIC_IMAGE_RECT=STATIC_IMAGE.get_rect(center=(WIDTH//2,HEIGHT//2))
SPEED= 7
FONT=pygame.font.Font(os.path.join('font','best.ttf'))



pygame.display.set_caption("PIXEL GAME")


create_obsacle = pygame.USEREVENT + 1
pygame.time.set_timer(create_obsacle,900)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1=pygame.image.load(os.path.join('resorce','Player','player_walk_1.png')).convert_alpha()
        player_walk_2=pygame.image.load(os.path.join('resorce','Player','player_walk_2.png')).convert_alpha()
        self.players = [player_walk_1,player_walk_2]
        self.player_index=0
        self.image=self.players[self.player_index]
        self.rect=self.image.get_rect(bottomleft=(80,300))

    def animation(self):
        if self.rect.bottom >= 300:
             self.player_index +=0.1
             self.image=self.players[round(self.player_index)]
             if self.player_index > 1:
                self.player_index=0
             self.image=self.players[round(self.player_index)]
        else:
            self.image=pygame.image.load(os.path.join('resorce','Player','jump.png')).convert_alpha()
    def jump(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.rect.bottom >= 300:
                self.rect.y -= 150
    def fall(self):
        self.rect.bottom +=5
        if self.rect.bottom > 300:
            self.rect.bottom =300
    
    

    def update(self):
       
        self.animation()
        self.jump()
        self.fall()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == "snail":
            snail1=pygame.image.load(os.path.join('resorce','snail','snail1.png')).convert_alpha()
            snail2=pygame.image.load(os.path.join('resorce','snail','snail2.png')).convert_alpha()
            self.images=[snail1,snail2]
            self.index=0
            self.image=self.images[self.index]
            self.x=random.randint(900,1200)
            self.y=300
            self.rect=self.image.get_rect(bottomleft=(self.x,self.y))
            
        else:
            fly1=pygame.image.load(os.path.join('resorce','Fly','Fly1.png')).convert_alpha()
            fly2=pygame.image.load(os.path.join('resorce','Fly','Fly2.png')).convert_alpha()
            self.images=[fly1,fly2]
            self.index=0
            self.image=self.images[self.index]
            self.y=150
            self.x=random.randint(900,1200)
            self.rect = self.image.get_rect(bottomleft=(self.x,self.y))
    def animation(self):
            self.index += 0.1
            if self.index > 1:
                self.index = 0
            self.image=self.images[round(self.index)]

    def move(self):
        self.x -= SPEED
        if self.x < - 100:
            self.kill()

        self.rect=self.image.get_rect(bottomleft=(self.x,self.y))
    
        


    def update(self):
        self.move()
        self.animation()  



player=Player()
player_group=pygame.sprite.GroupSingle()
player_group.add(player)
obstacle_group=pygame.sprite.Group()


game_active=False
def collide():
    if pygame.sprite.spritecollide(player,obstacle_group,False):return False
    else: return True


 
def draw(score_surf,score_surf_rect):
    WIN.blit(SKY,(0,0))
    WIN.blit(GROUND,(0,300))
    player_group.draw(WIN)
    player_group.update()
    obstacle_group.draw(WIN)
    obstacle_group.update()
    WIN.blit(score_surf,score_surf_rect)

    pygame.display.update()
def main():
  
    clock=pygame.time.Clock()
    run=True
    CONSTUCT = 0

    while run:
        game_active=collide()
        clock.tick(FPS)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break
            
            if game_active:
                if event.type == create_obsacle:
                    tp=random.choice(['fly','snail','snail','snail'])
                    objstacle=Obstacle(tp)
                    obstacle_group.add(objstacle)



        
        if game_active:
            SCORE = pygame.time.get_ticks()//1000
            SCORE= SCORE - CONSTUCT
            score_surf=pygame.transform.rotozoom(FONT.render(f'SCORE: {SCORE}',False,BLACK),0,2)
            score_surf_rect=score_surf.get_rect(center=(WIDTH//2,50))
            draw(score_surf,score_surf_rect)
        elif not game_active:
            CONSTUCT = pygame.time.get_ticks() // 1000
            WIN.fill((87,149,175))
            WIN.blit(STATIC_IMAGE,STATIC_IMAGE_RECT)
            WIN.blit(score_surf,(360,350))
            restart=pygame.transform.rotozoom(FONT.render('PRESS SPACE KEY TO RESTART',False,BLACK),0,2)
            WIN.blit(restart,(310,70))
            pygame.display.update()
            keys=pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                game_active = True
                obstacle_group.empty()

            
            pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()
