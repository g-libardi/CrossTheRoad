from time import time
from random import randint, sample
import random
from abc import ABC

def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) / 255 for i in (0, 2, 4))

car_colors = ["E899DC","53a548","e76f51","f4e04d","7371fc"]
car_colors = [hex_to_rgb(color) for color in car_colors]


class GameObject(ABC):
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._collider = False
        Engine.new(self)
        self.last_update = time()

    @property
    def collider(self):
        return self._collider
    
    @collider.setter
    def collider(self, value: bool):
        if value and not self._collider:
            BoxCollider.colliders.add(self)
        elif not value and self._collider:
            BoxCollider.colliders.remove(self)
        self._collider = value
    
    def update_time(self):
        self.last_update = time()

    def update(self, delta_time):
        pass
    
    @staticmethod
    def render(obj):
        pass

    @staticmethod
    def render_shadow(obj):
        pass
    
    def on_collision(self, other):
        pass

    def on_destroy(self):
        pass
    
    def destroy(self):
        Engine.destroy(self)


class Engine:
    last_update = time()
    objects = []
    _pause = False
    input_actions = {}

    @classmethod
    def new(cls, obj: GameObject):
        cls.objects.append(obj)
    
    @classmethod
    def destroy(cls, obj: GameObject):
        obj.on_destroy()
        if obj.collider:
            BoxCollider.colliders.remove(obj)
        cls.objects.remove(obj)

    @classmethod
    def update(cls):
        if cls._pause:
            for obj in cls.objects:
                type(obj).render(obj)
            for obj in cls.objects:
                type(obj).render_shadow(obj)
            return
        
        for obj in cls.objects:
            delta_time = time() - obj.last_update
            obj.update_time()
            obj.update(delta_time)
            type(obj).render(obj)
        
        for obj in cls.objects:
                type(obj).render_shadow(obj)
        
        BoxCollider.check_collisions()
        
        cls.last_update = time()
        print(len(cls.objects))

    @classmethod
    def pause(cls):
        cls._pause = True
    
    @classmethod
    def unpause(cls):
        cls._pause = False
        for obj in cls.objects:
            obj.update_time()
    
    @classmethod
    def register_input(cls, key, action):
        cls.input_actions[key] = action
    
    @classmethod
    def key_pressed(cls, key, x, y):
        if cls._pause:
            return
        if key in cls.input_actions:
            cls.input_actions[key]()

    @classmethod
    def clear_entities(cls):
        for obj in cls.objects:
            obj.destroy()
        cls.objects.clear()


class BoxCollider:
    colliders = set()
    
    @classmethod
    def check_collisions(cls):
        for collider in cls.colliders:
            for other in cls.colliders:
                if collider != other:
                    if collider.x < other.x + other.w and collider.x + collider.w > other.x and collider.y < other.y + other.h and collider.y + collider.h > other.y:
                        collider.on_collision(other)


class Player(GameObject):
    def __init__(self, x, y, w, h, speed):
        super().__init__(x, y, w, h)
        self.collider = True
        self.life = 1
        self.moving = False
        self.next_position = (self.x, self.y)
        self.direction = (0, 1)
        self.speed = speed
    
    def update(self, delta_time):
        if self.moving:
            speed = self.speed
            self.x += self.direction[0] * speed * delta_time
            self.y += self.direction[1] * speed * delta_time
            if abs(self.x - self.next_position[0]) < 0.1:
                self.x = self.next_position[0]
            if abs(self.y - self.next_position[1]) < 0.1:
                self.y = self.next_position[1]
            if (self.x, self.y) == self.next_position:
                self.moving = False

    def move_up(self):
        if self.moving == False:
            self.next_position = (self.x, self.y + 1)
            self.moving = True
            self.direction = 0, 1
    
    def move_down(self):
        if self.moving == False:
            self.next_position = (self.x, self.y - 1)
            self.moving = True
            self.direction = 0, -1
    
    def move_left(self):
        if self.moving == False:
            self.next_position = (self.x - 1, self.y)
            self.moving = True
            self.direction = -1, 0
    
    def move_right(self):
        if self.moving == False:
            self.next_position = (self.x + 1, self.y)
            self.moving = True
            self.direction = 1, 0

    def on_collision(self, other):
        self.life -= 1


class MapModule(GameObject):
    def __init__(self, x, y, w, h, module_type):
        super().__init__(x, y, w, h)
        self.type = module_type


class SimpleGrass(MapModule):
    def __init__(self, x, y, w, h, pos = 0,):
        super().__init__(x, y, w, h, 'simple_grass')


class Car(GameObject):
    def __init__(self, x, y, w, h, speed):
        super().__init__(x, y, w, h)
        self.speed = speed
        self.collider = True
        self.color = sample(car_colors, 1)[0]
    
    def update(self, delta_time):
        self.x += self.speed * delta_time


class SimpleRoad(MapModule):
    def __init__(self, x, y, w, h, car_spawn_rate = 0.5, car_speed = 1.5):
        super().__init__(x, y, w, h, 'simple_road')
        self.car_spawn_rate = car_spawn_rate
        self.car_speed = car_speed
        self.lanes = [[] for _ in range(h)]

    def add_car(self, delta_time):
        for i, lane in enumerate(self.lanes):
            if random.random() < self.car_spawn_rate * delta_time:
                if i % 2 == 0:
                    if not lane or lane[-1].x - self.x > 2.5:
                        lane.append(Car(self.x - 2, self.y + i, 2, 1, self.car_speed))
                else:
                    if not lane or self.w - lane[-1].x > 2.5:
                        lane.append(Car(self.x + self.w + 2, self.y + i, 2, 1, -self.car_speed))
    
    def update(self, delta_time):
        self.add_car(delta_time)
        for lane in self.lanes:
            for car in lane:
                if car.speed > 0 and car.x > self.w or car.speed < 0 and car.x < self.x - car.w:
                    lane.remove(car)
                    car.destroy()
    
    def on_destroy(self):
        for lane in self.lanes:
            for car in lane:
                car.destroy()


class Game(GameObject):
    def __init__(self, w, h, gen_bounds, game_speed, player_initial_y, out_of_screen_func, car_speed, car_spawn_rate, player_speed):
        super().__init__(0, 0, w, h)
        self.player = Player(self.w/2, player_initial_y, 0.7, 0.7, player_speed)
        self.player_initial_y = player_initial_y
        self.score = 0
        self.road_size = 0
        self.game_status = 0 # 0 - playing, 1 - game over
        self.modules = []
        self.__start()
        self.out_of_screen_bounds = out_of_screen_func
        self.gen_bounds = (-2, 20)
        self.game_speed = game_speed # squares per second
        self.player_speed = player_speed * game_speed
        self.car_speed = car_speed * game_speed
        self.car_spawn_rate = car_spawn_rate

    def __start(self):
        self.add_module(SimpleGrass(0, 0, self.w, 16))

    def add_module(self, module):
        self.modules.append(module)
        self.road_size += module.h
    
    def generate_module(self):
        module = SimpleRoad(0, self.road_size, self.w, randint(1, 4), self.car_spawn_rate, self.car_speed)
        self.add_module(module)
        grass = SimpleGrass(0, self.road_size, self.w, 2)
        self.add_module(grass)
    
    def free_module(self, module=None):
        if not module:
            module = self.modules.pop(0)
        module.destroy()

    def check_gameover(self):
        def get_line_point(x, p1, p2):
            return (p2[1] - p1[1]) / (p2[0] - p1[0]) * (x - p1[0]) + p1[1]
        if self.player.life <= 0:
            self.gameover()
        if self.out_of_screen_bounds(self.player.x, self.player.y):
            self.gameover()
        if not self.modules[0].y <= self.player.y < self.modules[-1].y + self.modules[-1].h:
            self.gameover()
        if not self.modules[0].x <= self.player.x < self.modules[0].x + self.modules[0].w:
            self.gameover()

    def update(self, delta_time):
        if self.player.y - 8 > self.score:
            self.score = int(self.player.y - 8)
        if self.check_gameover():
            self.gameover()
        else:
            self.y += self.game_speed * delta_time
        if self.y + self.h > self.road_size - self.gen_bounds[1]:
            self.generate_module()
        while self.modules[0].y + self.modules[0].h < self.y + self.gen_bounds[0]:
            self.free_module()
        if self.player.y > self.y + self.h / 2:
            self.y = self.player.y - self.h / 2

    def gameover(self):
        Engine.pause()
        self.game_status = 1
        print('Game Over')

    def reset(self):
        for module in self.modules:
            module.destroy()
        self.modules.clear()
        self.x = 0
        self.y = 0
        self.road_size = 0
        self.player.x = int(self.w/2)
        self.player.y = 8
        self.player.life = 1
        self.player.next_position = (self.player.x, self.player.y)
        self.game_status = 0
        self.score = 0
        self.__start()
        Engine.unpause()
        