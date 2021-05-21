
import numpy as np

from PIL import ImageGrab
import cv2


class Caption():
    def __init__( self, cascade_path_file ):
        self.cap( cascade_path_file )

    def cap( self, cascade_path, mode=1 ):
        while True:
            # スクリーンキャプチャ
            if( mode == 1 ):
                img = ImageGrab.grab( all_screens=True, bbox=( 1920, 0, 3840, 1080 ) )#subモニター
            elif( mode == 0 ):
                img = ImageGrab.grab()#mainモニター
            # PILのimageをndarrayに変換
            cv_img = np.array( img, dtype = np.uint8 )
            # 色変換
            #cv_img = cv2.cvtColor( cv_img, cv2.COLOR_RGB2BGR )
            cv_img = self.head( cascade_path, cv_img )
            # テスト：画面表示
            cv2.imshow( 'figure', cv_img )
            #cv2.waitKey( 0 )
            key = cv2.waitKey( 1 )
            # Escキーを入力されたら画面を閉じる
            if key == 27:
                break

        cv2.destroyAllWindows()

    def head( self, cascade_path, img ):
        #画像をグレースケールにする
        gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
        face_cascade = cv2.CascadeClassifier( cascade_path + "\\cascade.xml" )
        #顔検出を実行!
        faces = face_cascade.detectMultiScale( gray )
        #facesに顔の位置が入っているので、for文で読み取る
        for( x, y, w, h ) in faces:
        #矩形を顔の位置に矩形を描画する
            img = cv2.rectangle( img, ( x, y ), ( x + w, y + h ), ( 0, 0, 255 ), 2 )
        #色の順番を変更する
        img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )

        return img

#Caption( "AI_Kurumi\\kurumi_01" )