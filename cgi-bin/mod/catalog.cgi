#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с интернет магазином
 $|=1;
 use lib "../";
 use Modules::Constructor;
# use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
    $ref->{prefix}=$ref->{db_prefix};
#print qq[perf $ref->{prefix}];exit;
#!!!Проверка sid пользователя!!!#
 my $p=1;
 my $create_catalog=qq[
  CREATE TABLE $ref->{db_prefix}_catalog (
  `id` int(11) NOT NULL auto_increment,
  `idr` varchar(255) collate cp1251_bin NULL default '',
  `name` varchar(255) collate cp1251_bin NULL default '',
  `short` varchar(255) collate cp1251_bin default NULL,
  `opis` text collate cp1251_bin,
  `opis_r` text collate cp1251_bin,
  `cost` decimal(11,2) default '0.00',
  `mera` varchar(50) collate cp1251_bin default NULL,
  `status` tinyint(4) default '1',
  `articul` varchar(100) collate cp1251_bin default '1',
  `sort` int(11) default '0',
  `action` int(11) default '0',
  `zhir` varchar(50) collate cp1251_bin default NULL,
  `tara` varchar(100) collate cp1251_bin default NULL,
  `srok` varchar(100) collate cp1251_bin default NULL,
  `shtrih_kod` varchar(250) collate cp1251_bin default NULL,
  `gost` varchar(250) collate cp1251_bin default NULL,
  `img_end` varchar(10) collate cp1251_bin default 'jpg',
  PRIMARY KEY  (id),
  UNIQUE KEY name_idr (idr,name),
  KEY idr (idr),
  KEY name (name),
  KEY short (short)
) ];    
 my $create_basket=qq[
CREATE TABLE basket_$ref->{prefix} (
  id int(11) NOT NULL auto_increment,
  id_pol int(11) NOT NULL default '0',
  id_cat int(11) NOT NULL default '0',
  id_zakaz varchar(7) NOT NULL default '',
  number int(11) NOT NULL default '0',
  id_dostavka varchar(10) NULL default '',
  id_oplata varchar(10)  NULL default '',
  status int(11) NOT NULL default '0',
  col int(11) NOT NULL default '0',
  cost decimal(11,2) NOT NULL default '0.00',
  data_reg datetime NOT NULL default '0000-00-00 00:00:00',
  id_adres int(11) NULL default '0',
  PRIMARY KEY  (id),
  KEY id_cat (id_cat),
  KEY id_zakaz (id_zakaz),
  KEY status (status)
)
];      
 my $create_users_adres=qq[
CREATE TABLE users_adres_$ref->{prefix} (
  id int(11) NOT NULL auto_increment,
  id_pol int(11) NOT NULL default '0',
  country varchar(15) NOT NULL default '',
  post_index varchar(10) NOT NULL default '',
  region varchar(100) NOT NULL default '',
  city varchar(50) NOT NULL default '',
  fio varchar(50) NOT NULL default '',
  phone varchar(50) NOT NULL default '',
  street varchar(50) NOT NULL default '',
  home varchar(10) NOT NULL default '',
  place varchar(10) NOT NULL default '',
  dop varchar(255) NOT NULL default '',
  PRIMARY KEY  (id)
)
];      
 my $create_users_cat=qq[
CREATE TABLE users_cat_$ref->{prefix} (
  id int(11) NOT NULL auto_increment,
  name varchar(255) NOT NULL default '',
  l_name varchar(255) NOT NULL default '',
  f_name varchar(255) NOT NULL default '',
  pass varchar(15) NOT NULL default '',
  email varchar(100) NOT NULL default '',
  date_reg datetime NOT NULL default '0000-00-00 00:00:00',
  skidka int(11) NOT NULL default '0',
  PRIMARY KEY  (id),
  UNIQUE KEY email (email),
  KEY pass (pass,email)
)
];      
my $dbh=dbconnect;
#my $col=$dbh->selectrow_array("select count(*) from $ref->{db_prefix}_catalog");
if(!table_exists(qq[`$ref->{db_prefix}_catalog`])){
 my $catalog=$dbh->do($create_catalog);
# my $basket=$dbh->do($create_basket);
# my $user_adres=$dbh->do($create_users_adres);
# my $user_cat=$dbh->do($create_users_cat);
}
dbdisconnect($dbh);
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

if ($ref->{a} eq ''){list_cat($ref)} #Выводим все записи каталога по разделу 
if ($ref->{a} eq 'export'){view_export($ref)} #Форма  импорта экспорта Excel
if ($ref->{a} eq 'add'){add_cat($ref)} #Форма добавления/редактирования товара 
if ($ref->{a} eq 'edit_cat'){edit_cat($ref)} #Редактируем/добавляем товар 
if ($ref->{a} eq 'del_cat'){del_cat($ref)} #Удаляем товары 
if ($ref->{a} eq 'del_img'){del_img($ref)} #Удаляем картинку товара
if ($ref->{a} eq 'edit_st'){edit_st($ref)} #Выводим форму редактирования шапки каталога
if ($ref->{a} eq 'save'){save_st($ref)} #Сохраняем шапку 
if ($ref->{a} eq 'save_data'){save_data($ref)} #Сохраняем емайл адрес, валюту, количество записей на странице
if ($ref->{a} eq 'users'){list_users($ref)} #Выводим пользователей по дате регистрации (с сортировкой)
if ($ref->{a} eq 'update_skidki'){update_skidki($ref)} #Обновляем скидки
if ($ref->{a} eq 'del_user'){del_user($ref)} #Удаляем пользователя
if ($ref->{a} eq 'order'){list_order($ref)} #Выводим заказы пользователей
if ($ref->{a} eq 'update_order'){update_order($ref)} #Удаляем заказы пользователей/обновляем статус заказов
if ($ref->{a} eq 'view_order'){view_order($ref)} #Выводим информацию о заказе

sub edit_st {
my $ref=shift;
      my $def={  "main"=>"/constructor.html.$ref->{l}",
                 "text"=>"/constructor_editor.html.$ref->{l}",
              };
# use Storable;
# my $user_db = retrieve $ref->{path_db};
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
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
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

sub list_cat {
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_cat.html.$ref->{l}",
            "row"=>"/constructor_cat_row.html.$ref->{l}",
              };
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 #$ref->{user_db}=$user_db;
 my $user_db=$ref->{user_db};

 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $my_email=$user_db->{data}->{$ref->{id}}->{params}->{email}||$ref->{user}->{email};
 my $my_col_records=$user_db->{data}->{$ref->{id}}->{params}->{col_records}||'12';
 my $my_row_records=$user_db->{data}->{$ref->{id}}->{params}->{row_records}||'3';
 my $curency=$user_db->{data}->{$ref->{id}}->{params}->{curency}||'$';

 my $dostavka_post=$user_db->{data}->{$ref->{id}}->{params}->{dostavka_post}||'';
 my $dostavka_kurer=$user_db->{data}->{$ref->{id}}->{params}->{dostavka_kurer}||'';
 my $dostavka_ftp=$user_db->{data}->{$ref->{id}}->{params}->{dostavka_ftp}||'';
 my $dostavka_email=$user_db->{data}->{$ref->{id}}->{params}->{dostavka_email}||'';

 my $predoplata=$user_db->{data}->{$ref->{id}}->{params}->{predoplata}||'';
 my $postoplata=$user_db->{data}->{$ref->{id}}->{params}->{postoplata}||'';
 my $name_zag=$user_db->{data}->{$ref->{id}}->{zag}||$user_db->{data}->{$ref->{id}}->{name};;
 my $title=slovo(38,$ref->{l}).": $name_zag "; #Вывод записей каталога

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dbh=dbconnect;
 #для перехода по страницам
 my $CountPage=50;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop='';
 if($ref->{slovo}){
 $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(opis) like upper('%$ref->{slovo}%'))];
 }
 my $col="select count(*) from $ref->{db_prefix}_catalog where idr='$ref->{id}' $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from $ref->{db_prefix}_catalog where idr='$ref->{id}' $dop order by sort asc, id desc, name limit $off,$CountPage";
 #print $sel;
 my $sth=$dbh->prepare($sel);
    $sth->execute;
  $tpl->assign(
             DOSTAVKA_POST=>$dostavka_post,
             DOSTAVKA_KURER=>$dostavka_kurer,
             DOSTAVKA_FTP=>$dostavka_ftp,
             DOSTAVKA_EMAIL=>$dostavka_email,
             PREDOPLATA=>$predoplata,
             POSTOPLATA=>$postoplata,
             CURENCY=>$curency,
             EMAIL_OWNER=>$my_email,
             COL_RECORDS=>$my_col_records,
             ROW_RECORDS=>$my_row_records,
             MESSAGE=>$mes,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id},
             SLOVO=>$ref->{slovo},
             COUNT =>$count
   );
   my $sel=print_razdel_cat_2($ref);
      $sel=qq[<select name=idr_cat>$sel</select>];
    while(my $ref_cat=$sth->fetchrow_hashref){
     my $img='';
      if (-e "$ref->{path_host}/cat_image/$ref_cat->{id}-s.$ref_cat->{img_end}"){
      $img="<a target=_blank href='http://$ref->{user_doman}/cat_image/$ref_cat->{id}.$ref_cat->{img_end}'>есть</a>";
      }else{$img="нет";}
        my $sel_idr=$sel;
           $sel_idr=~s/value="$ref_cat->{idr}"/value="$ref_cat->{idr}" selected/gi;
        my $checked='';
           $checked='checked' if $ref_cat->{status};
#print qq[sort = $ref_cat->{sort}];
         $tpl->assign(
                ID_CAT   =>$ref_cat->{id},
                CHECKED   =>$checked,
                ARTICUL   =>$ref_cat->{articul},
                SELECT     =>$sel_idr,
                NAME     =>"$ref_cat->{name} $ref_cat->{mera}",
                ZHIR     =>$ref_cat->{zhir},
                SHTRIH_KOD     =>$ref_cat->{shtrih_kod},
                GOST     =>$ref_cat->{gost},
                SHORT     =>$ref_cat->{short},
                IMG     =>$img,
                COST     =>$ref_cat->{cost},
                SORT     =>$ref_cat->{sort},
                SID     =>$ref->{sid},
                LANG     =>$ref->{l},
                PAGEIN     =>$PageIn,
                PN     =>$p_n,
         );
         $tpl->parse("ROW_CAT",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}";
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

sub move_img {
 my $move_from=shift;
 my $move_to=shift;
 use File::Copy;
                move("$move_from","$move_to");
unlink "move_from";
return 1;
}

sub save_data {
 my $ref=shift;
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
my $pr_mes='19';
if($ref->{save} eq 'ok'){
      $user_db->{data}->{$ref->{id}}->{params}->{email}=$ref->{email_owner};
      $user_db->{data}->{$ref->{id}}->{params}->{col_records}=$ref->{col_records};
      $user_db->{data}->{$ref->{id}}->{params}->{row_records}=$ref->{row_records};
      $user_db->{data}->{$ref->{id}}->{params}->{curency}=$ref->{curency};
      $user_db->{data}->{$ref->{id}}->{params}->{dostavka_post}=$ref->{dostavka_post}||'';
      $user_db->{data}->{$ref->{id}}->{params}->{dostavka_kurer}=$ref->{dostavka_kurer}||'';
      $user_db->{data}->{$ref->{id}}->{params}->{dostavka_ftp}=$ref->{dostavka_ftp}||'';
      $user_db->{data}->{$ref->{id}}->{params}->{dostavka_email}=$ref->{dostavka_email}||'';

      $user_db->{data}->{$ref->{id}}->{params}->{predoplata}=$ref->{predoplata}||'';
      $user_db->{data}->{$ref->{id}}->{params}->{postoplata}=$ref->{postoplata}||'';

      my $kind='params';
      &store_db ($user_db,$ref->{id},$kind);
#      my $par=$user_db->{data}->{$ref->{id}}->{params};
#      my %par=%$par;
#      my @par_names=keys %par;
#    my $params='';
#      for (my $i=0;$i<=$#par_names;$i++){$params.=qq[$par_names[$i]=$par{$par_names[$i]},];}
#     chop $params;
      #print $params;exit;
      
 #   my $dbh=&dbconnect;
 #     $dbh->do("update structure set params='$params' where id='$ref->{id}'");
 #     dbdisconnect($dbh);
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

sub del_cat {
 my $ref=shift;
 my $dbh=dbconnect;
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 #$ref->{user_db}=$user_db;
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
 for (my $i=0;$i<=$#ar_id_cat;$i++){
  if (-e "$ref->{path_host}/cat_image/$ar_id_cat[$i]-s.jpg"){
  my $img_end=$dbh->selectrow_array("select img_end from catalog_ where id='$ar_id_cat[$i]'");
   unlink "$ref->{path_host}/cat_image/$ar_id_cat[$i]-s.jpg";
   unlink "$ref->{path_host}/cat_image/$ar_id_cat[$i]-m.jpg";
   unlink "$ref->{path_host}/cat_image/$ar_id_cat[$i]-s-50.jpg";
   unlink "$ref->{path_host}/cat_image/$ar_id_cat[$i].jpg";
  }
 }
 my $del=$dbh->do("delete from $ref->{db_prefix}_catalog where idr='$ref->{id}' and $dop");

 }
elsif($ref->{upd}){
 my @ar_id_cat=CGI::param('id_cat_upd');
 my @ar_idr=CGI::param('idr_cat');
 my @ar_shtrih_kod=CGI::param('shtrih_kod');
 my @ar_gost=CGI::param('gost');
 my @ar_sort=CGI::param('sort_cat');
 for (my $i=0;$i<=$#ar_id_cat;$i++){
        #if($ref->{user_db}->{data}->{$ar_idr[$i]}->{mod} eq 'catalog'){
        my $upd=$dbh->do("update $ref->{db_prefix}_catalog set idr='$ar_idr[$i]',sort='$ar_sort[$i]',shtrih_kod='$ar_shtrih_kod[$i]',gost='$ar_gost[$i]' where id='$ar_id_cat[$i]'");
        #}

	# увеличили пиктограмму до 200рх по ширине
	#my $img_end=$dbh->selectrow_array("select img_end from catalog_ where id='$ar_id_cat[$i]'");
	#if (-e "$ref->{path_host}/cat_image/$ar_id_cat[$i]-s.$img_end"){
                #делаем маленькую картинку       
        #         magick('200',"$ref->{path_host}/cat_image/$ar_id_cat[$i].$img_end","$ref->{path_host}/cat_image/$ar_id_cat[$i]-s.$img_end"); 
	#}
 }
 }
elsif($ref->{upd_status}){
 my @ar_id_cat=CGI::param('id_cat_upd');
 for (my $i=0;$i<=$#ar_id_cat;$i++){
        my $status=0;
        my $value_status="$ar_id_cat[$i]_status";
           $status=1 if $ref->{$value_status};
        my $upd=$dbh->do("update $ref->{db_prefix}_catalog set status='$status' where id='$ar_id_cat[$i]'");
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
sub del_img { #удаляем картинку
  my $ref=shift;
  my $img_end=$dbh->selectrow_array("select img_end from catalog_ where id='$ref->{id_cat}'");

  if (-e "$ref->{path_host}/cat_image/$ref->{id_cat}-s.$img_end"){
   unlink "$ref->{path_host}/cat_image/$ref->{id_cat}-s.$img_end";
   unlink "$ref->{path_host}/cat_image/$ref->{id_cat}-m.$img_end";
   unlink "$ref->{path_host}/cat_image/$ref->{id_cat}-s-50.$img_end";
   unlink "$ref->{path_host}/cat_image/$ref->{id_cat}.$img_end";
  }
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
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_cat_add.html.$ref->{l}"
              };

 my $ref_cat=$ref;
 if ($ref->{id_cat}){
 my $dbh=dbconnect;
 my $sel="select * from $ref->{db_prefix}_catalog where idr='$ref->{id}' and id='$ref->{id_cat}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    $ref_cat=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 }
 my $user_db = $ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $name_cat=$ref_cat->{name};
 if(!$ref_cat->{name}){$name_cat='New'}
 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';
 my $time=time;
 my $title=slovo(38,$ref->{l}) ." - $name_r "; #Редатирование товара
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $curency=$user_db->{data}->{$ref->{id}}->{params}->{curency}||'$';
 my $img_cat="";
 if(-e "$ref->{path_host}/cat_image/$ref_cat->{id}-s.$ref_cat->{img_end}"){
  $img_cat=qq[<a target=_blank title='Full screen' href="http://$ref->{user_doman}/cat_image/$ref->{id_cat}.$ref_cat->{img_end}">
<img src="http://$ref->{user_doman}/cat_image/$ref->{id_cat}-s.$ref_cat->{img_end}?$time" border=0></a>];
 }
   my $checked='';
      $checked='checked' if $ref_cat->{action} eq '1';
	$ref_cat->{short}=~s/\n|\r|\t/ /gi;
	$ref_cat->{short}=~s/\'/\"/gi;
	$ref_cat->{opis}=~s/\n|\r|\t/ /gi;
	$ref_cat->{opis}=~s/\'/\"/gi;
	$ref_cat->{opis_r}=~s/\n|\r|\t/ /gi;
	$ref_cat->{opis_r}=~s/\'/\"/gi;
    $tpl->assign (
        CHECKED=>$checked,
        CURENCY=>$curency,
        IMG_CAT=>$img_cat,
        NAME_ST=>$name_cat,
        MOD=>$user_db->{data}->{$ref->{id}}->{mod},
        ID=>$ref->{id},
        ID_CAT=>$ref->{id_cat},
        IDR=>$ref->{idr},
        NAME=>$ref_cat->{name},
        ZHIR=>$ref_cat->{zhir},
        TARA=>$ref_cat->{tara},
        SROK=>$ref_cat->{srok},
        SHORT=>$ref_cat->{short},
        OPIS=>$ref_cat->{opis},
        OPIS_R=>$ref_cat->{opis_r},
        MERA=>$ref_cat->{mera},
        COST=>$ref_cat->{cost},
        SHTRIH_KOD     =>$ref_cat->{shtrih_kod},
        GOST     =>$ref_cat->{gost},
        ARTICUL=>$ref_cat->{articul},
        TIME=>time,
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

sub edit_cat {
 my $ref=shift;
    $ref->{name}=~tr/'/"/; #'
    $ref->{mera}=~tr/'/"/; #'
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
my $user_db=$ref->{user_db};

 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';
 my $pr_mes='19';
 $ref->{action}='0' if !$ref->{action};
if($ref->{save} eq 'ok'){
 #if($mod_razdel eq 'catalog'){
 if(1==1){
  my $dbh=dbconnect;
 if($ref->{id_cat}){
  # my $sql="update $ref->{db_prefix}_catalog set opis_r=?,shtrih_kod=?,gost=?,action=?,name=?,short=?,mera=?,cost=?,opis=?,articul=?,zhir=?,tara=?,srok=? where id=? and idr=?";
   my $sql="update $ref->{db_prefix}_catalog set gost=?,action=?,name=?,short=?,mera=?,cost=?,opis=?,articul=?,zhir=?,tara=?,srok=? where id=? and idr=?";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{gost},$ref->{action},$ref->{name},$ref->{short},$ref->{mera},$ref->{cost},$ref->{opis},$ref->{articul},$ref->{zhir},$ref->{tara},$ref->{srok},$ref->{id_cat},$ref->{id});
   $sth->finish;
 }else{
  # my $sql="insert into $ref->{db_prefix}_catalog (opis_r,shtrih_kod,gost,action,name,short,mera,cost,opis,idr,articul,zhir,tara,srok) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)";
   my $sql="insert into $ref->{db_prefix}_catalog (gost,action,name,short,mera,cost,opis,idr,articul,zhir,tara,srok) values (?,?,?,?,?,?,?,?,?,?,?,?)";
   my $sth=$dbh->prepare($sql);
   my $ins=$sth->execute($ref->{gost},$ref->{action},$ref->{name},$ref->{short},$ref->{mera},$ref->{cost},$ref->{opis},$ref->{id},$ref->{articul},$ref->{zhir},$ref->{tara},$ref->{srok});
   $sth->finish;
   $ref->{id_cat}=$sth->{mysql_insertid};
       #print qq[ins=$ins, <br>$sql <br> $ref->{action},$ref->{name},$ref->{short},$ref->{mera},$ref->{cost},$ref->{ta},$ref->{id},$ref->{articul},$ref->{zhir},$ref->{tara},$ref->{srok}]; exit;
 }
 dbdisconnect($dbh);
####Загрузка картинки
 my $upfile=$ref->{upfile};
 if($upfile ne '' && $ref->{id_cat} ne ''){
      my @ar1=split /\\/,$upfile;
      my $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+//gi;
      $file=~tr/ ИЖСЙЕМЦЬЫГУЗТШБЮОПНКДФЩЪВЯЛХРЭАЧёижсйемцьыгузтшбюопнкдфщъвялхрэачЁ/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
      my $nmf=$ar2[0];
      my $typef=$ar2[$#ar2];
      $nmf=substr $nmf,0,25;
      $file="$nmf.$typef";
	#print qq[$file]; exit;
      # обновляем расширение картинки
      my $upd=$dbh->do("update $ref->{db_prefix}_catalog set img_end='$typef' where id='$ref->{id_cat}'");
     #print qq[update catalog_ set img_end='$typef' where id='$ref->{id_cat}']; exit;
                if(!-d "$ref->{path_host}/cat_image"){
                  mkdir_("$ref->{path_host}/cat_image");
                }
        my ($buf);
         open A, "+>$ref->{path_host}/cat_image/$ref->{id_cat}-.$typef";
         binmode(A);
         while (my $bytesread = read($upfile, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/cat_image/$ref->{id_cat}-.$typef";
        close A;

		my $img_logo="$ref->{path_root}/templates/vodznak.png";
		my $img_logo_small = "$ref->{path_root}/templates/smallvodznak.png";
		#print qq[$img_logo $img_logo_small];  exit;

                #делаем основную картинку принудительно 600
                 magick_width_only('500',"$ref->{path_host}/cat_image/$ref->{id_cat}-.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}.$typef"); 

		# вставляем водяной знак
		# composit_img("$ref->{path_host}/cat_image/$ref->{id_cat}.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}.$typef",$img_logo); 

                #делаем маленькую картинку       
                 magick_width_only('130',"$ref->{path_host}/cat_image/$ref->{id_cat}-.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}-s.$typef"); 

		# вставляем водяной знак
		#composit_img("$ref->{path_host}/cat_image/$ref->{id_cat}-s.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}-s.$typef",$img_logo_small);   


                #делаем картинку (бред менеджера)
                 magick_width_only('200',"$ref->{path_host}/cat_image/$ref->{id_cat}-.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}-m.$typef"); 
		
		# вставляем водяной знак
		# composit_img("$ref->{path_host}/cat_image/$ref->{id_cat}-m.$typef","$ref->{path_host}/cat_image/$ref->{id_cat}-m.$typef",$img_logo_small);   
                 #exit;
      }
####Загрузка картинки end

 
 }
}else{$pr_mes='20';}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
 my $sort=$user_db->{data}->{sort}||{};
 my %sort=%$sort;
 my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
#parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";

print qq[
<html>
<body>
<script>
location.href="/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&mes=$pr_mes&id_cat=$ref->{id_cat}&a=add&PageIn=$ref->{PageIn}&p_n=$ref->{p_n}";
</script>
</body>
</html>
];
  exit;
}

sub view_export {
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_cat_export.html.$ref->{l}",
              };
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $title=slovo(39,$ref->{l})." $name_r "; #экспорт импорт каталога

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

  $tpl->assign(
             ID=>$ref->{id},
             SID=>$ref->{sid},
             LANG=>$ref->{l},
                 MOD=>$user_db->{data}->{$ref->{id}}->{mod},
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

sub list_users { #Вывод пользователей с возможностью расставить скидки
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_cat_users.html.$ref->{l}",
            "row"=>"/constructor_cat_users_row.html.$ref->{l}",
              };
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $title=slovo(40,$ref->{l}); #Вывод пользователей

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dbh=dbconnect;
 #для перехода по страницам
 my $CountPage=50;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop=qq[and (upper(name) like upper('%$ref->{slovo}%')
 or upper(l_name) like upper('%$ref->{slovo}%')
 or upper(f_name) like upper('%$ref->{slovo}%')
 or upper(email) like upper('%$ref->{slovo}%'))];
 my $col="select count(*) from users_cat_$ref->{prefix} where 1 $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from users_cat_$ref->{prefix} where 1 $dop order by date_reg desc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
  $tpl->assign(
             MESSAGE=>$mes,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id},
             SLOVO=>$ref->{slovo},
             COUNT =>$count
   );
    while(my $ref_user=$sth->fetchrow_hashref){
                 my $fio="$ref_user->{l_name} $ref_user->{name} $ref_user->{f_name}";
             my ($data,$hour)=split / /,$ref_user->{date_reg};
             my ($y,$m,$d)=split /\-/,$data;
                 my $data_pr="$d.$m.$y $hour";
                 my $col_pokupok=$dbh->selectrow_array("select sum(col) from basket_$ref->{prefix} where id_pol='$ref_user->{id}' and status!='0'")||0;
         $tpl->assign(
                ID_USER   =>$ref_user->{id},
                FIO     =>$fio,
                DATA     =>$data_pr,
                EMAIL     =>$ref_user->{email},
                PASS     =>$ref_user->{pass},
                SKIDKA     =>$ref_user->{skidka},
                POKUPOK     =>$col_pokupok,
                SID     =>$ref->{sid},
                LANG     =>$ref->{l},
                ID     =>$ref->{id},
         );
         $tpl->parse("ROW_CAT_USERS",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&a=users&slovo=$ref->{slovo}";
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

sub update_skidki {
 my $ref=shift;
 my @ar_id_user=CGI::param('id_user');
 my @ar_skidka=CGI::param('skidka');
 my $str_id_cat='';
 my $dbh=dbconnect;
 for (my $i=0;$i<=$#ar_id_user;$i++){
 my $upd="update users_cat_$ref->{prefix} set skidka=$ar_skidka[$i] where id=$ar_id_user[$i]";
 my $sth=$dbh->prepare($upd);
    $sth->execute;
 }
 dbdisconnect($dbh);
 my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=19&$time"</script>
  </body>
  </HTML>
 ];
  exit;

}
sub del_user { #Удаляем пользователя и все его заказы и адреса
 my $ref=shift;
 my $dbh=dbconnect;
 my $del=$dbh->do("delete from users_cat_$ref->{prefix} where id='$ref->{id_user}'");
 my $del_adr=$dbh->do("delete from users_adres_$ref->{prefix} where id_pol='$ref->{id_user}'");
 my $del_basket=$dbh->do("delete from basket_$ref->{prefix} where id_pol='$ref->{id_user}'");
 dbdisconnect($dbh);
 my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=19&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub list_order {#выводим список всех заказов пользователя (вначале только подтвержденные, далее возможность сортировки)
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_cat_orders.html.$ref->{l}",
            "row"=>"/constructor_cat_orders_row.html.$ref->{l}",
              };
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $title=slovo(40,$ref->{l}); #Вывод пользователей

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dbh=dbconnect;
 #для перехода по страницам
 my $CountPage=50;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop1='';
 if (!$ref->{slovo}){
 $ref->{status}='0' if $ref->{status} eq '3';
 $ref->{status}=1 if $ref->{status} eq '';
 $dop1="and status='$ref->{status}'";
 }
 my $dop2='';
 my $dop='';
 $dop2="and id_pol='$ref->{id_user}'" if $ref->{id_user};
 if($ref->{slovo}){
  $dop=qq[and id_zakaz='$ref->{slovo}'];
 }
 my $col="select count(distinct id_zakaz) from basket_$ref->{prefix} where 1 $dop1 $dop2 $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from basket_$ref->{prefix}
         where 1 $dop $dop1 $dop2
         group by id_zakaz
         order by data_reg desc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
  $sth->execute;
  $tpl->assign(
             MESSAGE=>$mes,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             SLOVO=>$ref->{slovo},
             STATUS=>$ref->{status},
             ID_USER=>$ref->{id_user},
             ID=>$ref->{id},
             COUNT =>$count
   );
 my $sel_status1=qq[
 <select name=sel_status>
 <option value='0'>Не подтвержден
 <option value='1'>Подтвержден
 <option value='2'>Обработан
 </select>
 ];
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $curency=$user_db->{data}->{$ref->{id}}->{params}->{curency}||'$';
    while(my $ref_basket=$sth->fetchrow_hashref){
             my ($data,$hour)=split / /,$ref_basket->{data_reg};
             my ($y,$m,$d)=split /\-/,$data;
                 my $data_pr="$d.$m.$y $hour";
                 my $sel_status=$sel_status1;
         $sel_status=~s/value=\'$ref_basket->{status}\'/value=\'$ref_basket->{status}\' selected/gi;
                 my $sel_adres="select * from users_adres_$ref->{prefix} where id_pol='$ref_basket->{id_pol}'
                                 and id='$ref_basket->{id_adres}'";
                 my $sth2=$dbh->prepare($sel_adres);
         $sth2->execute;
                 my $ref_adres=$sth2->fetchrow_hashref||{};
             $sth2->finish;
                 my $fio='';
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{$ref_basket->{id_dostavka}};
      my $oplata=$oplata_rus;
        $oplata=$oplata_eng if $ref->{l} eq '2';
      my  $name_oplata=$oplata->{$ref_basket->{id_oplata}};
                 if($ref_adres->{id} ne ''){
                        $fio=qq[<b>$ref_adres->{fio}</b><br>
                        $ref_adres->{country},
                        $ref_adres->{post_index},
                         г.$ref_adres->{city},
                         ул.$ref_adres->{street},
                         д.$ref_adres->{home},
                         кв.$ref_adres->{place},
                         тел. $ref_adres->{phone}<br>
                ];
                }
                $fio.=qq[
                         <b>оплата:</b>$name_oplata <br>
                         <b>доставка:</b>$name_dostavka];

                 my $col_pokupok=$dbh->selectrow_array("select sum(col) from basket_$ref->{prefix} where id_zakaz='$ref_basket->{id_zakaz}'")||0;
                 my $cost=$dbh->selectrow_array("select sum(cost) from basket_$ref->{prefix} where id_zakaz='$ref_basket->{id_zakaz}'")||0;
                 my $skidka=$dbh->selectrow_array("select skidka from users_cat_$ref->{prefix} where id='$ref_basket->{id_pol}'")||0;
                        $cost=$cost-($cost*($skidka/100));
         $tpl->assign(
                                DATA    => $data_pr,
                                FIO    => $fio,
                                KOL    => $col_pokupok,
                                COST    => $cost,
                                CURENCY    => $curency,
                                SEL_STATUS    => $sel_status,
                ID_ZAKAZ      =>$ref_basket->{id_zakaz},
                ID_USER      =>$ref_basket->{id_pol},
                SID     =>$ref->{sid},
                LANG    =>$ref->{l},
                ID      =>$ref->{id},
         );
         $tpl->parse("ROW_CAT_BASKET",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/catalog.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&a=orders&status=$ref->{status}&slovo=$ref->{slovo}&id_user=$ref->{id_user}";
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

sub update_order {
 my $ref=shift;
 my $time=time;
 if($ref->{del_order}){
 my @ar_id_del_zakaz=CGI::param('id_del_zakaz');
 my $str_id_zakaz='';
 my $dop=qq[id_zakaz='$ar_id_del_zakaz[0]'];
 if($#ar_id_del_zakaz>0){
 $str_id_zakaz=join(',',@ar_id_del_zakaz);
 $str_id_zakaz=~s/\,$//gi;
 $str_id_zakaz=~s/\,/\'\,\'/gi;
 $str_id_zakaz="'$str_id_zakaz'";
 $dop=qq[id_zakaz in ($str_id_zakaz)];
 }
 my $dbh=dbconnect;
 my $del=$dbh->do("delete from basket_$ref->{prefix} where $dop");
#print qq[delete from basket_$ref->{prefix} where $dop = $del];exit;
 dbdisconnect($dbh);
 }elsif($ref->{update_status}){
 my @ar_sel_status=CGI::param('sel_status');
 my @ar_id_zakaz=CGI::param('id_zakaz');
#print qq[@ar_sel_status <br> @ar_id_zakaz];exit;
 my $dbh=dbconnect;
 for (my $i=0;$i<=$#ar_id_zakaz;$i++){
 my $upd="update basket_$ref->{prefix} set status='$ar_sel_status[$i]' where id_zakaz='$ar_id_zakaz[$i]'";
 my $sth=$dbh->prepare($upd);
    $sth->execute;
 }
 dbdisconnect($dbh);
 }
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=19&$time"</script>
  </body>
  </HTML>
 ];
  exit;

}

sub view_order { #Вывод заказа
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  
            "main"=>"/constructor_cat_view_order.html.$ref->{l}",
            "row"=>"/constructor_cat_view_order_row.html.$ref->{l}",
              };
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $title=slovo(41,$ref->{l}); #Вывод заказа

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dbh=dbconnect;
 my $sel="select * from basket_$ref->{prefix} where id_zakaz='$ref->{id_zakaz}'";
 my $sth=$dbh->prepare($sel);
  $sth->execute;
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $curency=$user_db->{data}->{$ref->{id}}->{params}->{curency}||'$';
          my $sel_u="select * from users_cat_$ref->{prefix} where id='$ref->{id_user}'";
          my $sth3=$dbh->prepare($sel_u);
                 $sth3->execute;
          my $ref_user=$sth3->fetchrow_hashref||{};
                 $sth3->finish;
 my $skidka=$ref_user->{skidka}||'0';
 my $all_cost=0;
 my $id_dostavka='';
 my $id_oplata='';
 my $id_user='';
 my $id_adres='';
    while(my $ref_basket=$sth->fetchrow_hashref){
             my ($data,$hour)=split / /,$ref_basket->{data_reg};
             my ($y,$m,$d)=split /\-/,$data;
                 my $data_pr="$d.$m.$y";
                 my $ref_catalog=$dbh->selectrow_hashref("select * from $ref->{db_prefix}_catalog where id='$ref_basket->{id_cat}'")||{};
         my $cost=($ref_catalog->{cost}*$ref_basket->{col})-(($ref_catalog->{cost}*$ref_basket->{col})*$skidka/100);
         $tpl->assign(
                DATA    => $data_pr,
                NAME    => $ref_catalog->{name},
                COST    => $cost,
                COL     => $ref_basket->{col},
                CURENCY => $curency,
                SID     =>$ref->{sid},
                LANG    =>$ref->{l},
                ID      =>$ref_catalog->{id},
                IDR      =>$ref_catalog->{idr},
                DOMEN      =>$ref->{user_doman},
                ID_ZAKAZ=>$ref->{id_zakaz},
         );
         $tpl->parse("ROW_CAT_BASKET",".row");
         $tpl->clear_href(1);
        $all_cost+=$cost;
        $id_user=$ref_basket->{id_pol};
        $id_adres=$ref_basket->{id_adres};
        $id_dostavka=$ref_basket->{id_dostavka};
        $id_oplata=$ref_basket->{id_oplata};
    }
    $sth->finish;
                 my $sel_adres="select * from users_adres_$ref->{prefix} where id_pol='$id_user'
                                 and id='$id_adres'";
                 my $sth2=$dbh->prepare($sel_adres);
         $sth2->execute;
                 my $ref_adres=$sth2->fetchrow_hashref||{};
             $sth2->finish;
                 my $fio=''; my $phone='';my $dop='';
                 if($ref_adres->{id}){
                        $fio=qq[<b>$ref_adres->{fio}</b><br>
                        $ref_adres->{country},<br>
                        $ref_adres->{post_index},
                         г.$ref_adres->{city},<br>
                         ул.$ref_adres->{street},
                         д.$ref_adres->{home},
                         кв.$ref_adres->{place}
                ];
                 $phone=$ref_adres->{phone};
                 $dop=$ref_adres->{dop}
                }else{
                $fio=''
                }
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{$id_dostavka};
      my $oplata=$oplata_rus;
        $oplata=$oplata_eng if $ref->{l} eq '2';
      my  $name_oplata=$oplata->{$id_oplata};
          my $fio_u=qq[$ref_user->{l_name} $ref_user->{name} $ref_user->{f_name}];
         $tpl->assign(
                                ADRES    => $fio,
                                EMAIL_U    => $ref_user->{email},
                                FIO_U    => $fio_u,
                                ALL_COST => $all_cost,
                                CURENCY  => $curency,
                                SKIDKA  => $skidka,
                                DOSTAVKA => $name_dostavka,
                                OPLATA   => $name_oplata,
                                PHONE   => $phone,
                                DOP   => $dop,
                SID      =>$ref->{sid},
                LANG     =>$ref->{l},
                ID       =>$ref->{id},
         );
 dbdisconnect($dbh);

# $tpl->parse(TEXT => "text");
# $tpl->clear_href(1);
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
            if(length($name)>20){
           $name=substr($name,0,20)."...";
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
sub print_razdel_cat_2 {
    my $ref=shift;
    my $sel="select * from structure where module='catalog'";
    my $sth=$ref->{dbh}->prepare($sel);
       $sth->execute();
    my $str="";
    while(my $ref_s=$sth->fetchrow_hashref){
        $str.=qq[<option value="$ref_s->{id}">$ref_s->{name}];
    }
    $sth->finish;
return $str;
}