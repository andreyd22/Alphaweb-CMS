#!/usr/bin/perl
#!!!Скрипт, отвечающий за настройку шаблонов
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $my_ref=Get_Param;
 $my_ref->{sid}=time;
#print qq[save = $ref->{save}];
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($my_ref);
 if($mes){
   print "
      <HTML><HEAD><title>authorization error</title></HEAD>
    <body>
    <script>parent.location.href='/cgi-bin/view.pl?a=mes&l=$my_ref->{l}&mes=$mes'</script>
    </body>
    </HTML>
     ";
 exit;
 }
#!!!Проверка sid пользователя!!!#

#!!!Проверка прав доступа!!!#
 $my_ref->{who}='edit_design';
 &check_status($my_ref);
#!!!Проверка прав доступа end !!!#

 if ($my_ref->{'a'} eq '') {&main($my_ref); } #Вывод документа
 if ($my_ref->{'a'} eq 'save') {&save_assign($my_ref); } #
 if ($my_ref->{'a'} eq 'default_assign') {&default_assign($my_ref); } #
 if ($my_ref->{'a'} eq 'list_templates') {&list_templates($my_ref); } #
 if ($my_ref->{'a'} eq 'view_template') {&view_template($my_ref); } #
 if ($my_ref->{'a'} eq 'save_template') {&save_template($my_ref); } #сохраняем шаблон

sub main {
  my $ref=shift||{};
#  if(!$ref->{path_db}){print "<sparent.location.href='http://$host_name'</script>"; exit;}
  if(!-e "$ref->{path_template}/index.ini"){print "<script>alert('Choose template');parent.location.href='http://$host_name/cgi-bin/view_templates.pl?sid=$ref->{sid}'</script>"; exit;}

      my $def={  
                                "main"=>"/constructor.html.$ref->{l}",
                                "text"=>"/constructor_assign_template.html.$ref->{l}",
                                "row"=>"/constructor_assign_template_row.html.$ref->{l}",
             };
 my $title=slovo(27,$ref->{l}); #Настройка параметров шаблонов
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 #    $ref->{user_db}=$user_db;
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
#      use Data::Dumper;
#      print Dumper($ref);
#Считываем параметры из файла assign.ini начало
   open A, "$ref->{path_template}/assign.ini";
   my @lines=<A>;
   close A;
   my @ar_opis=();
   my @ar_type=();
   my @ar_name_alias=();
   my $j=0;
my $dbh=dbconnect;
my $col=$dbh->selectrow_array("select count(*) from template_info");

if($col<=0){

   $j=0;
   for(@lines){
    $lines[$j]=~s/\n|\r//gi;
        chomp($lines[$j]);
    my ($alias,$value,$opis,$value_eng,$opis_eng,$type)=split /\=/,$lines[$j];
     if($alias && $alias ne 'hr' && $type){
       $value=$value_eng if $ref->{l}==2;
       $opis=$opis_eng if $ref->{l}==2;
       $user_db->{template}->{assign}->{$alias}=$value;
           push @ar_type,$type;
           push @ar_opis,$opis;                 
           push @ar_name_alias,$alias;                  
     }
    $j++;
   }
  
    my $kind='template';
    &store_db( $user_db, $ref->{id},$kind);

#store $user_db, $ref->{path_db};
}else{
   $j=0;
   for(@lines){
    $lines[$j]=~s/\n|\r//gi;
        chomp($lines[$j]);
    my ($alias,$value,$opis,$value_eng,$opis_eng,$type)=split /\=/,$lines[$j];
     if($alias && $alias ne 'hr' && $type){
        if($ref->{l}eq '2'){
        $value=$value_eng;
        $opis=$opis_eng;
        }
#print qq[$alias = $value <br>];
#       if(!$user_db->{template}->{assign}->{$alias}){
#       $user_db->{template}->{assign}->{$alias}=$value;
#          }
           push @ar_type,$type;
           push @ar_opis,$opis;                 
           push @ar_name_alias,$alias;                  
     }
    $j++;
   }
}

dbdisconnect($dbh);

my $href_ar_type=\@ar_type;
my $href_ar_opis=\@ar_opis;
my $href_ar_name_alias=\@ar_name_alias;
#Считываем параметры из файла assign.ini конец
$tpl=print_assign($ref,$tpl,$href_ar_type,$href_ar_opis,$href_ar_name_alias);
my $mes='';
if ($ref->{mes}){$mes=message($ref)}
 $tpl->assign(
             MESSAGE=>$mes,
             SID=>$ref->{sid},
             LANG=>$ref->{l}
             );
 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}

sub print_assign {
         my $ref=shift;
         my $tpl=shift;
         my $href_ar_type=shift;
         my $href_ar_opis=shift;
         my $href_ar_name_alias=shift;
     my @ar_type=@$href_ar_type;
     my @ar_opis=@$href_ar_opis;
     my @ar_name_alias=@$href_ar_name_alias;
     my $i=0;
                for(@ar_type){
                 my $link="";
                 my $width='';
                 my $preview='';
#                $ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}=~tr/'/"/; #"'
                 my $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name='$ar_name_alias[$i]' value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1>];
                 if($ar_type[$i] eq 'text'){
                  $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name='$ar_name_alias[$i]' value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1>];
                 }
                 if($ar_type[$i] eq 'img_viewer' || $ar_type[$i] eq 'magick'){
                 my $img_url="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}";
                        $img_url=~s/http:\/\/$ref->{user_doman}//gi;
             my $img_path="$ref->{path_host}$img_url";
             if($ref->{l} eq '1'){
                   $link=qq[<a href="javascript:" onclick="return win_assign(getCookie('sid'),'$ar_name_alias[$i]');">Выбрать рисунок</a>];
             }else{
                   $link=qq[<a href="javascript:" onclick="return win_assign(getCookie('sid'),'$ar_name_alias[$i]');">Choose picture</a>];
             }
                        if(-e $img_path){
                         my $ref_size=size_img($img_path)||{};
                         if($ref_size->{width}>400){
#                               $img_path=resize_img('400',$img_path);
                                $width=" width=400";
                         }
#                       my $ok=write_on_picture($img_new);
                        }
#                       print qq[<br>img_for_print = $img_new <br>];
#                        my $link_img="http://$ref->{user_doman}$img_url";
                        my $link_img="$img_url";
#print qq[$link_img];
                        if($img_url){
                        $preview=qq[<table><tr><td align=center><img src="$link_img"$width></td></tr></table>];
                        }
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name='$ar_name_alias[$i]' value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1> $link];
                 }
                 if($ar_type[$i] eq 'textarea'){
                  $pr_form=qq[<textarea id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" cols=60 rows=5 class=textarea>$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}</textarea>];
                        }
                 if($ar_type[$i] eq 'color_link'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'1');">
$color_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name='$ar_name_alias[$i]' value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1> $link];
                        $preview=qq[<table><tr><td align=center><A href="javascript:" title="" id='link$ar_name_alias[$i]' style='color:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example link</A></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'size_link'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'2');">
$size_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name='$ar_name_alias[$i]' value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1> $link];
                        $preview=qq[<table><tr><td align=center><A href="javascript:" title="" id='link$ar_name_alias[$i]' style='font-size:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example link size</a></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'font_link'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'4');">
$font_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' class=i1> $link];
                        $preview=qq[<table><tr><td align=center><A href="javascript:" title="" id='link$ar_name_alias[$i]' style='font-family:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example link font</a></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'type_link'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'5');">
$type_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}" class=i1> $link];
                        $preview=qq[<table><tr><td align=center><A href="javascript:" title="" id='link$ar_name_alias[$i]' style='text-decoration:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example link decoration</a></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'color_text'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'1');">
$color_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}" class=i1> $link];
                        $preview=qq[<table><tr><td align=center><p id='link$ar_name_alias[$i]' style='color:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example text color</p></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'size_text'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'2');">
$size_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}" class=i1> $link];
                        $preview=qq[<table><tr><td align=center><p id='link$ar_name_alias[$i]' style='font-size:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example text size</p></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'font_text'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'4');">
$font_option
</select>
];
                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}" class=i1> $link];
                        $preview=qq[<table><tr><td align=center><p id='link$ar_name_alias[$i]' style='font-family:$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}'>Example text font</p></td></tr></table>];
                        }
                 if($ar_type[$i] eq 'color_background'){
                   $link=qq[
<select class=i1 name='select_$ar_name_alias[$i]' onChange="set_value('$ar_name_alias[$i]',options[selectedIndex].value,'3');">
$color_option
</select>
];

                $pr_form=qq[<input type=text id="$ar_name_alias[$i]" name="$ar_name_alias[$i]" value="$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}" class=i1> $link];
                $preview=qq[<table width=200 height=40><tr><td bgcolor='$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]}' align=center id='link$ar_name_alias[$i]'><p>Example background</p></td></tr></table>];
                        }
                 
         $tpl->assign(
                LINK              =>$link,
                OPIS              =>$ar_opis[$i],
                NAME_ASSIGN       =>$ar_name_alias[$i],
                PR_FORM           =>$pr_form,
                VALUE             =>$ref->{user_db}->{template}->{assign}->{$ar_name_alias[$i]},
                PREVIEW           =>$preview
         );
         $tpl->parse("ROW",".row");
         $tpl->clear_href(1);
                $i++;
                }
return $tpl;
}

sub save_assign {
 my $ref=shift;
# my $tpl=shift;
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
#Считываем параметры из файла assign.ini начало
   open A, "$ref->{path_template}/assign.ini";
   my @lines=<A>;
   close A;
   my $j=0;
   my @ar_alias=();
   for(@lines){
     $lines[$j]=~s/\n|\r//gi;
        chomp($lines[$j]);
    my ($alias,$value,$opis,$value_eng,$opis_eng,$type)=split /\=/,$lines[$j];
     if($alias && $alias ne 'hr'){
           $ref->{$alias}=~s/http:\/\/$ref->{user_doman}//gi;
         $ref->{alias}=~s/"/'/gi; #'"
       $user_db->{template}->{assign}->{$alias}=$ref->{$alias};
     }
    $j++;
   }

my $pr_mes='19';
 if($ref->{save} eq 'ok'){

    my $kind='template';
    &store_db( $user_db, $ref->{id},$kind);

}else{
$pr_mes='20';
}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
print qq[
<html>
<body>
<script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="/cgi-bin/mod/template.cgi?sid=$ref->{sid}&l=$ref->{l}&mes=$pr_mes&rnd=$time"
</script>
</body>
</html>
];
exit;
}

sub list_templates {
  my $ref=shift||{};
  #if(!$ref->{path_db}){print "parent.location.href='http://$host_name'</script>"; exit;}
  if(!-e "$ref->{path_template}/index.ini"){print "<script>alert('Choose template');parent.location.href='http://$host_name/cgi-bin/view_templates.pl?sid=$ref->{sid}'</script>"; exit;}

      my $def={  
                                "main"=>"/constructor.html.$ref->{l}",
                                "text"=>"/constructor_define_template.html.$ref->{l}",
                "row"=>"/constructor_define_template_row.html.$ref->{l}",
             };
 my $title=slovo(28,$ref->{l}); #Ручная настройка шаблонов 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 #    $ref->{user_db}=$user_db;
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};

 opendir DIR,$ref->{path_template} or die $!;
 my @ar_files=readdir(DIR);
 close DIR;
 my @ini_files=();

 for (my $i=2;$i<=$#ar_files;$i++){
   if($ar_files[$i]=~/\.ini$/&&$ar_files[$i]!~/assign\.ini/){
   push @ini_files,$ar_files[$i];
   }
 }
 my $opis_alias='';
 for(my $j=0;$j<=$#ini_files;$j++){
   open A, "$ref->{path_template}/$ini_files[$j]";
   my @ar_str=<A>;
   close A;
   for(my $k=0;$k<=$#ar_str;$k++){
   chomp($ar_str[$k]);
   my ($alias,$name,$opis,$opis2,$status)=split /\=/,$ar_str[$k];
       $opis=$opis2 if $ref->{l}==2;
#           if($alias eq 'GUEST_FORM'){next}
                if($alias ne 'OSN' && $alias ne 'MAIN'){
           $opis_alias.=qq[<b>$alias</b>:$opis<br>];
                }else{
                $alias='';
                }
      $tpl->assign(
            NAME=>$name,
            OPIS=>$opis,
            STATUS=>$status,
            ALIAS=>$alias,
            SID=>$ref->{sid},
                        LANG=>$ref->{l}
      );
      $tpl->parse("ROW",".row");
      $tpl->clear_href(1);
        }
 }
      $tpl->assign(
                        OPIS_ALIAS=>$opis_alias
                );
 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();

}

sub view_template {
my $ref=shift;
      my $def={  "main"=>"/constructor.html.$ref->{l}",
                 "text"=>"/constructor_define_editor.html.$ref->{l}",
             };
 my $title=slovo(29,$ref->{l})."$ref->{name}"; #Редактор шаблона 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
my $mes='';
if ($ref->{mes}){$mes=message($ref)}
open A, "$ref->{path_template}/$ref->{name}";
my @ar_text=<A>;
close A;
my $text=join('',@ar_text);
   $text=~s/\</\[/gi;
   $text=~s/\>/\]/gi;
 $tpl->assign(
             MESSAGE=>$mes,
             DATA=>$text,
             NAME=>$ref->{name},
             SID=>$ref->{sid},
             LANG=>$ref->{l}
             );
 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}
sub save_template {
 my $ref=shift;
my $str=$ref->{text};
my $i=0;
my $flag=0;
my $reg='';

while($str=~/\$\{(\w+)\}?|\$(\w+)?/g){
 $i=1;
 $reg=$1||$2;
 my $new=$';
 while($new=~/\$\{$reg\}|\$$reg/g){
  $i++;
  if($i>5||$reg eq 'MAIN_MENU_1'||$reg eq 'MAIN_MENU_2'||$reg eq 'SUB_MENU_2'){
    $flag=1;
    last;
  }
 }
  if($flag==1){last}
}

if($flag==1){
print qq[
<html>
<body>
<script>alert("Double alias $reg !");location.href="$ref->{referrer}"</script>
</body>
</html>
];
}else{
my $pr_mes='19';
 if($ref->{save} eq 'ok'){

 $ref->{text}=~s/\n\r|\r\n/\n/gi;                                                                                 
 $ref->{text}=~s/\[/\</gi;                                                                                      
 $ref->{text}=~s/\]/\>/gi;                                                                                      
 $ref->{text}=~s/\<\%/\[\%/gi;                                                                                  
 $ref->{text}=~s/\%\>/\%\]/gi;                                                                                  
                                                                                                                   
 $ref->{text}=~s/--\<([^\>]+)\>/--\[$1\]/gi;        
 $ref->{text}=~s/\<([^\<^\>]+)\>--/\[$1\]--/gi;                                                                 

 open A, "+>$ref->{path_template}/$ref->{name}";
 print A $ref->{text};
 close A;
}else{ $pr_mes='20'; }
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
   #use Storable;
   #my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};

   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;

print qq[
<html>
<body>
<script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
</body>
</html>
];
}
  exit;
}        

sub default_assign {
     my $ref=shift||{};
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 #    $ref->{user_db}=$user_db;
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
#Считываем параметры из файла assign.ini начало
   open A, "$ref->{path_template}/assign.ini";
   my @lines=<A>;
   close A;
   my $j=0;
    $j=0;
   for(@lines){
        chomp($lines[$j]);
    my ($alias,$value,$opis,$value_eng,$opis_eng,$type)=split /\=/,$lines[$j];
     if($alias && $alias ne 'hr'){
       $value=$value_eng if $ref->{l}==2;
       $user_db->{template}->{assign}->{$alias}=$value;
     }
    $j++;
   }
  #store $user_db, $ref->{path_db};

$ref->{referrer}=~s/\&mes=19//gi;
my $time=time;
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
print qq[
<html>
<body>
<script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=19&$time";
</script>
</body>
</html>
];

  exit;

}