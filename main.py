from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from game import *
from time import time
from PIL import Image
from models import *

global game, last_update
game = Game()
last_update = time()

def load_texture(file_path):
    image = Image.open(file_path).convert("RGBA")
    texture_data = image.tobytes("raw", "RGBA", 0, -1)

    width, height = image.size
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def draw_textured_quad(texture_id, x, y, z, width=1.0, height=1.0):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, texture_id)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(x, y, z)

    glTexCoord2f(1, 0)
    glVertex3f(x + width, y, z)

    glTexCoord2f(1, 1)
    glVertex3f(x + width, y + height, z)

    glTexCoord2f(0, 1)
    glVertex3f(x, y + height, z)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def set_coordinates():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, game.w, 0, game.h, -50, 50)
    glMatrixMode(GL_MODELVIEW)


def set_camera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Move the camera
    glTranslatef(0, 8, 0)
    
    # Rotate the camera
    glRotatef(-45, 1, 0, 0)
    glRotatef(0, 0, 1, 0)
    glRotatef(-45, 0, 0, 1)

    glTranslatef(-4, -game.y, 0)


def display():
    # global last_update
    # print('FPS: ', 1 / (time() - last_update))
    # last_update = time()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    set_coordinates()
    glLoadIdentity()
    set_camera()
    lighting()

    Engine.update()

    if game.game_status == 1:
        texture_id = load_texture("gameover.png")
        draw_textured_quad(texture_id, game.x + 2, game.y - 3, 3, game.w - 2, game.h - 2)

    glutSwapBuffers()

def on_special_key(key, x, y):
    Engine.key_pressed(key, x, y)

def main():
    Player.render = render_player
    Car.render = render_car
    SimpleGrass.render = render_simple_grass
    SimpleRoad.render = render_simple_road
    Engine.register_input(GLUT_KEY_UP, game.player.move_up)
    Engine.register_input(GLUT_KEY_DOWN, game.player.move_down)
    Engine.register_input(GLUT_KEY_LEFT, game.player.move_left)
    Engine.register_input(GLUT_KEY_RIGHT, game.player.move_right)

    glutInit()
    glutInitWindowSize(800, 800)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Cross The Road!")
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutSpecialFunc(on_special_key)
    glEnable(GL_DEPTH_TEST)
    glutMainLoop()

if __name__ == "__main__":
    main()