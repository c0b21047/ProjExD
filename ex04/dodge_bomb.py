import pygame as pg
import sys
import random

def start(): #スタート画面(未実装)
    font = pg.font.Font(None,120)
    start_txt = font.render(f"push space_key to start", True,"BLACK")

    clock = pg.time.Clock()
    while True:
        scrn_sfc.blit(bg_sfc,bg_rct)
        scrn_sfc.blit(start_txt,(500,500))
        key_stats = pg.key.get_pressed()
        if key_stats[pg.K_SPACE]:
            return
        pg.display.update()
        clock.tick(1000) #練習2

def end(): #ゲームオーバ画面
    score =  main()
    font = pg.font.Font(None,120)
    end_txt = font.render(f"your score is {score}!", True,"BLACK") #スコア表示の文字
    font = pg.font.Font(None,360)
    clock = pg.time.Clock()
    
    R,G,B = 255,0,0 #RGBの初期値
    while True: #ウィンドウが閉じられるまで表示
        scrn_sfc.blit(bg_sfc,bg_rct)
        scrn_sfc.blit(end_txt,(500,500))
        if R == 255: #文字の色変え
            if B != 0:
                B -= 5
            else:
                G += 5
        if G == 255:
            if R != 0:
                R -= 5
            else:
                B += 5
        if B == 255:
            if G != 0:
                G -= 5
            else:
                R += 5

        gameover = font.render("GAME OVER", True,(R,G,B)) #GAMEOVERの文字
        scrn_sfc.blit(gameover,(50,200))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        pg.display.update()
        clock.tick(1000) #練習2
    

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
    #start()
    scrn_sfc.blit(bg_sfc,bg_rct)
    pg.display.update()
    score = 0

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

    point_sfc = pg.Surface((20,20))
    point_sfc.set_colorkey("black")
    point_rct = point_sfc.get_rect()
    point_rct.center = random.randint(0,scrn_rct.width),random.randint(0,scrn_rct.height) #三角形の作成とランダムな初期位置の設定

    fonto = pg.font.Font(None,40) #スコア表示のフォント

    R,G,B = 255,0,0 #RGBの初期値
    clock = pg.time.Clock()

    while True:
        scrn_sfc.blit(bg_sfc,bg_rct)

        score_txt = fonto.render(f"score:{score}",True,"WHITE") #スコア表示用のテキスト
        pg.draw.polygon(point_sfc,(R,G,B),[(0,20),(10,0),(20,20)],0) #三角形の設定
        
        if R == 255: #三角形の色変え
            if B != 0:
                B -= 5
            else:
                G += 5
        if G == 255:
            if R != 0:
                R -= 5
            else:
                B += 5
        if B == 255:
            if G != 0:
                G -= 5
            else:
                R += 5 
         
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_stats = pg.key.get_pressed()
        if key_stats[pg.K_LSHIFT]: #左シフトキーを押している間こうかとんの移動速度が2倍
            tv = 2
        else:
            tv = 1
        if key_stats[pg.K_UP]:
            tori_rct.centery -= tv
        if key_stats[pg.K_DOWN]:
            tori_rct.centery += tv
        if key_stats[pg.K_LEFT]:
            tori_rct.centerx -= tv
        if key_stats[pg.K_RIGHT]:
            tori_rct.centerx += tv #練習4

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
        scrn_sfc.blit(score_txt,(0,0))
        scrn_sfc.blit(draw_sfc,draw_rct)
        scrn_sfc.blit(point_sfc,point_rct)
        scrn_sfc.blit(tori_sfc,tori_rct)

        if tori_rct.colliderect(draw_rct): #練習8
            return score

        if tori_rct.colliderect(point_rct): #得点処理
            score += 1
            point_rct.center = random.randint(0,scrn_rct.width),random.randint(0,scrn_rct.height) #三角形の再配置
            if score % 3 == 0: #スコアが3の倍数時に速度が2倍
                vx *= 2
                vy *= 2

        pg.display.update()
        clock.tick(1000) #練習2
    


if __name__ == "__main__":
    pg.init()
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect() #練習１

    end()
    pg.quit()
    sys.exit()
