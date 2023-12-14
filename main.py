from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import glutStrokeCharacter, GLUT_STROKE_MONO_ROMAN
from game import *
from time import time
from PIL import Image
from models import *

global game, last_update
game = None
last_update = time()
ORTHO_CORDS = (0, 13, 0, 13, -50, 50)

def draw_textured_quad(texture_id, x, y, z, width=1.0, height=1.0, color_filter=None):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

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

def render_text(x, y, text, color=(1, 1, 1), scale=0.0005):
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glTranslatef(x, y, 0)
    glScalef(scale, scale, scale)
    glLineWidth(30)
    glColor3f(*color)
    for ch in text:
        glutStrokeCharacter(GLUT_STROKE_MONO_ROMAN, ord(ch))
    glPopMatrix()

def set_coordinates():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(*ORTHO_CORDS)
    glMatrixMode(GL_MODELVIEW)

camera_type = 0
def set_camera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Rotate the camera
    initial_player_pos = game.player_initial_y + game.player.h/2
    if camera_type == 0:
        glTranslatef(ORTHO_CORDS[3]/2, initial_player_pos, 0)
        glRotatef(-45, 1, 0, 0)
        glRotatef(0, 0, 1, 0)
        glRotatef(-25, 0, 0, 1)
        glTranslatef(-game.w/2, -initial_player_pos, 0)
    elif camera_type == 1:
        glRotatef(-45, 1, 0, 0)
        glRotatef(0, 0, 1, 0)
        glRotatef(0, 0, 0, 1)
        glTranslatef(-game.w/2 + ORTHO_CORDS[3]/2, 0, 0)
    glTranslatef(0, -game.y, 0)

def timer_func(value):
    glutPostRedisplay()
    glutTimerFunc(1000 // 60, timer_func, 0)

is_pressed = {}
def on_special_key(key, x, y):
    is_pressed[key] = True

def on_special_key_up(key, x, y):
    is_pressed[key] = False

def on_keyboard(key, x, y):
    global game
    if key == b'r':
        game.reset()
    elif key == b'p':
        if Engine._pause:
            game.unpause()
        else:
            game.pause()
    elif key == b'c':
        global camera_type
        camera_type = (camera_type + 1) % 2

def check_keys():
    for key in is_pressed:
        if is_pressed[key]:
            Engine.key_pressed(key, 0, 0)

def render_screen_ui():
    global score
    glPushMatrix()
    
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 1, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)

    player_y_text = f'Score:{game.score}'
    render_text(0.03, 0.92, player_y_text)

    if game.game_status == 1:
        texture_id = textures['gameover']
        glColor3f(1, 1, 1)
        draw_textured_quad(texture_id, 0.1, 0.275, 0, 0.8, 0.45)

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

def display():
    global last_update
    # print('FPS: ', 1 / (time() - last_update))

    check_keys()
    last_update = time()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    set_coordinates()
    glLoadIdentity()
    set_camera()
    lighting()

    Engine.update()

    render_screen_ui()

    glutSwapBuffers()

def reshape(width, height):
    size = min(width, height)
    x = (width - size) / 2
    y = (height - size) / 2
    glViewport(int(x), int(y), size, size)

def is_point_outside_screen(x, y, z=1.5):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        screen_x, screen_y, screen_z = gluProject(x, y, z, modelview, projection, viewport)

        # Adjust the window coordinates by the position of the viewport
        screen_x -= viewport[0]
        screen_y -= viewport[1]

        return screen_x < 0 or screen_x > viewport[2] or screen_y < 0 or screen_y > viewport[3]

def init_game():
    global game

    game_settings = {
        'w': 24,
        'h': 13,
        'gen_bounds': (-8, 20),
        'game_speed': 2,
        'player_initial_y': 8,
        'player_speed': 4,
        'car_speed': 2,
        'car_spawn_rate': 0.6,
        'out_of_screen_func': is_point_outside_screen,
    }

    game = Game(**game_settings)
    Player.render = render_player
    Car.render = render_car
    SimpleGrass.render = render_simple_grass
    SimpleRoad.render = render_simple_road
    Player.render_shadow = render_player_shadow
    Car.render_shadow = render_car_shadow
    Engine.register_input(GLUT_KEY_UP, game.player.move_up)
    Engine.register_input(GLUT_KEY_DOWN, game.player.move_down)
    Engine.register_input(GLUT_KEY_LEFT, game.player.move_left)
    Engine.register_input(GLUT_KEY_RIGHT, game.player.move_right)

def main():
    init_game()

    glutInit()
    glutInitWindowSize(800, 800)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutCreateWindow("Cross The Road!")
    glutDisplayFunc(display)
    glutTimerFunc(1000 // 60, timer_func, 0)
    glutSpecialFunc(on_special_key)
    glutSpecialUpFunc(on_special_key_up)
    glutKeyboardFunc(on_keyboard)
    glutReshapeFunc(reshape)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    load_textures()
    glutMainLoop()

if __name__ == "__main__":
    main()