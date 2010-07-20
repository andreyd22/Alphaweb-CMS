#!/usr/bin/perl
$|=1;
use lib  "../";
use Modules::Constructor;
use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
#print qq[$ref->{sid}];exit;
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML>
  <body>
  <script>location.href='/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes'</script>
  </body>
   </HTML>
     ";
 exit;
 }
 if($ref->{file}=~/\.\/|\.\%2f/gi||$ref->{dir}=~/\.\/|\.\%2f/gi){
 my $log="./hack.log";
 my $subject=qq[Попытка взлома с сайта $host_name];
 my ($year,$mon,$mday,$hour,$min,$sec)=get_data();
 my $message=qq[
 -----------------$mon.$mday.$year $hour:$min:$sec $ref->{ip} $ref->{user}->{login}------------
 Запрещенный запрос
 file: $ref->{file}
 dir: $ref->{dir}
 Попытка взлома с сайта http://$host_name
 ip: $ref->{ip}
 ----------------------END $ref->{ip}----------------
 ];
 print qq[<center>Server now busy, try your request later</center>];
# print $message;
 open A, ">>$log";
 print A $message;
 close A;
# &send_mail($root_mail,$subject,$message);
 exit;
 }
 if ($ref->{'a'} eq '') {&main($ref); } #Вывод папок пользователя
 if ($ref->{'a'} eq 'new_dir') {&new_dir($ref); } #Создаем новую папку в текущей директории
 if ($ref->{'a'} eq 'del') {
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
        my $path_my="$ref->{path_host}/$ref->{dir}/$ref->{file}";
        &del($ref,$path_my); } #Удаляем папку или файлы

 sub main {
         my $ref=shift;
         $ref->{user}->{login}=~/^(\w)/;
         my $first_char=$1;
         my @arr_files=();
         my $flag=0;
         my $def={};
         my $tpl={};
         if(!$ref->{file}){$ref->{file}='';}
         $ref->{file}=~s/\/\.\.|\/\.//g;
         my @ar_dirs=split /\//,$ref->{file};
         my $size=$#ar_dirs;
         my $back=undef;
         if($size>=0){
         my $del=splice @ar_dirs, $size, 1, ();
            $back=join ('/',@ar_dirs);
         }else{$back='';}
         if (-d "$ref->{path_host}"."$ref->{file}"){
          $flag=1; # Ставим флаг что это директория
         }elsif(-e "$ref->{path_host}"."$ref->{file}"){
          $flag=2; # Ставим флаг что это файл
         }else{$flag=1;$ref->{file}='';}
         if($flag==1){
                 $def={  "main"=>"/img_viewer_index.html.$ref->{l}",
                    "table"=>"/img_viewer_table.html.$ref->{l}",
                    "row" =>"/img_viewer_row.html.$ref->{l}"
                 };
                                 my $title=slovo(14,$ref->{l})." $ref->{file} - "; #Управление файлами: 
                 $ref->{def}=$def;
                 $ref->{title}=$title;
                 $tpl=tplb($ref);
                  opendir DIR, "$ref->{path_host}"."$ref->{file}";
                  my @arr_files2=readdir(DIR);
                  #shift @arr_files;shift @arr_files;
                  close DIR;
		  use sort 'stable';
		    my @arr_files=sort @arr_files2;
                 foreach my $file (@arr_files){
		     next if $file=~/^\.{1,2}$/;
                     my $action=undef;
                     my $icon="text.gif";
                     my ($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat("$ref->{path_host}"."$ref->{file}/$file");
                         $size=$size/1024;
                         $size=sprintf "%.0f",$size;
                         $size.="K";
                     if (-d "$ref->{path_host}"."$ref->{file}/$file"){
                         $icon="folder.gif";
                         my $size_use=`du -sh $ref->{path_host}$ref->{file}/$file`;
                         my @ar_size=split /\t/,$size_use;
                         my $size_file=$ar_size[0];
                            $size=$size_file;
                     }else{
                           if($file=~/([\w-]+\.((?:gif|jpe?g)))$/ix){
                             $icon="image.gif"
                           }
                           if($file=~/([\w-]+\.((?:htm|html)))$/ix){
                             $icon="webpage.gif"
                           }
                     my $name_form=$ref->{name_form}||"f_url";
                     my $url_link="/$ref->{file}/$file";
                        $url_link=~s/\/+/\//gi;
                        $url_link="http://$ref->{user_doman}".$url_link;
                     if ($ref->{l} eq '1'){
                     $action.=qq[<a href="$url_link" target=_blank><img src="/img/icons/browse.gif" border=0 alt='Открыть в новом окне'></a>&nbsp;];
                     }else{
                     $action.=qq[<a href="$url_link" target=_blank><img src="/img/icons/browse.gif" border=0 alt='Open in new window'></a>&nbsp;];
                     }

                     my $user_file="/$ref->{file}/$file";
                        $user_file=~s/\/+/\//gi;
                        $user_file="http://".$ref->{user_doman}.$user_file;
                     if($ref->{type} ne 'old'){
                      if ($ref->{l} eq '1'){
                           if($file=~/([\w-_]+\.((?:gif|jpe?g)))$/ix){
                            $action.=qq[<a href="javascript:" onclick="SelectImage('$user_file')"><img src="/img/icons/paste.gif" border=0 alt='Вставить картинку '></a>&nbsp;];
                           }else{
                            $file=~/\.([a-z])$/ix;
                            my $ext=$1;
                            $action.=qq[<a href="javascript:" onclick="SelectFile('$user_file','$size','$ext')"><img src="/img/icons/paste.gif" border=0 alt='Вставить файл'></a>&nbsp;];
                           }
                           if($ref->{type} eq 'old'){
                            $action.=qq[<a href="javascript:" onclick="paste_img('$user_file','$name_form');"><img src="/img/icons/paste.gif" border=0 alt='Вставить картинку '></a>&nbsp;];
                           }
                      }else{
                           if($file=~/([\w-_]+\.((?:gif|jpe?g)))$/ix){
                            $action.=qq[<a href="javascript:" onclick="paste_img('$user_file','$name_form');SelectImage('$user_file')"><img src="/img/icons/paste.gif" border=0 alt='Вставить картинку eng'></a>&nbsp;];
                           }else{
                            $file=~/\.([a-z])$/ix;
                            my $ext=$1;
                            $action.=qq[<a href="javascript:" onclick="paste_img('$user_file','$name_form');SelectFile('$user_file','$size','$ext')"><img src="/img/icons/paste.gif" border=0 alt='Вставить файл eng'></a>&nbsp;];
                           }
                      }
                     }
                     if($ref->{type} eq 'old'){
                      $action.=qq[<a href="javascript:" onclick="paste_img('$user_file','$name_form');"><img src="/img/icons/paste.gif" border=0 alt='Вставить картинку '></a>&nbsp;];
                     }

                     }
                     my $dir_del="/";
                     if ($ref->{file}){$dir_del=$ref->{file}."/";}
                        if($ref->{l} eq '1'){
                        $action.=qq[<a href="/cgi-bin/mod/img_viewer.pl?a=del&sid=$ref->{sid}&dir=$dir_del&file=$file&name_form=$ref->{name_form}&type=$ref->{type}" onClick="return Sure('$dir_del','$file','$ref->{sid}');"><img src="/img/icons/delete.gif"border=0 alt='Удалить файл/папку'></a>];
                        }else{
                        $action.=qq[<a href="/cgi-bin/mod/img_viewer.pl?a=del&sid=$ref->{sid}&dir=$dir_del&file=$file&l=2&name_form=$ref->{name_form}&type=$ref->{type}" onClick="return Sure('$dir_del','$file','$ref->{sid}');"><img src="/img/icons/delete.gif"border=0 alt='Delete'></a>];
                        }
                     my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime($mtime);
                     $year+=1900;
                     my $file_result=$ref->{file}."/".$file;
                     $file_result=~s/\/+/\//gi;
                     $tpl->assign(
                             TYPE=>$ref->{type},
                             ICON=>$icon,
                             FILE=>$file_result,
                             FILE_NAME=>$file,  
                             DIR=>$ref->{file},
                             SIZE_OF_FILE=>$size,
                             MODIFICATION=>"$mday-$mon-$year $hour:$min:$sec",
                             ACTION=>$action,
                             NAME_FORM=>$ref->{name_form}
                           );
                           $tpl->parse("ROWS",".row");
                           $tpl->clear_href(1);
                 }
                     $tpl->assign(
                             DIR=>$ref->{file},
                             BACK_DIR=>$back,
                             NAME_FORM=>$ref->{name_form}
                           );


         }else{
                 $def={  "main"=>"/img_viewer_index.html.$ref->{l}",
                         "table"=>"/img_viewer_data.html.$ref->{l}"
                 };
                                 my $title=slovo(14,$ref->{l})." $ref->{file} - "; #Управление файлами: 
                 $ref->{def}=$def;
                 $ref->{title}=$title;
                 $tpl=tplb($ref);
                 open A,"$ref->{path_host}"."$ref->{file}";
                 my @ar_file=<A>;
                 close A;
                 my $text=join("",@ar_file);
                 $text=~s/\n/\|\|===brake===\|\|/gi;
                 $text=CGI::escapeHTML($text);
                 $text=~s/\|\|===brake===\|\|/<br>/gi;
                 $tpl->assign(DATA=>$text,
                             BACK_DIR=>$back  
                 );
         }
         $tpl->parse(TEXT=>"table");
         $tpl->parse(CONTENT => "main");
         $tpl->clear_href(1);
         my $content = $tpl->fetch("CONTENT");
         print $$content;
         $tpl->clear_href(1);
         $tpl->clear();
 }

 sub new_dir {
        my $ref=shift;
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
      $ref->{new_dir}=~tr/ ИЖСЙЕМЦЬЫГУЗТШБЮОПНКДФЩЪВЯЛХРЭАЧёижсйемцьыгузтшбюопнкдфщъвялхрэачЁ/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
        if (-d "$ref->{path_host}/$ref->{dir}"){
#           mkdir "$ref->{path_host}/$ref->{dir}/$ref->{new_dir}",'0755';
                   if($ref->{save} eq 'ok'){
           mkdir_("$ref->{path_host}/$ref->{dir}/$ref->{new_dir}");
                   }
        }
 print qq[
  <HTML>
  <body>
  <script>location.href='/cgi-bin/mod/img_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&type=$ref->{type}'</script>
  </body>
</HTML>
 ];
  exit;
 }
 sub del {
        my $ref=shift;
        my $path_my=shift;
        if (-d "$path_my"){
           opendir DIR, "$path_my";
           my @ar=readdir(DIR);
           close DIR;
           shift(@ar);shift(@ar);
           foreach my $file_name (@ar){
            if(-d "$path_my/$file_name"){
                del($ref,"$path_my/$file_name");
            }
            else{
               unlink "$path_my/$file_name";
#                del($ref,"$path/$file_name");
            }
           }
           rmdir "$path_my";
        }else{
           unlink  "$path_my";
        }
 print qq[
  <HTML>
  <body>
  <script>location.href='/cgi-bin/mod/img_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}&name_form=$ref->{name_form}&type=$ref->{type}'</script>
  </body>
</HTML>
 ];
  exit;

 }

