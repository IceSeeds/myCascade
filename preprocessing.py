
import os
import sys
import shutil

from PIL import Image

class Preprocessing():
    def __init__( self, out_name, def_ng = False, finish = False ):
        self.abs_path = os.path.dirname( os.path.abspath( __file__ ) ) + "\\"

        self.out_name = out_name

        self.ng_folder = "ng"
        self.ok_folder = "ok"

        self.ng_list_name = "ng_list.txt"
        self.ok_list_name = "ok_list.txt"

        self.def_ng = def_ng

        self.finish = finish

        if not self.finish:
            self.out_folder = self.abs_path
            try:
                os.remove( self.abs_path + self.ng_list_name )
                os.remove( self.abs_path + self.ok_list_name )
                os.remove( self.abs_path + self.out_name )
            except FileNotFoundError or PermissionError:
                pass
            

    def __pre( self ):        
        if not os.path.exists( self.out_folder ):
            os.mkdir( self.out_folder )
        else:
            print( "folder 作成完了" )

        if not os.path.exists( self.out_folder + self.ng_folder ):
            os.mkdir( self.out_folder + self.ng_folder )
        if not os.path.exists( self.out_folder + self.ok_folder ):
            os.mkdir( self.out_folder + self.ok_folder )

    def __gif2png( self, path, file ):
        file_path = path + file
        img_path = file_path.split( "." )[0]

        img = Image.open( file_path )
        img.save( img_path + '.png' )


    def file_ng( self ):
        if self.def_ng:
            self.ng_list_name = "def_ng_list.txt"
            self.ng_folder    = "def_ng"

        out_name = self.out_folder + self.ng_list_name
        ng_path  = self.out_folder + self.ng_folder + "\\"
        
        all_file = ""
        files = os.listdir( ng_path )
        for file in files:
            img_path = ng_path + file
            all_file += img_path + "\n"
            
        with open( out_name, mode='w', encoding="utf-8" ) as f:
            f.write( all_file )

    def file_ok( self ):
        out_name = self.out_folder + self.ok_list_name
        ok_path  = self.out_folder + self.ok_folder + "\\"

        all_file = ""
        files = os.listdir( ok_path )
        for file in files:
            if file.endswith( '.gif' ):
                self.__gif2png( ok_path, file )
                os.remove( ok_path + file )
            if not file.endswith( '.png' ):
                continue

            img = Image.open( ok_path + file )
            all_file += self.ok_folder + "\\" + file + " 1 1 1 " + str( img.size[0] - 1 ) + " " + str( img.size[1] - 1 ) + "\n"

        with open( out_name, mode='w', encoding="utf-8" ) as f:
            f.write( all_file )


    def create_samples( self, num = 1000 ):
        create = ( self.abs_path + "opencv_createsamples"
                   " -vec " + self.out_folder + self.out_name + ".vec"
                   " -info " + self.out_folder + self.ok_list_name +
                   " -num " + str( num ) + 
                   " -bgcolor 0" )
        print( create )
        os.system( create )

    def train_sample( self, out_file, vec_file, neg_num = 10, stage_num = 20, pos_num = 0,  ):
        if not os.path.exists( self.out_folder + out_file ):
            os.mkdir( self.out_folder + out_file )
        
        pos_num = sum( os.path.isfile( os.path.join( self.abs_path + self.ok_folder, name ) ) for name in os.listdir( self.abs_path + self.ok_folder ) ) 

        os.system( self.abs_path + "opencv_traincascade.exe"
                   " -data " + self.out_folder +  out_file + 
                   " -vec " + self.out_folder + vec_file + ".vec"
                   " -bg " + self.out_folder + self.ng_list_name +
                   " -numStages " + str( stage_num ) + 
                   " -numPos " + str( pos_num * 0.9 ) + 
                   " -numNeg " + str( neg_num ) )


    def move_glob( self, src_path, dst_path ):
        for file in os.listdir( src_path ):
            src_all = os.path.join( src_path, file )
            dst_all = os.path.join( dst_path, file )
        
            shutil.move( src_all, dst_all )

    def main( self, pos_num = 5, neg_num = 10, stage_num = 20 ):
        if self.finish:
            __out = self.abs_path + self.out_name + "\\" + self.out_name + "\\"
            if not os.path.exists( __out ):
                os.mkdir( __out )
            shutil.move( self.abs_path + self.out_name + ".vec", __out )
            if not self.def_ng:
                shutil.move( self.abs_path + self.ng_list_name, __out )
            shutil.move( self.abs_path + self.ok_list_name, __out )

            if not os.path.exists( __out + self.ng_folder ):
                os.mkdir( __out + self.ng_folder )
            if not os.path.exists( __out + self.ok_folder ):
                os.mkdir( __out + self.ok_folder )

            if not self.def_ng:
                self.move_glob( self.abs_path + self.ng_folder, __out + self.ng_folder )
            self.move_glob( self.abs_path + self.ok_folder, __out + self.ok_folder )

            sys.exit()

        if not os.path.exists( self.out_name + self.ng_list_name ):
            self.file_ng()

        if not os.path.exists( self.out_name + self.ok_list_name ):
            self.file_ok()

        if not os.path.exists( self.out_name + self.out_name + ".vec" ):
            self.create_samples()
        
        self.train_sample( self.out_name, self.out_name, pos_num=pos_num, neg_num=neg_num, stage_num=stage_num )

#pre.move_glob(  pre.abs_path + pre.ng_folder, pre.out_folder + pre.ng_folder )
#pre.move_glob(  pre.abs_path + pre.ok_folder, pre.out_folder + pre.ok_folder )

"""
if __name__ == '__main__':
    pre = Preprocessing( "kurumi_02", finish=False )
    pre.main( neg_num=5 )

    cap.Caption( pre.abs_path + pre.out_name )
"""
