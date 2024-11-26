import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={pg.K_UP:(0,-5),
       pg.K_DOWN:(0,5),
       pg.K_LEFT:(-5,0),
       pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect) -> tuple [bool, bool]:
    """
    引数のrctが画面内かどうか判断する関数
    引数:rct
    戻り値:bool2つのタプル(横,縦）/画面内がTrue
    """
    tate, yoko = True, True  #画面内か判断する
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return (yoko, tate)

def game_over(screen: pg.Surface) -> None:
    """
    演習ex1
    ゲームオーバーの時の処理
    ブラックアウトとGame Overの文字、こうかとんの表示
    引数:スクリーンのsurface
    戻り値なし
    """
    go_img = pg.Surface((WIDTH, HEIGHT))  #ブラックアウト用のsurface
    pg.draw.rect(go_img, 0, pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)
    screen.blit(go_img, [0, 0])
    # Gameoverの文字
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(txt, txt_rct)
    # 泣いてるこうかとん用のsurface(2つ)
    ckk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    ckk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    ckk_rct = ckk_img.get_rect()
    ckk2_rct = ckk2_img.get_rect()
    ckk_rct.center = txt_rct.left-50, HEIGHT/2
    ckk2_rct.center = txt_rct.right+50, HEIGHT/2
    screen.blit(ckk_img, ckk_rct)
    screen.blit(ckk2_img, ckk2_rct)
    pg.display.update()
    time.sleep(5)
    return

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    演習ex2
    拡大した爆弾の大きさと加速度を保存したリストを作る関数
    引数:なし
    戻り値:拡大爆弾Surfaceのリストと加速度のリストのタプル
    """
    accs=[]
    ex_bombs=[]
    for i in range(1, 11):
        accs.append(i)
        bb_img = pg.Surface((20*i, 20*i))
        pg.draw.circle(bb_img, (255, 0, 0), (10*i, 10*i), 10*i)
        bb_img.set_colorkey(0)
        ex_bombs.append(bb_img)
    return (ex_bombs, accs)

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    演習ex3
    移動量に応じて対応する向きの画像のこうかとんを返す関数
    引数:移動量のタプル
    戻り値:向きを変えた画像Surface
    """
    kk_img0=pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgm45=pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9)
    kk_img45=pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9)
    kk_img90=pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 0.9)
    # 方向に応じた画像の辞書の作成
    kk_dict={(0,0):kk_img0,
             (-5,0):kk_img0,
             (-5,-5):kk_imgm45,
             (0,-5):pg.transform.flip(kk_img90, True, True),
             (5,-5):pg.transform.flip(kk_imgm45, True, False),
             (5,0):pg.transform.flip(kk_img0, True, False),
             (5,5):pg.transform.flip(kk_img45, True, False),
             (0,5):pg.transform.flip(kk_img90, True, False),
             (-5,5):kk_img45,
    }
    return kk_dict[sum_mv]

def calc_orientation(org: pg.Rect, dst: pg.Rect,
                     current_xy: tuple[float, float]) -> tuple[float, float]:
    pass

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img=pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)    
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()  #演習2の爆弾拡大関数の呼び出し
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey(0) 
    bb_rct = bb_img.get_rect()
    bb_rct.center = (random.randint(0,WIDTH),random.randint(0,HEIGHT))
    vx,vy=5,5  #爆弾座標の変化量
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  #爆弾と衝突してゲームオーバー
            game_over(screen)  #ゲームオーバー
            return
        screen.blit(bg_img, [0, 0])

        #tmrに応じて爆弾サイズと速度を上昇
        bb_img = bb_imgs[min(tmr//500, 9)]
        #幅と高さを取得
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]

        key_lst = pg.key.get_pressed()
        sum_mv = [0,0]

        for key,move in DELTA.items():  #辞書に移動量を保存
            if key_lst[key]:
                sum_mv[0]+=move[0]
                sum_mv[1]+=move[1]
        kk_img=get_kk_img(tuple(sum_mv))
        kk_rct.move_ip(sum_mv)
        bb_rct.move_ip(avx, avy)
        # こうかとんが画面外だった場合元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        # 爆弾が画面外の場合跳ね返る
        bb_res_y, bb_res_t=check_bound(bb_rct)
        if not bb_res_y:
            vx*=-1
        if not bb_res_t:
            vy*=-1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
