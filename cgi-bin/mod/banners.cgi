#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с новостями сайта
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
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
CREATE TABLE IF NOT EXISTS `banners` (
  `id` int(10) NOT NULL auto_increment,
  `link` varchar(255) collate cp1251_bin NOT NULL default '',
  `file` varchar(255) collate cp1251_bin NOT NULL default '',
  `place` int(11) default '1',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin AUTO_INCREMENT=1 
];      
my $dbh=dbconnect;
my $col=$dbh->selectrow_array("select count(*) from banners");
if($col<=0){
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
 use Storable;
 my $user_db = retrieve $ref->{path_db};
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
 use Storable;
 my $user_db = retrieve $ref->{path_db};
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
            "text"=>"/constructor_banners.html.$ref->{l}",
            "row"=>"/constructor_banners_row.html.$ref->{l}" 
              };

my $user_db=$ref->{user_db};
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
             IDR_NEWS=>'banners',
             PAGEIN=>$ref->{PageIn},
             PN=>$ref->{p_n}
   );
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=10;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from banners";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
 my $sel="select * from banners  order by id desc limit $off,$CountPage";

 my $sth=$dbh->prepare($sel);
    $sth->execute;
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day/$month/$year $hour:$min";
         $tpl->assign(
                MOD	=>$user_db->{data}->{$ref->{id}}->{mod},
		PLACE	=>$ref_news->{place},
                DATA 	 =>$data_print,
                ID   	=>$ref_news->{id},
                IDR  	 =>'banners',
                ZAG  	 =>"Баннер № $ref_news->{id}",
                SHORT 	=>$ref_news->{short},
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
            "text"=>"/constructor_banners_add.html.$ref->{l}"
              };



 my $dbh=dbconnect;
 my $sel="select * from banners where id='$ref->{id}'";
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
my $banner=qq[];
if ($ref_news->{file}){$banner=qq[<img src="/base/banners/$ref_news->{file}">]};
my ($year,$month,$day,$hour,$min,$sec);
    if($ref_news->{data_reg}){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         ($year,$month,$day)=split /-/,$data;
         ($hour,$min,$sec)=split/:/,$time;
    } else {
     ($year,$month,$day,$hour,$min,$sec)=&get_data;
    }
    my $place=qq[
	<select name="place">
	<option value="1">Блок слева
	<option value="2">Блок сверху
	<option value="3">Блок справа
	<option value="4">Блок снизу
	</select>
    ];
    $place=~s/value=\"$ref_news->{place}\"/value=\"$ref_news->{place}\" selected/gi;
    $tpl->assign (
        MOD=>$ref->{user_db}->{data}->{banners}->{mod},
        NAME_ST=>$name_news,
        ID=>$ref_news->{id},
        IDR=>'banners',
        LINK=>$ref_news->{link},
        FILE=>$ref_news->{file},
        PLACE=>$place,
        BANNER=>$banner,
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

my $user_db=$ref->{user_db};
 my $mod_razdel=$user_db->{data}->{$ref->{idr}}->{mod}||'';
 my $pr_mes='19';
 my $upfile=$ref->{upfile};

my $file='';
 if($upfile ne ''){

  if($ref->{save} eq 'ok'){
      my @ar1=split /\\/,$upfile;
      $file=$ar1[$#ar1];
      my $fold=$file;
         $file=~s/\s+//gi;
      $file=~tr/ ИЖСЙЕМЦЬЫГУЗТШБЮОПНКДФЩЪВЯЛХРЭАЧёижсйемцьыгузтшбюопнкдфщъвялхрэачЁ/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
      my @ar2=split /\./,$file;
      my $nmf=$ar2[0];
      my $typef=$ar2[1];
      $nmf=substr $nmf,0,25;
      $file="$nmf.$typef";
                if(!-d "$ref->{path_host}/banners"){
                  mkdir_("$ref->{path_host}/banners");
                }
        my ($buf);

         open A, "+>$ref->{path_host}/banners/$file";
         binmode(A);
         while (my $bytesread = read($upfile, $buf, 1024)) {
         print A $buf;
          }
        chmod 0644, "$ref->{path_host}/banners/$file";
        close A;
        }      
      };

if($ref->{save} eq 'ok'){
   my $dbh=dbconnect;
 if($ref->{id}){
   my $sql="update banners set link=?,file=?,place=? where id=? ";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{link},$ref->{file},$ref->{place},$ref->{id});
   $sth->finish;
 }else{
   my $sql="insert into banners (link, file,place) values (?,?,?)";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{link},$file,$ref->{place});
   $sth->finish;
 }
 dbdisconnect($dbh);
};
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
location.href="/cgi-bin/mod/banners.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{idr}&mes=$pr_mes"
</script>
</body>
</html>
];
  exit;
}

sub del {
 my $ref=shift;
 my $dbh=dbconnect;
 my $del=$dbh->do("delete from banners where id='$ref->{id}'");
    dbdisconnect($dbh);
my $pr_mes=19;
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;

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

my $user_db=$ref->{user_db};

my $pr_mes='19';
if($ref->{save} eq 'ok'){
 if($ref->{col_records}=~/^\d+$/&&$ref->{col_records}<100){
    $user_db->{data}->{$ref->{id}}->{params}->{col_records}=$ref->{col_records};
    store $user_db,  $ref->{path_db};
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
