from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# import time
import math
import random


#flags
# scale = True 
game = True
valid = False
cht = False
fpview = False
selfshoot = True
end = False

#import vals
# time1 = time.time()

#arrays
eni = [] #to store 5 enemies datas
guli = [] 

#globals
angle = 0 #player angle 
camera_pos = (0,500,500)
fovY = 122
gr_len = 90
t_eni  = 5
jibon  = 5
guli_miss = 0
enm_count = 5
murder = 0
p_x ,p_y = 0, 0 #player x and y position

#function to draw text in game
def draw_text(x, y, text, font):
    p,q = x,y
    glColor3f(.9,.9,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(p,q)
    for i in text:
        glutBitmapCharacter(font, ord(i))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


#grid floor drawing [12x12]
def draw_chess_borad():
    global gr_len
    for r in range(12):
        begin_y =gr_len*6 - r*gr_len
        for j in range(12):
            begin_x = gr_len*6 - j*gr_len
            glBegin(GL_QUADS)
            #selecting alternate color
            if (r+j)%2==0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(begin_x,begin_y,0)
            glVertex3f(begin_x - gr_len, begin_y, 0)
            glVertex3f(begin_x - gr_len, begin_y - gr_len, 0)
            glVertex3f(begin_x, begin_y - gr_len, 0)
            glEnd()

def game_wall():
    global gr_len
    ht = gr_len*1.5

    glBegin(GL_QUADS)
    glColor3f(0, 1, 0)
    glVertex3f(-540, -540, 0)
    glVertex3f(-540,  540, 0)
    glVertex3f(-540,  540, ht)
    glVertex3f(-540, -540, ht)

    glColor3f(0, 0, 1)
    glVertex3f(540, -540, 0)
    glVertex3f(540,  540, 0)
    glVertex3f(540,  540, ht)
    glVertex3f(540, -540, ht)

    glColor3f(0, 1, 1)
    glVertex3f(-540, -540, 0)
    glVertex3f( 540, -540, 0)
    glVertex3f( 540, -540, ht)
    glVertex3f(-540, -540, ht)

    glColor3f(1, 1, 1)
    glVertex3f(-540, 540, 0)
    glVertex3f( 540, 540, 0)
    glVertex3f( 540, 540, ht)
    glVertex3f(-540, 540, ht)

    glEnd()

def draw_players():
    global p_x,p_y,game,angle,valid,jibon

    #talpatar shepai
    glPushMatrix()
    glTranslatef(p_x,p_y,0)
    glRotatef(angle, 0, 0, 1)  
    if game==False :
        glRotatef(90,0,1,0) #laying down the player in floor

    #leg_piece
    glColor3f(0, 0, 1)
    glTranslatef(0,-15,-90)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 7, 80, 10, 10) #quadric, base radius, top radius, height, slices, stacks
    glColor3f(0, 0, 1)
    glTranslatef(0,-75,0)
    gluCylinder(gluNewQuadric(), 15, 7, 80, 10, 10) 

    #udor
    glColor3f(0.4, 0.5, 0)
    glTranslatef(0, 35, -10)
    glutSolidCube(70)

    #bonduk
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 0, 15)
    glTranslatef(30, 0, -40) 
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 15, 3, 100, 10, 10) 
  

    #hath
    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, -25, 0)
    gluCylinder(gluNewQuadric(), 12, 5, 50, 10, 10) 

    glColor3f(1, 0.7, 0.6)
    glTranslatef(0, 50, 0)
    gluCylinder(gluNewQuadric(), 12, 5, 50, 10, 10) 

    # Matha
    glColor3f(0, 0, 0)
    glTranslatef(40,-25, -18)
    gluSphere(gluNewQuadric(), 28, 10, 10)

    glPopMatrix()

#ememies maker
def sotru(e):
    x,y,s = e[0],e[1],e[3]
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(s, s, s)
    
    # if scale: #if use  time function
    #     glScalef (1.2, 1.2, 1.2) 
    # else:
    #     glScalef (.8, .8, .8) 

    glColor3f(1, 0, 0)
    glTranslatef(0, 0, 40)
    gluSphere(gluNewQuadric(), 40, 21, 21)

    glColor3f(0,0,0)
    glTranslatef(0, 0, 45)
    gluSphere(gluNewQuadric(), 19, 11, 11)
    glPopMatrix()

def ran_pos_maker():
    global gr_len
    min = int(12*gr_len/2) #to check if pos crosses boundary
    while True:
        x,y = random.randint(-(min-55),(min-55)),random.randint(-(min-55),(min-55))
        if abs(x) > 150 or abs(y) > 150: 
            break
    return [x,y,0,1.1,.003]

#assigning x and y pos of five enemies
for i in range(t_eni):
    eni.append(ran_pos_maker())

#guli
def pointthreemm():
    global guli,cht
    glColor3f(1, 0, 0)
    for i in guli:
        x,y,z = i[0],i[1],i[2]
        glPushMatrix()
        glTranslatef(x,y,z)
        if cht:
            glutSolidCube(8)
        else:
            glutSolidCube(15)

        glPopMatrix()

#brush fire
def firethebullet():
    global guli, game, guli_miss, jibon, eni, cht, valid,murder
    for barud in guli:
            barud[0] += barud[3] * 15
            barud[1] += barud[4] * 15

    k = 0
    while k < len(guli):
        if abs(guli[k][0]) >= 540 or abs(guli[k][1]) >= 540:
            guli.pop(k)
            if  not cht and not valid and guli_miss<=10:
                guli_miss += 1
                print(f'Missed fire : {guli_miss}')
              # Increment missed bullet count here
        else:
            k += 1
    
    if guli_miss >= 10 or jibon == 0:
            game = False
            eni.clear()


#enemy attack
#animate the hero
def kill_the_hero():
    global  guli_miss, murder, jibon, game, p_x, p_y,eni,end

    for i in eni:
        dx = p_x - i[0]
        dy = p_y - i[1]
        durotto = (dx**2 + dy**2)**.5

        if durotto > 1:
            i[0] += (dx / durotto) * 0.05
            i[1] += (dy / durotto) * 0.05

        i[3] += i[4]
        if i[3] >= 1.4 :
            i[4] = -i[4]
        elif i[3] <= 0.6:
            i[4] = -i[4]

    if game==True:
        for e in eni:
            x,y,z = p_x - e[0],p_y - e[1],0-e[2]
            if abs(x) < 50 and abs(y) < 50 and abs(z)<50:
                if jibon > 0:
                    jibon -= 1
                    print(f'Remainig life : {jibon}')
                    eni.remove(e)
                    eni.append(ran_pos_maker())
                    if jibon<=0:
                        eni.clear()
                        game = False
                        

                        break
      
    glutPostRedisplay()

#to deploy cheat mode
def auto_rifile():
    global fpview,game,angle,p_x,p_y,guli,murder,valid

    if cht==True and game!=False:
            angle+=0.7
            angle%= 360
            kon = math.radians(angle)
            x_dir = -math.cos(kon)
            y_dir = -math.sin(kon)
            bx = p_x + 50 * math.sin(kon) + x_dir * 140
            by = p_y - 50 * math.cos(kon) + y_dir * 140 
            bz = 10
            guli.append([bx, by, bz, x_dir, y_dir, 0])

            for j in eni[:]:
                distn = ((j[0] - bx)**2 + (j[1] - by)**2)**.5
                if distn == 0:
                    continue
                dt = x_dir * (j[0] - bx) / distn + y_dir * (j[1] - by) / distn


                if dt > 0.99 and distn <= 450 :
                    dx, dy, dz = j[0] - bx, j[1] - by, j[2] - bz
                    len = (dx**2 + dy**2 + dz**2)**.5
                    if len == 0:
                        continue

                    x,y,z = (dx / len, dy / len, dz / len)
                    temp = [bx, by, bz, x, y, z]
                    guli.append(temp)

                    murder += 1
                    print(f'Bullet fired')
                    eni.remove(j)
                    
                    eni.append(ran_pos_maker())
                    break
    glutPostRedisplay()


def botkill():
    global guli, murder, eni, jibon, game

    bulremove = []
    new = []

    for i in eni:
        fired = False
        for j in guli:
            x = j[0] - i[0]
            y = j[1] - i[1]
            z = j[2] - i[2]

            if abs(x) < 35 and abs(y) < 35 and abs(z) < 35:
                fired = True
                murder += 1
                print('Bullet fired')
                bulremove.append(j)
                break

        if fired:
            new.append(ran_pos_maker())
        else:
            new.append(i)

    for t in bulremove:
        if t in guli:
            guli.remove(t)

    eni[:] = new

#game controller buttons
def keyboardListener(key, x, y):
    global p_x,p_y,angle,fpview,cht,game,selfshoot,t_eni,valid,murder,guli_miss,jibon
    speed= 5
    
    if key == b'w' and game:
        i = p_x-math.cos(math.radians(angle)) * speed
        j = p_y- math.sin(math.radians(angle)) * speed
        if -540<=i<=540 and -540<=j<=540:
            p_x = i
            p_y = j
        
    elif key == b's' and game:
        i = p_x+math.cos(math.radians(angle)) * speed
        j = p_y+ math.sin(math.radians(angle)) * speed
        if -540<=i<=540 and -540<=j<=540: 
             p_x = i
             p_y = j
            
    elif key == b'a' and game:
        angle+=5

    elif key == b'd' and game:
        angle-=5

    elif key == b'v' and cht and game:
        fpview = not fpview

    elif key == b"c" and game: #cheat mode
        cht = not cht
        if cht :
            auto_rifile()     
        else:
            guli.clear()
            # eni.clear()
            # for i in range(t_eni):
            #     new = ran_pos_maker()
            #     eni.append(new)
            # guli_miss = 0
            # game = True
            # print("Game restarted!")
            # valid = False
            glutPostRedisplay()

        
    elif key == b'r' and game==False: #restart
        guli.clear()
        eni.clear()
        for i in range(t_eni):
            new = ran_pos_maker()
            eni.append(new)

        murder = 0
        guli_miss = 0
        jibon = 5
        game = True
        angle = 0
        print("Game restarted!")
        valid = False
        glutPostRedisplay()
    
    glutPostRedisplay()


def specialKeyListener(key, x, y):

    global camera_pos
    xi, yj, zk = camera_pos
   
    if key == GLUT_KEY_UP:
        zk-=5
    
    if key == GLUT_KEY_DOWN:
        zk+=5

    if key == GLUT_KEY_LEFT:
        if xi>-600:
            xi -= 5
            yj-=1
            zk-=.25
        
    if key == GLUT_KEY_RIGHT:
        if xi<450:
            xi += 5
            yj+=1
            zk-=.25
        
    camera_pos = (xi, yj, zk)


def mouseListener(button, state, x, y):
    global fpview,game,angle,p_x,p_y,guli
    if game==True:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            kon = math.radians(angle)
            x_dir = -math.cos(kon)
            y_dir = -math.sin(kon)
            bx = p_x + 50 * math.sin(kon) + x_dir * 140
            by = p_y - 50 * math.cos(kon) + y_dir * 140 
            bz = 10
            guli.append([bx, by, bz, x_dir, y_dir, 0])

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN :
        if game:
            fpview = not fpview
        glutPostRedisplay()

def setupCamera():
    glMatrixMode(GL_PROJECTION)  
    glLoadIdentity()  
    gluPerspective(fovY, 1.25, 0.1, 1500) 
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity() 
    global fpview, p_x, p_y, angle

    if fpview:
        n_x = p_x - math.cos(math.radians(angle)) * 25
        n_y = p_y - math.sin(math.radians(angle)) * 25
        n_z = 40
        x = p_x - math.cos(math.radians(angle)) * 90
        y = p_y - math.sin(math.radians(angle)) * 90
        z = 35
        gluLookAt(n_x, n_y, n_z, 
                  x, y, z, 
                  0, 0, 1)
        
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z,  # Cam pos
                0, 0, 0,  # Look tar
                0, 0, 1)  # Upp vector (z_axis)


def idle():
    
    # global scale, time1
    # ftime = time.time()

    # if ftime - time1 >= .7:
    #     scale = not scale
    #     time1 = ftime
    kill_the_hero()
    botkill()
    firethebullet()
    auto_rifile()
    glutPostRedisplay()


def showScreen():
    global jibon, guli_miss, murder , eni,jibon,cht
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() 
    glViewport(0, 0, 1000, 800)  
    setupCamera() 
    draw_chess_borad()
    game_wall()
    draw_players()
    pointthreemm()

    for i in eni:
        sotru(i)
   
    if game:
        draw_text(10, 790, f"Life Remainig: {jibon}",GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 760, f"Match Score : {murder} ",GLUT_BITMAP_TIMES_ROMAN_24)
        if cht:
            draw_text(10, 730, f"Fire Missed : {0} ",GLUT_BITMAP_TIMES_ROMAN_24)
        else:
            draw_text(10, 730, f"Fire Missed : {guli_miss} ",GLUT_BITMAP_TIMES_ROMAN_24)


    else:
        draw_text(10, 790, f"Game is Over. Score is {murder}.",GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(10, 760, f'Press <R> to RESTART',GLUT_BITMAP_TIMES_ROMAN_24)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    glutInitWindowSize(1050, 850)  
    glutInitWindowPosition(0, 0)  
    wind = glutCreateWindow(b"-PUBG-")  

    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener)  
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  
    glutMainLoop()  

if __name__ == "__main__":
    main()
