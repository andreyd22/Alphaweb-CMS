#!/usr/bin/perl
$|=1;
use lib  "../";
use Modules::Constructor;
use strict;
 print "Content-type:text/html\r\n\r\n";
#        use CGI::Cookie;
#        my $cook=fetch CGI::Cookie();
#     use Data::Dumper;
#     print Dumper($cook->{sid}->{value}->[0]);
 my $ref=Get_Param;
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
 &send_mail($root_mail,$subject,$message);
 exit;
 }
 if ($ref->{'a'} eq '') {&main($ref); } #Вывод папок пользователя
 if ($ref->{'a'} eq 'new_dir') {&new_dir($ref); } #Создаем новую папку в текущей директории
 if ($ref->{'a'} eq 'del') {
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
                my $my_path="$ref->{path_host}/$ref->{dir}/$ref->{file}";
                &del($ref,$my_path); } #Удаляем папку или файлы
 if ($ref->{'a'} eq 'edit_file') {
        if($ref->{editor}eq 'simple'){edit_file_simple($ref);#Редактор файлов простой
        }
        else{&edit_file($ref); } #Редактор файлов расширенный
 }
 if ($ref->{'a'} eq 'save_file') {&save_file($ref); } #Сохраняем измененный файл

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
         $ref->{file}=~s/\/\//\//g;
         $ref->{file}=~s/\/$//g;
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
                 $def={  
		    "main"=>"/constructor.html.$ref->{l}",
                    "table"=>"/file_viewer_table.html.$ref->{l}",
                    "row" =>"/file_viewer_row.html.$ref->{l}"
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
		 #foreach my $file (sort { -M $a <=> -M $b } glob("$ref->{path_host}"."$ref->{file}"."/*")){
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
                                         my $url_link="/$ref->{file}/$file";
                                            $url_link=~s/\/+/\//gi;
                                            $url_link="http://$ref->{user_doman}".$url_link;

                                         if($ref->{l} eq '1'){
                     $action.=qq[<a href="$url_link" target=_blank><img src="/img/icons/browse.gif" border=0 alt='Открыть в новом окне'></a>&nbsp;];
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=edit_file&sid=$ref->{sid}&dir=$ref->{file}&file=$file&l=1"><img src="/img/icons/icon_export_doc.gif" border=0 alt='Расширенный редактор'></a>&nbsp;];
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=edit_file&editor=simple&sid=$ref->{sid}&dir=$ref->{file}&file=$file&l=1"><img src="/img/icons/edit.gif" border=0 alt='Простой редактор'></a>&nbsp;];
                                         }else{
                     $action.=qq[<a href="$url_link" target=_blank><img src="/img/icons/browse.gif" border=0 alt='Open in new window'></a>&nbsp;];
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=edit_file&sid=$ref->{sid}&dir=$ref->{file}&file=$file&l=2"><img src="/img/icons/icon_export_doc.gif" border=0 alt='Full editor'></a>&nbsp;];
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=edit_file&editor=simple&sid=$ref->{sid}&dir=$ref->{file}&file=$file&l=2"><img src="/img/icons/edit.gif" border=0 alt='Simple editor'></a>&nbsp;];
                                         }
                     }
                     my $dir_del="/";
                     if ($ref->{file}){$dir_del=$ref->{file}."/";}
                     if($ref->{l} eq '1'){
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=del&sid=$ref->{sid}&dir=$dir_del&file=$file" onClick="return Sure('$dir_del','$file','$ref->{sid}');"><img src="/img/icons/delete.gif" border=0 alt='Удалить файл/папку'></a>];
                                         }else{
                     $action.=qq[<a href="/cgi-bin/mod/file_viewer.pl?a=del&sid=$ref->{sid}&dir=$dir_del&file=$file&l=2" onClick="return Sure('$dir_del','$file','$ref->{sid}');"><img src="/img/icons/delete.gif" border=0 alt='Delete file/dir'></a>];
                                         }
                     my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime($mtime);
                     $year+=1900;
                     $tpl->assign(
                             ICON=>$icon,
                             FILE=>$ref->{file}."/".$file,
                             FILE_NAME=>$file,  
                             DIR=>$ref->{file},
                             SIZE_OF_FILE=>$size,
                             MODIFICATION=>"$mday-$mon-$year $hour:$min:$sec",
                             ACTION=>$action
                           );
                           $tpl->parse("ROWS",".row");
                           $tpl->clear_href(1);
                 }
                     $tpl->assign(
                             DIR=>$ref->{file},
                             BACK_DIR=>$back  
                           );


         }else{
                 $def={  "main"=>"/constructor.html.$ref->{l}",
                         "table"=>"/file_viewer_data.html.$ref->{l}"
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
         $tpl->parse(CONTENT=>"main");
         $tpl->clear_href(1);
         my $content = $tpl->fetch("CONTENT");
	 use Data::Dumper;
#	 print Dumper($tpl);
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
  <script>location.href="/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}"</script>
  </body>

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
#                                del($ref,"$path");
                        }
           }
           rmdir "$path_my";
        }else{
           unlink  "$path_my";
        }
 print qq[
  <HTML>
  <body>
  <script>location.href='/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}'</script>
  </body>
</HTML>
 ];
 }

sub edit_file {
 my $ref=shift;
 my $def={  
                "main"=>"/constructor_i.html.$ref->{l}",
                "text"=>"/file_editor.html.$ref->{l}"
          };
 my $title=slovo(16,$ref->{l})." $ref->{file} - "; #расширенный редактор: 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $text='';
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
                my ($text_head,$text_bottom);
 if(-e "$ref->{path_host}"."$ref->{dir}/$ref->{file}"){
 open A, "$ref->{path_host}"."$ref->{dir}/$ref->{file}";
 my @ar_text=<A>;
 $text=join("",@ar_text);
 close A;
 if($text=~s/<html><body>//si){
 $text_head="<html> <body>";
 }
 elsif($text=~s/<html>(.+?)<body>//si){
 $text_head="<html>$1<body>";
 }
 elsif($text=~s/<html><body(.+?)>//si){
 $text_head="<html> <body$1>";
 }
 elsif($text=~s/<html>(.+?)<body(.+?)>//si){
 $text_head='<html>'.$1."<body$2>";
 }
 $text=~s/<\/body>//si;
 $text=~s/<\/html>//si;
 $text_bottom='</body></html>';
 }else{
        if($ref->{paste_html}){
         $text_head=qq[
<HTML>
  <HEAD>
    <TITLE>Document</TITLE>
 </HEAD>
<BODY>];
         $text_bottom=qq[
</BODY>  </HTML>];
        }
 }
 $text_head=~s/\</\[/gi;
 $text_head=~s/\>/\]/gi;
 $text_bottom=~s/\</\[/gi;
 $text_bottom=~s/\>/\]/gi;
# $text=~s/\</\[/gi;
# $text=~s/\>/\]/gi;
 $tpl->assign(
             HEAD=>$text_head,
             BOTTOM=>$text_bottom,
             DATA=>$text,
                         FILE=>$ref->{file},
                         DIR=>$ref->{dir}
             );
 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}

sub save_file {
 my $ref=shift;
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
if($ref->{save} eq 'ok'){
open A, "+>$ref->{path_host}$ref->{dir}/$ref->{file}";
my ($top,$bottom);
#if($ref->{head}){$top=qq[<!--head begin-->
#$ref->{head}
#<!--head end-->];}
if($ref->{head}){$top=qq[
$ref->{head}
];}
#if($ref->{bottom}){$bottom=qq[
#<!--bottom begin-->
#$ref->{bottom}
#<!--bottom end-->];}
if($ref->{bottom}){$bottom=qq[
$ref->{bottom}
];}
 $top=~s/\[/\</gi;
 $top=~s/\]/\>/gi;
 $bottom=~s/\[/\</gi;
 $bottom=~s/\]/\>/gi;
 $ref->{ta}=~s/\[/\</gi;
 $ref->{ta}=~s/\]/\>/gi;

 print A qq[$top
$ref->{ta}
$bottom];
 close A;
}
 print qq[
  <HTML>
  <body>
  <script>location.href="/cgi-bin/mod/file_viewer.pl?sid=$ref->{sid}&file=$ref->{dir}&l=$ref->{l}"</script>
  </body>
  </HTML>
 ];
  exit;
}
sub edit_file_simple {
 my $ref=shift;
 my $def={  
                "main"=>"/constructor.html.$ref->{l}",
                "text"=>"/file_editor_simple.html.$ref->{l}"
          };
 my $title=slovo(17,$ref->{l})." $ref->{file} - "; #Простой редактор: 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $text='';
        $ref->{user}->{login}=~/^(\w)/;
        my $first_char=$1;
        my ($text_head,$text_bottom);
 if(-e "$ref->{path_host}"."$ref->{dir}/$ref->{file}"){
 open A, "$ref->{path_host}"."$ref->{dir}/$ref->{file}";
 my @ar_text=<A>;
 $text=join("",@ar_text);
 close A;
 }else{
        if($ref->{paste_html}){
         $text_head=qq[
<HTML>
  <HEAD>
    <TITLE>Document</TITLE>
 </HEAD>
<BODY>
<!--enter your code here begin-->
];
         $text_bottom=qq[
<!--enter your code here end-->
</BODY> </HTML>
];
        }
 }
 $text_head=~s/\</\[/gi;
 $text_head=~s/\>/\]/gi;
 $text_bottom=~s/\</\[/gi;
 $text_bottom=~s/\>/\]/gi;
 $text=~s/\</\[/gi;
 $text=~s/\>/\]/gi;

 $tpl->assign(
             DATA=>$text_head.$text.$text_bottom,
                         FILE=>$ref->{file},
                         DIR=>$ref->{dir}
             );
 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();

}