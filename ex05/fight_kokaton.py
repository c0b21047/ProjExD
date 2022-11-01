import pygame as pg
import sys
from random import randint,choice

BIRD_CH_SPEED = 2
FIRE_RATE = 100

class Screen:
    """
    スクリーン生成クラス
    """
    def __init__(self, title, rect, file):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(rect)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file)
        self.bgi_rct = self.sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) # 練習2


class Bird:
    """
    こうかとん画像クラス
    """

    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.fac = [0,0]
        self.vel = 1
        self.reload = 0

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        key_delta = {
            pg.K_UP:    [0, self.vel * (-1)],
            pg.K_DOWN:  [0, self.vel],
            pg.K_LEFT:  [self.vel * (-1), 0],
            pg.K_RIGHT: [self.vel, 0],
        }
        fac_x, fac_y = 0, 0

        if key_states[pg.K_LSHIFT]: #左シフトを押している間加速
            self.vel  = BIRD_CH_SPEED
        else:
            self.vel = 1

        for key, delta in key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                fac_x += delta[0]
                fac_y += delta[1]
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.fac = [fac_x,fac_y]
        if self.reload != 0:
            self.reload -= 1
        self.blit(scr)
    

class Shot:
    def __init__(self, scr:Screen,kkt:Bird):
        rote_dict = {315:[-1, -1], 270:[-1, 0], 225:[-1, 1], 0:[0, -1],
                     180:[0, 1], 45:[1, -1], 90:[1, 0], 135:[1, 1]}
        self.sfc = pg.Surface((20, 20))
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.polygon(self.sfc, (255, 0, 255), [(10, 0), (20, 5), (15, 20), (5, 20), (0, 10)])
        for key,item in rote_dict.items():
            if item == kkt.fac:
                self.sfc = pg.transform.rotate(self.sfc, key)
        self.rct = self.sfc.get_rect()
        self.rct.center = kkt.rct.center
        self.vx = kkt.fac[0] * 5
        self.vy = kkt.fac[1] * 5

    def blit(self,scr):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr):
        self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)

class Bomb:
    """
    爆弾クラス
    """
    def __init__(self, colors, radius, velocity, scr:Screen):
        self.sfc = pg.Surface((20, 20)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        self.color = colors
        pg.draw.circle(self.sfc, self.color, (10, 10), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        spawn_lst = [(randint(20, scr.rct.width-20), 20),
                     (scr.rct.width-20, randint(20, scr.rct.height-20)),
                     (scr.rct.height-20, randint(20, scr.rct.width-20)),
                     (20, randint(20, scr.rct.height-20))]
        self.rct.center = choice(spawn_lst)
        self.vx, self.vy = velocity
        self.life = 1

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

    def update(self, scr:Screen):
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.rct.move_ip(self.vx, self.vy) # 練習6
        self.blit(scr) # 練習5


class Point: 
    """
    三角形の作成とランダムな初期位置の設定
    """
    def __init__(self,scr:Screen):
        self.sfc = pg.Surface((20,20))
        self.sfc.set_colorkey("black")
        self.rct = self.sfc.get_rect()
        self.rct.center = randint(10,scr.rct.width-10), randint(10, scr.rct.height-10)
        self.color = (255,0,0)
        pg.draw.polygon(self.sfc,self.color,[(0,20),(10,0),(20,20)],0)

    def ch_xy(self,scr):
        self.rct.center = randint(10,scr.rct.width-10), randint(10, scr.rct.height-10)

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen):
        pg.draw.polygon(self.sfc,self.color,[(0,20),(10,0),(20,20)],0)
        self.color = ch_color(self.color)
        self.blit(scr)


def ch_color(color):
    R, G, B = color
    if R == 255: #三角形の色変え
        if B != 0:
            B -= 3
        else:
            G += 3
    if G == 255:
        if R != 0:
            R -= 3
        else:
            B += 3
    if B == 255:
        if G != 0:
            G -= 3
        else:
            R += 3
    return R, G, B
         

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    score = 0
    fvx, fvy = 1,1
    # 練習1
    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")

    # 練習3
    kkt = Bird("fig/6.png", 2.0, (900, 400))

    # 練習5
    bombs = [Bomb((255,0,0), 10, (fvx,fvy), scr)]
 
    pnt = Point(scr)

    fonto = pg.font.Font(None,40) #スコア表示のフォント
    
    clock = pg.time.Clock() # 練習1
    bullets = []
    while True:
        scr.blit()
        for event in pg.event.get(): # 練習2
            if event.type== pg.QUIT:
                return

        score_txt = fonto.render(f"score:{score}",True,"WHITE") #スコア表示用のテキスト
        scr.sfc.blit(score_txt,(0,0))
        for bmb in bombs:
            bmb.update(scr)
        pnt.update(scr)
        
        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE]:
            if kkt.fac != [0, 0] and kkt.reload == 0:
                bullets.append(Shot(scr,kkt))
                kkt.reload = FIRE_RATE

        if bullets:
            for ins in bullets:
                ins.update(scr)

        kkt.update(scr)

        if pg.time.get_ticks()%1000 == 1:
            bombs.append(Bomb((255,0,0), 10, (+1,+1), scr))

        for i,bmb in enumerate(bombs,0):
                #    練習8
            if kkt.rct.colliderect(bmb.rct): # こうかとんrctが爆弾rctと重なったら
                return

            for bullet in bullets:
                if bullet.rct.colliderect(bmb.rct):
                    bmb.life -= 1
                    print(bmb.life)
                    if bmb.life <= 0:
                        del bombs[i]
                        print(len(bombs))



        if kkt.rct.colliderect(pnt.rct): #得点処理
            score += 1
            pnt.ch_xy(scr)
            if score % 3 == 0: #スコアが3の倍数時に速度が2倍
                for bomb in bombs:
                    bomb.vx *= 2
                    bomb.vy *= 2
                fvx *= 2
                fvy *= 2



        pg.display.update() #練習2
        clock.tick(1000)



if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()
