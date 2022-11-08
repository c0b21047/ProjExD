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
        title：スクリーンのタイトル
        rect：スクリーンの大きさ
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
        背景を動かす
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
        img：画像ファイルのパス
        zoom：拡大率
        xy：初期座標のタプル
        """
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vel = 0 #移動速度(ジャンプの速度)

    def blit(self, scr:Screen):
        """
        描画
        scr：スクリーンのインスタンス
        """
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        """
        動きの設定
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
        img：画像ファイルのパス
        zoom：拡大率
        xy：初期座標
        """
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self,scr:Screen):
        """
        描画
        scr：スクリーンのインスタンス
        """
        scr.sfc.blit(self.sfc,self.rct)

    def update(self,scr:Screen,speed):
        """
        動きの設定
        scr：スクリーンのインスタンス
        speed：障害物が迫ってくる速さ
        """
        self.rct.centerx -= speed
        self.blit(scr)  


class Score:
    """
    スコア用クラス
    """
    def __init__(self,font,color):
        self.val = 0
        self.fonto = font #スコア表示のフォント
        self.color = color
       
    def blit(self,scr:Screen):
        scr.sfc.blit(self.fonto.render(f"score:{self.val:.0f}",True,self.color), (0, 0))
        
    def add_score(self):
        self.val += 100

    def update(self,scr:Screen ):
        self.val += 0.1
        self.blit(scr)

def main():
    """
    メイン関数
    """
    scr = Screen("避けろ！こうかとん", (1600,900), "fig/pg_bg.jpg") #スクリーンのインスタンス生成
    kkt = Tori("fig/3_1.png", 2.0, (600, 450)) #こうかとんのインスタンス生成
    obj_lst = ["fig/textbook1_kokugo.png", "fig/textbook2_sansu.png",
        "fig/textbook3_sugakuu.png", "fig/textbook4_rika.png",
        "fig/textbook5_syakai.png", "fig/textbook6_eigo.png"] #障害物のファイルパスのリスト
    objects = [] #障害物のインスタンス用のリスト

    speed = 5 #速度

    score = Score(pg.font.Font(None,60), "BLACK")
    sub_score = 0

    clock = pg.time.Clock() # 練習1
    while True:
        scr.update(speed)
        for event in pg.event.get(): # 練習2
            if event.type== pg.QUIT:
                return
        
        kkt.update(scr)
        if not int(random.random() * OBJECT_RATE) and len(objects) < MAX_OBJECT: #障害物の生成
            objects.append(Obj(random.choice(obj_lst), 0.5, (scr.rct.width,450))) #障害物のインスタンス生成
        
        for i,objct in enumerate(objects): #各障害物について
            objct.update(scr,speed)
            if kkt.rct.colliderect(objct.rct): #衝突判定
                return

            if objct.rct.centerx < 0: #画面外にいった障害物を削除
                del objects[i]
                score.add_score()
                if score.val - sub_score > 1000:
                    speed += 1
                    sub_score += 1000

        score.update(scr)
        pg.display.update() #練習2
        clock.tick(1000)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()