import pgzrun
from pgzero.actor import Actor
from pgzero.rect import Rect
import random

# TELA E MUNDO
CELL_SIZE = 32
WORLD_CELLS = 32
WIDTH = CELL_SIZE * WORLD_CELLS
HEIGHT = CELL_SIZE * WORLD_CELLS

# ESTADO
STATE_MENU = 0
STATE_PLAY = 1

# CONTROLE DO SOM DE PASSO
is_walking_sound_playing = False

# MENU
class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.rect = Rect(pos, size)

    def draw(self):
        screen.draw.filled_rect(self.rect, "gray")
        screen.draw.textbox(self.text, self.rect, color="white")

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# JOGADOR E INIMIGOS
class GameObject:
    def __init__(self, prefix, start_cell):
        self.prefix = prefix
        self.cell = [start_cell[0], start_cell[1]]
        self.last_cell = [start_cell[0], start_cell[1]]
        self.frame = 0
        self.anim_timer = 0.0
        self.direction = 'left'  # Inicia o jogador indo para a esquerda
        self.moving = False

        self.walk_frames = {
            'left': [f"{prefix}_walk{i}_left" for i in range(1, 7)],
            'right': [f"{prefix}_walk{i}_right" for i in range(1, 7)]
        }

        self.idle_frames = {
            'left': [f"{prefix}_idle{i}_left" for i in range(1, 4)],
            'right': [f"{prefix}_idle{i}_right" for i in range(1, 4)]
        }

        px, py = self.cell[0] * CELL_SIZE, self.cell[1] * CELL_SIZE
        self.actor = Actor(self.idle_frames['left'][0], topleft=(px, py))

    def update(self, dt):
        self.anim_timer += dt
        if self.anim_timer >= 0.1:
            self.anim_timer = 0
            frames = self.walk_frames[self.direction] if self.moving else self.idle_frames[self.direction]
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]

        self.actor.topleft = (
            self.cell[0] * CELL_SIZE,
            self.cell[1] * CELL_SIZE
        )

        self.last_cell[0] = self.cell[0]
        self.last_cell[1] = self.cell[1]

class Player(GameObject):
    def __init__(self, start_cell):
        super().__init__('player', start_cell)
        self.move_timer = 0.0
        self.move_cooldown = 0.1  # Tempo entre passos (em segundos)

    def try_move(self, dx, dy, dt):
        self.move_timer += dt
        if self.move_timer >= self.move_cooldown:
            moved = self.move(dx, dy)
            # Não toca mais som aqui! Controle será feito no update().
            self.move_timer = 0.0

    def move(self, dx, dy):
        nx, ny = self.cell[0] + dx, self.cell[1] + dy
        if 0 <= nx < WORLD_CELLS and 0 <= ny < WORLD_CELLS:
            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'
            if [nx, ny] != self.cell:
                self.cell = [nx, ny]
                return True  # Movido com sucesso
        return False  # Não se moveu

class Enemy(GameObject):
    def __init__(self, prefix, start_cell):
        super().__init__(prefix, start_cell)

    def roam(self):
        if random.random() < 0.02:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)])
            nx = max(0, min(WORLD_CELLS - 1, self.cell[0] + dx))
            ny = max(0, min(WORLD_CELLS - 1, self.cell[1] + dy))

            if dx > 0:
                self.direction = 'right'
            elif dx < 0:
                self.direction = 'left'

            self.cell = [nx, ny]
            self.moving = (dx != 0 or dy != 0)
        else:
            self.moving = False

# INICIAR JOGO
game_state = STATE_MENU
sound_on = True
music_played = False  # Controla se a música já foi iniciada

buttons = [
    Button("Iniciar", (WIDTH // 2 - 80, HEIGHT // 2 - 60), (160, 40)),
    Button("Som: On", (WIDTH // 2 - 80, HEIGHT // 2), (160, 40)),
    Button("Sair", (WIDTH // 2 - 80, HEIGHT // 2 + 60), (160, 40)),
]

background = Actor('background', topleft=(0, 0))
player = Player((5, 5))
enemies = [
    Enemy('enemy1', (10, 10)),
    Enemy('enemy2', (15, 15))
]

def start_music():
    global music_played
    if not music_played:
        music.play('bg_music')
        music.set_volume(0.5)
        music_played = True
    else:
        if sound_on:
            music.unpause()
        else:
            music.pause()

# CICLO DO JOGO
def draw():
    screen.clear()
    if game_state == STATE_MENU:
        for btn in buttons:
            btn.draw()
    else:
        background.draw()
        player.actor.draw()
        for e in enemies:
            e.actor.draw()

def update(dt):
    global game_state, music_played, is_walking_sound_playing
    if game_state == STATE_MENU:
        if not music_played and sound_on:
            start_music()
        elif music_played:
            if sound_on:
                music.unpause()
            else:
                music.pause()
    elif game_state == STATE_PLAY:
        player.moving = keyboard.left or keyboard.right or keyboard.up or keyboard.down

        if keyboard.left:
            player.direction = 'left'
            player.try_move(-1, 0, dt)
        elif keyboard.right:
            player.direction = 'right'
            player.try_move(1, 0, dt)
        elif keyboard.up:
            player.try_move(0, -1, dt)
        elif keyboard.down:
            player.try_move(0, 1, dt)

        player.update(dt)

        for e in enemies:
            e.roam()
            e.update(dt)

        # Controle do som de passos:
        if player.moving:
            if not is_walking_sound_playing:
                sounds.move.play(-1)  # Toca em loop infinito
                is_walking_sound_playing = True
        else:
            if is_walking_sound_playing:
                sounds.move.stop()
                is_walking_sound_playing = False

def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == STATE_MENU:
        if buttons[0].clicked(pos):
            game_state = STATE_PLAY
        elif buttons[1].clicked(pos):
            sound_on = not sound_on
            buttons[1].text = f"Som: {'On' if sound_on else 'Off'}"
            if sound_on:
                music.unpause()
            else:
                music.pause()
        elif buttons[2].clicked(pos):
            exit()

pgzrun.go()