import random
import os

# import basic pygame modules
import pygame as pg

# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


# game constants
MAX_SHOTS = 5  # most player bullets onscreen
STRONG_SHOTS = 1 # maxshotsよりも範囲の広い弾
BULLET_NUMBERS = 5 # STRONG_SHOTSを打てる回数
ALIEN_ODDS = 22  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 12  # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 640, 480)
SCORE = 0
SCENE = 0 #ゲーム画面の状態

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface


def load_sound(file):
    """because pygame can be be compiled without mixer."""
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None

def draw_text(screen,x,y,text,size,col):#文字表示の関数
    font = pg.font.Font(None,size)
    s = font.render(text,True,col)
    x = x - s.get_width()/2
    y = y - s.get_height()/2
    screen.blit(s,[x,y])


class Player(pg.sprite.Sprite):
    """Representing the player as a moon buggy type car."""

    speed = 10
    bounce = 24
    gun_offset = -11
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction:
            self.facing = direction
        self.rect.move_ip(direction * self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)
        if direction < 0:
            self.image = self.images[0]
        elif direction > 0:
            self.image = self.images[1]
        self.rect.top = self.origtop - (self.rect.left // self.bounce % 2)

    def gunpos(self):
        pos = self.facing * self.gun_offset + self.rect.centerx
        return pos, self.rect.top


class Alien(pg.sprite.Sprite):
    """An alien space ship. That slowly moves down the screen."""

    speed = 13
    animcycle = 12
    images = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.facing = random.choice((-1, 1)) * Alien.speed
        self.frame = 0
        if self.facing < 0:
            self.rect.right = SCREENRECT.right

    def update(self):
        self.rect.move_ip(self.facing, 0)
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing
            self.rect.top = self.rect.bottom + 1
            self.rect = self.rect.clamp(SCREENRECT)
        self.frame = self.frame + 1
        self.image = self.images[self.frame // self.animcycle % 3]


class Explosion(pg.sprite.Sprite):
    """An explosion. Hopefully the Alien and not the player!"""

    defaultlife = 12
    animcycle = 3
    images = []

    def __init__(self, actor):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=actor.rect.center)
        self.life = self.defaultlife

    def update(self):
        self.life = self.life - 1
        self.image = self.images[self.life // self.animcycle % 2]
        if self.life <= 0:
            self.kill()


class Shot(pg.sprite.Sprite):

    speed = -11
    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()

class ChargeShot(pg.sprite.Sprite):
    speed = -20
    images = []

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=pos)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top <= 0:
            self.kill()        


class Bomb(pg.sprite.Sprite):
    speed = 9
    images = []

    def __init__(self, alien):
        pg.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=alien.rect.move(0, 5).midbottom)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 470:
            Explosion(self)
            self.kill()


class Score(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = "black"
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(10, 450)

    def update(self):
        if SCORE != self.lastscore:
            self.lastscore = SCORE
            msg = "Score: %d" % SCORE
            self.image = self.font.render(msg, 0, self.color)


class BulletCount(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.font = pg.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = "black"
        self.lastcount = -1
        self.update()
        self.rect = self.image.get_rect().move(530, 450)

    def update(self):
        if BULLET_NUMBERS != self.lastcount:
            self.lastcount = BULLET_NUMBERS
            msg = "BULLETNUM: %d" % BULLET_NUMBERS
            self.image = self.font.render(msg, 0, self.color)

def main(winstyle=0):
    # Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()

    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    fullscreen = False
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # Load images, assign to sprite classes
    # (do this before the classes are used, after screen setup)
    img = load_image("tori.png")
    Player.images = [img, pg.transform.flip(img, 1, 0)]
    img = load_image("effect2.png")
    Explosion.images = [img, pg.transform.flip(img, 0, 0)]
    Alien.images = [load_image(im) for im in ("obake1.png", "obake2.png", "obake3.png")]
    Bomb.images = [load_image("panp.png")]
    Shot.images = [load_image("egg.jpg")]
    ChargeShot.images = [load_image("bimu.png")]
    

    # decorate the game window
    icon = pg.transform.scale(Alien.images[0], (32, 32))
    pg.display.set_icon(icon)
    pg.display.set_caption("負けるな！こうかとん")
    pg.mouse.set_visible(0)

    # create the background, tile the bgd image
    bgdtile = load_image("background.jpg")
    background = pg.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pg.display.flip()

    # Initialize Game Groups
    aliens = pg.sprite.Group()
    shots = pg.sprite.Group()
    bombs = pg.sprite.Group()
    all = pg.sprite.RenderUpdates()
    lastalien = pg.sprite.GroupSingle()

    # assign default groups to each sprite class
    Player.containers = all
    Alien.containers = aliens, all, lastalien
    Shot.containers = shots, all
    ChargeShot.containers = shots, all
    Bomb.containers = bombs, all
    Explosion.containers = all
    Score.containers = all
    BulletCount.containers = all

    # Create Some Starting Values
    global score
    alienreload = ALIEN_RELOAD
    clock = pg.time.Clock()

    # initialize our starting sprites
    global SCORE, BULLET_NUMBERS
    player = Player()
    Alien()  # note, this 'lives' because it goes into a sprite group
    if pg.font:
        all.add(Score())
        all.add(BulletCount())# 特大攻撃の残り回数を描画
        
    # load the sound effects
    boom_sound = load_sound("boom.wav")
    shoot_sound = load_sound("car_door.wav")

    global SCENE
    # Run our main loop whilst the player is alive.
    while player.alive():        
        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen

        keystate = pg.key.get_pressed()       
        if SCENE == 0: # タイトル画面
            screen.blit(background, (0,0))
            draw_text(screen, 320, 200, "Shooting Game", 100, "black")
            draw_text(screen, 340, 350, "S KEY START!!", 50, "red")
            if keystate[pg.K_s] == 1:
                SCENE = 1
                screen.blit(background, (0,0))
        if SCENE == 1: # ゲームプレイ画面
            # clear/erase the last drawn sprites
            all.clear(screen, background)
            # update all the sprites
            all.update()

            # handle player input
            direction = keystate[pg.K_RIGHT] - keystate[pg.K_LEFT]
            player.move(direction)
            firing = keystate[pg.K_SPACE]
            st_firing = keystate[pg.K_z]
            if not player.reloading and firing and len(shots) < MAX_SHOTS:
                Shot(player.gunpos())
                if pg.mixer:
                    shoot_sound.play()

            if not player.reloading and st_firing and len(shots) < STRONG_SHOTS:
                if BULLET_NUMBERS != 0: # 弾丸が0になったらChargeShotクラスの弾丸が打てなくなる
                    ChargeShot(player.gunpos())
                    BULLET_NUMBERS -= 1
                if pg.mixer:
                    shoot_sound.play()
            player.reloading = firing

            # Create new alien
            if alienreload:
                alienreload = alienreload - 1
            elif not int(random.random() * ALIEN_ODDS):
                Alien()
                alienreload = ALIEN_RELOAD

            # Drop bombs
            if lastalien and not int(random.random() * BOMB_ODDS):
                Bomb(lastalien.sprite)

            # Detect collisions between aliens and players.
            for alien in pg.sprite.spritecollide(player, aliens, 1):
                if pg.mixer:
                    boom_sound.play()
                Explosion(alien)
                Explosion(player)
                SCORE = SCORE + 1
                player.kill()

            # See if shots hit the aliens.
            for alien in pg.sprite.groupcollide(aliens, shots, 1, 1).keys():
                if pg.mixer:
                    boom_sound.play()
                Explosion(alien)
                SCORE = SCORE + 1

            # SCOREが10に達したらクリア
            if SCORE == 10:
                # 生存時間
                cong_font = pg.font.Font(None, 100)
                cong_text = cong_font.render("Congratulation!!", True, "black")
                screen.blit(cong_text, [50, 200])
                pg.display.flip()
                pg.time.wait(2000)
                return

            # See if alien boms hit the player.
            for bomb in pg.sprite.spritecollide(player, bombs, 1):
                if pg.mixer:
                    boom_sound.play()
        
                Explosion(player)
                Explosion(bomb)
                player.kill()

            # draw the scene
            dirty = all.draw(screen)
            pg.display.update(dirty)
            
            # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
            clock.tick(40)

        pg.display.update()


    # 生存時間
    time_font = pg.font.SysFont(None, 50)
    timer = (pg.time.get_ticks()//1000)
    text = time_font.render(f"Survival time: {timer}seconds", True, (0, 0, 0))
    screen.blit(text, [130, 300])
    pg.display.update()
    pg.time.wait(2000)

# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()
