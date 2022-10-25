import pygame as pg
import sys
import random

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

        draw_rct.move_ip(vx,vy) #練習6
        scrn_sfc.blit(draw_sfc,draw_rct)
        scrn_sfc.blit(tori_sfc,tori_rct)

        pg.display.update()
        clock.tick(1000) #練習2
    


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
