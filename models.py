from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from random import sample
import math
from PIL import Image

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
    "orange": (1, 0.5, 0),
}

textures = {}
def load_texture(name, file_path):
    image = Image.open(file_path).convert("RGBA")
    texture_data = image.tobytes("raw", "RGBA", 0, -1)
    width, height = image.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    textures[name] = texture_id
    return texture_id

def load_textures():
    load_texture('grass', './assets/grass.png')
    load_texture('gameover', './assets/gameover.png')
    load_texture('road', './assets/road.png')


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

def cube(x0, y0, z0, xf, yf, zf, texture=None, tex_scale=1):
    # cube with quads and normals
    glPushMatrix()
    if texture:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glBegin(GL_QUADS)
    if not texture:
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
    else:
        glNormal3f(0, 0, 1)
        glTexCoord2f(0, 0)
        glVertex3f(x0, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(xf, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(xf, yf, z0)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(x0, yf, z0)

        glNormal3f(0, 0, -1)
        glTexCoord2f(0, 0)
        glVertex3f(x0, y0, zf)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(xf, y0, zf)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(xf, yf, zf)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(x0, yf, zf)

        glNormal3f(0, 1, 0)
        glTexCoord2f(0, 0)
        glVertex3f(x0, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(xf, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(xf, y0, zf)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(x0, y0, zf)

        glNormal3f(0, -1, 0)
        glTexCoord2f(0, 0)
        glVertex3f(x0, yf, z0)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(xf, yf, z0)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(xf, yf, zf)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(x0, yf, zf)

        glNormal3f(1, 0, 0)
        glTexCoord2f(0, 0)
        glVertex3f(x0, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(x0, yf, z0)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(x0, yf, zf)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(x0, y0, zf)

        glNormal3f(-1, 0, 0)
        glTexCoord2f(0, 0)
        glVertex3f(xf, y0, z0)
        glTexCoord2f((xf-x0) / tex_scale, 0)
        glVertex3f(xf, yf, z0)
        glTexCoord2f((xf-x0) / tex_scale, (yf-y0) / tex_scale)
        glVertex3f(xf, yf, zf)
        glTexCoord2f(0, (yf-y0) / tex_scale)
        glVertex3f(xf, y0, zf)
    glEnd()
    if texture:
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def render_simple_grass(obj):
    # glColor4f(0, 1.0, 0, 1)
    glColor3f(1, 1, 1)
    cube(obj.x, obj.y, 0, obj.x + obj.w, obj.y + obj.h, 1, textures['grass'], 10)

def render_simple_road(obj):
    glColor3f(1, 1, 1)
    cube(obj.x, obj.y, 0, obj.x + obj.w, obj.y + obj.h, 1, textures['road'], 1)

def render_player(obj):
    z = 1
    delta = math.sin(math.sqrt((obj.x - obj.next_position[0]) ** 2 + (obj.y - obj.next_position[1]) ** 2) * math.pi)
    glPushMatrix()
    z += 0.5 * delta
    
    glTranslatef(obj.x, obj.y, z)
    glTranslatef(obj.w/2, obj.h/2, 0)
    glScalef(1 - 0.2 * delta, 1 - 0.2 * delta, 1 + 0.4 * delta)
    if obj.direction == (0, -1):
        glRotatef(180, 0, 0, 1)
    else:
        glRotatef(-90 * obj.direction[0], 0, 0, 1)
    glScalef(obj.w, obj.h, obj.h)
    glTranslatef(-0.5, -0.5, 0)
    
    glColor3f(*colors['white'])
    #chicken
    cube(0.00, 0.30, 0.20, 1.00, 0.80, 0.65)  # wings
    cube(0.20, 0.10, 0.10, 0.80, 0.70, 0.70)  # body
    cube(0.25, 0.00, 0.30, 0.75, 0.30, 0.70)  # tail
    cube(0.35, 0.00, 0.60, 0.65, 0.10, 0.80)  # tail
    
    cube(0.30, 0.60, 0.40, 0.70, 0.95, 1.20)  # head

    glColor3f(*colors['orange'])
    cube(0.20, 0.40, 0.00, 0.40, 0.80, 0.10)  # left foot
    cube(0.60, 0.40, 0.00, 0.80, 0.80, 0.10)  # right foot
    cube(0.40, 0.95, 0.85, 0.60, 1.00, 1.00)  # beak
    glColor3f(*colors['red'])
    cube(0.40, 0.75, 1.20, 0.60, 0.90, 1.30)  # red comb

    glColor3f(*colors['black'])
    cube(0.30, 0.95, 1.00, 0.40, 0.96, 1.10)  # left eye
    cube(0.60, 0.95, 1.00, 0.70, 0.96, 1.10)  # right eye
    glPopMatrix()

def render_player_shadow(obj):
    # shadow
    glPushMatrix()
    glTranslatef(0, 0, 0.001)
    s = 1-0.3 * math.sin(math.sqrt((obj.x - obj.next_position[0]) ** 2 + (obj.y - obj.next_position[1]) ** 2) * math.pi)
    glTranslatef(obj.x, obj.y, 1)
    glTranslatef(obj.w/2, obj.h/2, 0)
    glScalef(obj.w * 1.1, obj.h * 1.1, 1)
    glScalef(s, s, obj.h)
    glColor4f(0, 0, 0, 0.1)
    glutSolidCylinder(0.5, 0.001, 10, 10)
    glPopMatrix()

def render_car(obj):
    glPushMatrix()
    z = 1
    car_color = obj.color
    glTranslatef(obj.x, obj.y, z)
    if obj.speed > 0:
        glTranslatef(obj.w/2, obj.h/2, 0)
        glRotatef(180, 0, 0, 1)
        glTranslatef(-obj.w/2, -obj.h/2, 0)
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

def render_car_shadow(obj):
    # shadow
    glPushMatrix()
    glTranslatef(obj.x, obj.y, 1)
    glScalef(obj.w, obj.h, 1)
    glColor4f(0, 0, 0, 0.1)
    cube(0.00, 0.00, 0.001, 1.00, 1.00, 0.002)
    glPopMatrix()
