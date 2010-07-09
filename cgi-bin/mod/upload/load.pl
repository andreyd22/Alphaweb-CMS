#!/usr/bin/perl
$|=1;
use lib "../../";
use Modules::Constructor;
#use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
        $ref->{'time'}=time;
        $ref->{prefix}=$ref->{user_doman};
        $ref->{prefix}=~s/\-|\./_/gi;
        $ref->{prefix}='';
 my $mes=check_auth($ref);
 if($mes){
   print qq[
     <HTML>
  <body>
  <script>location.href="/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes"</script>
  </body>
    
    </HTML>
     ];
 exit;
 }

 if ($ref->{a} eq '') {&main($ref)}
 if ($ref->{a} eq 'edit_gallery') {&edit_gallery($ref)} #–едактируем галерею фотографий
 if ($ref->{a} eq 'cat_image') {&cat_image($ref)}
 if ($ref->{a} eq 'cat_excel_export') {&cat_excel_export($ref)}
 if ($ref->{a} eq 'cat_excel_import') {&cat_excel_import($ref)}
 if ($ref->{a} eq 'unzip') {&main($ref);&unzip($ref);}
sub main {
  my $time=time;
  my $ref=shift;
  my $upfile=$ref->{upfile};
      if($upfile ne ''){
 if($ref->{save} eq 'ok'){
      my @ar1=split /\\/,$upfile;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
        my ($buf);
         open A, "+>$ref->{path_host}/$ref->{dir}/$file";
         binmode(A);
#       print qq[ok $upfile to $ref->{path_host}/$ref->{dir}/$file]; exit;
         while (my $bytesread = read($upfile, $buf, 1024)) {
#        print qq[$bytesread . ];
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/$ref->{dir}/$file";
        close A;
 my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks)
 = stat("$ref->{path_host}/$ref->{dir}/$file");
$size=$size/1024;
#if($size>1000){
#unlink "$ref->{path_host}/$ref->{dir}/$file";
#}
#print qq[$ref->{path_host}/$ref->{dir}/$file];exit;
if(!$ref->{ok}){
#print qq[загрузка прошла]; exit;
print qq[  <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&name_form=$ref->{name_form}&rnd=$time'></HEAD></HTML>];
}else{
print qq[  <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/img_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&name_form=$ref->{name_form}&rnd=$time'></HEAD></HTML>];
}
        }      
      }
      else{
if(!$ref->{ok}){
print qq[  <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&name_form=$ref->{name_form}&l=$ref->{l}&rnd=$time'></HEAD></HTML>];
}else{
print qq[  <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/img_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&name_form=$ref->{name_form}&rnd=$time'></HEAD></HTML>];
}
      }
}
sub unzip {
  my $time=time;
  my $ref=shift;
 if($ref->{save} eq 'ok'){
  my $upfile=$ref->{upfile};
      my @ar1=split /\\/,$upfile;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
  if(-e "$ref->{path_host}/$ref->{dir}/$file" && $typef=~/^zip$/gi){
   system ("unzip $ref->{path_host}"."$ref->{dir}/$file -d $ref->{path_host}"."$ref->{dir} > /dev/null ");
   unlink "$ref->{path_host}/$ref->{dir}/$file";
  }
 }
 print qq[  <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0; URL=/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&rnd=$time'></HEAD></HTML>];
}

sub cat_image {
  my $time=time;
  my $ref=shift;
 my $upfile=$ref->{upfile};
 if($upfile ne '' && $ref->{id_cat} ne ''){
  if($ref->{save} eq 'ok'){
      my @ar1=split /\\/,$upfile;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/cat_image"){
                  mkdir_("$ref->{path_host}/cat_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/cat_image/$ref->{id_cat}.jpg";
         binmode(A);
         while (my $bytesread = read($upfile, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/cat_image/$ref->{id_cat}.jpg";
        close A;
		my $img_logo="$ref->{path_root}/templates/vodznak.png";
		my $img_logo_small = "$ref->{path_root}/templates/smallvodznak.png";
		print qq[$img_logo $img_logo_small];
                #делаем маленькую картинку       
                 magick('120',"$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","$ref->{path_host}/cat_image/$ref->{id_cat}-s.jpg"); 

                #делаем маленькую картинку дл€ анонсов     
                # magick('50',"$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","$ref->{path_host}/cat_image/$ref->{id_cat}-s-50.jpg"); 

                #делаем среднюю картинку дл€ анонсов     
                 magick('200',"$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","$ref->{path_host}/cat_image/$ref->{id_cat}-m.jpg"); 
		# вставл€ем вод€ной знак
		composit_img("$ref->{path_host}/cat_image/$ref->{id_cat}-m.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-m.jpg",$img_logo_small);   
                #делаем большую картинку
                 magick('500',"$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","$ref->{path_host}/cat_image/$ref->{id_cat}.jpg"); 

		# вставл€ем вод€ной знак
		composit_img("$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg",$img_logo);   
#my $path_img=shift;
#my $font=shift || 'tahoma';
#my $color=shift || 'white';
#my $size_text=shift || 40;
#my $gravity=shift || 'Center';
#my $text=shift || 'привет';
#my $ok=write_on_picture("$ref->{path_host}/cat_image/$ref->{id_cat}.jpg","","black",20,"",$ref->{user_doman});
#<HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}&id_cat=$ref->{id_cat}&a=add&PageIn=$ref->{PageIn}&p_n=$ref->{p_n}'></HEAD></HTML>
  # use Storable;
  # my $user_db = retrieve $ref->{path_db};
   my $user_db =$ref->{user_db};
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
print qq[
  <HTML>
  <body>
 $ref->{id_cat}  загрузка прошла удачно];
#sleep(5);
print qq[
  <script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}&id_cat=$ref->{id_cat}&a=add&PageIn=$ref->{PageIn}&p_n=$ref->{p_n}"</script>
  </body>
  </HTML>

];
        }      
      }
      else{
print qq[<HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}&id_cat=$ref->{id_cat}&a=add&mes=20&PageIn=$ref->{PageIn}&p_n=$ref->{p_n}'></HEAD>
<body>«агрузка не прошла</body>
</HTML>];
      }
}

sub cat_excel_export {
  my $time=time;
  my $ref=shift;
  my $upfile=$ref->{upfile};
  my $temp='temp'.time.'.xls';
 if($upfile ne '' && $ref->{id} ne ''){
 if($ref->{save} eq 'ok'){
        my ($buf);
         open A, "+>$ref->{path_host}/$temp";
         binmode(A);
         while (my $bytesread = read($upfile, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/$temp";
        close A;
#use Storable;
#my $user_db = retrieve $ref->{path_db};
my $user_db =$ref->{user_db};
#use Spreadsheet::ParseExcel;
#use Spreadsheet::ParseExcel::FmtUnicode;
my $dbh=dbconnect;
my $oExcel = new Spreadsheet::ParseExcel;
my $oFmtR = Spreadsheet::ParseExcel::FmtUnicode->new(Unicode_Map => "CP1251"); 
my $oBook = $oExcel->Parse("$ref->{path_host}/$temp", $oFmtR);
my($iR, $iC, $oWkS, $oWkC);
 foreach my $oWkS (@{$oBook->{Worksheet}}){
    for(my $iR = $oWkS->{MinRow}||1 ; 
        defined $oWkS->{MaxRow} && $iR <= $oWkS->{MaxRow} ; $iR++) {
my ($id_cat,$id,$name,$cost,$mera,$opis,$short,$articul);
      for(my $iC = $oWkS->{MinCol} ;
           defined $oWkS->{MaxCol} && $iC <= $oWkS->{MaxCol} ; $iC++) {
           $oWkC = $oWkS->{Cells}[$iR][$iC];
           next if !$oWkC;
#print qq[iR = $iR ... iC =$iC<br>];
#exit;
            if ($iC==0) {$id_cat=$oWkC->Value if($oWkC);}
         elsif ($iC==1) {$id=$oWkC->Value if($oWkC)||' ';}
         elsif ($iC==2) {$articul=$oWkC->Value if($oWkC)||' ';}
         elsif ($iC==3) {$name=$oWkC->Value if($oWkC)||' ';}
         elsif ($iC==4) {$short=$oWkC->Value if($oWkC)|| ' '}
         elsif ($iC==5) {$cost=$oWkC->Value if($oWkC)|| ' '}
         elsif ($iC==6) {$mera=$oWkC->Value if($oWkC)|| ' ';}
         elsif ($iC==7) {$opis=$oWkC->Value if($oWkC)|| ' ';}
        }

                $id=$ref->{id} if !$id;
#                $name=encoder($name,'win','koi');
#                $mera=encoder($mera,'win','koi')||' '; 
#                $opis=encoder($opis,'win','koi');
#                $short=encoder($short,'win','koi');
if($name && $user_db->{data}->{$id}->{mod} eq 'catalog'){
 if($id_cat){
   my $sql="update catalog_$ref->{prefix} set name=?,short=?,mera=?,cost=?,opis=?,articul=? where id=? and idr=?";
   my $sth=$dbh->prepare($sql);
   $sth->execute($name,$short,$mera,$cost,$opis,$id_cat,$id,$articul);
   $sth->finish;
   }else{
   my $sql="insert into catalog_$ref->{prefix} (name,short,mera,cost,opis,idr,articul) values (?,?,?,?,?,?,?)";
   my $sth=$dbh->prepare($sql);
   $sth->execute($name,$short,$mera,$cost,$opis,$id,$articul);
   $sth->finish;
  }
 }
 }
}
 dbdisconnect($dbh);
unlink "$ref->{path_host}/$temp";
print qq[<HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}'></HEAD></HTML>];
        }      
      }
      else{
print qq[<HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}&id_cat=$ref->{id_cat}&a=export&mes=20'></HEAD></HTML>];
      }

}

sub cat_excel_import {
  my $time=time;
  my $ref=shift;
#        use Spreadsheet::WriteExcel;

        # Create a new Excel workbook
        my $workbook = Spreadsheet::WriteExcel->new("$ref->{path_host}/excel_price.xls");

        # Add a worksheet
        my $worksheet = $workbook->addworksheet();

        #  Add and define a format
        my $format2 = $workbook->addformat();    # Add a format
        $format2->set_bold();
        my $format = $workbook->addformat();    # Add a format
        $format->set_bold();
        $format->set_color('red');
        $format->set_align('center');

        # Write a formatted and unformatted string, row and column notation.
        $worksheet->write(0, 0, "E-shop price $ref->{user_doman}", $format);
                        my($name_id,$name_idr,$name_name,$name_cost,$name_mera,$name_short,$name_articul);
            $name_id="ID товара";$name_idr="ID раздела";$name_name="Ќаименование";
                        $name_cost="÷ена";$name_mera="≈д. измерени€";
                        $name_short="јнонс товара";$name_articul="јртикул";
                # $name_id=encoder($name_id,'koi','win')||' ';
                # $name_idr=encoder($name_idr,'koi','win')||' ';
                # $name_name=encoder($name_name,'koi','win')||' ';
                # $name_cost=encoder($name_cost,'koi','win')||' ';
                # $name_mera=encoder($name_mera,'koi','win')||' ';
                # $name_short=encoder($name_short,'koi','win')||' ';

                $worksheet->write(1,    0, $name_articul,$format2);
                $worksheet->write(1,    1, $name_idr,$format2);
                $worksheet->write(1,    2, $name_name,$format2);
                $worksheet->write(1,    3, $name_short, $format2);
                $worksheet->write(1,    4, $name_cost, $format2);
                $worksheet->write(1,    5, $name_mera,$format2);
#               $worksheet->write(1,    5, $name_opis,$format2);

                my $dbh=dbconnect;
                my $sel="select * from catalog_$ref->{prefix} where 1 order by idr asc, name asc";
                my $sth=$dbh->prepare($sel);
            $sth->execute;
                my $i=2;
            while(my $ref_cat=$sth->fetchrow_hashref){
#                        my $name=encoder($ref_cat->{name},'koi','win')||' ';
#                        my $mera=encoder($ref_cat->{mera},'koi','win')||' '; 
#                        my $short=encoder($ref_cat->{short},'koi','win')||' '; 
                        my $name=$ref_cat->{name};
                        my $mera=$ref_cat->{mera}; 
                        my $short=$ref_cat->{short}; 
#                       my $opis=encoder($ref_cat->{opis},'koi','win')||' ';

                $worksheet->write($i,    0, "$ref_cat->{articul}",);
                $worksheet->write($i,    1, "$ref_cat->{idr}",);
                $worksheet->write($i,    2, "$name",$format2);
                $worksheet->write($i,    3, "$short",$format2);
                $worksheet->write($i,    4, "$ref_cat->{cost}", $format2);
                $worksheet->write($i,    5, "$mera",);
#               $worksheet->write($i,    5, "$opis",);
                        $i++;
           }
       $sth->finish;
                 dbdisconnect($dbh);
print qq[<html><head><title>E-shop</title></head>
                <body><script>location.href="http://$ref->{user_doman}/excel_price.xls"</script></body></html>
];
}

sub edit_gallery { #ƒобавл€ем редактируем фото в галерее
 my $ref=shift;
    $ref->{name}=~tr/'/"/; #'
  my $dbh=dbconnect;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db =$ref->{user_db};
 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';
 my $pr_mes='19';
      if($ref->{upfile} eq '' && !$ref->{id_cat}){
print qq[<HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;URL=/cgi-bin/mod/gallery.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time&id=$ref->{id}&id_cat=$ref->{id_cat}&a=add&mes=20'></HEAD></HTML>];
exit;
      }
#  $ref->{name}=encoder($ref->{name},'win','koi')||' ';
#  $ref->{opis}=encoder($ref->{opis},'win','koi')||' ';
if($ref->{save} eq 'ok'){
 if($mod_razdel eq 'gallery'){
 if($ref->{id_cat}){
#   my $sql="update gallery_$ref->{prefix} set konkurs_number=?,users_id=?,name=?,url=?,opis=?,author=?,sort=? where id=? and idr=?";
   my $sql="update gallery_$ref->{prefix} set name=?,url=?,opis=?,author=?,sort=? where id=? and idr=?";
   my $sth=$dbh->prepare($sql);
  $sth->execute($ref->{name},$ref->{url},$ref->{ta},$ref->{author},$ref->{sort},$ref->{id_cat},$ref->{id});
  $sth->finish;
#       print qq[$sql<br>$ref->{name},$ref->{ta},$ref->{author},$ref->{id_cat},$ref->{id}<br> col1= $col1]; exit;
 }else{
   my $sql="insert into gallery_$ref->{prefix} (date_reg,name,url,opis,idr,author,sort) values (NOW(),?,?,?,?,?,?)";
   my $sth=$dbh->prepare($sql);
    my $sort=$ref->{sort}||0;
   my $ins=$sth->execute($ref->{name},$ref->{url},$ref->{ta},$ref->{id},$ref->{author},$sort);
   $sth->finish;
   $ref->{id_cat}=$sth->{mysql_insertid};
#       print qq[$sql<br>$ref->{name},$ref->{id},$ref->{author}]; exit;
#print qq[$ins = $sql<br>($ref->{users_id},$ref->{name},$ref->{url},$ref->{ta},$ref->{id},$ref->{author},$sort)]; exit;
 }
 }
}else{$pr_mes='20';}
print qq[$ref->{id_cat}];
#print qq[ok]; exit;

###ƒобавл€ем фото
  my $time=time;
  my $upfile=$ref->{upfile};
      if($upfile ne '' && $ref->{id_cat} ne ''){
      my @ar1=split /\\/,$upfile;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/gallery_image"){
                  mkdir_("$ref->{path_host}/gallery_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/gallery_image/$ref->{id_cat}-.jpg";
         binmode(A);
         while (my $bytesread = read($upfile, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/gallery_image/$ref->{id_cat}-.jpg";
        close A;
	 my $img_logo="$ref->{path_root}/templates/cwclive.png";

	 my $img_base="$ref->{path_host}/gallery_image/$ref->{id_cat}-.jpg";
	 my $img_base_new="$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg";

                #делаем большую картинку на 800 пикселов
                magick('800',"$ref->{path_host}/gallery_image/$ref->{id_cat}-.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg"); 

                my $ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg");
		# вставл€ем вод€ной знак
		composit_img("$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg",$img_logo);   

                #делаем маленькую картинку       
                 magick($ref->{width},"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-s.jpg"); 
		 #ƒелаем картинку 300 по ширине
                 magick(300,"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-m.jpg"); 
                 #делаем большую картинку
                 #magick('500',"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-m.jpg"); 
                 #$ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg");


   #прописываем размеры картинки
   my $sql="update gallery_$ref->{prefix} set width=?,height=? where id=? and idr=?";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref_size->{width},$ref_size->{height},$ref->{id_cat},$ref->{id});
   $sth->finish;

      }


  my $upfile1=$ref->{upfile1};
      if($upfile1 ne '' && $ref->{id_cat} ne ''){
      my @ar1=split /\\/,$upfile1;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/gallery_image"){
                  mkdir_("$ref->{path_host}/gallery_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg";
         binmode(A);
         while (my $bytesread = read($upfile1, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg";
        close A;
        my $ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg");
                 #делаем маленькую картинку       
                 magick($ref->{width},"$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-1-s.jpg"); 
                 #magick(50,"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-s-50.jpg"); 
                 $ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg");

                 if($ref_size->{width}>700){
                 #делаем большую картинку
                 magick('700',"$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg"); 
                 }


      }

  my $upfile2=$ref->{upfile2};
      if($upfile2 ne '' && $ref->{id_cat} ne ''){
      my @ar1=split /\\/,$upfile2;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/gallery_image"){
                  mkdir_("$ref->{path_host}/gallery_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg";
         binmode(A);
         while (my $bytesread = read($upfile2, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg";
        close A;
        my $ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg");
                #делаем маленькую картинку       
                 magick($ref->{width},"$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-2-s.jpg"); 
                 #magick(100,"$ref->{path_host}/gallery_image/$ref->{id_cat}.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-s-50.jpg"); 
                 $ref_size=size_img("$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg");

                 if($ref_size->{width}>700){
                 #делаем большую картинку
                 magick('700',"$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg","$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg"); 
                 }


      }

  my $upfile3=$ref->{logo};
      if($upfile3 ne '' && $ref->{id_cat} ne ''){
      my @ar1=split /\\/,$upfile3;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+|\0|\%//gi;
      $file=~tr/ »∆—…≈ћ÷№џ√”«“ЎЅёќѕЌ ƒ‘ўЏ¬яЋ’–Ёј„Єижсйемцьыгузтшбюопнкдфщъв€лхрэач®/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
	  my $nmf=join("\.",(@ar2)[0..$#ar2-1]);
	  my $typef=$ar2[$#ar2];
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/gallery_image"){
                  mkdir_("$ref->{path_host}/gallery_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/gallery_image/$ref->{id_cat}-logo.jpg";
         binmode(A);
         while (my $bytesread = read($upfile3, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/gallery_image/$ref->{id_cat}-logo.jpg";
        close A;

      }

###добавл€ем фото конец



$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
 my $sort=$user_db->{data}->{sort}||{};
 my %sort=%$sort;
 my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;

print qq[
<html>
<body>
заргузка прошла успешно
<script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="/cgi-bin/mod/gallery.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&mes=$pr_mes&id_cat=$ref->{id_cat}&a=add&PageIn=$ref->{PageIn}&p_n=$ref->{p_n}";
</script>
</body>
</html>
];
  dbdisconnect($dbh);
  exit;
}
