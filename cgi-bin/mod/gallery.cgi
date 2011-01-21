#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с галереей фотографий
 $|=1;
 use CGI::Carp qw(fatalsToBrowser);
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
    $ref->{prefix}=$ref->{db_prefix};
my $p=1;
#print qq[perf $ref->{prefix}];exit;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><title>Authorization error</title></HEAD>
    <body>
    <script>parent.location.href='/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes'</script>
    </body>
    </HTML>
     ";
 exit;
 }
#!!!Проверка sid пользователя!!!#
#!!!Проверка уровня доступа!!!
check_access($ref);
#!!!Проверка уровня доступа end!!!

#Создаем таблицу 
my $create_gallery=qq[
CREATE TABLE `$ref->{db_prefix}_gallery` (
  `id` int(11) NOT NULL auto_increment,
  `idr` varchar(50) NOT NULL default '',
  `name` varchar(150) NOT NULL default '',
  `opis` text NOT NULL,
  `width` int(11) NOT NULL default '0',
  `height` int(11) NOT NULL default '0',
  `sort` int(11) NOT NULL default '0',
  `author` varchar(50) NOT NULL default '',
  `date_reg` date default NULL,
  `url` varchar(250) default NULL,
  PRIMARY KEY  (`id`),
  KEY `author` (`author`),
  KEY `idr` (`idr`)
)
];
my $dbh=dbconnect;
#my $col=$dbh->selectrow_array("select count(*) from gallery");
if(!table_exists(qq[`$ref->{db_prefix}_gallery`])){
my $gallery=$dbh->do($create_gallery);
}
dbdisconnect($dbh);
if ($ref->{a} eq ''){list_cat($ref)} #Выводим все записи галереи
if ($ref->{a} eq 'add'){add_cat($ref)} #Форма добавления/редактирования фотографии
if ($ref->{a} eq 'edit_cat'){edit_cat($ref)} #Редактируем/добавляем фото 
if ($ref->{a} eq 'del_cat'){del_cat($ref)} #Удаляем фото
if ($ref->{a} eq 'del_foto_1'){del_foto_1($ref)} #Удаляем фото
if ($ref->{a} eq 'del_foto_2'){del_foto_2($ref)} #Удаляем фото
if ($ref->{a} eq 'del_logo'){del_logo($ref)} #Удаляем фото
if ($ref->{a} eq 'edit_st'){edit_st($ref)} #Выводим форму редактирования шапки галереи
if ($ref->{a} eq 'save'){save_st($ref)} #Сохраняем шапку 
if ($ref->{a} eq 'save_data'){save_data($ref)} #Сохраняем количество записей на странице, количество фотографий в ряду


sub edit_st { #Выводим форму редактирования шапки
my $ref=shift;
      my $def={  "main"=>"/constructor_document_editor_main.html.$ref->{l}",
                 "text"=>"/constructor_editor_gallery.html.$ref->{l}",
              };
# use Storable;
# my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';

 my $title=slovo(37,$ref->{l})." $name_r "; #Редактор шапки
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
my $mes='';
if ($ref->{mes}){$mes=message($ref)}
open A, "$ref->{path_db}.$ref->{id}.data";
my @ar_text=<A>;
close A;
my $text=join('',@ar_text);
 $tpl->assign(
             MESSAGE=>$mes,
             NAME_ST=>$user_db->{data}->{$ref->{id}}->{name},
             DATA=>$text,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id}
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
sub save_st {
 my $ref=shift;
 my $pr_mes='19';
# use Storable;
# my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 if($ref->{save} ne 'ok'){$pr_mes='20';}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
print qq[
  <HTML>
  <body>
  <script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
 if($ref->{save} eq 'ok'){
 open A, "+>$ref->{path_db}.$ref->{id}.data";
 print A $ref->{ta};
 close A;
 }
  exit;
}

sub list_cat { #вывод галереи фотографий для редактирования / удаления
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_gallery.html.$ref->{l}",
            "row"=>"/constructor_gallery_row.html.$ref->{l}",
              };
# use Storable;
# my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $my_col_records=$user_db->{data}->{$ref->{id}}->{params}->{col_records}||'12';
 my $my_col_rows=$user_db->{data}->{$ref->{id}}->{params}->{col_rows}||'3';

 my $name_zag=$user_db->{data}->{$ref->{id}}->{zag}||$user_db->{data}->{$ref->{id}}->{name};;
 my $title=slovo(48,$ref->{l}).": $name_zag "; #Вывод записей каталога

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dbh=dbconnect;
 #для перехода по страницам
 my $CountPage=50;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(opis) like upper('%$ref->{slovo}%'))];
 my $col="select count(*) from $ref->{db_prefix}_gallery where idr='$ref->{id}' $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from $ref->{db_prefix}_gallery where idr='$ref->{id}' $dop order by sort asc, id desc, name limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
  $tpl->assign(
             COL_RECORDS=>$my_col_records,
             COL_ROWS=>$my_col_rows,
             MESSAGE=>$mes,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id},
             SLOVO=>$ref->{slovo},
             COUNT =>$count
   );
   my $sel=print_razdel_cat('',$ref,'');
      $sel=qq[<select name="idr_cat"><option value="">Не менять $sel</select>];
    while(my $ref_cat=$sth->fetchrow_hashref){
      my $sel_new=$sel;
      $sel_new=~s/value="$ref_cat->{idr}"/value="$ref_cat->{idr}" selected/gi;
     my $img='';
      if (-e "$ref->{path_host}/gallery_image/$ref_cat->{id}-s.jpg"){
      $img="<a target=_blank href='http://$ref->{user_doman}/gallery_image/$ref_cat->{id}.jpg'>есть</a>";
      }else{$img="нет";}
#      if (-e "$ref->{path_host}/gallery_image/$ref_cat->{id}.jpg"){
#      $img="<a target=_blank href='http://$ref->{user_doman}/gallery_image/$ref_cat->{id}.jpg'>есть</a>";
#      }else{$img="нет";}
#print qq[$ref_cat->{idr} <br>];

         $tpl->assign(
                ID_CAT   =>$ref_cat->{id},
                NAME     =>$ref_cat->{name},
                OPIS     =>$ref_cat->{opis},
                SORT     =>$ref_cat->{sort},
                WIDTH     =>$ref_cat->{width},
                AUTHOR     =>$ref_cat->{author},
                HEIGHT     =>$ref_cat->{height},
                IMG      =>$img,
                SID      =>$ref->{sid},
                LANG     =>$ref->{l},
                PAGEIN   =>$PageIn,
                SELECT   => $sel_new,
                PN       =>$p_n,
         );
         $tpl->parse("ROW_CAT",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/gallery.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}";
    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $tpl->assign (
            PEREHOD=>$perehod
    );
    #Переход по страницам

 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}


sub save_data {
 my $ref=shift;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
   my $user_db=$ref->{user_db};
my $pr_mes='19';
if($ref->{save} eq 'ok'){
      $user_db->{data}->{$ref->{id}}->{params}->{col_records}=$ref->{col_records};
      $user_db->{data}->{$ref->{id}}->{params}->{col_rows}=$ref->{col_rows};
      my $kind='params';
      &store_db( $user_db,  $ref->{id},$kind);
#      my $par=$user_db->{data}->{$ref->{id}}->{params};
#      my %par=%$par;
#      my @par_names=keys %par;
#    my $params='';
#      for (my $i=0;$i<=$#par_names;$i++){$params.=qq[$par_names[$i]=$par{$par_names[$i]},];}
#     chop $params;   
#   my $dbh=&dbconnect;
#      $dbh->do("update structure set params='$params' where id='$ref->{id}'");
#      dbdisconnect($dbh);
}else{$pr_mes='20';}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}
sub del_foto_1 {
 my $ref=shift;
   unlink "$ref->{path_host}/gallery_image/$ref->{id_cat}-1-s.jpg";
   unlink "$ref->{path_host}/gallery_image/$ref->{id_cat}-1.jpg";
print qq[Фото удалено <a href="/cgi-bin/mod/gallery.cgi?a=add&id_cat=$ref->{id_cat}&id=$ref->{id}">Продолжить редактирование</a>];
}
sub del_foto_2 {
 my $ref=shift;
   unlink "$ref->{path_host}/gallery_image/$ref->{id_cat}-2-s.jpg";
   unlink "$ref->{path_host}/gallery_image/$ref->{id_cat}-2.jpg";
print qq[Фото удалено <a href="/cgi-bin/mod/gallery.cgi?a=add&id_cat=$ref->{id_cat}&id=$ref->{id}">Продолжить редактирование</a>];
}
sub del_logo {
 my $ref=shift;
   unlink "$ref->{path_host}/gallery_image/$ref->{id_cat}-logo.jpg";
print qq[Фото удалено <a href="/cgi-bin/mod/gallery.cgi?a=add&id_cat=$ref->{id_cat}&id=$ref->{id}">Продолжить редактирование</a>];
}

sub del_cat {
 my $ref=shift;
 my $dbh=dbconnect;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 if($ref->{del}){
 my @ar_id_cat=CGI::param('id_cat');
 my $str_id_cat='';
 my $dop=qq[id='$ar_id_cat[0]'];
 if($#ar_id_cat>0){
 $str_id_cat=join(',',@ar_id_cat);
 $str_id_cat=~s/\,$//gi;
 $dop=qq[id in ($str_id_cat)];
 }
#print qq[ok];
 my $del=$dbh->do("delete from $ref->{db_prefix}_gallery where idr='$ref->{id}' and $dop");
 for (my $i=0;$i<=$#ar_id_cat;$i++){
  if (-e "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-s.jpg"){
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-s.jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i].jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-1-s.jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-1.jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-2-s.jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-2.jpg";
   unlink "$ref->{path_host}/gallery_image/$ar_id_cat[$i]-logo.jpg";
  }
 }
 }
elsif($ref->{upd}){
 my @ar_id_cat=CGI::param('id_cat_upd');
 my @ar_idr=CGI::param('idr_cat');
 my @ar_sort=CGI::param('sort');
 for (my $i=0;$i<=$#ar_id_cat;$i++){
#print qq[ok $ref->{user_db}->{data}->{$ar_idr[$i]}->{mod}]; exit;
        if($ref->{user_db}->{data}->{$ar_idr[$i]}->{mod} eq 'gallery' && $ar_idr[$i] ne '' && $ar_idr[$i] ne '0'){
        my $upd=$dbh->do("update $ref->{db_prefix}_gallery set idr='$ar_idr[$i]' where id='$ar_id_cat[$i]'");
#        print qq[update $ref->{db_prefix}_gallery set idr='$ar_idr[$i]' where id='$ar_id_cat[$i]';<br>];
        }
 }
# exit;
 }
elsif($ref->{sort}){
 my @ar_id_cat=CGI::param('id_cat_upd');
 my @ar_idr=CGI::param('idr_cat');
 my @ar_sort=CGI::param('id_sort');
 for (my $i=0;$i<=$#ar_id_cat;$i++){
        my $upd=$dbh->do("update $ref->{db_prefix}_gallery set sort='$ar_sort[$i]' where id='$ar_id_cat[$i]'");
 }
 }
 dbdisconnect($dbh);
 my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub add_cat {
 my $ref=shift;
 my $def={  "main"=>"/constructor_document_editor_mod.html.$ref->{l}",
            "text"=>"/constructor_gallery_add.html.$ref->{l}"
              };

 my $dbh=dbconnect;
 my $ref_cat=$ref;
 if ($ref->{id_cat}){
 my $sel="select * from $ref->{db_prefix}_gallery where idr='$ref->{id}' and id='$ref->{id_cat}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    $ref_cat=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 }
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $name_cat=$ref_cat->{name};
 if(!$ref_cat->{name}){$name_cat='New'}
 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';

 my $title=slovo(48,$ref->{l}) ." - $name_r "; #Редатирование товара
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $curency=$user_db->{data}->{params}->{curency}||'$';
 my $img_cat="";
 if(-e "$ref->{path_host}/gallery_image/$ref_cat->{id}-s.jpg"){
  $img_cat.=qq[<a target=_blank title='Full screen' href="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}.jpg">
<img src="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-s.jpg" border=0></a><br>];
 }
 if(-e "$ref->{path_host}/gallery_image/$ref_cat->{id}-1-s.jpg"){
  $img_cat.=qq[<a target=_blank title='Full screen' href="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-1.jpg">
<img src="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-1-s.jpg" border=0></a><br>
    <a href="/cgi-bin/mod/gallery.cgi?a=del_foto_1&id_cat=$ref->{id_cat}&id=$ref->{id}">[удалить фото 1]</a><br>

];
 }
 if(-e "$ref->{path_host}/gallery_image/$ref_cat->{id}-2-s.jpg"){
  $img_cat.=qq[<a target=_blank title='Full screen' href="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-2.jpg">
<img src="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-2-s.jpg" border=0></a><br>
    <a href="/cgi-bin/mod/gallery.cgi?a=del_foto_2&id_cat=$ref->{id_cat}&id=$ref->{id}">[удалить фото 2]</a><br>

];
 }
 if(-e "$ref->{path_host}/gallery_image/$ref_cat->{id}-logo.jpg"){
  $img_cat.=qq[
<img src="http://$ref->{user_doman}/gallery_image/$ref->{id_cat}-logo.jpg" border=0><br>
    <a href="/cgi-bin/mod/gallery.cgi?a=del_logo&id_cat=$ref->{id_cat}&id=$ref->{id}">[удалить лого]</a><br>
    ];
 }
=r1
 my $sel_users="select * from users_ order by login, name";
 my $sth=$dbh->prepare($sel_users);
    $sth->execute;
    my $sel_users=qq[<select name="users_id"><option value="27">Автор не определен (Выберите из списка)</option>];
    while(my $ref_u=$sth->fetchrow_hashref){
	$sel_users.=qq[<option value="$ref_u->{id}">$ref_u->{l_name} $ref_u->{name} $ref_u->{f_name}($ref_u->{login})</option>];
    }
    $sth->finish;
    $sel_users.="</select>";

    $sel_users=~s/value=\"$ref_cat->{users_id}\"/value=\"$ref_cat->{users_id}\" SELECTED/gi;

    my $sel_konkurs=qq[<select name="konkurs_number"><option value="8">8 фотоконкурс</option><option value="9">9 фотоконкурс</option><option value="10">10 фотоконкурс</option></select>];

    $sel_konkurs=~s/value=\"$ref_cat->{konkurs_number}\"/value=\"$ref_cat->{konkurs_number}\" SELECTED/gi;
=cut

   $ref_cat->{opis}=~s/\n/ /gi;
   $ref_cat->{opis}=~s/\s+/ /gi;
   $ref_cat->{opis}=~s/'/"/gi; #'

    $tpl->assign (
        IMG_CAT=>$img_cat,
        NAME_ST=>$name_cat,
        MOD=>$user_db->{data}->{$ref->{id}}->{mod},
        ID=>$ref->{id},
        ID_CAT=>$ref->{id_cat},
        IDR=>$ref->{idr},
        NAME=>$ref_cat->{name},
#        SEL_USERS=>$sel_users,
#        SEL_KONKURS=>$sel_konkurs,
        URL=>$ref_cat->{url},
        AUTHOR=>$ref_cat->{author},
        OPIS=>$ref_cat->{opis},
        SORT=>$ref_cat->{sort},
        SID=>$ref->{sid},
        LANG=>$ref->{l},
        PAGEIN     =>$ref->{PageIn},
        PN     =>$ref->{p_n},
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

sub print_razdel_cat {
    my $idr=shift||'0';
    my $ref=shift;
    my $sel=shift;
        my $sort=$ref->{user_db}->{data}->{sort}||{};
        my $parent=$ref->{user_db}->{data}->{parent}||{};
    my %sort=%$sort;
    my %parent=%$parent;
    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    foreach my $key (@ar_sort_key){
        if($parent{$key} eq $idr){
        my $nbsp='';
        for (my $t=0;$t<=$p;$t++){
          $nbsp.="&nbsp;";
        }
        my $name=$ref->{user_db}->{data}->{$key}->{name};
            if(length($name)>25){
            $name=substr($name,0,25)."...";
            }
        $sel.=qq[<option value="$key">$nbsp-$name];
        $p++;
        if($key ne ''){
        $sel=print_razdel_cat($key,$ref,$sel);
        }
        $p--;
        }
    }
return $sel;
}