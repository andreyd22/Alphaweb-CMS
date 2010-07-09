#!/usr/bin/perl
#!!!Скрипт, отвечающий за построение меню + ссылки на подключенные модули
 $|++;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
 my $err;
  ($ref->{l}, $err)=data_filter($ref->{l});
  ($ref->{mes}, $err)=data_filter($ref->{mes});
  ($ref->{a}, $err)=data_filter($ref->{a});

#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;
    URL=/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes'></HEAD></HTML>
     ";
 exit;
 }
  if(!-e "$ref->{path_template}/index.ini"){
print "<script>location.href='/cgi-bin/view_templates.pl?sid=$ref->{sid}&l=$ref->{l}'</script>"; exit;}
#!!!Проверка sid пользователя!!!#

 $ref=get_structure($ref);
 my $user_db=$ref->{user_db}; 

#     use Data::Dumper;
#     print Dumper($ref->{user_db});

 my $def={  "main"=>"/constructor_menu_main.html.$ref->{l}",
            "row"=>"/constructor_menu_row.html.$ref->{l}" 
         };
 $ref->{def}=$def;
 my $tpl=tplb($ref);

 my $i=1;
 my $j=1;
 my $k=1;
my $dbh=dbconnect();
 $tpl=print_menu1('0',$ref,$tpl); #Строим рекурсивно меню разделов
dbdisconnect();
 
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear();



sub print_menu {
    my $id_p=shift||'0';
    my $ref=shift;
    my $tpl=shift;
    if(!$id_p){$id_p='0';}
        my $sort=$ref->{user_db}->{data}->{sort}||{};
        my $parent=$ref->{user_db}->{data}->{parent}||{};

     use Data::Dumper;
     print Dumper($sort);

    my %sort=%$sort;
    my %parent=%$parent;

    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    foreach my $key (@ar_sort_key){
        if($parent{$key} eq $id_p){
my $key1=$key;
$key1=~s/\&/\-\-/gi;
my $pr_link="/cgi-bin/mod/$ref->{user_db}->{data}->{$key}->{mod}.cgi?sid=$ref->{sid}&id=$key1&l=$ref->{l}";
my $name_r=$ref->{user_db}->{data}->{$key}->{name};
 $name_r=~s/\"|\'/\`/gi; #`
#print qq[$name_r <br>];
   if(length($name_r)>18){
   $name_r=substr $name_r, 0,15;
   $name_r.="...";
   } 
   
#if ($ref->{user_db}->{data}->{$key}->{link}){$pr_link=$ref->{user_db}->{data}->{$key}->{link};}

    my $flag=0;
    my $insfld="insDoc";
    foreach my $key_new (keys %parent){
     if($parent{$key_new} eq $key){$flag=1;$insfld="insFld";}
        if($flag){last;}
}
     my $link='';
     my $ins='';
     my $iffld='';
     if($id_p eq '0'){ 
        $ins="foldersTree";
        $insfld="insFld";
     }else{
        my $k_n=$k-1;
        $ins="aux".$k_n;
     } #onclick=\"return Delete(2,'$name_r');\"
    my $lng=$ref->{user_db}->{data}->{$key}->{lang}||"ru";
    my $view="$ref->{user_db}->{data}->{$key}->{mod}/$key.html";
    print qq[$host_name <br>];
#    my $dop_content=qq[<td><a href='http://$host_name/view/$ref->{user_db}->{data}->{$key}->{mod}/$key' title='Просмотр' target=_blank><img src='/img/icons/browse.gif' border=0 alt='Посмотреть результат'></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&idp=$key' title='Добавить подраздел' target=main><img src='/img/icons/icon_add.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&id=$key' title='Свойства раздела' target=main><img src='/img/icons/icon_properties.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=del&id=$key' title='Удалить раздел' target=main><img src='/img/icons/delete.gif' border=0></a></td> ];
    my $dop_content=qq[<td><a href='/cgi-bin/mod/document.cgi?id=$key&page=simple&l=$ref->{l}&sid=$ref->{time}' title='Простой редактор' target=main><img src='/img/icons/text.gif' border=0 alt='Простой редактор' hspace=5></a></td> 
    					<td><a href='http://$host_name/$view' title='Просмотр' target=_blank><img src='/img/icons/browse.gif' border=0 alt='Посмотреть результат'></a></td> 
    					<td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&idp=$key' title='Добавить подраздел к разделу: $name_r' target=main><img src='/img/icons/icon_add.gif' border=0></a></td> 
    					<td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&id=$key' title='Свойства раздела: $name_r' target=main><img src='/img/icons/icon_properties.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=del&id=$key' title='Удалить раздел: $name_r' target=main><img src='/img/icons/delete.gif' border=0></a></td> ];
     if($flag>0){ #если есть флаг - значит у этого звена есть дочерние ветки
        $iffld='gFld';
        $link=qq[aux$k= $insfld($ins,gFld("<b>$name_r</b>","$pr_link","$dop_content"))];
     }else{$iffld='gLnk';
        $link=qq[$insfld($ins,gLnk("R","$name_r","$pr_link","$dop_content"))];
     }
#my $link = qq[
#<table width=100% cellspacing=0 cellpadding=0>
#<tr>
#<td width=$i nowrap>&nbsp;</td><td><a href="$pr_link" class=link$j target="main" title='Редактировать содержимое раздела $ref->{user_db}->{data}->{$key}->{name}'>$name_r</a></td>
#</tr>
#</table>
#
#<!--insDoc(foldersTree,gLnk('R','<font color=#0042ae>Услуги</font><br><br>', "section.php?action=show_menu&id=118")) 
#    aux1= insFld(foldersTree,gFld("<b><font color=#0042ae>Проекты</b></font>", "section.php?action=show_menu&id=119")) 
#    insDoc(aux1, gLnk("R", "<font color=#0042ae>Статьи</font><br><br>","section.php?action=show_submenu&id=142"))
#-->
#
#];
        $tpl->assign(
                HOST=>$host_name,
                SID=>$ref->{sid},
                LINK=>$link,
                NAME_RAZDEL=>$ref->{user_db}->{data}->{$key}->{name},
                LANG=>$ref->{l},
                ID=>$key1,
                MOD=>$ref->{user_db}->{data}->{$key}->{mod}
        );
        $tpl->parse("CONSTRUCTOR_MENU",".row");
        $i+=6;
        $j++;
        if($key ne ''){
        $k++;
        $tpl=print_menu($key,$ref,$tpl);
        $k--;
        }
        $i-=6;
        $j--;
     }
    }
return $tpl;
}

sub print_menu1 {
    my $id_p=shift||'0';
    my $ref=shift;
    my $tpl=shift;
    if(!$id_p){$id_p='0';}

        my $parent=$ref->{user_db}->{data}->{parent}||{};
        my %parent=%$parent;

my $sth=$dbh->prepare("select * from structure where parent='$id_p' and domain = '$ref->{host_name}' order by sort_id asc");
$sth->execute;
while ( my $ref_m=$sth->fetchrow_hashref)
{               my $key=$ref_m->{id};
		my $key1=$key;
		$key1=~s/\&/\-\-/gi;
		my $pr_link="/cgi-bin/mod/$ref_m->{module}.cgi?sid=$ref->{sid}&id=$key1&l=$ref->{l}";
		my $name_r=$ref_m->{name};
		$name_r=~s/\"|\'/\`/gi; #`
		#print qq[$name_r <br>];
		if(length($name_r)>18){
			$name_r=substr $name_r, 0,15;
			$name_r.="...";
   		} 
   
		my $flag=0;
	        my $insfld="insDoc";
		foreach my $key_new (keys %parent){
			if($parent{$key_new} eq $key){$flag=1;$insfld="insFld";}
		        if($flag){last;}
		}
		my $link='';
		my $ins='';
		my $iffld='';
		if($id_p eq '0'){ 
		        $ins="foldersTree";
		        $insfld="insFld";
	        }else{
		        my $k_n=$k-1;
		        $ins="aux".$k_n;
		} #onclick=\"return Delete(2,'$name_r');\"
		my $lng=$ref->{user_db}->{data}->{$key}->{lang}||"ru";
	    my $view="$ref_m->{module}/$key.html";
#    my $dop_content=qq[<td><a href='http://$host_name/view/$ref->{user_db}->{data}->{$key}->{mod}/$key' title='Просмотр' target=_blank><img src='/img/icons/browse.gif' border=0 alt='Посмотреть результат'></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&idp=$key' title='Добавить подраздел' target=main><img src='/img/icons/icon_add.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&id=$key' title='Свойства раздела' target=main><img src='/img/icons/icon_properties.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=del&id=$key' title='Удалить раздел' target=main><img src='/img/icons/delete.gif' border=0></a></td> ];
		my $dop_content=qq[<td><a href='/cgi-bin/mod/document.cgi?id=$key&page=simple&l=$ref->{l}&sid=$ref->{time}' title='Простой редактор' target=main><img src='/img/icons/text.gif' border=0 alt='Простой редактор' hspace=5></a></td> <td><a href='http://$host_name/$view' title='Просмотр' target=_blank><img src='/img/icons/browse.gif' border=0 alt='Посмотреть результат'></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&idp=$key' title='Добавить подраздел к разделу: $name_r' target=main><img src='/img/icons/icon_add.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=add&id=$key' title='Свойства раздела: $name_r' target=main><img src='/img/icons/icon_properties.gif' border=0></a></td> <td><a href='/cgi-bin/mod/razdels.cgi?sid=$ref->{sid}&l=$ref->{lang}&a=del&id=$key' title='Удалить раздел: $name_r' target=main><img src='/img/icons/delete.gif' border=0></a></td> ];
	        if($flag>0){ #если есть флаг - значит у этого звена есть дочерние ветки
		        $iffld='gFld';
		        $link=qq[aux$k= $insfld($ins,gFld("<b>$name_r</b>","$pr_link","$dop_content"))];
	        }else{$iffld='gLnk';
		        $link=qq[$insfld($ins,gLnk("R","$name_r","$pr_link","$dop_content"))];
	        }
        $tpl->assign(
                HOST=>$host_name,
                SID=>$ref->{sid},
                LINK=>$link,
                NAME_RAZDEL=>$ref->{user_db}->{data}->{$key}->{name},
                LANG=>$ref->{l},
                ID=>$key1,
                MOD=>$ref->{user_db}->{data}->{$key}->{mod}
        );
        $tpl->parse("CONSTRUCTOR_MENU",".row");
        $i+=6;
        $j++;
        if($key ne ''){
        $k++;
        $tpl=print_menu1($key,$ref,$tpl);
        $k--;
        }
        $i-=6;
        $j--;

}
$sth->finish;
return $tpl;
}
