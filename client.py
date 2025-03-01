import pygame
from network import Network
import pickle
pygame.font.init()

width=500
height=500

win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Client")

class Button:

    def __init__(self,text,x,y,color):
        self.text=text
        self.x=x
        self.y=y
        self.color=color
        self.width=100
        self.height=80

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        font = pygame.font.SysFont("courier_new", 20)
        font.set_bold(True)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))


    def click(self,pos): #passing mouse cursor coordinates as "pos"
        x1=pos[0]
        y1=pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


#Scores
player1sc=0
player2sc=0


def redrawWindow(win,game,p):
    win.fill((128,128,128))
    
    if not(game.connected()):
        font = pygame.font.SysFont("courier_new", 25)
        font.set_bold(True)
        text = font.render("Waiting for Player...", 1, (0,0,150))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("courier_new", 25)
        font.set_bold(True)
        text = font.render("Your Move", 1, (218, 165, 32))
        
        p1Score=font.render(f"Score: {player1sc}",1, (255,255,255))
        p2Score=font.render(f"Score: {player2sc}",1, (255,255,255))
        win.blit(text, (60, 120))

        text = font.render("Opponents", 1, (218, 165, 32))
        win.blit(text, (300, 120))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting..", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting..", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (70, 250))
            win.blit(text1, (310, 250))
            win.blit(p2Score,(0,0))
        else:
            win.blit(text1, (70, 250))
            win.blit(text2, (310, 250))
            win.blit(p1Score,(0,0))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


#Making objects of Button class and storing in btns
btns=[Button("Rock",50,350,(70, 130, 180)),Button("Scissor",200,350,(205, 133, 143)),Button("Paper",350,350,(54, 69, 79))] 


def main():
    global player1sc,player2sc
    run=True
    clock=pygame.time.Clock()
    n=Network()
    player=int(n.getP())
    print("You are player ",player)

    while run:
        clock.tick(60)
        try:
            game=n.send("get")
        except:
            run=False
            print("Couldn't get game!")
            break

        if game.bothWent():  #if both players are current playing
            redrawWindow(win,game,player)   #keep redrawing the game
            pygame.time.delay(500)
            try:
                game=n.send("reset") #after players have made their move and got the result
            except:
                run=False
                print("Couldn't get game")
                break

             #Displaying the result on screen

            font = pygame.font.SysFont("courier_new", 70)
            font.set_bold(True)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (0, 128, 128))
                if player==1:
                    player2sc+=1
                else:
                    player1sc+=1    
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (0, 128, 128))
            else:
                text = font.render("You Lost!", 1, (0, 128, 128))

            win.blit(text, (width/2 - text.get_width()/2, ((height/2 - text.get_height()/2)-40)))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    # Load images
    rock_img = pygame.image.load("rocks.png")
    paper_img = pygame.image.load("paper.png")
    scissors_img = pygame.image.load("scissor.png")

    # Scale images
    rock_img = pygame.transform.scale(rock_img, (70, 70))
    paper_img = pygame.transform.scale(paper_img, (70, 70))
    scissors_img = pygame.transform.scale(scissors_img, (80, 80))

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))

        #Fonts
        font2 = pygame.font.SysFont("courier_new", 25)
        font1 = pygame.font.SysFont("courier_new", 35)
        font1.set_bold(True)
        font1.set_underline(True)

        #Rendering text
        text1 = font1.render("Rock, Paper, Scissor", 1, (0,0,150))
        text2 = font2.render("Click to Play!", 1, (255,255,255))

        #display text and images
        win.blit(text1, (45,120))
        win.blit(text2, (140,200))
        win.blit(rock_img, (210, 300))    
        win.blit(paper_img, (350, 370)) 
        win.blit(scissors_img, (60, 350)) 

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()

