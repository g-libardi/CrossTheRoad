from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GLUT import glutStrokeCharacter, GLUT_STROKE_MONO_ROMAN
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
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    return texture_id

def draw_textured_quad(texture_id, x, y, z, width=1.0, height=1.0, color_filter=None):
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    # Set the color to red
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
    glOrtho(0, 20, 0, 20, -50, 50)
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

    glTranslatef(-game.w / 3, -game.y - 8, 0)


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

    player_y_text = f'Score: {game.score}'
    render_text(0.005, 0.92, player_y_text)

    if game.game_status == 1:
        texture_id = load_texture("gameover.png")
        draw_textured_quad(texture_id, 0, 0, 0, 1, 1)

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
    Engine.pause()
    size = min(width, height)
    x = (width - size) / 2
    y = (height - size) / 2
    glViewport(int(x), int(y), size, size)

    def is_point_outside_screen(x, y, z=1.0):
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        screen_x, screen_y, screen_z = gluProject(x, y, z, modelview, projection, viewport)

        # Adjust the window coordinates by the position of the viewport
        screen_x -= viewport[0]
        screen_y -= viewport[1]

        return screen_x < 0 or screen_x > viewport[2] or screen_y < 0 or screen_y > viewport[3]

    game.out_of_screen_bounds = is_point_outside_screen
    Engine.unpause()
    

def init_game():
    Player.render = render_player
    Car.render = render_car
    SimpleGrass.render = render_simple_grass
    SimpleRoad.render = render_simple_road
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
    glutMainLoop()

if __name__ == "__main__":
    main()