from typing import KeysView
import pygame as pg
import sys
import random

def check_bound(obj_rct,scr_rct):
    """
    obj_rct：こうかとんrct、または、爆弾rct
    scr_rct：スクリーンrct
    領域内：+1/領域外：-1
    """
    yoko, tate = 1,1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko,tate


    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect() #練習１

    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc,0,2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900,400 #練習3

    draw_sfc = pg.Surface((20,20))
    pg.draw.circle(draw_sfc, (255,0,0), (10,10), 10)
    draw_sfc.set_colorkey("black")
    draw_rct = draw_sfc.get_rect()
    draw_rct.center = random.randint(0,scrn_rct.width),random.randint(0,scrn_rct.height) #練習5
    vx,vy = 1,1

    clock = pg.time.Clock()
    while True:
        scrn_sfc.blit(bg_sfc,bg_rct)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_stats = pg.key.get_pressed()
        if key_stats[pg.K_UP]:
            tori_rct.centery -= 1
        if key_stats[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_stats[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_stats[pg.K_RIGHT]:
            tori_rct.centerx += 1 #練習4

        yoko,tate = check_bound(tori_rct,scrn_rct)
        if yoko == -1:
            if key_stats[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_stats[pg.K_RIGHT]:
                tori_rct.centerx -= 1
        if tate == -1:
            if key_stats[pg.K_UP]:
                tori_rct.centery += 1
            if key_stats[pg.K_DOWN]:
                tori_rct.centery -= 1

        yoko, tate = check_bound(draw_rct,scrn_rct)
        vx *= yoko
        vy *= tate
        draw_rct.move_ip(vx,vy) #練習7

        scrn_sfc.blit(draw_sfc,draw_rct)
        scrn_sfc.blit(tori_sfc,tori_rct)

        if tori_rct.colliderect(draw_rct): #練習8
            return

        pg.display.update()
        clock.tick(1000) #練習2
    


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
