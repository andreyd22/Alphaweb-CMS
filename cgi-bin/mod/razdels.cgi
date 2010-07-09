#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с разделами сайта
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
# my $ref=Get_Param;
 my $ref=Get_Param;
 $ref->{sid}=time;
#    $ref->{prefix}=$ref->{user_doman};
#    $ref->{prefix}=~s/\-|\./_/gi;

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

#!!!Проверка прав доступа!!!#
 $ref->{who}='add_razdel';
 &check_status($ref);
 &check_access($ref);
#!!!Проверка прав доступа end !!!#

#Объявляем счетчики для рекурсивного постоения разделов
  my $i=1;
  my $j=1;
  my $o=1;
  my $p=1;
if ($ref->{a} eq 'add'){add_form($ref)} #Форма добавления/редактирования раздела
if ($ref->{a} eq 'save'){save($ref)} #Добавляем новый раздел
if ($ref->{a} eq 'del'){del($ref)} #Удаляем разделы по одному
if ($ref->{a} eq 'porjadok'){porjadok($ref)} #Выводим разделы для последующей сортировки
if ($ref->{a} eq 'view_sort'){view_sort($ref)} #Сортируем разделы
if ($ref->{a} eq 'change_parent'){change_parent($ref)} #Меняем родителя
if ($ref->{a} eq 'change_sort'){change_sort($ref)} #Меняем сортировку

sub add_form {
my $ref=shift;
$ref->{id_old}=$ref->{id};
$ref->{id}=time if !$ref->{id};
      my $def={  "main"=>"/constructor.html.$ref->{l}",
                 "text"=>"/constructor_add_razdel.html.$ref->{l}",
                 "visible"=>"/constructor_check_visible.html.$ref->{l}",
                 "option"=>"/constructor_option_mod.html.$ref->{l}",
                 "option_tpl"=>"/constructor_option_mod.html.$ref->{l}",
                 "option_lang_tpl"=>"/constructor_option_mod.html.$ref->{l}",
                 "row2"=>"/constructor_razdels_option.html.$ref->{l}" 
              };

# use Storable;
# my $user_db = retrieve $ref->{path_db}||{};
 $ref=get_structure($ref);
 my $user_db=$ref->{user_db};
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'Новый раздел';
 my $title=slovo(24,$ref->{l})."$name_r "; #Свойства раздела 
#use Data::Dumper;
#print Dumper($user_db->{data}->{$ref->{id}}->{index_ini});
 if(!$ref->{idp}){ $ref->{idp}=$user_db->{data}->{parent}->{$ref->{id}} || '0'; }
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $link_path="";
  my $id_sub_menu=$ref->{idp};
 if($ref->{idp}){
  #Для разделов 2-го уровня рекурсивно ищем главный раздел
  A:
  $ref->{all_id}.=" $id_sub_menu";
  if ($ref->{user_db}->{data}->{parent}->{$id_sub_menu} ne '0' && $ref->{user_db}->{data}->{parent}->{$id_sub_menu} ne '')
    {$id_sub_menu=$ref->{user_db}->{data}->{parent}->{$id_sub_menu}; goto A; }

 my $link_pt=$ref->{all_id};
    $link_pt=~s/^\s+|\s+$//gi;
 my @ar_link_path=split / /, $link_pt;
    for(my $i=$#ar_link_path;$i>=0;$i--){
        my $pr_link="/$ar_link_path[$i].html";
        if ($ref->{user_db}->{data}->{$ar_link_path[$i]}->{link}){$pr_link=$ref->{user_db}->{data}->{$ar_link_path[$i]}->{link};}
        my $name_link=$ref->{user_db}->{data}->{$ar_link_path[$i]}->{name};
        if($ar_link_path[$i] ne $ref->{id}){
        $link_path.=qq[/ <a href="$pr_link" target=_blank>$name_link</a> ];
        }else{
        $link_path.=qq[/ <b>$name_link</b> ];
        }
    }
#    $link_path=~s/^\///gi;
 }
$tpl->assign(
    LINK_PATH=>$link_path
);
#Выбираем где показывать данный раздел
 foreach my $key (keys(%visible)){
   $tpl->assign(
         CHECK_VISIBLE_NAME=>$key,
         VISIBLE_NAME=>$visible{$key}->[$ref->{l}-1]
   );
   if($user_db->{data}->{$ref->{id}}->{visible}){
    if($user_db->{data}->{$ref->{id}}->{visible}->{$key}==1){
           $tpl->assign(
                 CHECKED_VISIBLE=>"checked"
           );
    }else{
           $tpl->assign(
                 CHECKED_VISIBLE=>""
            );
        }
   }else{
           $tpl->assign(
                 CHECKED_VISIBLE=>"checked"
           );
   }
   $tpl->parse("CHECK_VISIBLE",".visible");
   $tpl->clear_href(1);
 }
#Выбираем какой тип раздела раздел 
 my $mods=$user_db->{mods}||{};
 my %mods=%$mods;
 my $sel;
 if($user_db->{data}->{$ref->{id}}->{mod}){ #Проверяем к какому типу уже прикреплен данный раздел
   $sel=$user_db->{data}->{$ref->{id}}->{mod};
 }
 else{
   $sel="document";
 }

 foreach my $key (keys(%mods)){ #Проходим по хешу всех модулей
   my $key1=$key;
   $key1=~s/\.cgi$//gi;
   $tpl->assign(
         OPTION_VALUE=>$key1,
         OPTION_NAME=>$mods{$key}->[$ref->{l}-1]
   );
   if($key1 eq $sel){
           $tpl->assign(
                 SELECTED=>"selected"
           );
   }else{
           $tpl->assign(
                 SELECTED=>""
           );
   }
   $tpl->parse("OPTION_MOD",".option");
   $tpl->clear_href(1);
 }
#Ставим скрипт говорящий что смена раздела приведет к потере всех данных в разделе
 if($user_db->{data}->{$ref->{id}}->{mod}){
    $tpl->assign(
       CONFIRM=>qq[onChange="return Delete('3','')"]
    );
 }

#Выбираем на какие разделы выводить ссылки при выводе раздела
 my $sel_view;
 if($user_db->{data}->{$ref->{id}}->{link_view}){
   $sel_view=$user_db->{data}->{$ref->{id}}->{link_view};
 } else{   $sel_view="child"; }

 foreach my $key (keys(%link_view)){
   my $key1=$key;
   $key1=~s/\.cgi$//gi;
   $tpl->assign(
         OPTION_VALUE=>$key1,
         OPTION_NAME=>$link_view{$key}->[$ref->{l}-1]
   );
   if($key1 eq $sel_view){
           $tpl->assign(
                 SELECTED=>"selected"
           );
   }else{
           $tpl->assign(
                 SELECTED=>""
           );
   }
   $tpl->parse("OPTION_LINK",".option");
   $tpl->clear_href(1);
 }
#какие ссылки выводить конец

#Выбираем шаблон раздела
 my $sel_tpl;
 if($user_db->{data}->{$ref->{id}}->{index_ini}){$sel_tpl=$user_db->{data}->{$ref->{id}}->{index_ini};}
 else{ $sel_tpl="index.tpl"; }

 opendir DIR,$ref->{path_template} or die $!;
 my @ar_files=readdir(DIR);
 close DIR;
# print @ar_files;
 my @ini_files=();
 for (my $i=0;$i<=$#ar_files;$i++){
   if($ar_files[$i]=~/index(.+?)\.ini/gi||$ar_files[$i]=~/index\.ini/gi){
#    $ar_files[$i]=~s/\.ini//gi;
   push @ini_files,$ar_files[$i];
   }
 }
# print @ini_files;
 my $opis_alias='';
 for(my $j=0;$j<=$#ini_files;$j++){
   open A, "$ref->{path_template}/$ini_files[$j]";
   my $ar_str=<A>;
   close A;
   chomp($ar_str);
   my ($alias,$name,$opis,$opis2,$status)=split /\=/,$ar_str;
       $opis=$opis2 if $ref->{l}==2;
   $tpl->assign(
         OPTION_VALUE=>$name,
         OPTION_NAME=>$opis
   );
   if($name =~ /$sel_tpl/){
           $tpl->assign(
                 SELECTED=>"selected"
           );
   }else{
           $tpl->assign(
                 SELECTED=>""
           );
   }
   $tpl->parse("OPTION_LINK_TPL",".option_tpl");
   $tpl->clear_href(1);

 }

#Выбираем язык раздела
 my $sel_tpl;
 if($user_db->{data}->{$ref->{id}}->{lang}){$sel_tpl=$user_db->{data}->{$ref->{id}}->{lang};}
 else{$sel_tpl="ru"; }

 foreach my $key (keys(%lang_tpl)){
   $tpl->assign(
         OPTION_VALUE=>$key,
         OPTION_NAME=>$lang_tpl{$key}
   );
   if($key eq $sel_tpl){
           $tpl->assign(
                 SELECTED=>"selected"
           );
   }else{
           $tpl->assign(
                 SELECTED=>""
           );
   }
   $tpl->parse("OPTION_LANG_TPL",".option_lang_tpl");
   $tpl->clear_href(1);
 }

#какие ссылки выводить конец

#Ставим сотрировку равную time или же берем уже существующую, если раздел редактируется
 my $sort=time;
 if($user_db->{data}->{sort}->{$ref->{id}}){
   $sort=$user_db->{data}->{sort}->{$ref->{id}};
 }
#строим разделы для включений
 $ref->{user_db}=$user_db; #Складываем ссылку на хеш пользовательских данных в общую ссылку $ref
 for(my $inc=0;$inc<=4;$inc++){
  $ref->{user_db}->{data}->{$ref->{id}}->{include_col}->[$inc]='10' if !$ref->{user_db}->{data}->{$ref->{id}}->{include_col}->[$inc];
  $tpl->assign(
        "COL_INC$inc"=> $ref->{user_db}->{data}->{$ref->{id}}->{include_col}->[$inc],
        "NUM_INC$inc"=> $ref->{user_db}->{data}->{$ref->{id}}->{include_num}->[$inc],
  );
#  $tpl->clear_href(1);
   $i=1;
   $j=1;
   $o=1;
   $p=1;

  $tpl=print_razdels_include('0',$ref,$tpl,$inc); # выводим рекурсивно разделы в select
  $tpl->clear(1);

 }
#Выводим остальную информацию по разделу
$user_db->{data}->{$ref->{id}}->{name}=~s/"/'/gi; #'"
 my $select_admins=''; #Выбираем всех администраторов сайта для расстановке прав
 my $dbh=dbconnect();
 my $dop='';
    if(!$ref->{admin_ref}->{grant}){
      $dop="and id='$ref->{admin_ref}->{id}'";
    }
 my $sel="select * from admin_groups where status=1 $dop order by id asc";
 my $sth=$dbh->prepare($sel);
    $sth->execute();
    while(my $ref_admin=$sth->fetchrow_hashref){
     $select_admins.="<option value='$ref_admin->{login}'>$ref_admin->{name}"
    }
    $sth->finish;
    dbdisconnect($dbh);
    $select_admins=~s/\'$user_db->{data}->{$ref->{id}}->{access}\'/\'$user_db->{data}->{$ref->{id}}->{access}\' selected/gi;
 $tpl->assign(
    ADMIN_GROUPS => $select_admins,
    LINK=>$user_db->{data}->{$ref->{id}}->{link},
    NAME=>$user_db->{data}->{$ref->{id}}->{name},
    ZAG=>$user_db->{data}->{$ref->{id}}->{zag},
    KEYWORDS=>$user_db->{data}->{$ref->{id}}->{keywords},
    DESCRIPTION=>$user_db->{data}->{$ref->{id}}->{description},
    LANG=>$ref->{l},
    SORT=>$sort,
    ID=>$ref->{id},
    ID_OLD=>$ref->{id_old},
    IDP=>$ref->{idp}
 );
 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear();
}

sub save {#Сохраняем данные
 my $ref=shift;
 #use Storable;
 #my $user_db = retrieve  $ref->{path_db};
my $user_db=$ref->{user_db};

 if($user_db->{data}->{$ref->{id}}->{mod}){
   if($user_db->{data}->{$ref->{id}}->{mod} ne $ref->{mod}){
   my $del=del($ref);
  }
 }
$ref->{id}=~s/\s+//gi;
$ref->{id}=time if !$ref->{id};
$ref->{id}=~tr/&,='"`\|/-______/;
 $ref->{description}=~s/"/'/gi; #'"
 $ref->{keywords}=~s/"/'/gi; #'"
 $ref->{id}=~tr/ ИЖСЙЕМЦЬЫГУЗТШБЮОПНКДФЩЪВЯЛХРЭАЧёижсйемцьыгузтшбюопнкдфщъвялхрэачЁ/_qwertyuiop__asdfghjkl__zxcvbnm___qwertyuiop__asdfghjkl__zxcvbnm___/;
 if($ref->{id}!~/^[A-Za-z_0-9-]+$/){$ref->{id}=time}
my $dbh=dbconnect();
     my $sort_id=$dbh->selectrow_array("select sort_id from structure where id='$ref->{id_old}' and domain = '$ref->{host_name}'");	
     if (!$sort_id){
	$sort_id=$dbh->selectrow_array("select max(sort_id) from structure where parent='$ref->{idp}' and domain = '$ref->{host_name}'");
	$sort_id++;
     };	
#     

 if($ref->{id_old}&&($ref->{id_old} ne $ref->{id})){ #проверка на смену раздела (латинское название)

    $dbh->do("update structure set id='$ref->{id}' where id='$ref->{id_old}' and domain = '$ref->{host_name}'");
   if ($!){print qq[Такой раздел уже существует!<br><a href="location.history(-1);">BACK</a>];exit;}
   $dbh->do("update structure set parent='$ref->{id}' where parent='$ref->{id_old}' and domain = '$ref->{host_name}'");
# переименовываем user_db.$ref->{id}.* если такие есть
  #my $list;
  open A,"ls -a $ref->{path_to_db}/user_db.$ref->{id_old}.* |";
  my @ar_list = <A>;
 close A;
  #my @ar_list = split / /,$list;
  my $list =  join(//,@ar_list);

  for (my $i=0;$i<=$#ar_list;$i++){
    my $new_name = $ar_list[$i];

    $new_name =~ s/$ref->{id_old}/$ref->{id}/g;

   if (!-e"$new_name") {
	open OLD, "$ar_list[$i]";
	my @old = <OLD>;
	close OLD;
	open NEW, "+>$new_name";
	foreach (@old){print NEW $_;};
	close NEW;
	unlink $ar_list[$i];
   }else {print qq[Такой раздел уже существует!<br><a href="location.history(-1);">BACK</a>];exit;}
  }

  #print qq[id $ref->{id}:$ref->{user_db}->{data}->{$ref->{id}}->{mod}; $ref->{id_old} :$ref->{user_db}->{data}->{$ref->{id_old}}->{mod}; ];
  # Меняем таблицу формы
  if($ref->{user_db}->{data}->{$ref->{id_old}}->{mod} eq 'reg'){
	  my $dbh=dbconnect();
	  #print qq["RENAME TABLE `reg_$ref->{id_old}`  TO `reg_$ref->{id}`"];
	  #exit;
	  # переименовываем таблицу
	  $dbh->do("RENAME TABLE `reg_$ref->{id_old}`  TO `reg_$ref->{id}`");
	  #dbdisconnect($dbh);
  }

 } # сменили лат.название раздела

 if (($user_db->{data}->{parent}->{$ref->{id}}||$user_db->{data}->{parent}->{$ref->{id}} eq '0') && $user_db->{data}->{parent}->{$ref->{id}} ne $ref->{idp}){
    $ref->{idp}=$user_db->{data}->{parent}->{$ref->{id}};
 }
 $ref->{idp}||=0;$sort_id||=0;
   my $pr_mes='19';

my ($inc_id, $inc_col, $inc_num);

 for(my $pos=0;$pos<=4;$pos++){
	 $inc_id.=qq[|$ref->{"id_inc$pos"}];
	 $inc_col.=qq[|$ref->{"col_inc$pos"}];
	 $inc_num.=qq[|$ref->{"num_inc$pos"}];
 }

$inc_id=~s/^\|//;
$inc_col=~s/^\|//;
$inc_num=~s/^\|//;
 my $visible='';
 foreach my $key (keys(%visible)){
         $visible.=qq[$key=$ref->{$key},]
 }
$visible=~s/\,$//;


 if($ref->{save} eq 'ok'){
#     if ($ref->{mod} eq 'catalog'){cat_tree($ref);}
     my $sql='';
     my $ex=$dbh->selectrow_array("select count(*) from structure where id='$ref->{id}' and domain='$ref->{host_name}'");
     if ($ex<=0) {
	 $sql=qq[insert into structure (id,parent,name,zag,keywords,
			description,access,index_ini,lang,link,module,
			sort_id,link_view,include_id,include_col,include_num,
			visible,domain) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)];
	}
     else { $sql=qq[update structure set id=?,parent=?,name=?,zag=?,
			keywords=?,description=?,access=?,index_ini=?,
			lang=?,link=?,module=?,sort_id=?,link_view=?,include_id=?,
			include_col=?,include_num=?,visible=? where id='$ref->{id}' and domain=?];
	}   	
	my $sth=$dbh->prepare($sql);
	my$ok1=$sth->execute($ref->{id},$ref->{idp},$ref->{name},$ref->{zag},$ref->{keywords},$ref->{description},
					$ref->{admin_groups},$ref->{index_tpl},$ref->{lang_tpl},$ref->{link},$ref->{mod},
					$sort_id,$ref->{link_view},$inc_id, $inc_col,$inc_num,$visible,$ref->{host_name});
	
					
						$sth->finish;
   print qq[<center><b>сохранение прошло успешно</b></center>];

  }else{$pr_mes='20';print qq[сохранение не прошло];}
dbdisconnect($dbh);
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
my $mes1=slovo(32,$ref->{l});
my $mes2=slovo(33,$ref->{l});
#parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}"
print  qq[
  <HTML><head>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css">
  </head>
  <body>
  <script>parent.menu.location.href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time";
parent.load.location.href="/cgi-bin/view/$ref->{mod}.cgi?id=$ref->{id}&sid=$ref->{sid}"
</script>
  <br><br><center><a href="/cgi-bin/mod/$ref->{mod}.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&rnd=$time">
      $mes1  - <b>$ref->{name}</b></a>
        <br><br> <a href="/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{l}&a=add&id=$ref->{id}">&lt;&lt$mes2 - <b>$ref->{name}</b></a>
	          </center>
<!--/cgi-bin/view/$ref->{mod}.cgi?id=$ref->{id}&sid=$ref->{sid}-->
  </body>
  </HTML>
];
exit; #"
}
sub del {
 my $ref=shift;

 if(!$ref->{type}&&$ref->{a} eq 'del'){
 print qq[<center><b>Удаляется информация раздела "<b style="color:red">$ref->{user_db}->{data}->{$ref->{id}}->{name}</b> и связанных модулей" ?<br><br>
 При удалении раздела вся информация прикрепленного модуля будет также удалена </b>
<br><br><br>
 <a href="/cgi-bin/mod/razdels.cgi?a=del&id=$ref->{id}&type=del_ok">Да, удалить информацию раздела</a><br><br>
 <a href="javascript:history.go(-1)">Нет, я не хочу удалять раздел</a>
 </center>
 ]; exit;
 }
# print qq[$ref->{short_del}]; exit;
 $ref->{id_new}=$ref->{id};
 $ref=get_structure($ref);
 my $user_db = $ref->{user_db};

 my $data=$user_db->{data}||{};
 my $parent=$user_db->{data}->{parent}||{};
 my $sort=$user_db->{data}->{sort}||{};

 my %data=%$data;
 my %parent=%$parent;
 my %sort=%$sort;

 #if ($parent{$ref->{id}} eq '0' && $ref->{a} eq 'del'){
#print qq[
# <center><b>Вы попытались удалить главную страницу языковой версии сайта</b>, <br>
#  <b style="color:red">Действие было отменено</b></center>
# ];exit;
# }
my $dbh=&dbconnect;
my $count=$dbh->selectrow_array("select count(*) from structure where parent='$ref->{id}' and domain='$ref->{host_name}'");
dbdisconnect($dbh);
if($count>0 && $ref->{a} eq 'del'){
        #title 6
my $mes1=slovo(34,$ref->{l});
my $mes2=slovo(35,$ref->{l});
print qq[<script>alert('$mes1');
</script>
<center>$mes2 <b>$user_db->{data}->{$ref->{id}}->{name}</b><br>($mes1)</center>
];
exit;

}
   

 if ($ref->{a} eq 'del' && !$ref->{short_del}){ #производим удаление текстовой инфы только приявном удалении
  unlink "$ref->{path_db}.$ref->{id}.data"; #Удаляем основной документ
  unlink "$ref->{path_db}.$ref->{id}.data.2"; #это на случай если захотим сделать подвал (например в новостях или в гостевой или в каталоге)
 }elsif($ref->{id_old}&&$ref->{id_new}&&$ref->{id_old}ne$ref->{id_new}){
   use File::Copy;
   move("$ref->{path_db}.$ref->{id_old}.data","$ref->{path_db}.$ref->{id_new}.data");
   my $dbh=&dbconnect;
	my $sth=$dbh->prepare("update structure set parent='$ref->{id_new}' where parent='$ref->{id_old}' and domain='$ref->{host_name}'");
	$sth->execute;
	$sth->finish;
   dbdisconnect($dbh);	
 }
=t пока не будем удалять данные при удалении раздела
 if($data->{$ref->{id}}->{mod} eq 'news' &&!$ref->{short_del}){
  my $dbh=&dbconnect;
  my $del=$dbh->do("delete from news where idu='$ref->{user}->{id}' and idr='$ref->{id}'");
  dbdisconnect($dbh);
 }
 
 
 if($data->{$ref->{id}}->{mod} eq 'news' && $ref->{short_del} && $ref->{id_new} && $ref->{id_old}){
  my $dbh=&dbconnect;
  my $upd=$dbh->do("update news set idr='$ref->{id_new}' where idu='$ref->{user}->{id}' and idr='$ref->{id_old}'");
  dbdisconnect($dbh);
 }

 if($data->{$ref->{id}}->{mod} eq 'guest' &&!$ref->{short_del}){
  my $dbh=&dbconnect;
  my $del=$dbh->do("delete from guest where idu='$ref->{user}->{id}' and idr='$ref->{id}'");
  dbdisconnect($dbh);
 }
 if($data->{$ref->{id}}->{mod} eq 'guest' &&$ref->{short_del} && $ref->{id_new} && $ref->{id_old}){
  my $dbh=&dbconnect;
  my $upd=$dbh->do("delete guest set idr='$ref->{id_new}' where idu='$ref->{user}->{id}' and idr='$ref->{id_old}'");
  dbdisconnect($dbh);
 }

 if($data->{$ref->{id}}->{mod} eq 'catalog' &&!$ref->{short_del}){
  my $dbh=&dbconnect;
  my $sel="select * from cat_works where cw_predmet='$ref->{id}'";
  my $sth=$dbh->prepare($sel);
     $sth->execute();
     while(my $ref_cat=$sth->fetchrow_hashref){
       if (-e "$ref->{path_host}/cat_image/$ref->{id}-$ref_cat->{id}-s.jpg"){
         unlink "$ref->{path_host}/cat_image/$ref->{id}-$ref_cat->{id}-s.jpg";
         unlink "$ref->{path_host}/cat_image/$ref->{id}-$ref_cat->{id}.jpg";
       }
     }
     $sth->finish;
  my $del=$dbh->do("delete from cat_works where cw_predmet='$ref->{id}'");
  dbdisconnect($dbh);
 }
 if($data->{$ref->{id}}->{mod} eq 'catalog' &&$ref->{short_del} && $ref->{id_new} && $ref->{id_old}){
  my $dbh=&dbconnect;
  my $upd=$dbh->do("update cat_works set cw_predmet='$ref->{id_new}' where cw_predmet='$ref->{id_old}'");
  dbdisconnect($dbh);
 }

 if($data->{$ref->{id}}->{mod} eq 'gallery' &&!$ref->{short_del}){
  my $dbh=&dbconnect;
  my $sel="select * from gallery_$ref->{prefix} where idr='$ref->{id}'";
  my $sth=$dbh->prepare($sel);
  my $col=$sth->execute();
     while(my $ref_cat=$sth->fetchrow_hashref){
       if (-e "$ref->{path_host}/gallery_image/$ref->{id}-$ref_cat->{id}-s.jpg"){
         unlink "$ref->{path_host}/gallery_image/$ref->{id}-$ref_cat->{id}-s.jpg";
         unlink "$ref->{path_host}/gallery_image/$ref->{id}-$ref_cat->{id}.jpg";
       }
     }
     $sth->finish;
  my $del=$dbh->do("delete from gallery_$ref->{prefix} where idr='$ref->{id}'");
  dbdisconnect($dbh);
 }
 if($data->{$ref->{id}}->{mod} eq 'gallery' && $ref->{short_del} && $ref->{id_new} && $ref->{id_old}){
  my $dbh=&dbconnect;
  my $upd=$dbh->do("update gallery_$ref->{prefix} set idr='$ref->{id_new}' where idu='$ref->{user}->{id}' and idr='$ref->{id_old}'");
  dbdisconnect($dbh);
 }
=cut
 # Меняем таблицу формы
 if($data->{$ref->{id}}->{mod} eq 'reg' && !$ref->{short_del}){
  my $dbh=&dbconnect;
  # переименовываем таблицу
  #my $upd=$dbh->do("RENAME TABLE `reg_$ref->{id_old}`  TO `reg_$ref->{id_new}`");

  # При изменении типа все таки удаляем таблицу
  my $del=$dbh->do("drop table `reg_$ref->{id}`");
  dbdisconnect($dbh);
 }


if(!$ref->{short_del}){
my $dbh=&dbconnect;
$dbh->do("delete from structure where id='$ref->{id}' and domain = '$ref->{host_name}'");
dbdisconnect($dbh);
}else{
my $dbh=&dbconnect;
$dbh->do("delete from structure where id='$ref->{id_old}' and domain = '$ref->{host_name}'");
dbdisconnect($dbh);
}

 if($ref->{a} eq 'del'){
my $mes1=slovo(36,$ref->{l});
print qq[
  <HTML><HEAD></HEAD>
  <body>
  <script>parent.menu.location.href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}";
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ref->{id}}->{mod}.cgi?id=$ref->{id}&sid=$ref->{sid}";
</script>
  <center>$mes1</center>
  </body>
  </HTML>
];
 }else{1}
}

#"

sub porjadok {
 my $ref=shift;
      my $def={  "main"=>"/constructor.html.$ref->{l}",
                 "text"=>"/constructor_razdels_change.html.$ref->{l}",
                 "row"=>"/constructor_razdels_row.html.$ref->{l}" 
              };
 my $title=slovo(25,$ref->{l}); #Сортировка разделов 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

# use Storable;
# my $user_db = retrieve $ref->{path_db};
# $ref->{user_db}=$user_db; #Складываем ссылку на хеш пользовательских данных в общую ссылку $ref

 $ref=get_structure($ref);

 $tpl=print_razdels1('0',$ref,$tpl); #Строим рекурсивно меню разделов


 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear();
}

sub print_razdels1 { #строим дерево разделов для сортировки
    my $id_p=shift;
    my $ref=shift;
    my $tpl=shift;
    if(!$id_p){$id_p='0';}

    #my $parent=$ref->{user_db}->{data}->{parent}||{};

    #my %parent=%$parent;

    my $y=0;
my $dbh=dbconnect;

my $ref_s=$dbh->selectall_arrayref("select id,sort_id,name,module,link from structure where parent='$id_p' and domain = '$ref->{host_name}' order by sort_id asc");

my @res_arr = map {@$_} @$ref_s;
#print join('<br>',@res_arr);
dbdisconnect($dbh);

foreach my $itm ( @$ref_s) {
        my $key=@{$itm}[0];
        my $name=@{$itm}[2];
        my $mod=@{$itm}[3];
        my $link=@{$itm}[4];

my $pr_link="/cgi-bin/mod/$mod.cgi?sid=$ref->{sid}&id=$key&l=$ref->{l}";
if ($link){$pr_link=$link;}
my $link = qq[
<table cellspacing=0 cellpadding=0>
<tr>
<td width=$i nowrap>&nbsp;</td><td>-<a href="$pr_link" class=link$j target=main>$name</a></td>
</tr>
</table>
];
        $tpl->assign(
                LINK=>$link,
                NAME_RAZDEL=>$name,
                LANG=>$ref->{l},
		SORT_ID=>@$itm[1],
                ID=>$key,
        );
        $tpl->parse("CONSTRUCTOR_MENU",".row");
        $tpl->clear_href(1);
        $i+=10;
        $j++;
        if($key ne ''){
        $tpl=print_razdels1($key,$ref,$tpl);
        }
        $i-=10;
        $j--;
      
      $y++;
    }
return $tpl;
}

sub sort_ { #сортируем раздел меняем сортировки между 2-мя соседними разделами
   my $ref=shift;
   my $pr_mes='19';
   # use Storable;
   # my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
   if($ref->{position}){
    my $sort=$user_db->{data}->{sort}||{};
    my %sort=%$sort;
       my $temp_1=$sort{$ref->{position}};
       my $temp_2=$sort{$ref->{id}};
          $sort{$ref->{position}}=$temp_2;
          $sort{$ref->{id}}=$temp_1;
    $sort=\%sort;
    $user_db->{data}->{sort}=$sort;
   if($ref->{save} eq 'ok'){
   &store_db( $user_db,  $ref->{id});
#   my $dbh=&dbconnect;
#      $dbh->do("update structure set sort_id='$sort' where id='$ref->{id}'");
#      dbdisconnect($dbh);
   }else{$pr_mes='20';}
  }
  $ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
   my $time=time;
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;

print qq[
  <HTML>
  <body>
  <script>parent.menu.location.href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time";
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=$pr_mes&rnd=$time"</script>
  </body>
  </HTML>
 ];
  exit;
} #"

sub view_sort {
 my $ref=shift;
 $ref->{idp}=0 if !$ref->{idp};
      my $def={  "main"=>"/constructor.html.$ref->{l}",
                 "text"=>"/constructor_razdels_change_parent.html.$ref->{l}",
                 "row"=>"/constructor_razdels_row.html.$ref->{l}" ,
                 "row2"=>"/constructor_razdels_option.html.$ref->{l}" 
              };
 my $title=slovo(26,$ref->{l}); #Переопределение родительского раздела
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 $ref=get_structure($ref);

# use Storable;
# my $user_db = retrieve $ref->{path_db};
# $ref->{user_db}=$user_db; #Складываем ссылку на хеш пользовательских данных в общую ссылку $ref

 $tpl->assign(
              NAME_R=>$ref->{user_db}->{data}->{$ref->{id}}->{name},
              ID_CHILED=>$ref->{id}
              );
 $tpl=print_razdels_parent1('0',$ref,$tpl); # выводим рекурсивно разделы в select
 $tpl=print_razdels1($ref->{id},$ref,$tpl); #Строим рекурсивно разделы, начиная с того который хотим переопределить

 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear();

}

sub print_razdels_parent { #строим дерево разделов для замены родительского раздела
    my $id_p=shift;
    my $ref=shift;
    my $tpl=shift;
    if(!$id_p){$id_p='0';}

    my $sort=$ref->{user_db}->{data}->{sort}||{};
    my $parent=$ref->{user_db}->{data}->{parent}||{};

    my %sort=%$sort;
    my %parent=%$parent;

    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    foreach my $key (@ar_sort_key){
        if($parent{$key} eq $id_p && $parent{$key} ne $ref->{id} &&$key ne $ref->{id}){
        my $select='';
        if($key eq $parent{$ref->{id}}){
        $select="selected";
        }
        my $nbsp='';
        for (my $t=0;$t<=$p;$t++){
          $nbsp.="&nbsp;";
        }
        $tpl->assign(
                SELECTED=>$select,
                OPTION_VALUE=>$key,
                OPTION_NAME=>$nbsp.$ref->{user_db}->{data}->{$key}->{name},
                LANG=>$ref->{l}
        );
        $tpl->parse("SELECT",".row2");
        $tpl->clear_href(1);
        $o+=10;
        $p++;
        if($key ne ''){
        $tpl=print_razdels_parent($key,$ref,$tpl);
        }
        $o-=10;
        $p--;
      }
    }
return $tpl;
}
sub print_razdels_parent1 { #строим дерево разделов для замены родительского раздела
    my $id_p=shift;
    my $ref=shift;
    my $tpl=shift;
    if(!$id_p){$id_p='0';}

    my $parent=$ref->{user_db}->{data}->{parent}||{};
    my %parent=%$parent;

my $dbh=dbconnect;
my $sth=$dbh->prepare("select * from structure where parent='$id_p' and domain = '$ref->{host_name}'");

#print qq[select * from structure where parent='$id_p'];

$sth->execute;
while(my $ref_s=$sth->fetchrow_hashref)
{       my $key=$ref_s->{id};

        my $select='';
        if($key eq $parent{$ref->{id}}){
        $select="selected";
        }
        my $nbsp='';
        for (my $t=0;$t<=$p;$t++){
          $nbsp.="&nbsp;";
        }
        $tpl->assign(
                SELECTED=>$select,
                OPTION_VALUE=>$key,
                OPTION_NAME=>$nbsp.$ref_s->{name},
                LANG=>$ref->{l}
        );
        $tpl->parse("SELECT",".row2");
        $tpl->clear_href(1);
        $o+=10;
        $p++;
        if($key ne ''){
        $tpl=print_razdels_parent1($key,$ref,$tpl);
        }
        $o-=10;
        $p--;
      }
dbdisconnect($dbh);   
return $tpl;
}

sub change_parent {

    my $ref=shift;
        my $pr_mes='19';
#    use Storable;
#    my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
 if(!$ref->{idp}){$ref->{idp}='0'};
    
 if($ref->{save} eq 'ok'){

my @ar_id=CGI::param('sort_id_id');
my @ar_sort=CGI::param('sort_id');
my $dbh=dbconnect();
   my $sql="update structure set parent=? where id=? and domain = '$ref->{host_name}'";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{idp},$ref->{id});
   $sth->finish;


for (my $i=0; $i<=$#ar_id; $i++)
{
   my $sql="update structure set sort_id=? where id=? and domain = '$ref->{host_name}'";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ar_sort[$i],$ar_id[$i]);
   $sth->finish;
};
dbdisconnect($dbh);

  } else {$pr_mes='20';}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
   my $sort=$user_db->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;

print qq[
  <HTML>
  <body>
  <script>parent.menu.location.href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time";
parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="/cgi-bin/mod/razdels.cgi?a=porjadok&sid=$ref->{sid}&l=$ref->{l}&mes=$pr_mes&rnd=$time"</script>
  </body>
  </HTML>
 ];
  exit;
}
sub change_sort {

    my $ref=shift;
        my $pr_mes='19';
#    use Storable;
#    my $user_db = retrieve $ref->{path_db};
   $ref=get_structure($ref);
   my $user_db=$ref->{user_db};
my @ar_id=CGI::param('sort_id_id');
my @ar_sort=CGI::param('sort_id');
my $dbh=dbconnect();
for (my $i=0; $i<=$#ar_id; $i++)
{
   my $sql="update structure set sort_id=? where id=? and domain = '$ref->{host_name}'";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ar_sort[$i],$ar_id[$i]);
   $sth->finish;
};
dbdisconnect($dbh);

my $time=time;
print qq[
  <HTML>
  <body>
  <script>parent.menu.location.href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}&rnd=$time";
parent.load.location.href="/cgi-bin/mod/razdels.cgi?a=porjadok&sid=$ref->{sid}&l=$ref->{l}&mes=$pr_mes&rnd=$time";
location.href="/cgi-bin/mod/razdels.cgi?a=porjadok&sid=$ref->{sid}&l=$ref->{l}&mes=$pr_mes&rnd=$time"</script>
  </body>
  </HTML>
 ];
  exit;
}
#parent.load.location.href="/cgi-bin/view/$user_db->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
#"
sub print_razdels_include { #строим дерево разделов для включений

    my $id_p=shift;
    my $ref=shift;
    my $tpl=shift;
    my $pos=shift;
    if(!$id_p){$id_p='0';}

    my $sort=$ref->{user_db}->{data}->{sort}||{};
    my $parent=$ref->{user_db}->{data}->{parent}||{};

    my %sort=%$sort;
    my %parent=%$parent;

    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    foreach my $key (@ar_sort_key){
        if($parent{$key} eq $id_p){
        my $select='';
        my $nbsp='';
        for (my $t=0;$t<=$p;$t++){
          $nbsp.="&nbsp;";
        }
       $ref->{user_db}->{data}->{$ref->{id}}->{include_id}->[$pos]='0' if !$ref->{user_db}->{data}->{$ref->{id}}->{include_id}->[$pos];
        if($key eq $ref->{user_db}->{data}->{$ref->{id}}->{include_id}->[$pos]){
         $select="selected";
        }
        $tpl->assign(
                OPTION_VALUE=>$key,
                OPTION_NAME=>$nbsp.$ref->{user_db}->{data}->{$key}->{name},
                LANG=>$ref->{l},
                SELECTED=>$select
                        );
         $tpl->parse("SELECT$pos",".row2");
         $tpl->clear_href(1);
       
      
        $o+=10;
        $p++;
        if($key ne ''){
        $tpl=print_razdels_include($key,$ref,$tpl,$pos);
        }
        $o-=10;
        $p--;
      }
    }
   
return $tpl;
}

