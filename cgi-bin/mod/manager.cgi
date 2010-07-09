#!/usr/bin/perl 
#!!!Менеджер пользователей системы
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
   print qq[
      <HTML><HEAD><title>authorization error</title></HEAD>
    <body>
    <script>parent.location.href="/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes"</script>
    </body>
    </HTML>
     ];
 exit;
 }
#!!!Проверка sid пользователя!!!#
if ($ref->{a} eq ''){list_users($ref)} #Выводим список пользователей-администраторов
if ($ref->{a} eq 'message'){message($ref)} #выдаем ошибки об нехватке прав доступа и т.п.
if ($ref->{a} eq 'view'){view_user($ref)} #Добавляем/редактируем пользователя (форма)
if ($ref->{a} eq 'save_user'){save_user($ref)} #сохранение данных пользователя
if ($ref->{a} eq 'del_user'){del_user($ref)} #Удаляем данные пользователя

sub list_users { #Вывод пользователей 
 my $ref=shift;
 my $mes='';
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_admin_groups.html.$ref->{l}",
            "row"=>"/constructor_admin_groups_row.html.$ref->{l}",
              };
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};

 my $title="Менеджер пользователей"; #Вывод пользователей

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

 my $dop="";
 if(!$ref->{admin_ref}->{grant}){$dop="and id='$ref->{admin_ref}->{id}'";}

 my $dbh=dbconnect;
 #для перехода по страницам
 my $CountPage=25;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from admin_groups where 1 $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from admin_groups where 1 $dop order by id asc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $mess='';
 $tpl->assign(
             MESSAGE=>$mess,
             MOD=>$user_db->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id},
             COUNT =>$count
   );
    while(my $ref_user=$sth->fetchrow_hashref){
         my $add_razdel='no'; my $edit_design='no'; my $grant='no'; my $status='inactive';
         if($ref_user->{add_razdel}){$add_razdel='ok';}
         if($ref_user->{edit_design}){$edit_design='ok';}
         if($ref_user->{grant}){$grant='ok';}
         if($ref_user->{status}){$status='<b style="color:green">active</b>';}
         $tpl->assign(
                ID_USER    =>$ref_user->{id},
                LOGIN      =>$ref_user->{login},
                EMAIL      =>$ref_user->{email},
                NAME       =>$ref_user->{name},
                OPIS       =>$ref_user->{opis},
                ADD_RAZDEL =>$add_razdel,
                EDIT_DESIGN=>$edit_design,
                GRANT      =>$grant,
                STATUS     =>$status,
                SID        =>$ref->{sid},
                LANG       =>$ref->{l},
                ID         =>$ref->{id},
         );
         $tpl->parse("ROW_USERS",".row");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $url1="/cgi-bin/mod/manager.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&slovo=$ref->{slovo}";
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

sub message { #вывод сообщений об отказе доступа уже авторизованного пользователя
 my $ref=shift;
 my $def={  "main"=>"/constructor.html.$ref->{l}",
              };

 my $title="Менеджер пользователей"; #Вывод пользователей

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $message='<br><br><b>Доступ на данное действие закрыт, обратитесь к админстратору сайта</b><br><br><br><br><br><br><br><br>';
 $tpl->assign (TEXT => $message );
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();

}

sub view_user { #Добавление/редактирование профиля пользователя
 my $ref=shift;
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_admin_groups_add.html.$ref->{l}"
          };
 if(!$ref->{admin_ref}->{grant}){$ref->{id_user}=$ref->{admin_ref}->{id}}
 my $dbh=dbconnect;
 my $sel="select * from admin_groups where id='$ref->{id_user}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_user=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 if(!$ref_user->{id}){$ref_user=$ref;}
 my $title=slovo(23,$ref->{l}); #Новости 

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 my $mess='';
 if($ref->{mess} eq 'login_error'){$mess="Логин и пароль должны быть в латинской раскладке, без пробелов";}
 if($ref->{mess} eq 'ok'){$mess="Даные сохранены";}
    $tpl->assign (
        MESSAGE=>$mess,
        NAME=>$ref_user->{name},
        ID_USER=>$ref_user->{id},
        LOGIN=>$ref_user->{login},
        EMAIL=>$ref_user->{email},
        OPIS=>$ref_user->{opis},
        STATUS=>$ref_user->{status},
        ADD_RAZDEL=>$ref_user->{add_razdel},
        EDIT_DESIGN=>$ref_user->{edit_design},
        GRANT=>$ref_user->{grant},
        ID=>$ref->{id},
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

sub save_user {
 my $ref=shift;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db=$ref->{user_db};
 my $mod_razdel=$user_db->{data}->{$ref->{id}}->{mod}||'';
 my $pr_mes='19';
 if(!$ref->{admin_ref}->{grant})
   { $ref->{id_user}=$ref->{admin_ref}->{id};$ref->{status}=$ref->{admin_ref}->{status};
     $ref->{add_razdel}=$ref->{admin_ref}->{add_razdel};
     $ref->{edit_design}=$ref->{admin_ref}->{edit_desgn};
     $ref->{grant}=$ref->{admin_ref}->{grant};
   }
 my $dbh=dbconnect;
 if($ref->{id_user}){
  if($ref->{login}!~/[a-z0-9\,\.\[\;\']+/gi){
    $ref->{mess}='login_error'; #ошибка в логине или пароле
    view_user($ref);exit;
  }
   my $sql="update admin_groups set name=?,login=?,opis=?,add_razdel=?,edit_design=?,`grant`=?,email=?,status=?  where id=?";
   my $sth=$dbh->prepare($sql);
   $sth->execute($ref->{name},$ref->{login},$ref->{opis},$ref->{add_razdel},$ref->{edit_design},$ref->{grant},$ref->{email},$ref->{status},$ref->{id_user});
   $sth->finish;
   if($ref->{pass}){
    #if($ref->{pass}!~/[a-z0-9\,\.\[\;\']+/gi){
    # $ref->{mess}='login_error';
    # view_user($ref);exit;}
    $sql="update admin_groups set pass=md5(?) where id=?";
    $sth=$dbh->prepare($sql);
    my $upd=$sth->execute($ref->{pass},$ref->{id_user});
    $sth->finish;
   }
 }else{
    if($ref->{pass}!~/[a-z0-9\,\.\[\;\']+/gi||$ref->{login}!~/[a-z0-9\,\.\[\;\']+/gi){
     $ref->{mess}='login_error';
     view_user($ref);exit;
    }
    if(!$ref->{admin_ref}->{grant}){
        $ref->{who}="grant";
        &check_status($ref);exit;
    }
    $ref->{add_razdel}='0' if !$ref->{add_razdel};
    $ref->{edit_design}='0' if !$ref->{edit_design};
    $ref->{grant}='0' if !$ref->{grant};
   my $sql="insert into admin_groups (name,login,opis,add_razdel,edit_design,`grant`,email,status,pass) 
            values (?,?,?,?,?,?,?,?,md5('$ref->{pass}'))";
   my $sth=$dbh->prepare($sql);
   my $ins=$sth->execute($ref->{name},$ref->{login},$ref->{opis},$ref->{add_razdel},$ref->{edit_design},$ref->{grant},$ref->{email},$ref->{status});
   $sth->finish;
 }
 dbdisconnect($dbh);
 my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=19&$time&mess=ok"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub del_user {
 my $ref=shift;
 my $dbh=dbconnect();
 my $del=$dbh->do("delete from admin_groups where id='$ref->{id_user}' and login!='admin'");
    dbdisconnect($dbh);
 my $time=time;
 print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=19&$time&mess=ok"</script>
  </body>
  </HTML>
 ]; exit;
}
