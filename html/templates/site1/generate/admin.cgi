#!/usr/bin/perl
#модуль сгенерирован
 $|=1;
 use lib "../";
 use Modules::Constructor_view;
 use Modules::Constructor;
 use strict;
 my $ref=Get_Param_view||{};
# my $ref=Get_Param;
 my $p=1;
#print qq[perf $ref->{prefix}];exit;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 print "Content-type:text/html\r\n\r\n";

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


 $ref->{index_tpl} = "index_admin.tpl"; 
 $ref->{tpl_}="$ref->{module_name}_admin.tpl";
 $ref->{name_action}="Администрирование $ref->{module_name}";

 if ($ref->{'a'} eq '') {$ref=list($ref); } #Вывод списка анкет
 if ($ref->{'a'} eq 'form_edit') {$ref=form_edit($ref); } #Вывод редактора анкеты
 if ($ref->{'a'} eq 'save') {$ref=save($ref); } #сохранение информации
 if ($ref->{'a'} eq 'del') {$ref=del($ref); } #даление анкеты с  фотографиями
 print_($ref);


sub list {
 my $ref=shift;
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=100;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop='';
 my $order = "order by id desc ";
 if ($ref->{order_name}){$order = "order by $ref->{order_name} $ref->{asc}"}
 my $col="select count(*) from $ref->{module_name} where 1 $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 my $modp=$count%$CountPage;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 if(int($count/$CountPage)==$count/$CountPage){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}

    my $tbl_name="$ref->{module_name}";
    my $query="select * from $ref->{module_name} where 1 $order limit $off,$CountPage";

    ($ref->{name_fields},$ref->{ar_data},$ref->{fields_comment},$ref->{type_fields})=select_sql($ref,$tbl_name,$query,[],1);

    #sереход по страницам
    my $url1=$ref->{location};
    $url1=~s/&{0,1}p_n=([0-9]+)?//gi;


    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;
    return $ref;
}

sub form_edit {
 my $ref=shift;

    my $tbl_name="$ref->{module_name}";
    my $query="select * from $ref->{module_name} where id='$ref->{id}'";

    ($ref->{name_fields},$ref->{ar_data},$ref->{fields_comment},$ref->{type_fields})=select_sql($ref,$tbl_name,$query,[],1);
    $ref->{ref_data}=$ref->{ar_data}[0];
    if (!$ref->{id}){
	$ref->{ref_data}=$ref;
    }

 return $ref;
}

sub save {
    my $ref=shift;

    if($ref->{id}){
	 $ref->{update_status}=update_sql($ref,$ref->{module_name},$ref->{id});
    }else{
	$ref->{id}=insert_sql($ref,$ref->{module_name});
    }

return $ref; 
}

sub del {
my $ref = shift;
    $ref->{delete_status}=delete_sql($ref,$ref->{module_name},$ref->{id});
return $ref;
}
1;