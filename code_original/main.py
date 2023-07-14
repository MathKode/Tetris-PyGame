import random
import pygame
pygame.init()

screen = pygame.display.set_mode((520,760))
pygame.display.set_caption("Tetris")

area = []
for y in range(0,760,40):
    ls=[]
    for x in range(0,520,40):
        ls.append(0)
    area.append(ls)

"""
area[5][3] = 1
area[6][4] = 2
area[5][4] = 3
area[3][1] = 4
area[1][1] = 5
"""

#print(area)

        #top, right, left, bottom, middle
couleur=[[(23,23,23),(0,0,0),(23,23,23),(0,0,0),(15,15,15)],
         [(225,0,50),(161,0,44),(200,0,75),(94,0,18),(254,0,86)],
         [(62,175,255),(0,71,161),(0,116,250),(0,34,95),(0,110,230)],
         [(75,245,0),(19,94,1),(70,210,1),(45,161,0),(85,220,1)],
         [(255,223,62),(161,156,0),(253,239,0),(89,94,0),(255,245,0)],
         [(177,0,253),(75,0,93),(175,62,254),(116,0,161),(193,0,255)]
        ]

def cube(screen,x,y,top,right,left,bottom,middle,width,height,tube):
    #Barre du Haut
    pygame.draw.polygon(screen,top,((x,y),(x+width,y),(x+width-tube,y+tube),(x+tube,y+tube)))
    #Barre Gauche
    pygame.draw.polygon(screen,left,((x,y),(x+tube,y+tube),(x+tube,y+height-tube),(x,y+height)))
    #Barre Droite
    pygame.draw.polygon(screen,right,((x+width,y),(x+width-tube,y+tube),(x+width-tube,y+height-tube),(x+width,y+height)))
    #Barre du Bas
    pygame.draw.polygon(screen,bottom,((x,y+height),(x+tube,y+height-tube),(x+width-tube,y+height-tube),(x+width,y+height)))
    #Milieu
    pygame.draw.rect(screen,middle,pygame.Rect(x+tube,y+tube,width-2*tube,height-2*tube))

def possible_move(area,x,y):
    result=[] #RIGHT ; LEFT ; BOTTOM
    try:result.append(area[y][x+1] == 0 and x+1<len(area[0]))
    except:result.append(False)
    try:result.append(area[y][x-1] == 0 and x-1>=0)
    except:result.append(False)
    try:result.append(area[y+1][x] == 0)
    except:result.append(False)
    return result

def new_active_shape():
    shape=[[
             [0,5],[0,6],[0,7],
                   [1,6]
            ],
            [
             [0,5],[0,6],
             [1,5],[1,6]
            ],
            [
             [0,5],[0,6],
                   [1,6],[1,7]
            ],
            [
                   [0,6],[0,7],
             [1,5],[1,6]
            ],
            [
             [0,5],[0,6],[0,7],
                         [1,7]
            ],
            [
                         [0,7],
             [1,5],[1,6],[1,7]
            ],
            [
             [0,5],[0,6],[0,7],[0,8]
            ]
            ]
    active_shape = shape[random.randint(0,65431)%len(shape)]
    active_color = random.randint(1,5)
    return active_shape, active_color

def print_shape(area,shape,color):
    for i in shape:
        area[i[0]][i[1]] = color
    return area

def go_down(area, active_shape, active_color, score):
    old_active_shape = active_shape.copy()
    result = True
    for cube in active_shape:
        move = possible_move(area,cube[1],cube[0])
        #print(move)
        if move[2] == False and [cube[0]+1,cube[1]] not in active_shape:
            #print("NOT POSSIBLE")
            result=False
    if result:
        #Go down:
        index=0
        for i in active_shape:
            active_shape[index] = [i[0]+1,i[1]]
            index+=1
    else :
        score+=1
        #print("END CUBE FALL")
        area, score=line_check(area,score)
        active_shape, active_color = new_active_shape()
        old_active_shape = []
        #Fin de partie test
        apparition_possible=True
        for i in active_shape:
            if area[i[0]][i[1]] !=0:
                apparition_possible=False
        if not apparition_possible:
            print(f"--- END ---\n| Score : \n|      {score}\n-----------")
            exit(0)

    return active_shape, active_color, old_active_shape, area, score

def move_shape(area, active_shape, active_color, direction):
    print_shape(area,active_shape,0)
    result = True
    for cube in active_shape:
        move = possible_move(area,cube[1],cube[0])
        if move[direction] == False:
            if direction == 0: #RIGHT
                if [cube[0],cube[1]+1] not in active_shape:
                    result=False
            elif direction == 1: #LEFT
                if [cube[0],cube[1]-1] not in active_shape:
                    result=False
    if result == True:
        for cube in active_shape:
            if direction==0:
                cube[1] += 1
            elif direction==1:
                cube[1] -=1
    print_shape(area,active_shape,active_color)
    return active_shape, area

def rotate_shape(area, active_shape, active_color):
    #Rotation x->y and y->x From the rotate point
    rotate_point=active_shape[0]
    #print(rotate_point)
    new_shape=[[0,0]]
    for cube in active_shape[1:]:
        y=cube[0]-rotate_point[0]
        x=cube[1]-rotate_point[1]
        new_x = y * -1
        new_y = x 
        #print(y, x, new_y,new_x)
        new_shape.append([new_y,new_x])
    for i in new_shape:
        i[0] += rotate_point[0]
        i[1] += rotate_point[1]
    #Test new shape
    result=True
    for cube in new_shape:
        if area[cube[0]][cube[1]] != 0 and cube not in active_shape:
            result = False
    
    if result:
        #print("rotate Allow")
        area = print_shape(area, active_shape, 0)
        area = print_shape(area, new_shape, active_color)
        return area, new_shape
    return area, active_shape

def line_check(area, score):
    new_area = []
    nb=0
    for line in area:
        if 0 not in line:
            nb+=1
            score+=3
        else:
            new_area.append(line)
    for i in range(nb):
        new_area.insert(0,[0]*len(line))
    return new_area, score

active_shape, active_color = new_active_shape()
area = print_shape(area,active_shape,active_color)

FPS = 25
clock = pygame.time.Clock()

try:
    music = ["code_original/Theme1.mp3","code_original/Theme2.mp3","code_original/Theme3.mp3","code_original/Theme4.mp3","code_original/Theme5.mp3"]
    random.shuffle(music)
    pygame.mixer.music.load(music[0])
    pygame.mixer.music.queue(music[1])
    pygame.mixer.music.queue(music[2])
    pygame.mixer.music.queue(music[3])
    pygame.mixer.music.queue(music[4])
    pygame.mixer.music.play()
except:
    try:
        music = ["Theme1.mp3","Theme2.mp3","Theme3.mp3","Theme4.mp3","Theme5.mp3"]
        random.shuffle(music)
        pygame.mixer.music.load(music[0])
        pygame.mixer.music.queue(music[1])
        pygame.mixer.music.queue(music[2])
        pygame.mixer.music.queue(music[3])
        pygame.mixer.music.queue(music[4])
        pygame.mixer.music.play()
    except:
        pass
game = True
tour = 0
end_tour = 0.7
kright=True
kleft=True
kdown=True
kup=True
tour_total=1
play_time=1
score=0
down_tour=0
while game:
    for event in pygame.event.get():
        try:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and kright:
                    active_shape, area = move_shape(area,active_shape,active_color,0)
                    kright=False
                if event.key == pygame.K_LEFT and kleft:
                    active_shape, area = move_shape(area,active_shape,active_color,1)
                    kleft=False
                if event.key == pygame.K_DOWN and kdown:
                    kdown=False
                    down_tour=0
                    active_shape, active_color, old_active_shape, area, score = go_down(area,active_shape,active_color,score)
                    area = print_shape(area,old_active_shape,0)
                    area = print_shape(area,active_shape,active_color)
                if event.key == pygame.K_UP and kup:
                    kup=False
                    area, active_shape = rotate_shape(area, active_shape, active_color)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    kright=True
                if event.key == pygame.K_LEFT:
                    kleft=True
                if event.key == pygame.K_DOWN:
                    kdown=True
                if event.key == pygame.K_UP:
                    kup=True
        except:
            print("Erreur Mouvemenr")
        if event.type == pygame.QUIT:
            game=False
    
    
    #Affichage block
    """
    Code Couleur:
        0 = Empty
        1 = Red
        2 = Bleu
        3 = Green
        4 = Yellow
        5 = Purple
    """
    y=0
    for row in area:
        x=0
        for column in row:
            if column==0:
                tube=5
            else:
                tube=7
            rgb=couleur[column]
            cube(screen,x,y,rgb[0],rgb[1],rgb[2],rgb[3],rgb[4],40,40,tube)
            x+=40
        y+=40

    pygame.display.flip()
    screen.fill((15,15,15))
    clock.tick(FPS)

    tour += 1
    if tour > int(end_tour*FPS):
        active_shape, active_color, old_active_shape, area, score = go_down(area,active_shape,active_color,score)
        area = print_shape(area,old_active_shape,0)
        area = print_shape(area,active_shape,active_color)
        tour=0

    tour_total+=1
    if tour_total%25==0:
        play_time+=1
    if play_time%20==0 and end_tour>0.5 : #Toutes les 30s
        print("SPEED UP"," "*10)
        end_tour-=0.25
        play_time+=1
    print("Score :",score,end='\r')

    if down_tour>int(FPS/4):
        kdown=True
        down_tour=0
    down_tour+=1
    