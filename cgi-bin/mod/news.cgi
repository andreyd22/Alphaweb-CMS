#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с новостями сайта
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;

 $ref=get_structure($ref);

 $ref->{sid}=time;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><title>authorization error</title></HEAD>
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
 my $create_news=qq[
CREATE TABLE `news` (
  `id` int(11) NOT NULL auto_increment,
  `idu` int(11) NULL default '0',
  `data_reg` datetime NULL default '0000-00-00 00:00:00',
  `zag` varchar(255) NOT NULL default '',
  `title` varchar(255) NULL default '',
  `description` varchar(255) NULL default '',
  `keywords` varchar(255) NULL default '',
  `short` text NOT NULL,
  `full_news` text NOT NULL,
  `idr` varchar(50) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `idr` (`idr`),
  KEY `idu` (`idu`)
)
];      
my $dbh=dbconnect;
#my $col=$dbh->selectrow_array("select count(*) from $ref->{prefix}news");
if(!table_exists(qq[`news`])){
 my $news=$dbh->do($create_news);
}
dbdisconnect($dbh);

if ($ref->{a} eq ''){list_news($ref)} #Выводим все новости (form insert new article)
if ($ref->{a} eq 'edit_st'){edit_st($ref)} #Выводим форму редактирования шапки новостей
if ($ref->{a} eq 'save'){save_st($ref)} #Сохраняем шапку новостей
if ($ref->{a} eq 'view'){view_news($ref)} #Выводим форму для редактирования новости (form insert new article)
if ($ref->{a} eq 'save_news'){save($ref)} #Сохраняем информацию
if ($ref->{a} eq 'del'){del($ref)} #Удаляем информацию
if ($ref->{a} eq 'change_col'){change_col($ref)} #Изменяем кол-во выводимых записей на странице

sub edit_st {
my $ref=shift;
      my $def={  "main"=>"/constructor_document_editor_main.html.$ref->{l}",
                 "text"=>"/constructor_editor_news.html.$ref->{l}",
             };
# use Storable;
#   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
# my $user_db = retrieve $ref->{path_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';

 my $title=slovo(22,$ref->{l})." $name_r - "; #Новости :: Редактируем шапку
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
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 if($ref->{save} eq 'ok'){
 open A, "+>$ref->{path_db}.$ref->{id}.data";
 print A $ref->{ta};
 close A;
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

sub list_news {
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_news.html.$ref->{l}",
            "row"=>"/constructor_news_row.html.$ref->{l}" 
              };

# use Storable;
 my $user_db =$ref->{user_db};
 my $col_records=$user_db->{data}->{$ref->{id}}->{params}->{col_records}||10;
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';

 my $title=slovo(23,$ref->{l})." :: $name_r -"; #Доступ разрешен 


 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
  $tpl->assign(
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             COL_RECORDS=>$col_records,
             MESSAGE=>$mes,
             IDR_NEWS=>$ref->{id},
             PAGEIN=>$ref->{PageIn},
             PN=>$ref->{p_n}
   );
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=10;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from news where idu='$ref->{user}->{id}' and idr='$ref->{id}'";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
 my $sel="select id,idr,data_reg,zag,short,full_news from news where idu='$ref->{user}->{id}' and idr='$ref->{id}' order by data_reg desc limit $off,$CountPage";

 my $sth=$dbh->prepare($sel);
    $sth->execute;
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day/$month/$year $hour:$min";
         $tpl->assign(
                MOD=>$user_db->{data}->{$ref->{id}}->{mod},
                DATA  =>$data_print,
                ID   =>$ref_news->{id},
                IDR   =>$ref_news->{idr},
                ZAG_NEWS   =>$ref_news->{zag},
                SHORT =>$ref_news->{short},
#                FULL_NEWS =>$ref_news->{full_news}
         );
         $tpl->parse("ROW_NEWS",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/news.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}";
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
sub view_news {
 my $ref=shift;
 my $def={  "main"=>"/constructor_document_editor_main.html.$ref->{l}",
            "text"=>"/constructor_news_add.html.$ref->{l}"
              };



 my $dbh=dbconnect;
 my $sel="select * from news where id='$ref->{id_news}' and idu='$ref->{user}->{id}' and idr='$ref->{idr}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_news=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 my $name_news=$ref_news->{zag};
 if(!$ref_news->{zag}){$name_news='New'}

 my $title=slovo(23,$ref->{l})." $name_news"; #Новости 

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

my ($year,$month,$day,$hour,$min,$sec);
    if($ref_news->{data_reg}){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         ($year,$month,$day)=split /-/,$data;
         ($hour,$min,$sec)=split/:/,$time;
    } else {
     ($year,$month,$day,$hour,$min,$sec)=&get_data;
    }

   $ref_news->{full_news}=~s/\n/ /gi;
   $ref_news->{full_news}=~s/\s+/ /gi;
   $ref_news->{full_news}=~s/'/"/gi; #'

   $ref_news->{short}=~s/\n/ /gi;
   $ref_news->{short}=~s/\s+/ /gi;
   $ref_news->{short}=~s/'/"/gi; #'

    $tpl->assign (
        MOD=>$ref->{user_db}->{data}->{$ref->{idr}}->{mod},
        NAME_ST=>$name_news,
        ID=>$ref->{idr},
        ID_NEWS=>$ref_news->{id},
        IDR=>$ref->{idr},
        ZAG_NEWS=>$ref_news->{zag},
        TITLE_NEWS=>$ref_news->{title},
        KEYWORDS_NEWS=>$ref_news->{keywords},
        DESCRIPTION_NEWS=>$ref_news->{description},
        DAY=>$day,
        MONTH=>$month,
        YEAR=>$year,
        MIN=>$min,
        SEC=>$sec,
        HOUR=>$hour,
        SHORT=>$ref_news->{short},
        FULL_NEWS=>$ref_news->{full_news},
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
sub save {
 my $ref=shift;
    $ref->{zag}=~tr/'/"/; #'

   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';
 my $pr_mes='19';
 if($mod_razdel eq 'news'){
   my $dbh=dbconnect;
 if($ref->{id_news}){
   my $sql="update news set title=?,keywords=?,description=?,zag=?,data_reg=?,short=?,full_news=? where id=? and idu=? and idr=?";
   my $sth=$dbh->prepare($sql);
   my $ok=$sth->execute($ref->{title},$ref->{keywords},$ref->{description},$ref->{zag},"$ref->{year}-$ref->{month}-$ref->{day} $ref->{hour}:$ref->{min}:$ref->{sec}",$ref->{short},$ref->{full_news},$ref->{id_news},$ref->{user}->{id},$ref->{id});
   $sth->finish;
    #print qq[$ref->{title},$ref->{keywords},$ref->{description},$ref->{zag},"$ref->{year}-$ref->{month}-$ref->{day} $ref->{hour}:$ref->{min}:$ref->{sec}",$ref->{short},$ref->{full_news},$ref->{id_news},$ref->{user}->{id},$ref->{id}]; exit;
 }else{
   my $sql="insert into news (title,keywords,description,zag,data_reg,short,full_news,idu,idr) values (?,?,?,?,?,?,?,?,?)";
   my $sth=$dbh->prepare($sql);
   my $ok = $sth->execute($ref->{title},$ref->{keywords},$ref->{description},$ref->{zag},"$ref->{year}-$ref->{month}-$ref->{day} $ref->{hour}:$ref->{min}:$ref->{sec}",$ref->{short},$ref->{full_news},$ref->{user}->{id},$ref->{id});
   $sth->finish;
 }

=r2 
 if($ref->{id_news}){
   my $sql="update $ref->{prefix}news set zag=?,data_reg=?,short=?,full_news=? where id=? and idu=? and idr=?";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{zag},"$ref->{year}-$ref->{month}-$ref->{day} $ref->{hour}:$ref->{min}:$ref->{sec}",$ref->{short},$ref->{full_news},$ref->{id_news},$ref->{user}->{id},$ref->{id});
   $sth->finish;
 }else{
   my $sql="insert into $ref->{prefix}news (zag,data_reg,short,full_news,idu,idr) values (?,?,?,?,?,?)";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{zag},"$ref->{year}-$ref->{month}-$ref->{day} $ref->{hour}:$ref->{min}:$ref->{sec}",$ref->{short},$ref->{full_news},$ref->{user}->{id},$ref->{id});
   $sth->finish;
 }
=cut

 dbdisconnect($dbh);
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
location.href="$ref->{referrer}&mes=$pr_mes&$time"
</script>
</body>
</html>
];
  exit;
}

sub del {
 my $ref=shift;
 my $dbh=dbconnect;
 my $del=$dbh->do("delete from news where id='$ref->{id_news}' and idu='$ref->{user}->{id}' and idr='$ref->{idr}'");
    dbdisconnect($dbh);
my $pr_mes=19;
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
#   use Storable;
#   my $user_db = retrieve $ref->{path_db};
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);
   my $user_db=$ref->{user_db};
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
my $time=time;
 print qq[
  <HTML>
  <body>
  <script>
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=$pr_mes&$time"
</script>
  </body>
  </HTML>
 ];
  exit;
}
sub change_col {
 my $ref=shift;
#use Storable;
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);
   my $user_db=$ref->{user_db};
my $pr_mes='19';
if($ref->{save} eq 'ok'){
 if($ref->{col_records}=~/^\d+$/&&$ref->{col_records}<100){
#	my $dbh=&dbconnect;
#	$dbh->do("update structure set params='col_records=$ref->{col_records}' where id='$ref->{id}'");
#	dbdisconnect($dbh);
    $user_db->{data}->{$ref->{id}}->{params}->{col_records}=$ref->{col_records};
    &store_db( $user_db, $ref->{id});
 }
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
