import pygame
from pygame import key
import random
import copy 
import time

pygame.init() #game initialise
screen=pygame.display.set_mode((1000,1000)) #makes screen

#important variable and functions:
#RGB Value

black   =(0,0,0)
white   =(255,255,255)
yellow  =(255,200,0)
green   =(0,255,0)
red     =(255,0,0)
blue    =(0,180,255)
green   =(0,255,0)
gray    =(200,200,200)

def img(string, coordx, coordy):
    image=pygame.image.load(string)
    screen.blit(image,(coordx-50,coordy-50))
def sounds(x):
    pygame.mixer.Sound("sounds/"+x).play()
def text(string, coordx, coordy, fontSize,text_color=(130,130,130),font='arial'):
    font = pygame.font.SysFont(font,int(fontSize)) 
    text = font.render(str(string), True,text_color) 
    textRect = text.get_rect()
    textRect.center = (coordx,coordy+5) 
    screen.blit(text, textRect)
def rect(x,y,w,h,color=(220,220,220)):
    pygame.draw.rect(screen,color,[x,y,w,h])
def draw_grid(grid_color=white):
    for i in range(0,10):
        rect(i*100,0,1,900,grid_color)    
        rect(0,i*100,900,1,grid_color)
        rect(i*300,0,6,900,grid_color)    
        rect(0,i*300,900,6,grid_color)

#-----------------PUZZLE GENERATION---------------
empty=[[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0]]
que=copy.deepcopy(empty)
gen=copy.deepcopy(empty)

#tells whether its possible to put a number in a particular square
def possible(y,x,n,puz=gen):
    for i in range(9):
        if puz[y][i]==n:
            return False
        elif puz[i][x]==n:
            return False
    p=y-(y%3)
    q=x-(x%3)
    for i in range(p,p+3):
        for j in range(q,q+3):
            if puz[i][j]==n:
                return False
    return True

#gives coordinates of empty square
def zero(puz=gen):
    for i in range(9):
        for j in range(9):
            if puz[i][j]==0:
                return(j,i)
    return False

#uses possible() and zero() ,it goes to an empty square and tries to put
#a number in the sqaure, if possible ,it will put it and go to next empty
#square through recursion. If it gets stuck, it will back-track
#and go to previous empty square and try another number.

def generate_puzzle(difficulty):
    global gen
    gen=copy.deepcopy(empty)
    def generate(puz=gen):
        global que
        if zero(puz)!=False:
            (x,y)=zero(puz)
            for i in range(1,10):
                n=random.randrange(1,10)
                if possible(y,x,n,puz):
                    puz[y][x]=n
                    if generate(puz=gen):
                        return True
                    puz[y][x]=0
        else:
            que=copy.deepcopy(puz)
            return puz
    generate()
    difficulty(que)

#
#difficulties
def easy(puz=que):
    for i in range(20):
        x=random.randrange(0,9)
        y=random.randrange(0,9)
        puz[y][x]=0
def medium(puz=que):
    for i in range(40):
        x=random.randrange(0,9)
        y=random.randrange(0,9)
        puz[y][x]=0
def hard(puz=que):
    for i in range(60):
        x=random.randrange(0,9)
        y=random.randrange(0,9)
        puz[y][x]=0
    
#----------------MAIN MENU------------------
class button:
    def __init__(self,x,y,size,color):
        self.x=x
        self.y=y
        self.size=size
        self.color=color

congrats=0
def mainmenu():
#buttons on screen:
    play=button(500,400,75,black)
    solve=button(500,500,75,black)
    classic=button(300,500,60,black)
    color=button(700,500,60,black)
    easy_diff=button(200,600,60,black)
    medium_diff=button(500,600,60,black)
    hard_diff=button(800,600,60,black)
    go=button(500,800,75,black)
    quit=button(500,800,75,black)

    def draw_grid():
        for i in range(0,10):
            rect(i*100+50,50,1,900)    
            rect(50,i*100+50,900,1)
            rect(i*300+50,50,6,900)    
            rect(50,i*300+50,900,6)
    
    font='consolas'
    def background():
        screen.fill(white)
        draw_grid()
        generate_puzzle(easy)
        background_puzzle=copy.deepcopy(que)
        for i in range(0,9):
            for j in range(0,9):            
                current_square=background_puzzle[i][j]
                x=100+100*j
                y=100+100*i
                if current_square==0:
                    text("  ", x, y, 60,(100,100,100),font)
                else:
                    text(current_square, x, y, 60,(170,170,170),font)

    def congratulation(time=60):
        background()
        text("CONGRATS!",500, 400, 120,green,'consolas')        
        text("Score:"+str(time)+"s!",500, 550, 120,black,'consolas')        
    global congrats
    congrats=congratulation
    page=1
    menu=True
    gamemode='classic'
    difficulty=easy
    while menu:
        background()
        text("SUDOKU", 500, 200, 125,(0,0,0),font)
        text("PLAY", play.x, play.y,play.size,play.color,font)        
        if page==1:
            text("SOLVE",solve.x, solve.y,solve.size,solve.color,font)
            text("Quit",quit.x,quit.y,quit.size,quit.color,font)
        if page!=1:
            text("classic",classic.x, classic.y, classic.size,classic.color,font)
            text("color",color.x, color.y, color.size,color.color,font)
        if page==3:
            text("easy",easy_diff.x, easy_diff.y, easy_diff.size,easy_diff.color,font)
            text("medium",medium_diff.x, medium_diff.y, medium_diff.size,medium_diff.color,font)
            text("hard",hard_diff.x,hard_diff.y,hard_diff.size,hard_diff.color,font)
            text("GO",go.x, go.y,go.size,go.color,font)
            
        for ev in pygame.event.get():    
#quit----
            if ev.type==pygame.QUIT:
                menu=False
            if ev.type==pygame.KEYDOWN:
                keys=ev.key
#mouse----
            if ev.type==pygame.MOUSEMOTION:
                m=pygame.mouse.get_pos()
                (mx,my)=m
                mouse_in_play=abs(mx-play.x)<100 and abs(my-play.y)<30
                mouse_in_solve=abs(mx-solve.x)<120 and abs(my-solve.y)<30
                mouse_in_classic=abs(mx-classic.x)<140 and abs(my-classic.y)<30
                mouse_in_color=abs(mx-color.x)<120 and abs(my-color.y)<30
                mouse_in_easy=abs(mx-easy_diff.x)<120 and abs(my-easy_diff.y)<30
                mouse_in_medium=abs(mx-medium_diff.x)<120 and abs(my-medium_diff.y)<30
                mouse_in_hard=abs(mx-hard_diff.x)<120 and abs(my-hard_diff.y)<30
                mouse_in_go=abs(mx-go.x)<70 and abs (my-go.y)<60
                mouse_in_quit=abs(mx-quit.x)<70 and abs (my-quit.y)<40

                if page==1:    
                    if mouse_in_play:   play.color=yellow
                    else:               play.color=black
                    if mouse_in_solve:  solve.color=yellow
                    else:               solve.color=black
                    if mouse_in_quit:   quit.color=yellow
                    else:               quit.color=black
                elif page==3:
                    if mouse_in_go:     go.color=yellow
                    else:               go.color=black

            if ev.type==pygame.MOUSEBUTTONDOWN:
                if page==1:
                    if mouse_in_play:
                        sounds("click.wav")
                        page=2
                        play.color=yellow
                    if mouse_in_solve:
                        sounds("click.wav")
                        solve_game()
                    if mouse_in_quit:
                        menu=False
                else:
                    if mouse_in_play:
                        sounds("click.wav")
                        page=1
                        classic.color,color.color=black,black
                if page!=1:
                    if mouse_in_classic or mouse_in_color:
                        sounds("click.wav")
                        page=3
                        color.color=black
                        classic.color=black
                    if mouse_in_classic:
                        gamemode='classic'
                        classic.color=yellow
                    if mouse_in_color:
                        gamemode='color'
                        color.color=yellow
                if page==3:
                    if mouse_in_easy or mouse_in_medium or mouse_in_hard:
                        sounds("click.wav")
                        easy_diff.color=black
                        medium_diff.color=black
                        hard_diff.color=black
                    if mouse_in_easy:
                        difficulty=easy
                        easy_diff.color=yellow
                    if mouse_in_medium:
                        difficulty=medium
                        medium_diff.color=yellow
                    if mouse_in_hard:
                        difficulty=hard
                        hard_diff.color=yellow
                    if mouse_in_go:
                        sounds("click.wav")
                        if gamemode=='classic':
                            play_game(difficulty)
                        elif gamemode=='color':
                            play_color(difficulty)
        text("BY:Aditya Rao        Sakthe Balan A        Abhishek SV", 500, 975, 25,black,font)
        pygame.display.flip()

#CLASSIC GAMEMODE:
def play_game(difficulty):
    generate_puzzle(difficulty)
    start_time=time.time()
    question_state=copy.deepcopy(que)
    cal=copy.deepcopy(question_state)
    ans=copy.deepcopy(gen)
    current_square=cal[0][0]
    end=False 
    hint=False 
    hint_time=0 
    (mx,my)=(0,0)
    inverted_text_color =black
    text_color          =white
#
    def reset():
        nonlocal cal
        nonlocal question_state
        nonlocal click
        nonlocal start_time
        nonlocal user_guess
        nonlocal ans
        ans= copy.deepcopy(gen)
        question_state=copy.deepcopy(que)
        click=False
        start_time=time.time()
        user_guess=0
        cal=copy.deepcopy(question_state)

    wallpaper=1
    user_guess=0  
    click=False
    running =True
    while running:
        current_time=time.time()
        img("wallpaper/"+str(wallpaper)+".png",50,50)
        for ev in pygame.event.get():    
#quit----
            if ev.type==pygame.QUIT:
                running=False            
#keyboard----
            if ev.type==pygame.KEYDOWN:
                keys=ev.key
                if keys==pygame.K_w: 
                    wallpaper_choice=[1,2]
                    wallpaper_choice.remove(wallpaper)
                    wallpaper=random.choice(wallpaper_choice)
                if keys==pygame.K_h:
                    hint_time=time.time()
                    hint=True
                if keys==pygame.K_TAB:
                    generate_puzzle(difficulty)
                    reset()
#
                if keys==pygame.K_r:        reset()
                if keys==pygame.K_1:        user_guess=1
                elif keys==pygame.K_2:      user_guess=2
                elif keys==pygame.K_3:      user_guess=3
                elif keys==pygame.K_4:      user_guess=4
                elif keys==pygame.K_5:      user_guess=5
                elif keys==pygame.K_6:      user_guess=6
                elif keys==pygame.K_7:      user_guess=7
                elif keys==pygame.K_8:      user_guess=8
                elif keys==pygame.K_9:      user_guess=9
                elif keys==pygame.K_0:      user_guess=0
#mouse----
            if ev.type==pygame.MOUSEBUTTONDOWN:
                m=pygame.mouse.get_pos()
                (mx,my)=m   
                if my<900:          click=True
                elif my>900:
                    sounds("click.wav")
                    if mx<100:      user_guess=1
                    elif mx<200:    user_guess=2
                    elif mx<300:    user_guess=3
                    elif mx<400:    user_guess=4
                    elif mx<500:    user_guess=5
                    elif mx<600:    user_guess=6
                    elif mx<700:    user_guess=7
                    elif mx<800:    user_guess=8
                    elif mx<900:    user_guess=9
                    elif mx<1000:   user_guess=0

#putting numbers on screen-------
        for i in range(0,9):
            for j in range(0,9):
                question=question_state[i][j]
                current_square=cal[i][j]
                answer=ans[i][j]
                x=50+100*j
                y=50+100*i
                mouse_in_square=abs(x-mx)<50 and abs(y-my)<50
                if click:
                    if mouse_in_square:
                        if current_square==0 and user_guess==0:
                            pass
                        elif question==0:
                            cal[i][j]=user_guess
                            sounds("click.wav")
                        click=False

                if current_square==0:                       text("  ", x, y, 60,text_color)
                elif current_square==user_guess and hint==False: text(current_square, x, y, 60 ,yellow)
                elif current_square==question:              text(current_square, x, y, 60,white)  
                elif hint:
                    if current_square==answer:              text(current_square, x, y, 60,green)                            
                    else:                                   text(current_square, x, y, 60,red)                                        
                else:                                       text(current_square, x, y, 60,blue)
                if cal[i][j]!=ans[i][j]:                    end=False

#putting options at bottom----
        for k in range(0,10):
            if k!=0:
                rect(100*k-80,920,60,60,text_color)
                text(k, (100*k-50), 950, 60,inverted_text_color)        
                if k==user_guess:       
                    rect(100*k-80,920,60,60,inverted_text_color)            
                    text(k, 100*k-50, 950, 60,text_color)
            else:
                rect(920,920,60,60,text_color)
                text(str(0), 950, 950, 60,inverted_text_color)
                if k==user_guess:       
                    rect(920,920,60,60,inverted_text_color)            
                    text(0, 950, 950, 60,text_color)

#putting timer and hint at side of screen----
        if hint==0:
            rect(920,120,60,60,text_color)
            text("H", 950, 146, 50,inverted_text_color)
        elif hint==1:
            rect(920,120,60,60,green)
            text("H", 950, 146, 50,text_color)
        if hint and (current_time-hint_time>1):
            hint=False

        if end==False:
            draw_grid()
            timer=int(current_time-start_time)
            text(timer,950, 50, 50,text_color)
        if end:
            congrats(str(timer))
        end=True 
        pygame.display.flip()

#COLOR MODE:
def play_color(difficulty):
    generate_puzzle(difficulty)
    start_time=time.time()
    question_state=copy.deepcopy(que)
    cal=copy.deepcopy(question_state)
    ans=copy.deepcopy(gen)

    current_square=cal[0][0]
    end=False 
    (mx,my)=(0,0)  #will hold mouse position
    background_color =white #background color
    wallpaper=2
    def draw_grid():
        for i in range(0,10):
            rect(i*100-2,0-2,4,903,black)    
            rect(0-2,i*100-2,903,4,black)
            rect(i*300-4,0-4,8,903,gray)    
            rect(0-4,i*300-4,903,8,gray)

    def reset():
        nonlocal cal
        nonlocal question_state
        nonlocal click
        nonlocal start_time
        nonlocal user_guess
        nonlocal ans
        ans= copy.deepcopy(gen)
        question_state=copy.deepcopy(que)
        click=False
        start_time=time.time()
        user_guess=0
        cal=copy.deepcopy(question_state)

    screen.fill(background_color)
    user_guess=0  #hold user guesses
    click=False  #check if mouse is clicked
    running=True 

    while running:
        current_time=time.time()
        img("wallpaper/"+str(wallpaper)+".png",50,50)
        for ev in pygame.event.get():    
#quit----
            if ev.type==pygame.QUIT:    running=False            
#keyboard----
            if ev.type==pygame.KEYDOWN:
                keys=ev.key
                if keys==pygame.K_TAB:
                    generate_puzzle(difficulty)
                    reset()
                if keys==pygame.K_r:    reset()
                if keys==pygame.K_1:    user_guess=1
                elif keys==pygame.K_2:  user_guess=2
                elif keys==pygame.K_3:  user_guess=3
                elif keys==pygame.K_4:  user_guess=4
                elif keys==pygame.K_5:  user_guess=5
                elif keys==pygame.K_6:  user_guess=6
                elif keys==pygame.K_7:  user_guess=7
                elif keys==pygame.K_8:  user_guess=8
                elif keys==pygame.K_9:  user_guess=9
                elif keys==pygame.K_0:  user_guess=0
#mouse----
            if ev.type==pygame.MOUSEBUTTONDOWN:
                m=pygame.mouse.get_pos()
                (mx,my)=m   
                if my<900:          click=True
                elif my>900:
                    sounds("click.wav")
                    if mx<100:      user_guess=1
                    elif mx<200:    user_guess=2
                    elif mx<300:    user_guess=3
                    elif mx<400:    user_guess=4
                    elif mx<500:    user_guess=5
                    elif mx<600:    user_guess=6
                    elif mx<700:    user_guess=7
                    elif mx<800:    user_guess=8
                    elif mx<900:    user_guess=9
                    elif mx<1000:   user_guess=0
#putting numbers on screen-------
        for i in range(0,9):
            for j in range(0,9):
                question=question_state[i][j]
                current_square=cal[i][j]
                answer=ans[i][j]
                x=50+100*j
                y=50+100*i
                mouse_in_square=abs(x-mx)<50 and abs(y-my)<50
                if click:
                    if mouse_in_square:
                        if current_square==0 and user_guess==0:
                            pass
                        elif question==0:
                            cal[i][j]=user_guess
                            sounds("click.wav")
                        click=False
                if current_square==0:
                    rect(x-50,y-50,100,100,black)
                elif current_square==user_guess and user_guess !=0:
                    img("color/yellow_border/"+str(user_guess)+".png",x,y)
                elif current_square==question:
                    img("color/"+str(current_square)+".png",x,y)
                else:                     
                    img("color/white_border/"+str(current_square)+".png",x,y)
                if current_square!=answer:
                    end=False
#putting options at bottom----
        for k in range(0,10):
            if k!=0:
                rect(100*k-90,910,80,80,black)
                img("color/option/"+str(k)+".png",100*k-30,970)      
                if k==user_guess:
                    rect(100*k-90,910,80,80,yellow)
                    img("color/option/"+str(k)+".png",100*k-30,970)      
            else:
                rect(910,910,80,80,black)
                rect(920,920,60,60,white)
                if k==user_guess:
                    rect(910,910,80,80,yellow)
                    rect(920,920,60,60,white)
        if end==False:
            draw_grid()
            timer=int(current_time-start_time)
            text(timer,950, 50, 40,white)
        if end:
            congrats(str(timer)) 
        end=True 
        pygame.display.flip()

#--------SOLVER--------
def solve_game():
    cal=copy.deepcopy(empty)
    temp=copy.deepcopy(empty)
    current_square=cal[0][0]
    (mx,my)=(0,0)  #will hold mouse position
    keys=0
    solve=False
    solve_start=0
    solve_end=0
    background_color =black #background color
    text_color       =white #text color
    wallpaper=1

    def reset():
        nonlocal cal
        nonlocal click
        nonlocal solve
        click=False
        cal=copy.deepcopy(temp)
        solve=False

    def solver(puz=cal):
        nonlocal solve_end
        solve_end=time.time()
        if solve_end-solve_start>2:
            return False
        if zero(puz)!=False:
            (x,y)=zero(puz)
            for i in range(1,10):
                n=solve_order[i-1]
                if possible(y,x,n,cal):
                    puz[y][x]=n
                    if solver(puz=cal):
                        return True
                    puz[y][x]=0
        else:
            return puz
    def Enter():
        nonlocal solve
        nonlocal solve_start
        reset()
        solve=True
        solve_start=time.time()
        random.shuffle(solve_order)
        solver(cal)
    screen.fill(background_color)
    solve_order=[1,2,3,4,5,6,7,8,9]
    user_guess=0  
    click=False
    solving =True 

    while solving:
        img("wallpaper/"+str(wallpaper)+".png",50,50)
        for ev in pygame.event.get():    
#quit----
            if ev.type==pygame.QUIT:    solving=False            
#keyboard----
            if ev.type==pygame.KEYDOWN:
                keys=ev.key
                if keys==pygame.K_RETURN:
                    Enter()
                if keys==pygame.K_w:
                    wallpaper_choice=[1,2]
                    wallpaper_choice.remove(wallpaper)
                    wallpaper=random.choice(wallpaper_choice)
                if keys==pygame.K_r:    reset()
                if keys==pygame.K_1:    user_guess=1
                elif keys==pygame.K_2:  user_guess=2
                elif keys==pygame.K_3:  user_guess=3
                elif keys==pygame.K_4:  user_guess=4
                elif keys==pygame.K_5:  user_guess=5
                elif keys==pygame.K_6:  user_guess=6
                elif keys==pygame.K_7:  user_guess=7
                elif keys==pygame.K_8:  user_guess=8
                elif keys==pygame.K_9:  user_guess=9
                elif keys==pygame.K_0:  user_guess=0
#mouse----
            if ev.type==pygame.MOUSEBUTTONDOWN:
                m=pygame.mouse.get_pos()
                (mx,my)=m   
                if my<900:          click=True
                elif my>900:
                    sounds("click.wav")
                    if mx<100:      user_guess=1
                    elif mx<200:    user_guess=2
                    elif mx<300:    user_guess=3
                    elif mx<400:    user_guess=4
                    elif mx<500:    user_guess=5
                    elif mx<600:    user_guess=6
                    elif mx<700:    user_guess=7
                    elif mx<800:    user_guess=8
                    elif mx<900:    user_guess=9
                    elif mx<1000:   user_guess=0
#putting numbers on screen-------
        for i in range(0,9):
            for j in range(0,9):
                current_square=cal[i][j]
                x=50+100*j
                y=50+100*i            
                mouse_in_square=abs(x-mx)<50 and abs(y-my)<50
                if click:
                    if mouse_in_square:
                        if user_guess==0:
                            cal[i][j]=user_guess
                            temp[i][j]=user_guess
                            sounds("click.wav")
                            click=False
                        elif possible(i,j,user_guess,temp):
                            cal[i][j]=user_guess
                            temp[i][j]=user_guess
                            sounds("click.wav")
                            click=False
                if current_square==0:
                    text("  ", x, y, 60,text_color)
                elif temp[i][j]!=cal[i][j]:
                    text(current_square, x, y, 60 ,yellow)
                else:
                    text(current_square, x, y, 60,text_color)
#putting options at bottom----
        for k in range(0,10):
            if k!=0:
                rect(100*k-80,920,60,60,text_color)
                text(k, (100*k-50), 950, 60,background_color)        
                if k==user_guess:       
                    rect(100*k-80,920,60,60,background_color)            
                    text(k, 100*k-50, 950, 60,text_color)
            else:
                rect(920,920,60,60,text_color)
                text(str(0), 950, 950, 60,background_color)
                if k==user_guess:
                    rect(920,920,60,60,background_color)            
                    text(0, 950, 950, 60,text_color)
        mouse_in_enter=abs(950-mx)<30 and abs(455-my)<335
        if click and mouse_in_enter:
            Enter()
            click=False
        if solve==True:
            if zero(cal)==False:
                rect(920,20,60,60,black)
                rect(925,25,50,50,green)
            else:
                rect(920,20,60,60,black)
                rect(925,25,50,50,red)
        rect(920,120,60,670,black)
        rect(925,125,50,660,white)
        draw_grid()
        pygame.display.flip()

if __name__=="__main__":
    mainmenu()