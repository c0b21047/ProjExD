import pygame as pg
import sys
import random
import datetime 

OBJECT_RATE = 200 #障害物の生成レート
MAX_OBJECT = 3 #障害物の最大個数

class Screen:
    """
    スクリーン生成クラス
    """
    def __init__(self, title, rect, file):
        """
        title：スクリーンのタイトル\n
        rect：スクリーンの大きさ\n
        file：背景画像のファイルパス
        """
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(rect)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(file)
        self.bgi_rct = self.sfc.get_rect()
        self.bg_x = 0

    def blit(self):
        """
        描画
        """
        self.sfc.blit(self.bgi_sfc, [self.bg_x-1600, 0])
        self.sfc.blit(self.bgi_sfc, [self.bg_x, 0])
    
    def update(self,speed):
        """
        背景を動かす\n
        speed：背景を動かす速度
        """
        self.bg_x = (self.bg_x - speed)%1600
        self.blit()
         

class Tori:
    """
    こうかとん画像クラス
    """
    def __init__(self, img, zoom, xy):
        """
        img：画像ファイルのパス\n
        zoom：拡大率\n
        xy：初期座標のタプル
        """
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vel = 0 #移動速度(ジャンプの速度)

    def blit(self, scr:Screen):
        """
        描画\n
        scr：スクリーンのインスタンス
        """
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        """
        動きの設定\n
        scr：スクリーンのインスタンス
        """
        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE] and self.vel == 0: #スペースキーでジャンプ
            self.vel = -8

        self.vel += 0.1 #重力を加算

        self.rct.centery += self.vel #移動

        if self.rct.centery >  450: #もとの位置を通り過ぎたら戻す
            self.rct.centery = 450
            self.vel = 0
        
        self.blit(scr)


class Obj:
    """
    障害物用クラス
    """
    def __init__(self,img,zoom,xy):
        """
        img：画像ファイルのパス\n
        zoom：拡大率\n
        xy：初期座標
        """
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self,scr:Screen):
        """
        描画\n
        scr：スクリーンのインスタンス
        """
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen,speed):
        """
        動きの設定\n
        scr：スクリーンのインスタンス\n
        speed：障害物が迫ってくる速さ
        """
        self.rct.centerx -= speed
        self.blit(scr)  


class Txt:
    """
    テキスト表示用クラス
    """
    def __init__(self,font,color,xy,text):
        """
        font：フォント\n
        color：文字の色\n
        xy：文字の中心座標\n
        text：テキストの内容
        """
        self.text = font.render(text, True, color)
        self.rct = self.text.get_rect()
        self.rct.center = xy

    def blit(self,scr:Screen):
        scr.sfc.blit(self.text, self.rct)
    

class Score():
    """
    スコア用クラス
    """
    def __init__(self,font,color):
        self.val = 0
        self.fonto = font 
        self.color = color
       
    def blit(self,scr:Screen):
        scr.sfc.blit(self.fonto.render(f"score:{self.val:.0f}",True,self.color), (0, 0))
        
    def add_score(self):
        self.val += 100

    def update(self,scr:Screen ):
        self.val += 0.1
        self.blit(scr)


def start_scr():
    """
    最初の画面
    """
    start_txt = Txt(pg.font.Font(None,120), "BLACK", (800, 450), "Push any key to start")
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type== pg.QUIT:
                return None
            if event.type == pg.KEYUP:
                return main()
                
        scr.update(0)
        start_txt.blit(scr)
        pg.display.update()
        clock.tick(1000)


def end_scr(score):
    """
    最後の画面
    """
    end_txt = Txt(pg.font.Font(None,120), "BLACK", (800, 300), "GAME OVER")
    end_score = Txt(pg.font.Font(None,80), "BLACK", (800, 500), f"Score: {score:.0f}")
    end_restart = Txt(pg.font.Font(None,60), "BLACK", (800, 700), "Push R to return to start")

    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type== pg.QUIT:
                return True
            if event.type == pg.KEYUP and event.key == pg.K_r:
                return False
                
        scr.update(0)
        end_txt.blit(scr)
        end_score.blit(scr)
        end_restart.blit(scr)
        pg.display.update()
        clock.tick(1000)


def main():
    """
    メイン関数
    """
    kkt = Tori("fig/3_1.png", 2.0, (600, 450)) #こうかとんのインスタンス生成
    obj_lst = ["fig/textbook1_kokugo.png", "fig/textbook2_sansu.png",
        "fig/textbook3_sugakuu.png", "fig/textbook4_rika.png",
        "fig/textbook5_syakai.png", "fig/textbook6_eigo.png"] #障害物のファイルパスのリスト
    objects = [] #障害物のインスタンス用のリスト

    speed = 5 #速度

    score = Score(pg.font.Font(None,60), "BLACK") #スコア表示インスタンス生成
    sub_score = 0 #速度上昇時の計算用

    clock = pg.time.Clock()
    while True:
        scr.update(speed)
        for event in pg.event.get():
            if event.type== pg.QUIT:
                return
        
        kkt.update(scr)
        if not int(random.random() * OBJECT_RATE) and len(objects) < MAX_OBJECT: #障害物の生成条件
            objects.append(Obj(random.choice(obj_lst), 0.5, (scr.rct.width,450))) #障害物のインスタンス生成
        
        for i,objct in enumerate(objects): #各障害物について
            objct.update(scr,speed)
            if kkt.rct.colliderect(objct.rct): #衝突判定
                return score.val

            if objct.rct.centerx < 0: #画面外にいった障害物を削除
                del objects[i]
                score.add_score()
                if score.val - sub_score > 1000: #スコアが1000の倍数を超えるたびに加速
                    speed += 1
                    sub_score += 1000

        score.update(scr)
        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    scr = Screen("避けろ！こうかとん", (1600,900), "fig/pg_bg.jpg") #スクリーンのインスタンス生成
    while True:
        score = start_scr()
        if end_scr(score):
            break
    pg.quit()
    sys.exit()