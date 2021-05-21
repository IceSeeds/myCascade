
from preprocessing import Preprocessing
from verification import Caption


if __name__ == '__main__':

    out_file_name = "KEG_UP" #出力フォルダ名
    negtive_num   = 75 #不正解画像数
    stage_num     = 30 #学習回数

    def_ng = True  #既存の不正解画像を使用
    finish = False #一つのフォルダにまとめる

    pre = Preprocessing( out_file_name, def_ng=def_ng, finish=finish )
    pre.main( neg_num=negtive_num, stage_num=stage_num )

    Caption( pre.abs_path + pre.out_name )
