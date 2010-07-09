#!/usr/bin/perl

$|=1;
use lib "../../";
use Modules::Constructor;
my $dir="/home/photokazan/domains/photo-kazan.ru/public_html/base/gallery_image";
opendir DIR, $dir;
my @ar=readdir(DIR);
closedir DIR;
	 my $img_logo="/home/photokazan/domains/photo-kazan.ru/public_html/base/vvodnay_200x100.png";


for(my $i=0;$i<=$#ar; $i++){

    my $name=$ar[$i];
    if($name=~s/^(\d+)\.jpg$/$1/){
    print "$name-.jpg\n";
     magick(800,"$dir/$name-.jpg","$dir/$name.jpg"); 
     composit_img("$dir/$name.jpg","$dir/$name.jpg",$img_logo);   
     magick(130,"$dir/$name.jpg","$dir/$name-s.jpg"); 
     magick(450,"$dir/$name.jpg","$dir/$name-m.jpg"); 
    }
}
=r2    
            #делаем маленькую картинку       
                 magick($ref->{width},"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-s.jpg"); 
		 #Делаем картинку 450 по ширине
                 magick(450,"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-m.jpg"); 
=cut