import pygame as pg
import sys
import random

# 練習7
def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''

    yoko, tate = +1, +1 # 領域
    yoko2, tate2 = +1, +1

    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko2 = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate2 = -1 # 領域外
    return yoko, tate

def main():
    count = 0 #爆弾にあたっている時間を計測
    clock = pg.time.Clock()

    # 練習1：スクリーンと背景画像
    pg.display.set_caption("逃げろ！こうかとん")
    screen_sfc = pg.display.set_mode((1600, 900)) # Surface
    screen_rct = screen_sfc.get_rect()            # Rect
    bgimg_sfc = pg.image.load("fig/pg_bg.jpg")    # Surface
    bgimg_rct = bgimg_sfc.get_rect()              # Rect
    screen_sfc.blit(bgimg_sfc, bgimg_rct)


    # 練習3：こうかとん
    kkimg_sfc = pg.image.load("fig/6.png")    # Surface
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0)  # Surface
    kkimg_rct = kkimg_sfc.get_rect()          # Rect
    kkimg_rct.center = 900, 400

    #追加：”ヒット”画像読み込み
    gameov_sfc = pg.image.load("fig/hit.jpeg")
    gameov_rct = gameov_sfc.get_rect()
    gameov_rct.center = (500, 300)
 
    #追加：爆弾を画像に変更
    bm1size = random.randint(100, 300)
    bmimg_sfc = pg.image.load("fig/bomb.png") # Surface
    bmimg_sfc = pg.transform.scale(bmimg_sfc, (bm1size, bm1size)) #Surface
    bmimg_rct = bmimg_sfc.get_rect() # Rect
    bmimg_rct.centerx = random.randint(0, screen_rct.width)
    bmimg_rct.centery = random.randint(0, screen_rct.height)
    vx, vy = +1, +1 # 練習6

    #追加：爆弾を1つ追加
    bm2size = random.randint(100, 300)
    bmimg2_sfc = pg.image.load("fig/bomb.png") # Surface
    bmimg2_sfc = pg.transform.scale(bmimg2_sfc, (bm2size, bm2size)) #Surface
    bmimg2_rct = bmimg_sfc.get_rect()
    bmimg2_rct.centerx = random.randint(0, screen_rct.width)
    bmimg2_rct.centery = random.randint(0, screen_rct.height)
    vx2, vy2 = +1, +1

    while True:
        screen_sfc.blit(bgimg_sfc, bgimg_rct)

        # 練習8
        if kkimg_rct.colliderect(bmimg_rct): 
            screen_sfc.blit(gameov_sfc, gameov_rct)
            count += 1
            
        if kkimg_rct.colliderect(bmimg2_rct):
            screen_sfc.blit(gameov_sfc, gameov_rct)
            count += 1
        
        #countが1000に達したら終了
        if count == 1000:
            return

        # 練習2
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        # 練習4
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]    == True: kkimg_rct.centery -= 3
        if key_states[pg.K_DOWN]  == True: kkimg_rct.centery += 3
        if key_states[pg.K_LEFT]  == True: kkimg_rct.centerx -= 3
        if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx += 3
        
        # 練習7
        if check_bound(kkimg_rct, screen_rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]    == True: kkimg_rct.centery += 3
            if key_states[pg.K_DOWN]  == True: kkimg_rct.centery -= 3
            if key_states[pg.K_LEFT]  == True: kkimg_rct.centerx += 3
            if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx -= 3
        screen_sfc.blit(kkimg_sfc, kkimg_rct)

        #爆弾の速度上昇
        if key_states[pg.K_s] == True:
            vx += 0.03
            vy += 0.03
            vx2 += 0.03
            vy2 += 0.03

        # 練習6
        bmimg_rct.move_ip(vx, vy)
        bmimg2_rct.move_ip(vx2, vy2)

        # 練習5
        screen_sfc.blit(bmimg_sfc, bmimg_rct)
        screen_sfc.blit(bmimg2_sfc, bmimg2_rct)
        # 練習7
        yoko, tate = check_bound(bmimg_rct, screen_rct)
        vx *= yoko
        vy *= tate
        yoko2, tate2 = check_bound(bmimg2_rct, screen_rct)
        vx2 *= yoko2
        vy2 *= tate2

        pg.display.update()
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

    
