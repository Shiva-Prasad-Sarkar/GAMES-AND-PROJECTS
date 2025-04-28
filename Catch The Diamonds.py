from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

#variables
W_Width, W_Height = 500,700 #window size
score = 0 #score
man_x = random.randint(-235,235) #diamond x vals for random pos
down = 50 #diamond y vals for animate
n_x = 0 #ball cather x vals to move
speed1 = 1 #diamond speed
speed2 = 15
r_d,g_d,b_d = random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0.1, 1)
last = time.time()

#flags
pause = False #is pause
end = False #cross button unconditional exit
new_game = False #arrow button new start
c_c = False #is checked collision of diamond and cather yet 
game  = True #is game running


#for drawing line using Midpoint algorithm
def zone_change(point,zone1,zone2):
    x,y = point
    if zone1==0:
        current_zone = zone2
        if current_zone==0:
            return (x,y)
        elif current_zone==1:
            return (y,x)
        elif current_zone==2:
            return (-y,x)
        elif current_zone==3:
            return (-x,y)
        elif current_zone==4:
            return (-x,-y)
        elif current_zone==5:
            return (-y,-x)
        elif current_zone==6:
            return (y,-x)
        elif current_zone==7:
            return (x,-y)
    else:
        current_zone = zone1
        if current_zone==0:
            return (x,y)
        elif current_zone==1:
            return (y,x)
        elif current_zone==2:
            return (y,-x)
        elif current_zone==3:
            return (-x,y)
        elif current_zone==4:
            return (-x,-y)
        elif current_zone==5:
            return (-y,-x)
        elif current_zone==6:
            return (-y,x)
        elif current_zone==7:
            return (x,-y)
        

def detect_zone(x0, y0, x1, y1):
    dx = x1-x0
    dy = y1-y0
    if abs(dx)<=abs(dy):
        if (dx > 0):
            if (dy <= 0):
                return 6
            else:
                return 1
        else:
            if (dy <= 0):
                return 5
            else:
                return 2
    else:
        if (dx <= 0):
            if (dy > 0):
                return 3
            else:
                return 4    
        else:
            if (dy > 0):
                return 0
            else:
                return 7


def middle_point(x0, y0, x1, y1,r,g,b,p=3):
    glColor3f(r,g,b)
    glPointSize(p)
    zone = detect_zone(x0, y0, x1, y1)
    x0,y0=zone_change((x0,y0),zone,0)
    x1,y1=zone_change((x1,y1),zone,0)
    dx = x1-x0
    dy = y1-y0
    x,y = x0,y0
    NE = 2*dy-2*dx
    E = 2*dy
    D = 2*dy-dx

    while x<=x1:
        p,q = zone_change((x,y),0,zone)
        glBegin(GL_POINTS)
        glVertex2f(p,q)
        glEnd()
        x+=1
        if D>0:
            D+=NE
            y+=1
        else:
            D+=E

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

#collision detect
def collision(b1x,b1y,b1w,b1h,b2x,b2y,b2w,b2h):
    if (b1x < (b2x + b2w)) and ((b1x + b1w) > b2x) and (b1y < (b2y + b2h)) and ((b1y + b1h) > b2y):
        return True
    else:
        return False
    
#game elements
def drawShapes():
    global pause
    #pause or runnig
    if pause==False:
        middle_point(-10,300,-10,345,.8,.6,.09)
        middle_point(10,300,10,345,.8,.6,.09)
    else:
        middle_point(-15,300,-15,345,.8,.6,.09)
        middle_point(-15,300,15,322,.8,.6,.09)
        middle_point(15,322,-15,345,.8,.6,.09)
  
    #restart
    middle_point(-240,322,-210,322,.03,.7,.9)
    middle_point(-240,322,-225,300,.03,.7,.9)
    middle_point(-240,322,-225,345,.03,.7,.9)

    #cross
    middle_point(245,300,210,345,.9,.2,.03)
    middle_point(245,345,210,300,.9,.2,.03)

def diamond_basket():
    global man_x 
    global down,n_x,pause,r_d,g_d,b_d 
    #diamond
    if game==True:
        middle_point(-10+man_x,330-down,0+man_x,345-down,r_d,g_d,b_d)
        middle_point(0+man_x,315-down,-10+man_x,330-down,r_d,g_d,b_d)
        middle_point(0+man_x,315-down,10+man_x,330-down,r_d,g_d,b_d)
        middle_point(10+man_x,330-down,0+man_x,345-down,r_d,g_d,b_d)
    
    if game==True and pause==False:
        middle_point(-250,299,250,299,r_d,g_d,b_d)
        middle_point(-250,-349,-250,349,r_d,g_d,b_d)
        middle_point(-250,-349,250,-349,r_d,g_d,b_d)
        middle_point(250,349,250,-349,r_d,g_d,b_d)
        middle_point(250,349,-250,349,r_d,g_d,b_d)
        


    #basket
    if game==True or pause==False:
        r,g,b = 1,1,1
    if game==False:
        r,g,b = .9,.2,.03
    elif  pause==True:
        r,g,b = .7,.2,.4
    middle_point(-50+n_x,-345,50+n_x,-345,r,g,b)
    middle_point(-50+n_x,-345,-60+n_x,-330,r,g,b)
    middle_point(50+n_x,-345,60+n_x,-330,r,g,b)
    middle_point(60+n_x,-330,-60+n_x,-330,r,g,b)


#game actions
def specialKeyListener(key, x, y):
    global n_x,speed2
    if game==True and pause==False:
        if key==GLUT_KEY_RIGHT:
            if 60+n_x<=250:
                n_x+=speed2
            
        if key==GLUT_KEY_LEFT:
            if -60+n_x>=-250:
                n_x-=speed2
        glutPostRedisplay()
        

def mouseListener(button, state, x, y):	
    global pause,new_game,end,game,score,man_x,down,n_x,speed1,speed2,c_c,r_d,g_d,b_d,last
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):   
            c_X, c_Y = convert_coordinate(x,y)
            if c_X >= -15 and c_Y >= 300 and c_X <= 15 and c_Y <= 345 and game==True:
                pause = not pause
                if pause:
                    print('Game Paused')
                
            if c_X >= -240 and c_Y >= 300 and c_X <= -210 and c_Y <= 345:
                new_game = True
            
            if c_X >= 210 and c_Y >= 300 and c_X <= 245 and c_Y <= 345:
                end = True

    
                       
    if end:
        print(f'GoodBye!Your score = {score}')
        glutLeaveMainLoop()
    
    if new_game:
        print("Starting Over!")
        pause = False
        end = False
        new_game = False
        score = 0
        man_x = random.randint(-235,235)
        r_d,g_d,b_d = random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0.1, 1)
        down = 50
        n_x = 0
        game  = True
        speed1 = 1
        speed2 = 15
        last = time.time()
        c_c=False

    if button==GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN: 	
            print(x,y)
            c_X, c_y = convert_coordinate(x,y)
            
    glutPostRedisplay()


#game play
def run():
    global pause,new_game,end,game,score,man_x,down,n_x,speed1,speed2,c_c,r_d,g_d,b_d,current
    drawShapes()
    diamond_basket()
    #diamond meausre:
    current_x = -10+man_x
    current_y = 315-down
    #box measure
    cur_x = -60+n_x
    cur_y = -345

    if current_y<=-345 and c_c==False:
        
        j = collision(current_x,current_y,20,45,cur_x,cur_y,120,15)
        if j==True:
            pause = False
            end = False
            new_game = False
            score +=1
            r_d,g_d,b_d = random.uniform(0.1, 1),random.uniform(0.1, 1),random.uniform(0.1, 1)
            print(f"Current Score: {score}")
            man_x = random.randint(-235,235)
            down = 50
            game  = True
            speed1 += 0.15
            #speed2 += 3

        else:
            print(f'Game over!Score {score}')
            game = False
            c_c=True
        

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)
    iterate()
    run()
    glutSwapBuffers()

# def animate():
#     global down,speed1,pause,game
#     if pause==False and game==True:     
#         if 350-down>-350:
#             down+=speed1
#         else:
#             down = 0
#     glutPostRedisplay()

#with delta time
def animate():
    global down, speed1, pause, game, last

    current = time.time()
    delta = current - last
    last = current
    

    if pause == False and game == True:
        if 350 - down > -350:
            down += speed1 * delta * 144
        else:
            down = 0

    glutPostRedisplay()
    

def iterate():
    glViewport(0, 0, 500, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -350, 350, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 700) 
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catchhhhhhhhhhhhhhhhhhhhhhhhhhhh!!!")
glutDisplayFunc(display)	
glutIdleFunc(animate)	
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()		