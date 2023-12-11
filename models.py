from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import sample
import math

colors = {
    "red": (1, 0, 0),
    "green": (0, 1, 0),
    "blue": (0, 0, 1),
    "yellow": (1, 1, 0),
    "cyan": (0, 1, 1),
    "magenta": (1, 0, 1),
    "white": (1, 1, 1),
    "black": (0, 0, 0),
    "gray": (0.5, 0.5, 0.5),
    "grey": (0.5, 0.5, 0.5),
}

def lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_POSITION, (-0.8, 1, -1.2, 0))  # Light now points downwards
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

def r_cube(x, y, z, dx, dy, dz, color=(1, 1, 1)):
    # cube with quads and normals
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor3f(*color)
    glNormal3f(0, 0, 1)
    glVertex3f(x, y, z)
    glVertex3f(x + dx, y, z)
    glVertex3f(x + dx, y + dy, z)
    glVertex3f(x, y + dy, z)
    glNormal3f(0, 0, -1)
    glVertex3f(x, y, z + dz)
    glVertex3f(x + dx, y, z + dz)
    glVertex3f(x + dx, y + dy, z + dz)
    glVertex3f(x, y + dy, z + dz)
    glNormal3f(0, 1, 0)
    glVertex3f(x, y, z)
    glVertex3f(x + dx, y, z)
    glVertex3f(x + dx, y, z + dz)
    glVertex3f(x, y, z + dz)
    glNormal3f(0, -1, 0)
    glVertex3f(x, y + dy, z)
    glVertex3f(x + dx, y + dy, z)
    glVertex3f(x + dx, y + dy, z + dz)
    glVertex3f(x, y + dy, z + dz)
    glNormal3f(1, 0, 0)
    glVertex3f(x, y, z)
    glVertex3f(x, y, z + dz)
    glVertex3f(x, y + dy, z + dz)
    glVertex3f(x, y + dy, z)
    glNormal3f(-1, 0, 0)
    glVertex3f(x + dx, y, z)
    glVertex3f(x + dx, y, z + dz)
    glVertex3f(x + dx, y + dy, z + dz)
    glVertex3f(x + dx, y + dy, z)
    glEnd()
    glPopMatrix()

def cube(x0, y0, z0, xf, yf, zf):
    glBegin(GL_QUADS)
    #normals
    glNormal3f(0, 0, 1)
    glVertex3f(x0, y0, z0)
    glVertex3f(xf, y0, z0)
    glVertex3f(xf, yf, z0)
    glVertex3f(x0, yf, z0)
    glNormal3f(0, 0, -1)
    glVertex3f(x0, y0, zf)
    glVertex3f(xf, y0, zf)
    glVertex3f(xf, yf, zf)
    glVertex3f(x0, yf, zf)
    glNormal3f(0, 1, 0)
    glVertex3f(x0, y0, z0)
    glVertex3f(xf, y0, z0)
    glVertex3f(xf, y0, zf)
    glVertex3f(x0, y0, zf)
    glNormal3f(0, -1, 0)
    glVertex3f(x0, yf, z0)
    glVertex3f(xf, yf, z0)
    glVertex3f(xf, yf, zf)
    glVertex3f(x0, yf, zf)
    glNormal3f(1, 0, 0)
    glVertex3f(x0, y0, z0)
    glVertex3f(x0, yf, z0)
    glVertex3f(x0, yf, zf)
    glVertex3f(x0, y0, zf)
    glNormal3f(-1, 0, 0)
    glVertex3f(xf, y0, z0)
    glVertex3f(xf, yf, z0)
    glVertex3f(xf, yf, zf)
    glVertex3f(xf, y0, zf)
    glEnd()

def render_simple_grass(obj):
    r_cube(obj.x, obj.y, 0, obj.w, obj.h, 1, (0, 1, 0))

def render_simple_road(obj):
    r_cube(obj.x, obj.y, 0, obj.w, obj.h, 1, (0.5, 0.5, 0.5))

def render_player(obj):
    z = 1
    glPushMatrix()
    z += 0.5 * math.sin(math.sqrt((obj.x - obj.next_position[0]) ** 2 + (obj.y - obj.next_position[1]) ** 2) * math.pi)
    r_cube(obj.x, obj.y, z, obj.w, obj.h, 1, (1, 0, 0))
    glPopMatrix()

def render_car(obj):
    glPushMatrix()
    z = 1
    car_color = obj.color
    #set metallic material
    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))
    # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1))
    # glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)
    glTranslatef(obj.x, obj.y, z)
    # Body of the car
    glColor3f(*car_color)
    cube(0, 0.1, 1/4, 1/5, 0.9, 4/5)
    cube(1/5, 0.1, 1/2, 3/5, 0.9, 4/5)
    cube(3/5, 0.1, 1/4, 7/5, 0.9, 4/5)
    cube(7/5, 0.1, 1/2, 9/5, 0.9, 4/5)
    cube(9/5, 0.1, 1/4, 2, 0.9, 4/5)

    # upper part of the car (z is height)
    glColor3f(0, 0, 0)
    cube(3/5, 0.1, 4/5, 8/5, 0.9, 6/5)
    glColor3f(*car_color)
    cube(3/5, 0.1, 6/5, 8/5, 0.9, 10/8)

    # wheels
    glColor3f(0.2, 0.2, 0.2)
    cube(1/5, 0.05, 0, 3/5, 0.95, 1/2)
    cube(7/5, 0.05, 0, 9/5, 0.95, 1/2)


    glPopMatrix()