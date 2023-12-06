from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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

def render_simple_grass(obj):
    r_cube(obj.x, obj.y, 0, obj.w, obj.h, 1, (0, 1, 0))

def render_simple_road(obj):
    r_cube(obj.x, obj.y, 0, obj.w, obj.h, 1, (0.5, 0.5, 0.5))

def render_player(obj):
    z = 1
    r_cube(obj.x, obj.y, z, obj.w, obj.h, 1, (1, 0, 0))

def render_car(obj):
    z = 1
    r_cube(obj.x, obj.y, z, obj.w, obj.h, 1, (0, 0, 1))
