#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с гостевой книгой
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;

 #!!!Проверка sid пользователя!!!#
 $ref->{sid}=time;
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
 $ref->{prefix}=$ref->{prefix}."_" if $ref->{prefix};
 my $create_guest=qq[
CREATE TABLE `$ref->{prefix}guest` (
  `id` int(11) NOT NULL auto_increment,
  `idu` int(11) NOT NULL default '0',
  `id_article` int(11) NOT NULL default '0',
  `idr` varchar(25) NOT NULL default '0',
  `data_reg` datetime NOT NULL default '0000-00-00 00:00:00',
  `name` varchar(255) NOT NULL default '',
  `email` varchar(100) NOT NULL default '',
  `subject` varchar(255) NOT NULL default '',
  `record` text NOT NULL,
  `ip` varchar(15) NOT NULL default '',
  `answer` text,
  PRIMARY KEY  (`id`),
  KEY `idu` (`idu`),
  KEY `idr` (`idr`)
) 
];      
my $dbh=dbconnect;

if(!table_exists(qq[`$ref->{prefix}guest`])){
 my $guest=$dbh->do($create_guest);
}
&dbdisconnect($dbh);
if ($ref->{a} eq ''){list_guest($ref)} #Выводим все записи гостевой книги для этого раздела
if ($ref->{a} eq 'edit_st'){edit_st($ref)} #Выводим форму редактирования шапки гостевой
if ($ref->{a} eq 'save'){save_st($ref)} #Сохраняем шапку гостевой
if ($ref->{a} eq 'change_col'){change_col($ref)} #Изменяем кол-во выводимых записей на странице
if ($ref->{a} eq 'block_list'){block_list($ref)} #Изменяем кол-во выводимых записей на странице
if ($ref->{a} eq 'answer'){answer($ref)} #Изменяем кол-во выводимых записей на странице
if ($ref->{a} eq 'del'){del($ref)} #Удаляем информацию
if ($ref->{a} eq 'del_all'){del($ref)} #Удаляем всю информацию

sub edit_st {
my $ref=shift;
      my $def={  "main"=>"/constructor_document_editor_main.html.$ref->{l}",
                 "text"=>"/constructor_editor_guest.html.$ref->{l}",
             };
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';

 my $title=slovo(20,$ref->{l})." $name_r - "; #Гоствеая :: Редактируем шапку

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
location.href="$ref->{referrer}&mes=$pr_mes&$time"
</script>
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


sub list_guest {
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_guest.html.$ref->{l}",
            "row"=>"/constructor_guest_row.html.$ref->{l}" 
              };

# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $col_records=$user_db->{data}->{$ref->{id}}->{params}->{col_records}||10;
 my $block_ip=$user_db->{data}->{$ref->{id}}->{params}->{block_ip}||'';
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $my_email=$user_db->{data}->{$ref->{id}}->{params}->{email}||'';

 my $title=slovo(21,$ref->{l})." $name_r -"; #Гостевая книга 

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
# $tpl=user_menu($ref,$tpl);


  $tpl->assign(
             EMAIL_OWNER=>$my_email,
             COL_RECORDS=>$col_records,
             BLOCK_IP=>$block_ip,
             MESSAGE=>$mes,
             IDR_GUEST=>$ref->{id},
             PAGEIN=>$ref->{PageIn},
             PN=>$ref->{p_n}
   );
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=15;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from $ref->{prefix}guest where idu='7' and idr='$ref->{id}'";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам

 my $sel="select * from $ref->{prefix}guest where idu='7' and idr='$ref->{id}' order by data_reg desc limit $off,$CountPage";

 my $sth=$dbh->prepare($sel);
    $sth->execute;
    while(my $ref_guest=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_guest->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day/$month/$year $hour:$min";
         $tpl->assign(
                DATA  =>$data_print,
                ID    =>$ref_guest->{id},
                IDR   =>$ref_guest->{idr},
                NAME   =>$ref_guest->{name},
                EMAIL =>$ref_guest->{email},
                SUBJECT =>$ref_guest->{subject},
                RECORD =>$ref_guest->{record},
                IP =>$ref_guest->{ip},
                ANSWER =>$ref_guest->{answer},
                PAGEIN=>$ref->{PageIn},
                PN=>$ref->{p_n}
         );
         $tpl->parse("ROW_GUEST",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
    dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/guest.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}";
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

sub del {
 my $ref=shift;
 my $dbh=dbconnect;
 if ($ref->{a} eq 'del_all'){
   my $del=$dbh->do("delete from $ref->{prefix}guest");
}
 else{
	my $del=$dbh->do("delete from $ref->{prefix}guest where id='$ref->{id}' and idu='7' and idr='$ref->{idr}'");
}
    dbdisconnect($dbh);
  #  use Storable;
  # my $user_db = retrieve $ref->{path_db};
  my $user_db=$ref->{user_db};
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
#    my $save_index=`$path/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi $ar_sort_key[0] $ref->{path_db} $ref->{path_host} $ref->{path_template} $ref->{user}->{id}`;
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $pr_mes='19';
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
 #  use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $pr_mes='19';
 if($ref->{save} eq 'ok'){
  if($ref->{col_records}=~/^\d+$/&&$ref->{col_records}<100){
      $user_db->{data}->{$ref->{id}}->{params}->{col_records}=$ref->{col_records};
      #store $user_db,  $ref->{path_db};
  }
      $user_db->{data}->{$ref->{id}}->{params}->{email}=$ref->{email_owner};
      my $kind='params';
      &store_db($user_db,  $ref->{id},$kind);
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
sub block_list {

 my $ref=shift;
 #use Storable;
 #my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $pr_mes='19';
 if($ref->{save} eq 'ok'){
  if(length($ref->{block_ip})<100){
    $ref->{block_ip}=~s/^\s+|\s+$//gi;
    $ref->{block_ip}=~s/\s+/ /gi;
    $ref->{block_ip}=~tr/\|/ /;
    $user_db->{data}->{$ref->{id}}->{params}->{block_ip}=$ref->{block_ip};
    my $kind='params';
    &store_db( $user_db,  $ref->{id},$kind);
#    my $params=join(',',$user_db->{data}->{$ref->{id}}->{params});
#   my $dbh=&dbconnect;
#      $dbh->do("update structure set params='$params' where id='$ref->{id}'");
#      dbdisconnect($dbh);
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

sub answer {
 my $ref=shift;
    $ref->{zag}=~tr/'/"/; #"'
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $pr_mes='19';
 if($ref->{save} eq 'ok'){
   my $dbh=dbconnect;
   if($ref->{id}){
    my $upd=$dbh->prepare("update guest set answer=? where id=? and idu=? and idr=?");
    $upd->execute($ref->{answer},$ref->{id},$ref->{user}->{id},$ref->{idr});
    $upd->finish;
   }
   dbdisconnect($dbh);
  }

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

