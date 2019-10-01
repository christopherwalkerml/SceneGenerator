import random,pygame,os,math,sys 
from tkinter import *
pygame.init() 

font = pygame.font.Font(None, 60) 

dir = os.path.dirname(os.path.realpath(__file__)) 

moon = pygame.image.load(dir+'\moon.png') 
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,50) 

sys.setrecursionlimit(1000000000) 

scrnwid = 1200 
scrnhig = 650 
win = pygame.display.set_mode((scrnwid,scrnhig)) 
time = 'day' 

BLACK = (0, 0, 0) 
WHITE = (255, 255, 255) 
GREY = (130, 130, 130) 
DDGREY = (30, 30, 30) 

RED = (255, 0, 0) 
ORANGE = (255, 127, 0) 
YELLOW = (255, 255, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255) 
INDIGO = (127, 0, 255) 
VIOLET = (255, 0, 255) 

DGREY = (71, 71, 71) 
BLUE = (0, 0, 255) 
LGREEN = (112, 255, 102) 
LWGREEN = (193, 255, 188) 

#BARKS
SAKURABARK = (130, 24, 1) 
BIRCHBARK = (224, 224, 224) 
OAKBARK = (165, 90, 28) 

#LEAVES
SAKURALEAF = (255, 191, 197) 
BIRCHLEAF = (61, 186, 59) 
OAKLEAF = (75, 132, 45) 

#GROUND
DARKGRASS = (85, 188, 77) 

#BACKGROUND
LIGHTBLUE = (107, 162, 249) 
NIGHTBLUE = (18, 47, 94) 

#global vars
CLOCK = pygame.time.Clock() 

#classes

class flower():

    def __init__(self, colour, x, y):
        self.colour = colour 
        self.x = x  #flower x
        self.petals = [[x, y, r(scrnhig - 100, scrnhig - 5), [True, r(200, 400)]]]  #petals x and y, and choose a random spot to die at on the floor
        self.petalsamt = 1 
        self.y = y  #flower y
        self.size = r(1,4) 
        self.ptimer = 0 
        self.ptmax = r(200,500) 
        flowerlist.append(self) 

    def draw(self):
        createflower(int(self.x - 5),int(self.y - 5),(360 / 9),9,5,self.colour)  #make this input not require (360/n)
        if self.colour == SAKURALEAF:
            self.ptimer += 1 
            for n,p in enumerate(self.petals):
                if (p[1] > ((scrnhig - 100) + self.y) / 2 and self.petalsamt < 2) or self.ptimer >= self.ptmax:
                    self.ptimer = 0 
                    self.petals.append([self.x, self.y, r(scrnhig - 100, scrnhig - 5), [True, r(200, 400)]]) #add a new petal if the current petal is halfway to the ground
                    self.petalsamt += 1 
                if p[0] > -10 and p[0] < scrnwid + 10 and p[1] >= -10 and p[1] < p[2]:
                    pygame.draw.circle(win, self.colour, (math.ceil(p[0]), math.ceil(p[1])), self.size) 
                    p[0] -= direc[0] * r(1,3) 
                    p[1] -= direc[1] * r(1,3)  #make the petal move with wind and gravity
                else:
                    if p[3][0] == True:
                        p[3][0] = False 
                        self.petalsamt -= 1 
                    p[3][1] -= 1 
                    if p[3][1] < 0:
                        del self.petals[n]  #delete the petal if it goes below the grass
                    pygame.draw.circle(win, self.colour, (math.ceil(p[0]), math.ceil(p[1])), self.size) 

class cloud():

    def __init__(self, colour, x, y, mode):
        self.colour = colour 
        self.x = x  #cloud x
        self.y = y  #cloud y
        self.mode = mode  #mode (ex: rain, snow, none)
        self.size = r(20,25) 
        self.blobs = r(5,9) 
        self.speed = direc[0] * r(2,4) 
        self.xylist = createcloud(0, 0, self.blobs, self.blobs, self.size, self.colour, []) #initialize the cloud blobs
        self.rainlist = []
        cloudlist.append(self)

    def draw(self):
        if self.speed < 0:
            if self.x - 100 > scrnwid:
                self.x = -200 
            else:
                self.x -= self.speed  #make sure that the clouds dont go past the screen borders
        elif self.speed > 0:
            if self.x + 250 < 0:
                self.x = scrnwid + 100 
            else:
                self.x -= self.speed 
        
        for xy in self.xylist:
            pygame.draw.circle(win, self.colour, (math.ceil(self.x + xy[0]), math.ceil(self.y + xy[1])), self.size)  #draw all the cloud blobs
        if self.mode == "rain": #if the weather is rainy
            for n,rains in enumerate(self.rainlist):
                pygame.draw.rect(win, BLUE, (math.ceil(rains[0]), math.ceil(rains[1]), 1, 1 + (direc[1] * 20)))  #draw each rain bit
                rains[0] -= direc[0] 
                rains[1] -= direc[1] * (20 + r(-1,3))  #make the rain move with gravity and wind
                if rains[1] > rains[2]:
                    del self.rainlist[n]  #delete the rain bit if it goes below the grass
            if r(0,8) == 0:
                self.rainlist.append([r(5, scrnwid - 5), 0, r(scrnhig - 100, scrnhig - 50)])  #add a new rain bit randomly

        elif self.mode == "snow": #if the weather is snowy
            for n,rains in enumerate(self.rainlist):
                if rains[2] == 1 or rains[2] == 8:
                    rains[3] *= -1 
                rains[2] += rains[3] 
                rains[1] -= (direc[1] * 5)  #make the snow move with gravity and wind
                rains[0] += (direc[0] * 5) 
                pygame.draw.circle(win, WHITE, (math.ceil(rains[0]), math.ceil(rains[1])), rains[2])  #draw each snowflake
                if rains[1] > scrnhig - 100:
                    del self.rainlist[n]  #delete the snowflake if it goes below the grass
            if r(0,15) == 0:
                self.rainlist.append([r(5, scrnwid - 5), 0, 1, -1])  #add a new snowflake randomly

class grass():

    def __init__(self, x, y, colour):
        self.x = x 
        self.y = y 
        self.colour = colour 
        if r(0,3) == 0:
            self.flowercol = (r(0,255), r(0,255), r(0,255)) 
        else:
            self.flowercol = 'none' 
        self.angle = math.pi * 3/2 
        self.angle2 = 0 
        self.sin = r(-1,1) 
        grasslist.append(self) 

    def draw(self):
        self.sin += 0.05 
        self.angle2 = math.sin(self.sin) * (math.pi * 1/8) 
        creategrass(self.x, self.y, self.angle, self.angle2, 10, 4, self.colour, 3, self.flowercol)

class thesun():

    def __init__(self, x ,y):
        self.changexy = 3.2 
        self.x = x  #set the sun x and y
        self.y = y 
        self.sunsin = 0 
        self.surf = pygame.Surface((scrnwid, scrnhig))  #create the time and moon surfaces
        self.lightsurf = pygame.Surface((scrnwid, scrnhig)) 
        self.lightsurf.fill((195, 195, 195)) 
        self.lightsurf.set_alpha(180) 
        self.lighttimer = r(300,600)  #set lightning variables
        for l in range(r(1,4)):
            self.ls = lightning(r(20, scrnwid - 20), 0, self.lightsurf)
        if weather[2] == GREY:
            self.surf.fill(DDGREY) 
        else:
            self.surf.fill(NIGHTBLUE) 
        self.rainsurf = drawbow() 
        self.surf.set_alpha(0) 

    def draw(self):
        global time
        if weather[2] == GREY:
            self.lighttimer -= 1 
            if self.lighttimer < 1:
                win.blit(self.ls, (0, 0)) 
                self.ls.set_alpha(self.ls.get_alpha() - 1) 
                if self.ls.get_alpha() == 0:
                    self.lighttimer = r(300,600) 
                    self.ls.set_alpha(180) 
                    for l in range(r(1,4)):
                        self.ls = lightning(r(20, scrnwid - 20), 0, self.lightsurf)
        self.changexy += 0.005 
        drawx = self.x + (((math.cos(self.changexy)) * (scrnwid / 2)))  #move the sun in an arc
        drawy = self.y + (((math.sin(self.changexy)) * (scrnhig))) 
        drawmx = self.x - (((math.cos(self.changexy)) * (scrnwid / 2)))  #move the moon in an arc
        drawmy = self.y - (((math.sin(self.changexy)) * (scrnhig))) 
        self.sunsin += 0.1 
        alphachange = 2 
        if drawy < scrnhig and self.surf.get_alpha() > 0:
            self.surf.set_alpha(self.surf.get_alpha() - alphachange) 
            self.rainsurf.set_alpha(self.rainsurf.get_alpha() + alphachange)  #make day and night fade in and out. Same for rainbows
            time = 'day' 
        elif drawy > scrnhig and self.surf.get_alpha() < 150:
            self.surf.set_alpha(self.surf.get_alpha() + alphachange) 
            self.rainsurf.set_alpha(self.rainsurf.get_alpha() - alphachange) 
            time = 'night' 
        win.blit(moon, (drawmx, drawmy)) 
        if weather[2] == LIGHTBLUE and weather[1] == 'rain':
            win.blit(self.rainsurf, (scrnwid / 3, scrnhig / 3))  #draw the moon, rainbow, and sun
        drawsun(drawx, drawy, 0, 50 + (math.sin(self.sunsin) * 20) , 360, YELLOW)  #move the sun across the sky

#regular functions

def drawbow():
    cols = [RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, VIOLET] 
    size = 600 
    rainsurf = pygame.Surface((1200, 1200)) 
    rainsurf.fill(LIGHTBLUE) 
    rainsurf.set_alpha(150) 
    for c in cols:
        pygame.draw.circle(rainsurf, c, (600, 600), size, 10) 
        size -= 10 
        
    return rainsurf 

def r(x1, x2):
    return random.randrange(x1,x2) 

def makescene(scene): #create the scene depending on the tree type
    global treelist, flowerlist, cloudlist, direc, weather, grasslist, mountainlist, rainbow, sun
    treelist = []  #make a list of all the branches
    cloudlist = []  #make a list of all the clouds
    flowerlist = []  #make a list of all the flowers
    grasslist = []  #make a list of grass pieces
    mountainlist = [] 
    if scene[0] == 'random':
        direc = (random.randrange(-5, 5) / 10, random.randrange(-4, -1) / 10)  #create a wind direction and speed
        weather = random.choice([['clear', 'none', LIGHTBLUE, DARKGRASS, LGREEN], [WHITE, 'none', LIGHTBLUE, DARKGRASS, LGREEN],
                                 [GREY, 'none', LIGHTBLUE, DARKGRASS, LGREEN], [DGREY, 'rain', GREY, DARKGRASS, LGREEN],
                                 ['clear', 'none', LIGHTBLUE, WHITE, LWGREEN], [WHITE, 'snow', LIGHTBLUE, WHITE, LWGREEN], [WHITE, 'none', LIGHTBLUE, WHITE, LWGREEN],
                                 [WHITE, 'rain', LIGHTBLUE, DARKGRASS, LGREEN]])         
        scene[0] = random.choice(['sakura', 'birch', 'oak'])
    else:
        weather = [scene[1], scene[2], scene[3], scene[4], scene[5]] 
        direc = (scene[6][0], scene[6][1])  #create a wind direction and speed

    #create mountains
    mountnum = r(1,4) 
    for ml in range(mountnum):
        rm = r(2,5) 
        if ml == 0:
            frac1 = 0 
            frac2 = (ml + 1 / mountnum) 
        else:
            frac1 = (ml / mountnum) 
            frac2 = ((ml + 1) / mountnum) 
        mountains(r(int(frac1 * scrnwid), int(frac2 * scrnwid)), rm, rm) 
    for gl in range(r(50,80)): #create grass
        grass(r(5, scrnwid - 5), r(scrnhig - 95, scrnhig - 5), weather[4])
    if weather[0] != "clear":
        for c in range(r(2, 8)): #create the weather (clouds, rain, snow etc)
            cld = cloud(weather[0], (scrnwid / 2) + r(-(scrnwid / 2), (scrnwid / 2)), 60 + r(-20,40), weather[1])  #create clouds with the weather. Clouds control rain
    if scene[0] == 'sakura': #create the trees depending on what type they are
        fractree(500 + (r(100,200)), scrnhig - 100, (math.pi * 3/2), 120, 10, SAKURABARK, 24, 3, SAKURALEAF) 
        fractree(500 + (r(-300,-200)), scrnhig - 100, (math.pi * 3/2), 80, 6, SAKURABARK, 12, 2, SAKURALEAF) 
    elif scene[0] == 'birch':
        fractree(500 + (r(-100,100)), scrnhig - 100, (math.pi * 3/2), 120, 10, BIRCHBARK, 24, 3, BIRCHLEAF) 
    elif scene[0] == 'oak':
        fractree(500 + (r(-100,100)), scrnhig - 100, (math.pi * 3/2), 120, 10, OAKBARK, 24, 3, OAKLEAF) 

    sun = thesun(scrnwid / 2, scrnhig) 
    
    if weather[0] == WHITE and weather[1] == 'rain':
        rainbow = True 
    else:
        rainbow = False 

#recursive functions

def lightning(x1, y1, surf, d = 0):
    if y1 >= scrnhig:
        return 
    else:
        x2 = x1 - r(-9,9)  #create a tree by changing the angle, length, and size of branches. Then create flower/leaf objects
        y2 = y1 + r(8,14) 
        pygame.draw.line(surf, WHITE, (x1,y1), (x2,y2), 2) 
        if d == 0:
            lightning(x2, y2, surf) 
            if r(0,6) > 4:
                lightning(x2, y2, surf, 1) 
            if r(0,6) > 4:
                lightning(x2, y2, surf, 1) 
        if r(0,5) > 3:
            if r(0,6) > 4:
                lightning(x2, y2, surf, 1) 
            if r(0,6) > 4:
                lightning(x2, y2, surf, 1) 
    return surf 

def mountains(rx, n, totn):
    if n > 0:
        ry = ((totn - n) / totn) * (scrnhig - 100) + r(20,50) 
        sy = (scrnhig - 100) 
        rc = r(140,160)  #add the mountain to the mountain list so that it can be drawn every frame
        m = [((rx, ry), (rx - (r(120, 200) * (n / totn)), sy),(rx + (r(100, 150) * (n / totn)), sy)), (rc, rc, rc)] 
        mountainlist.append(m) 
        pygame.draw.polygon(win, m[1], m[0])  #draw the mountain (unneccessary because it will be draw in the game loop)
        #snowcap height calculation : height of mountain * 0.25
        #then add the top position of the mountain so it fits properly
        #so... ((scrnhig - 100) * 0.25) + (0 + ((totn - n) / totn) * scrnhig)
        yy = ((sy - ry) * 0.25) + ry 
        ##############
        #now its time to calculate the first x position of the snowcap. This is some fun math, might I add.
        #x1 will need to be equal to the left width of the mountain, then multiplied by .25
        x1 = rx - ((rx - m[0][1][0]) * 0.25) 
        #x2 will need to be the same, but for the right width
        x2 = rx + ((m[0][2][0] - rx) * 0.25) 
        #these are the snowcap's coordinates \/
        m1 = [((rx, ry), (math.ceil(x1), yy), (math.ceil(x2), yy)), WHITE] 
        mountainlist.append(m1)  #append the mountain cap to the mountain list
        pygame.draw.polygon(win, m1[1], m1[0])  #draw the snowcap (unneccessary because it will be draw in the game loop)
        mountains(rx + r(20,160), n - 1, totn) 
        mountains(rx - r(20,160), n - 1, totn) 
    else:
        return 
    

def drawsun(x,y,angle,size,n,colour):
    if n > 1:
        x2 = x + (math.cos(angle) * size) 
        y2 = y + (math.sin(angle) * size) 
        pygame.draw.line(win, colour, (math.ceil(x), math.ceil(y)), (x2, y2), 1) 
        drawsun(int(x), int(y), angle + .1, size, n - 2, colour) 
    elif n <= 2:
        pygame.draw.circle(win, colour, (x, y), 31) 
    else:
        return 

def createcloud(x, y, blobs, n, size, colour, xylist): #recurse and create a cloud, and return the x and y of each cloud blob for future drawing
    pygame.draw.circle(win, colour, (math.ceil(x), math.ceil(y)), size + r(-3,3)) 
    x += ((size + r(-2,3)) / 2) 
    y += r(-5,5) 
    xylist.append([x, y]) 
    if n > 1:
        return createcloud(x, y, blobs, n - 1, size, colour, xylist) 
    else:
        return xylist  #return the x and y positions for each cloud blob

def createflower(x,y,petals,n,size,colour): #create a flower through recursion
    x -= int((size + 1) * math.cos(petals)) 
    y += int((size + 1) * math.sin(petals)) 
    pygame.draw.circle(win, colour, (x, y), size, 0)  #draw a circle out of circles
    if n > 1:
        createflower(x,y,petals+.9,n - 1,size,colour) 
    else:
        return 

def creategrass(x1, y1, angle, angle2, length, n, colour, width, flowercol):
    if n < 1:
        return 
    else:
        x2 = x1 - (length * math.cos(angle))  #create a tree by changing the angle, length, and size of branches. Then create flower/leaf objects
        y2 = y1 + (length * math.sin(angle)) 
        pygame.draw.line(win, colour, (x1,y1), (x2,y2), width) 
        n -= 1 
        if width > 1:
            width -= 1 
        if n > 1:
            creategrass(x2, y2, angle + angle2, angle2, length, n, colour, width, flowercol) 
        elif n == 1:
            if flowercol != 'none':
                pygame.draw.circle(win, flowercol, (round(x2), round(y2)), 3) 

def fractree(x1, y1, angle, length, n, colour, width, nwidth, leaf):
    if n < 1:
        return 
    else:
        x2 = x1 - (length * math.cos(angle))  #create a tree by changing the angle, length, and size of branches. Then create flower/leaf objects
        y2 = y1 + (length * math.sin(angle)) 
        length /= 1.5 
        pygame.draw.line(win, colour, (x1,y1), (x2,y2), width) 
        treelist.append([x1, y1, x2, y2, colour, width, n, leaf]) 
        n -= 1 
        if width > nwidth:
            width -= nwidth 
        if n > 1:
            fractree(x2, y2, angle - (r(35,95) / 100), length + (n * r(0,3)), n, colour, width, nwidth, leaf) 
            fractree(x2, y2, angle + (r(35,95) / 100), length + (n * r(0,3)), n, colour, width, nwidth, leaf) 
        if n < 3:
            if weather[3] != WHITE:
                f = flower(leaf, int(x2 - 5),int(y2 - 5)) 
                f.draw() 

#choose a beginning scene
#format: ['sakura,oak,birch'            - tree type
        #'clear', WHITE, DGREY          - cloud colour / type
        #'clear/rain/snow'              - weather
        #LIGHTBLUE, GREY,               - sky colour
        #DARKGRASS, WHITE               - ground colour
        #'LGREEN'                       - grass colour
        #(-0.5 -> 0.5, -0.4 -> -0.1)    - wind x speed, wind y speed
#examples:
#makescene(['oak', 'clear', 'clear', LIGHTBLUE, DARKGRASS, LGREEN, (0.3, -0.1)]) 
#makescene(['birch', DGREY, 'rain', GREY, DARKGRASS, LGREEN, (-0.2, -0.4)]) 
#or
#makescene(['random']) 

#My favourite:
makescene(['sakura', WHITE, 'rain', LIGHTBLUE, DARKGRASS, LGREEN, (0.3, -0.3)]) 
#if reuse is not commented out, it will remake the same one each time, but a little variated
same = False 
'''
def reuse():
    global same
    same = True 
    makescene(['sakura', WHITE, 'rain', LIGHTBLUE, DARKGRASS, LGREEN, (0.3, -0.3)]) 
reuse()
'''
#if you want to set your own scene with tkinter, set choose to True. Otherwise set it to false, and use the makescene() function

####################################################################################################################################

choose = True 

if choose:

    enter = Tk()  #make the tkinter inputs, and make sure that they are proper inputs

    label1 = Label(enter, text='Tree (sakura, oak, birch)')
    E1 = Entry(enter, bd = 1)
    label2 = Label(enter, text='Clouds (clear, WHITE, GREY)')
    E2 = Entry(enter, bd = 1)
    label3 = Label(enter, text='Weather (clear, rain, snow)')
    E3 = Entry(enter, bd = 1)
    label4 = Label(enter, text='Sky Colour (LIGHTBLUE, GREY)')
    E4 = Entry(enter, bd = 1)
    label5 = Label(enter, text='Ground Colour (DARKGRASS, WHITE)')
    E5 = Entry(enter, bd = 1)
    label6 = Label(enter, text='Grass Colour (LGREEN, LWGREEN)')
    E6 = Entry(enter, bd = 1)
    label7 = Label(enter, text='Wind x (-0.5 -> 0.5)')
    E7 = Entry(enter, bd = 1)
    label8 = Label(enter, text='Wind y (-0.4 -> -0.1)')
    E8 = Entry(enter, bd = 1)

    labels = [label1, E1, label2, E2, label3, E3, label4, E4, label5, E5, label6, E6, label7, E7, label8, E8] 

    def rando():
        makescene(['random']) 
        enter.destroy() 
        return 

    def setscene():
        if E1.get() != 'sakura' and E1.get() != 'oak' and E1.get() != 'birch':
            rando() 
        else:
            var1 = E1.get() 
            
        if E2.get() != 'clear' and E2.get() != 'WHITE' and E2.get() != 'GREY':
            rando() 
        elif E2.get() == 'WHITE':
            var2 = WHITE 
        elif E2.get() == 'GREY':
            var2 = GREY 
        else:
            var2 = 'clear' 
                
        if E3.get() != 'clear' and E3.get() != 'rain' and E3.get() != 'snow':
            rando() 
        else:
            var3 = E3.get() 
        
        if E4.get() != 'LIGHTBLUE' and E4.get() != 'GREY':
            rando() 
        elif E4.get() == 'LIGHTBLUE':
            var4 = LIGHTBLUE 
        elif E4.get() == 'GREY':
            var4 = GREY 

        if E5.get() != 'DARKGRASS' and E5.get() != 'WHITE':
            rando() 
        elif E5.get() == 'DARKGRASS':
            var5 = DARKGRASS 
        elif E5.get() == 'WHITE':
            var5 = WHITE 

        if E6.get() != 'LGREEN':
            rando() 
        elif E6.get() == 'LGREEN':
            var6 = LGREEN 

        try:
            float(E7.get()) 
            var7 = float(E7.get()) 
        except ValueError:
            rando() 

        try:
            float(E8.get()) 
            var8 = float(E8.get()) 
        except ValueError:
            rando() 

        makescene([var1, var2, var3, var4, var5, var6, (var7, var8)]) 
        enter.destroy() 

    ENTER = Button(enter, text ='Enter', command = setscene)

    for lx in labels:
        lx.pack()
    ENTER.pack(side = BOTTOM) 
    enter.mainloop()
    
####################################################################################################################################
while True:
    CLOCK.tick(60)
    win.fill(weather[2])  #redraw the scenery each frame to update rain, clouds, petals, etc
    sun.draw()  #draw the sun behind everything except the sky
    pygame.draw.rect(win, weather[3], (0, scrnhig - 100, scrnwid, 100))
    for m in mountainlist:
        pygame.draw.polygon(win, m[1], m[0]) 
    for c in cloudlist:
        c.draw() 
    for b in treelist:
        pygame.draw.line(win, b[4], (b[0], b[1]), (b[2], b[3]), b[5]) 
    for g in grasslist:
        g.draw() 
    for f in flowerlist:
        f.draw() 
    win.blit(sun.surf,(0,0)) #draw the sun / moon cycle in the sky after everything to make it all night-timey
    pygame.display.update() 
    for event in pygame.event.get(): #if a key is pressed, change the tree
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if same:
                    reuse()
                else:
                    makescene(['random']) 
