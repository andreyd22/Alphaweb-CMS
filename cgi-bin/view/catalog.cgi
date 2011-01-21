#!/usr/bin/perl
#модуль каталога продукции
 $|=1;
 use lib "../";
 use Modules::Constructor qw (Get_Param dbconnect dbdisconnect page_down $host_name &size_img
                              &check_auth &encoder &send_mail
                               &slovo);
 my ($dostavka_rus,$dostavka_eng,$oplata_rus, $oplata_eng, $status_rus, $status_eng);
 use Modules::Constructor_view;
 use strict;
use CGI::Carp qw(fatalsToBrowser);
my $ref=Get_Param_view||{};
 my $time=time;
# my $mes=check_plata($ref);

 # кэшировать шаблоны
 # $ref->{cach}="yes";
# $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 
 $ref->{index_tpl} = "index.tpl"; 
 $ref->{tpl_}="catalog_new.tpl";

        use CGI::Cookie;
        my $cook=fetch CGI::Cookie();
                $ref->{basket_cook}=$cook->{basket_cook};
                $ref->{user_cook}=$cook->{user_cook};
 if($ref->{a} ne 'basket' && $ref->{a} ne 'update_basket' 
        &&  $ref->{a} ne 'registration' && $ref->{a} ne 'authorize'  && $ref->{a} ne 'logout' 
&& $ref->{a} ne 'step3' && $ref->{a} ne 'step4'
 && $ref->{a} ne 'step5'
){
  print "Content-type:text/html\r\n\r\n";
        use Data::Dumper;
#       print Dumper($ref->{basket_cook}->{value});
#       print Dumper($ref->{user_cook}->{value});
 }
 if ($ref->{'a'} eq '') {$ref=&list_catalog($ref); } #Вывод каталога
 if ($ref->{'a'} eq 'full') {$ref=&full_catalog($ref); } #Вывод товара с подробным описанием
 if ($ref->{'a'} eq 'send') {$ref=&send_catalog($ref); } #Отправка заказа с формы полной информации о товаре
 if ($ref->{'a'} eq 'form_order') {$ref=&form_order($ref); } #Список товаров с общей формой заказа
 if ($ref->{'a'} eq 'send_order') {$ref=&send_order($ref); } #Отправка данных с общей формы заказа
=myback
# if ($ref->{'a'} eq 'basket') {&basket($ref); } #записываем куки с товаром
 if ($ref->{'a'} eq 'view_basket') {&view_basket($ref); } #Просмотр корзины пользователя
 if ($ref->{'a'} eq 'update_basket') {&update_basket($ref); } #Обновление корзины пользователя
 if ($ref->{'a'} eq 'view_info') {&view_info($ref); } #Авторизация / регистрация пользователя форма
 if ($ref->{'a'} eq 'registration') {&registration($ref); } #Регистрация пользователя
 if ($ref->{'a'} eq 'authorize') {&authorize($ref); } #авторизация пользователя
 if ($ref->{'a'} eq 'ok_authorize') {&ok_authorize($ref); } #авторизация пользователя через форму
 if ($ref->{'a'} eq 'logout') {&logout($ref); } #выходпользователя
 if ($ref->{'a'} eq 'step2') {&step2($ref); } #проверка есть ли кук и если есть вывод следующего шага: заполнение адреса, (потом выбор способа доставки) , либо сразу выкидываем на выбор способа оплаты step 3
 if ($ref->{'a'} eq 'check_adres') {&check_adres($ref); } #проверка адресов
 if ($ref->{'a'} eq 'save_adres') {&save_adres($ref); } #Форма записи / редактирования адресов доставки
 if ($ref->{'a'} eq 'update_adres') {&update_adres($ref); } #Запись адреса доставки
 if ($ref->{'a'} eq 'delete_adres') {&delete_adres($ref); } #Удаление адреса доставки
 if ($ref->{'a'} eq 'step3') {&step3($ref); } #проверка есть ли кук юзера и если есть перекидываем на выбор способа доставки
 if ($ref->{'a'} eq 'step4') {&step4($ref); } #проверка есть ли кук юзера и если есть перекидываем на выбор способа оплаты
# if ($ref->{'a'} eq 'check_data') {&check_data($ref); } #Проверка данных
 if ($ref->{'a'} eq 'step5') {&step5($ref); } #Проверка данных
 if ($ref->{'a'} eq 'update_order') {&update_order($ref); } #Подтверждение заказа
 if ($ref->{'a'} eq 'del_order') {&del_order($ref); } #Удаление заказа
 if ($ref->{'a'} eq 'view_orders') {&view_orders($ref); } #Просмотр заказов
 if ($ref->{'a'} eq 'view_oplata') {&view_oplata($ref); } #Просмотр банковской платежки, почтового платежа и т.п. и печать
=cut
#print qq[$ref->{a}];

 # выводим шаблон
 print_($ref);



sub list_catalog { #вывод элементов каталога (самих товаров)

 my $ref=shift;

 #если есть верхняя часть выводим
 if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){

 	$ref->{tpl_top}="user_db.$ref->{id}.data";
 }

 $ref->{currency}=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{curency}||'руб.';
 my $col_records=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{col_records}||12;
 my $col_rows=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{row_records}||3;
 my $zag=$ref->{user_db}->{data}->{$ref->{id}}->{zag}||$ref->{user_db}->{data}->{$ref->{id}}->{name};
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=$col_records||5;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop='';
 if($ref->{slovo}){
  $ref->{slovo}=~s/\%//gi;
#  $ref->{slovo}=~s/\%+$//gi;
  $ref->{slovo}=~s/^\s+//gi;
  $ref->{slovo}=~s/\s+$//gi;
#  $ref->{slovo}=~s/\s+/\%/gi;
#  $ref->{slovo}=~s/\%+/\%/gi;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
 $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(short) like upper('%$ref->{slovo}%'))];
    $ref->{zag}=$ref->{slovo}
 }
 my $dop_r="";
 if($ref->{id}){$dop_r="and idr='$ref->{id}'";}
 my $col="select count(*) from $ref->{db_prefix}_catalog where 1 $dop_r $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 my $order='order by sort asc, id desc';
    $order='order by name' if $ref->{sort} eq 'name';
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
 my $sel="select * from $ref->{db_prefix}_catalog where 1 $dop_r $dop $order limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
#    use Apache::Util 'escape_uri';
#    my $slovo_encode = escape_uri(encoder($ref->{slovo},'koi','win'))||'';

    $ref->{gal_ini_row}="$ref->{path_template}/catalog_row.tpl";
    open A, $ref->{gal_ini_row};
    my @ar_row=<A>;
    close A;
    my $str_row=join('',@ar_row);
    my $gal=''; my $inc=0;my $i=0;
    my @ar;
    while(my $ref_catalog=$sth->fetchrow_hashref){
    my $link_catalog="/catalog/$ref_catalog->{idr}/$ref_catalog->{id}.html";
        my ($img_cat,$img_cat_m);
        $ref_catalog->{name}=~s/"/'/gi; #"
         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}-s.$ref_catalog->{img_end}"){
          $ref_catalog->{img_cat}=qq[<a href="$link_catalog">
        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-s.$ref_catalog->{img_end}" border=0 align=left class="img_cat"></a>];
          $ref_catalog->{img_cat_m}=qq[<a href="$link_catalog">
        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-150.$ref_catalog->{img_end}" border=0 class="img_cat"></a>];
         }
         my $status="Есть на складе";
            $status="Нет в наличии" if !$ref_catalog->{status};
         $inc++;$i++;
      my $str_new=$str_row;
      my $alt="$ref_catalog->{name} / $zag $ref->{user_db}->{template}->{assign}->{TITLE}";
         $alt=~s/"/'/gi; $alt=~s/\s+/ /gi; $alt=~s/^\s+|\s+$//gi; $alt=~s/^\/|\/$//gi; #'"

         my ($data,$time)=split / /,$ref_catalog->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;

         $ref_catalog->{data_print}="$day.$month.$year";
      	 push @ar,$ref_catalog;
		
    }
    $ref->{ar_data}=\@ar;
         
    $sth->finish;
 dbdisconnect($dbh);
    #sереход по страницам
    my $url1=$ref->{location};
    $url1=~s/&{0,1}p_n=([0-9]+)?//gi;

    if($ref->{slovo}){
	    #sереход по страницам c поиска
	    $url1="/catalog/$ref->{id}.html?slovo=$ref->{slovo}";
    }

    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;

    return $ref;
}

sub full_catalog {#Полная информация о товаре
 my $ref=shift;
 my $tpl={};

 #Выводим информацию о товаре
 my $dbh=dbconnect;
 my $sel="select * from $ref->{db_prefix}_catalog where id='$ref->{id_cat}' and idr='$ref->{id}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_catalog=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
#  print "Content-type:text/html\r\n\r\n";
#print qq[$ref->{test}];
 if(!$ref_catalog->{id}){print qq[<center>Данные не найдены</center>];exit;}
  $ref->{zag}=$ref->{user_db}->{data}->{$ref->{id}}->{zag}||$ref->{user_db}->{data}->{$ref->{id}}->{name};
 $ref->{curency}=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $ref->{zag}=~tr/"'/``/;#"
 $ref_catalog->{name}=~tr/"'/``/;#"
        my $img_cat="";
        my $img_cat_s="";
        my $img_cat_m="";
        $ref_catalog->{name}=~s/"/'/gi;#"
        $ref_catalog->{opis}=~s/("|')images\//$1\/images\//gi;
#         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}-s.jpg"){
#          $img_cat=qq[<a target=_blank  href="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}.jpg">
#        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE} full screen" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-s.jpg" border=0></a>];
#         }
         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}.$ref_catalog->{img_end}"){

         my $ref_size=size_img("$ref->{path_host}/cat_image/$ref_catalog->{id}.$ref_catalog->{img_end}");
          $ref->{img_cat}=qq[
          <a href="http://$host_name" onclick="win_gallery('http://$ref->{user_doman}/cat_image/$ref_catalog->{id}.$ref_catalog->{img_end}','$ref_catalog->{name}',$ref_size->{width},$ref_size->{height}); return false;">
          <img align=left alt="$ref_catalog->{name} $ref->{zag} $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-s.$ref_catalog->{img_end}" class="img_cat"></a>];

          $ref->{img_cat_s}=qq[
          <a href="http://$host_name" onclick="win_gallery('http://$ref->{user_doman}/cat_image/$ref_catalog->{id}.$ref_catalog->{img_end}','$ref_catalog->{name}',$ref_size->{width},$ref_size->{height}); return false;">
          <img alt="$ref_catalog->{name} $ref->{zag} $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-150." border=0 class="img_cat"></a>];

          $ref->{img_cat_m}=qq[
          <a href="http://$host_name" onclick="win_gallery('http://$ref->{user_doman}/cat_image/$ref_catalog->{id}.$ref_catalog->{img_end}','$ref_catalog->{name}',$ref_size->{width},$ref_size->{height}); return false;">
          <img alt="$ref_catalog->{name} $ref->{zag} $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-150.$ref_catalog->{img_end}" border=0 hspace=5 class="img_cat"></a>];
         
         }
         my $status="Есть на складе";
            $status="Нет в наличии" if !$ref_catalog->{status};
         my $message='';
            $message=qq[Заполните обязательные поля <a href="#zakaz">формы</a>] if $ref->{mess} eq '1';
            $message=qq[Ошибка данных] if $ref->{mess} eq '3';
            $message=qq[Заявка на участие в тренинге упешно отправлена. Наши менеджеры свяжутся с вами. Вопрос только когда...? А никогда :) Шутка.] if $ref->{mess} eq 'ok';
 #Выводим новости
 $ref_catalog->{short_desc}=$ref_catalog->{short};
 $ref_catalog->{short_desc}=~s/<br>/ /gi;
 $ref_catalog->{short_desc}=~s/\s+/ /gi;
 $ref_catalog->{short_desc}=~s/"/'/gi; #'"
 $ref->{data}=$ref_catalog;
 $ref->{name_zag_site}=$ref_catalog->{name};
 return $ref;
}

sub send_catalog { #отправка заказа от пользовательня на адрес администратора (указывается в админке)
my $ref=shift;
 $ref->{zag}="Заказ принят";
if(!$ref->{id_cat}||!$ref->{col})
   {
   $ref->{mess}='error_field';$ref->{a}="full";$ref=&full_catalog($ref);
   }
else
   {
 my $dbh=dbconnect;
 my $sel="select * from $ref->{db_prefix}_catalog where id='$ref->{id_cat}' and idr='$ref->{id}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_catalog=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
    if(!$ref_catalog->{id}){ #возвращаем ошибку, если нет такого товара
      $ref->{mess}='3';
      &full_catalog($ref);
    }
 my $sel="select * from users_$ref->{prefix} where login='$ref->{cook}->{users_cook}->{value}->[0]' and pass='$ref->{cook}->{users_cook}->{value}->[1]'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 $ref->{users_ref}=$sth->fetchrow_hashref||{};

my $email=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{email};
my $subject="Заказ товара #$ref->{id_cat}";
my $text=qq[
Здравствуйте, администратор!
Поступила новая заявка на товар: 
$ref_catalog->{name}
Подробная информация о товаре:
http://$host_name/catalog/$ref->{id}/$ref->{id_cat}.html

Информация о покупателе:
ФИО: $ref->{users_ref}->{name}  $ref->{users_ref}->{l_name}
Кол-во: $ref->{col}
Название компании: $ref->{users_ref}->{dop}
Email: $ref->{users_ref}->{email}
Телефон: $ref->{users_ref}->{phone}
Город: $ref->{users_ref}->{city}
Удобный способ оплаты: $ref->{oplata}
Комментарий:
  $ref->{comments}
];
 &send_mail($email,$subject,$text);
 $ref->{mess}='ok';
 $ref->{a}="full";
 $ref=&full_catalog($ref);
 }
}

sub form_order { #Форма заказа с выбором различных элементов

 my $ref=shift;


 $ref->{currency}=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{curency}||'руб.';
 $ref->{zag}="Оформить заказ";
 $ref->{title}="Оформить заказ";
 my $dbh=dbconnect;

 my $sel="select * from structure where module='catalog'";
 my $sth=$dbh->prepare($sel);
    $sth->execute();
 my @ar_r=(); my @ar_cat=();
 while(my $ref_st=$sth->fetchrow_hashref){
     my $ref_cat=$dbh->selectall_arrayref("select * from $ref->{db_prefix}_catalog where idr='$ref_st->{id}' order by sort asc, id desc");
     my $cat_hash={name=>$ref_st->{name},data=>$ref_cat};
	
     push @ar_r,$cat_hash;
#     push @ar_cat,$ref_cat;
 }
 $sth->finish;
$ref->{ar_r}=\@ar_r;
#$ref->{ar_cat}=\@ar_cat;
# $ref->{ar_data_milk}=$dbh->selectall_arrayref("select * from $ref->{db_prefix}_catalog where idr='prod_milk' order by sort asc, id desc");

# $ref->{ar_data_cheese}=$dbh->selectall_arrayref("select * from $ref->{db_prefix}_catalog where idr='prod_cheese' order by sort asc, id desc");

# $ref->{ar_data_curd}=$dbh->selectall_arrayref("select * from $ref->{db_prefix}_catalog where idr='prod_curd' order by sort asc, id desc");

 dbdisconnect($dbh);
 return $ref;
}


sub send_order { #отправка заказа от пользовательня на адрес администратора (указывается в админке)
my $ref=shift;
 my $dbh=dbconnect;
    my $all_send="";
  $ref->{zag}="Отправка заказа";
 my $sel="select * from $ref->{db_prefix}_catalog where idr='prod_milk' order by sort asc, id desc";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $str_milk=""; 
    while(my $ref_cat=$sth->fetchrow_hashref){
	my $col=CGI::param("col_$ref_cat->{id}");
	if ($col){$str_milk.=qq[$ref_cat->{name}\t$col\n];}
    }
    $sth->finish;
 my $sel="select * from $ref->{db_prefix}_catalog where idr='prod_cheese' order by sort asc, id desc";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $str_cheese=""; 
    while(my $ref_cat=$sth->fetchrow_hashref){
	my $col=CGI::param("col_$ref_cat->{id}");
	if ($col){$str_cheese.=qq[$ref_cat->{name}\t$col\n];}
    }
    $sth->finish;
 my $sel="select * from $ref->{db_prefix}_catalog where idr='prod_curd' order by sort asc, id desc";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $str_curd=""; 
    while(my $ref_cat=$sth->fetchrow_hashref){
	my $col=CGI::param("col_$ref_cat->{id}");
	if ($col){$str_curd.=qq[$ref_cat->{name}\t$col\n];}
    }
    $sth->finish;
    if($str_milk){$all_send.=qq[МОЛОКО\n$str_milk\n];}
    if($str_cheese){$all_send.=qq[\nСЫР\n$str_cheese\n];}
    if($str_curd){$all_send.=qq[\nТворог\n$str_curd\n];}

 my $sel="select * from users_$ref->{prefix} where login='$ref->{cook}->{users_cook}->{value}->[0]' and pass='$ref->{cook}->{users_cook}->{value}->[1]'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 $ref->{users_ref}=$sth->fetchrow_hashref||{};

my $email=$ref->{root_mail};
my $subject="Обобщенный заказ товаров";
my $text=qq[
Здравствуйте, администратор!
Поступила новая заявка на товары: 

$all_send

Информация о покупателе:
ФИО: $ref->{users_ref}->{name}  $ref->{users_ref}->{l_name}
Кол-во: $ref->{col}
Название компании: $ref->{users_ref}->{dop}
Email: $ref->{users_ref}->{email}
Телефон: $ref->{users_ref}->{phone}
Город: $ref->{users_ref}->{city}
Удобный способ оплаты: $ref->{oplata}
Комментарий:
  $ref->{comments}
];
 &send_mail($email,$subject,$text);
 return $ref;
}

sub basket { #Добавляем товар в корзину
 my $ref=shift;
 my $strcook=$ref->{basket_cook}->{value}->[0]||'';
 if($ref->{basket_cook}->{value}->[0]!~/$ref->{id}\=/){
#print qq[ok];
#  $strcook.="zhopa|";
$strcook.="$ref->{id}=1|";
}
 else{
 $strcook=~/$ref->{id}\=(\d)\|/;
 my $col_new=$1+1;
 $strcook=~s/$ref->{id}=(\d)\|/$ref->{id}=$col_new\|/;
 }
  my  $expires='+12M';
#  $strcook.="zhopa";
#  $strcook='';
  my @ar=($strcook);
  my $c = new CGI::Cookie(
                        -name => "basket_cook",
                        -value => \@ar,
#                        -value => '',
                        -expires => $expires,
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);
#               &view_basket($ref);
 print "
  <HTML>
  <body>
<center>
<!--cookie was created $host_name<br>
<a href='/base/view/catalog/&a=view_basket'>Нажмите на эту ссылку, чтобы перейти в корзину</a>-->
<script>location.href='/base/view/catalog/&a=view_basket'</script>
</center>
  </body>
</HTML>"; exit;

}

sub view_basket { #просмотр корзины
 my $ref=shift;
 my $tpl={};
 $ref->{my_modul_ini}="catalog_basket";
 $ref->{zag}="Просмотр корзины";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)
 #Выводим каталог товаров в корзине
 ($ref,$tpl)=list_basket($ref,$tpl);
 #Выводим каталог товаров в корзине
 my $zag=slovo(41,$ref->{l}); #Корзина
 my $all_cost=$ref->{my_temp}->{all_cost}; 
 my $skidka=0;
 my $id_user=undef;
 if($ref->{user_cook}->{value}->[0]){
 my $dbh=dbconnect;
 my $sel_user="select id,skidka from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 ($id_user,$skidka)=$dbh->selectrow_array($sel_user);
 dbdisconnect($dbh);
 }
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $all_cost=$all_cost-($all_cost*($skidka/100));
 if(!$all_cost){
 $tpl->assign(
           CATALOG_BASKET_ROW =>qq[<tr><td colspan=5 align=center height=70><b>Ваша корзина пуста</b></td></tr>]
       );
 }
 $tpl->assign(
           CURENCY =>$curency,
           ALL_COST =>$all_cost,
           SKIDKA  =>$skidka,
       );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub list_basket { #вывод каждой записи корзины
 my $ref=shift;
 my $tpl=shift;
 my $strcook=$ref->{basket_cook}->{value}->[0];
 my @ar_cook=split /\|/,$strcook;
 my @ar_id=();
 my %hash_col='';
 for(my $i=0;$i<=$#ar_cook;$i++){
     my @ar_id_col=split/\=/,$ar_cook[$i];
     push @ar_id,$ar_id_col[0];
     $hash_col{$ar_id_col[0]}=$ar_id_col[1];
 }
 my $dop="and id='$ar_id[0]'";
 if($#ar_id>0){
 my $id_for_select=join(',',@ar_id);
 $id_for_select=~s/\,$//gi;
 $dop="and id in ($id_for_select)";
 }
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 my $dbh=dbconnect;
 my $sel="select * from $ref->{db_prefix}_catalog where 1 $dop order by name";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $all_cost=0;
    while(my $ref_catalog=$sth->fetchrow_hashref){
    my $link_catalog="/base/view/catalog/$ref_catalog->{idr}/$ref_catalog->{id}/full";
    my $cost=$ref_catalog->{cost}*$hash_col{$ref_catalog->{id}};
         $tpl->assign(
                ID_CAT  =>$ref_catalog->{id},
                LINK_CAT  =>$link_catalog,
                ID  =>$ref_catalog->{idr},
                NAME  =>$ref_catalog->{name},
                COST =>$cost,
                COL =>$hash_col{$ref_catalog->{id}},
                CURENCY =>$curency
         );
         $tpl->parse("CATALOG_BASKET_ROW",".CATALOG_BASKET_ROW");
         $tpl->clear_href(1);
                 $all_cost=$all_cost+$cost;
    }
    $sth->finish;
 dbdisconnect($dbh);
$ref->{my_temp}->{all_cost}=$all_cost;
return ($ref,$tpl);
}

sub update_basket {#Обновляем корзину
  my $ref=shift;
  my @ar_id=CGI::param('id_cat');
  my @ar_col=CGI::param('col_cat');
  my $strcook=$ref->{basket_cook}->{value}->[0];
 if($#ar_id==0){
   if($ar_col[0] eq '0'){
     $strcook=~s/$ref->{id_cat}\=(\d)\|//;
    }else{
     $strcook=~s/$ref->{id_cat}\=(\d)\|/$ref->{id_cat}\=$ref->{col_cat}\|/;
    }
 }else{
  $strcook='';
  for(my $i=0;$i<=$#ar_col;$i++){
        if($ar_col[$i]==0){next}
        if($ar_col[$i]=~/\D/gi){$ar_col[$i]=1}
       $strcook.="$ar_id[$i]=$ar_col[$i]|";
  }
 }
  my  $expires='+12M';
  my @ar=($strcook);
  my $c = new CGI::Cookie(
                        -name => "basket_cook",
                        -value => \@ar,
#                        -value => '',
                        -expires => $expires,
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);

# print qq[  <HTML>  <body>@ar_id strcook $strcook</body></HTML>]; exit;
# print "  <HTML>  <body><script>location.href='/base/view/catalog/&a=view_basket'</script>  </body></HTML>"; exit;
 print "  <HTML>  <body><script>location.href='$ref->{referrer}'</script>  </body></HTML>"; exit;
}

sub view_info {#Форма регистрации/авторизации
 my $ref=shift;
 my $tpl={};
 $ref->{my_modul_ini}="catalog_user";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 my $mes='';
 if($ref->{mes} eq '1') {$mes="Не все поля заполнены";}
 if($ref->{mes} eq '2') {$mes="Пароли не совпадают";}
 if($ref->{mes} eq '3') {$mes="Пользователь с таким email адресом уже зарегистрирован";}
 if($ref->{mes} eq '4') {$mes="Пользователь с таким email адресом не зарегистрирован в системе,<br> пройдите пожалуйста регистрацию";}
# my $zag="Авторизация / Регистрация";
 my $zag=slovo(42,$ref->{l}); #Авторизация / регистрация
 $tpl->assign(
                   MESS=>$mes,
                   EMAIL=>$ref->{email},
                   NAME=>$ref->{name},
                   L_NAME=>$ref->{l_name},
                   F_NAME=>$ref->{f_name},
                   TITLE=>"$zag  $ref->{user_db}->{template}->{assign}->{TITLE}",
                   DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
                   KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
       );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub authorize {#авторизация пользователя
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select email,pass from users_cat_$ref->{prefix} where email='$ref->{email}' and pass='$ref->{pass}'";
 my ($email,$pass)=$dbh->selectrow_array($sel_user);
 if (!$email||!$pass){
 print "Content-type:text/html\r\n\r\n";
  $ref->{mes}="4"; #нет данных
  &view_info($ref);
 exit;
 }else{

  my  $expires='';
  my @ar=($email,$pass);
  my $c = new CGI::Cookie(
                        -name => "user_cook",
                        -value => \@ar,
#                        -value => '',
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);
 $ref->{user_cook}->{value}=\@ar;
# &step2($ref);
  if($ref->{type} eq 'authorize'){
    print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=ok_authorize'</script>  </body></HTML>"; exit;
  }else{
    print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=step2'</script>  </body></HTML>"; exit;
  }
 }
}

sub logout {#выход пользователя
 my $ref=shift;
  my  $expires='';
  my @ar=();
  my $c = new CGI::Cookie(
                        -name => "user_cook",
                        -value => \@ar,
#                        -value => '',
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);
 $ref->{user_cook}->{value}=\@ar;
 print "  <HTML>  <body><center>Logout</center><script>location.href='http://$host_name'</script>  </body></HTML>"; exit;
}

sub registration {#Регистрация пользователя
 my $ref=shift;
 if(!$ref->{email}||!$ref->{pass1}||!$ref->{pass2}||!$ref->{name}||!$ref->{l_name}||!$ref->{f_name}){
 print "Content-type:text/html\r\n\r\n";
  $ref->{mes}="1"; #не все полязаполнены
   &view_info($ref); 
  exit;
 }
 if($ref->{pass1} ne $ref->{pass2}){
 print "Content-type:text/html\r\n\r\n";
  $ref->{mes}="2"; #не все полязаполнены
  &view_info($ref);
 exit;
 }
 my $dbh=dbconnect;
 my $sel_user="select count(*) from users_cat_$ref->{prefix} where email='$ref->{email}'";
 my $id=$dbh->selectrow_array($sel_user);
# print "Content-type:text/html\r\n\r\n";
#print qq[id = $id $sel_user]; exit;
 if ($id){
 print "Content-type:text/html\r\n\r\n";
  $ref->{mes}="3"; #такой пользователь уже есть 
  &view_info($ref);
 exit;
 }else{
 my $ins="insert into users_cat_$ref->{prefix} (name,l_name,f_name,email,pass,date_reg) values (?,?,?,?,?,now())";
 my $sth=$dbh->prepare($ins);
    $sth->execute($ref->{name},$ref->{l_name},$ref->{f_name},$ref->{email},$ref->{pass1});
  my  $expires='';
  my @ar=($ref->{email},$ref->{pass1});
  my $c = new CGI::Cookie(
                        -name => "user_cook",
                        -value => \@ar,
#                        -value => '',
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);
 $ref->{user_cook}->{value}=\@ar;
#  &step2($ref);
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=step2'</script>  </body></HTML>"; exit;
 }
 dbdisconnect($dbh);
}

sub step2 {# шаг 2. смотрим какие способы доставки есть в магазине, если есть доставка почтой или курьером, 
           # проверяем адреса доставки 
           # если нет доставки то cразу переходим к оплате
 my $ref=shift;
if (!$ref->{user_cook}->{value}->[0]){
  &view_info($ref);
 }elsif(!$ref->{basket_cook}->{value}->[0]) {
  &view_basket($ref);
 }
 else{
 my $dostavka_post=$ref->{user_db}->{data}->{params}->{dostavka_post}||'';
 my $dostavka_kurer=$ref->{user_db}->{data}->{params}->{dostavka_kurer}||'';
#Mprint qq[ok];
   if($dostavka_post ne '' || $dostavka_kurer ne ''){
                 my $dbh=dbconnect;
                 my $sel_user="select id from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
                 my $id_user=$dbh->selectrow_array($sel_user);
                 if(!$id_user){&view_info($ref); exit;}
                 my $sel="select count(*) from users_adres_$ref->{prefix} where id_pol='$id_user'";
                 my $col_adres=$dbh->selectrow_array($sel);
                 if(!$col_adres){
#                print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=update_adres'</script>  </body></HTML>"; exit;
                        &update_adres($ref);
                        } #Добавление нового адреса доставки
                 else{
                        &check_adres($ref);
#                print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=check_adres'</script>  </body></HTML>"; exit;
                        } #Выбор адреса доставки
   }
   else{
        &step3($ref); #Выбор способа оплаты
# print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=step3&step3=1'</script>  </body></HTML>"; exit;
        }
 }
}
sub step3 { #шаг 3 выбор способа доставки или переходим к шагу 4
 my $ref=shift;
 if(!$ref->{user_cook}->{value}->[0]){
#  &view_info($ref);
 print "Content-type:text/html\r\n\r\n";
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }
 elsif(!$ref->{basket_cook}->{value}->[0]) {
  print "Content-type:text/html\r\n\r\n";
  &view_basket($ref);
 }
else{
   if($ref->{update_basket}){
     &update_basket($ref);
   }else{
         my $dostavka_post=$ref->{user_db}->{data}->{params}->{dostavka_post}||'';
         my $dostavka_kurer=$ref->{user_db}->{data}->{params}->{dostavka_kurer}||'';
         my $dostavka_ftp=$ref->{user_db}->{data}->{params}->{dostavka_ftp}||'';
         my $dostavka_email=$ref->{user_db}->{data}->{params}->{dostavka_email}||'';
      print "Content-type:text/html\r\n\r\n";
          if($dostavka_post || $dostavka_kurer || $dostavka_ftp || $dostavka_email){
          &check_dostavka($ref);        
          }else{&step4($ref);}
  }
 }

}
sub step4 {#шаг 4 проверяем способ оплаты, если они вообще предусмотрены, либо переходим к шагу проверки данных
 my $ref=shift;
 if(!$ref->{user_cook}->{value}->[0]){
#  &view_info($ref);
 print "Content-type:text/html\r\n\r\n";
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }
 elsif(!$ref->{basket_cook}->{value}->[0]) {
 print "Content-type:text/html\r\n\r\n";
  &view_basket($ref);
 }
else{
   if($ref->{update_basket}){
     &update_basket($ref);
   }else{
         my $predoplata=$ref->{user_db}->{data}->{params}->{predoplata}||'';
         my $postoplata=$ref->{user_db}->{data}->{params}->{postoplata}||'';
      print "Content-type:text/html\r\n\r\n";
          if($predoplata || $postoplata){
          &check_oplata($ref);  
          }else{&check_data($ref);}
  }
 }

}
sub step5 { #шаг 5. пользователь проверяет свои данные 
 my $ref=shift;
 if(!$ref->{user_cook}->{value}->[0]){
#  &view_info($ref);
 print "Content-type:text/html\r\n\r\n";
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }
 elsif(!$ref->{basket_cook}->{value}->[0]) {
 print "Content-type:text/html\r\n\r\n";
  &view_basket($ref);
 }
else{
   if($ref->{update_basket}){
      &update_basket($ref);
   }elsif($ref->{order}){
    &order($ref);
   }
   else{
    print "Content-type:text/html\r\n\r\n";
    &check_data($ref);
   }
 }
}

sub check_adres { # Выбор адреса пользователя.
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id,skidka from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka)=$dbh->selectrow_array($sel_user);
 if(!$id_user){
#&view_info($ref); exit;
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }
 my $sel="select count(*) from users_adres_$ref->{prefix} where id_pol='$id_user'";
 my $col_adres=$dbh->selectrow_array($sel);
 if(!$col_adres){
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=update_adres'</script>  </body></HTML>"; exit;
        #                       &update_adres($ref);
 } #Добавление нового адреса доставки
 if(!$ref->{path_db}){print "<script>location.href='http://$host_name'</script>"; exit;}
 my $tpl={};
 $ref->{my_modul_ini}="catalog_user_adres";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)
 $ref->{id_pol}=$id_user;
 #Выводим список адресов
 ($ref,$tpl)=list_adres($ref,$tpl);
 #Выводим список адресов

 #Выводим каталог товаров
 ($ref,$tpl)=list_basket($ref,$tpl);
 #Выводим каталог товаров

# my $zag="Выбор адреса доставки";
 my $zag=slovo(43,$ref->{l}); #
 my $all_cost=$ref->{my_temp}->{all_cost}; 
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $all_cost=$all_cost-($all_cost*($skidka/100));
 $tpl->assign(
           CURENCY =>$curency,
           ALL_COST =>$all_cost,
           SKIDKA =>$skidka,
           ZAG  =>$zag,
           TITLE=>"$zag  $ref->{user_db}->{template}->{assign}->{TITLE}",
           DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
           KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );

 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub list_adres {#вывод списка всех адресов пользователя
 my $ref=shift;
 my $tpl=shift;
 my $dbh=dbconnect;
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$ref->{id_pol}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $c=0;
    while(my $ref_adres=$sth->fetchrow_hashref){
        if(!$c){
         $tpl->assign(
                        CHECK_ID_ADRES=>'checked'
        );
    }else{
         $tpl->assign(
                        CHECK_ID_ADRES=>''
        );
        }
        $c++;
         $tpl->assign(
                   COUNTRY=>$ref_adres->{country},
                   POST_INDEX=>$ref_adres->{post_index},
                   REGION=>$ref_adres->{region},
                   CITY=>$ref_adres->{city},
                   FIO=>$ref_adres->{fio},
                   PHONE=>$ref_adres->{phone},
                   STREET=>$ref_adres->{street},
                   HOME=>$ref_adres->{home},
                   PLACE=>$ref_adres->{place},
                   DOP=>$ref_adres->{dop},
                   ID_ADRES=>$ref_adres->{id},
         );
         $tpl->parse("CATALOG_USER_ADRES_ROW",".CATALOG_USER_ADRES_ROW");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);

 return ($ref,$tpl);
}

sub update_adres {#Форма добавления/редактирования адреса
 my $ref=shift;
 my $tpl={};
 $ref->{my_modul_ini}="catalog_add_adres";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 #Выводим адрес
 my $dbh=dbconnect;
 my $sel_user="select id from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my $id_user=$dbh->selectrow_array($sel_user);
 if(!$id_user){
#&view_info($ref); exit;
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_user' and id='$ref->{id_adres}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
# my $zag="Добавление/редактирование адреса доставки";
 my $zag=slovo(44,$ref->{l}); #
 my $mes='';
 if($ref->{mes} eq '1') {$mes="Не все поля заполнены";}
 $ref_adres=$ref if !$ref_adres->{id};
 $tpl->assign(
                   MESS=>$mes,
                   COUNTRY=>$ref_adres->{country},
                   POST_INDEX=>$ref_adres->{post_index},
                   REGION=>$ref_adres->{region},
                   CITY=>$ref_adres->{city},
                   FIO=>$ref_adres->{fio},
                   PHONE=>$ref_adres->{phone},
                   STREET=>$ref_adres->{street},
                   HOME=>$ref_adres->{home},
                   PLACE=>$ref_adres->{place},
                   DOP=>$ref_adres->{dop},
                   ID_ADRES=>$ref_adres->{id},
                   ZAG=>$zag,
                   TITLE=>"$zag  $ref->{user_db}->{template}->{assign}->{TITLE}",
                   DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
                   KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );

 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub save_adres {#Сохраняем новый , либо редактируем уже существующий адрес доставки
 my $ref=shift;
 if(!$ref->{country}||!$ref->{post_index}||!$ref->{city}||!$ref->{fio}||!$ref->{phone}||!$ref->{street}||!$ref->{home}||!$ref->{place}){
  $ref->{mes}="1"; #не все полязаполнены
   &update_adres($ref); 
  exit;
 }
 my $dbh=dbconnect;
 my $sel_user="select id from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my $id_user=$dbh->selectrow_array($sel_user);
 if(!$id_user){&view_info($ref); exit;}
 if (!$ref->{id_adres}){
 my $ins="insert into users_adres_$ref->{prefix} (id_pol,country,post_index,region,city,fio,phone,street,home,place,dop)
                                                   values (?,?,?,?,?,?,?,?,?,?,?)";
 my $sth=$dbh->prepare($ins);
    $sth->execute($id_user,$ref->{country},$ref->{post_index},$ref->{region},$ref->{city},$ref->{fio},$ref->{phone},$ref->{street},$ref->{home},$ref->{place},$ref->{dop});
 }else{
 my $ins="update users_adres_$ref->{prefix} set id_pol=?,country=?,post_index=?,region=?,city=?,fio=?,phone=?,street=?,home=?,place=?,dop=?
                                                   where id='$ref->{id_adres}' and id_pol='$id_user'";
 my $sth=$dbh->prepare($ins);
    $sth->execute($id_user,$ref->{country},$ref->{post_index},$ref->{region},$ref->{city},$ref->{fio},$ref->{phone},$ref->{street},$ref->{home},$ref->{place},$ref->{dop});
 }
# &check_adres($ref);
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=check_adres'</script>  </body></HTML>"; exit;
}

sub delete_adres {# удаляем адрес
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my $id_user=$dbh->selectrow_array($sel_user);
 if(!$id_user){&view_info($ref); exit;}
 my $del=$dbh->do("delete from users_adres_$ref->{prefix} where id='$ref->{id_adres}' and id_pol='$id_user'");
# &check_adres($ref);
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=check_adres'</script>  </body></HTML>"; exit;
}

sub check_dostavka { #Пользователь выбирает способ доставки
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id,skidka from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka)=$dbh->selectrow_array($sel_user);
 if(!$id_user){
#&view_info($ref); exit;
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }

 my $tpl={};
 $ref->{my_modul_ini}="catalog_user_dostavka";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 #Выводим каталог товаров
 ($ref,$tpl)=list_basket($ref,$tpl);
 #Выводим каталог товаров
 my $dostavka_post=$ref->{user_db}->{data}->{params}->{dostavka_post}||'';
 my $dostavka_kurer=$ref->{user_db}->{data}->{params}->{dostavka_kurer}||'';
 my $dostavka_ftp=$ref->{user_db}->{data}->{params}->{dostavka_ftp}||'';
 my $dostavka_email=$ref->{user_db}->{data}->{params}->{dostavka_email}||'';
 my $checked="checked";
  if($dostavka_post){
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{post};
         $tpl->assign(
                   NAME_DOSTAVKA=>$name_dostavka,
                   ID_DOSTAVKA=>'post',
                   CHECK_ID_DOSTAVKA=>$checked
         );
         $tpl->parse("CATALOG_USER_DOSTAVKA_ROW",".CATALOG_USER_DOSTAVKA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  if($dostavka_kurer){
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{kurer};
         $tpl->assign(
                   NAME_DOSTAVKA=>$name_dostavka,
                   ID_DOSTAVKA=>'kurer',
                   CHECK_ID_DOSTAVKA=>$checked
         );
         $tpl->parse("CATALOG_USER_DOSTAVKA_ROW",".CATALOG_USER_DOSTAVKA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  if($dostavka_ftp){
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
        my $name_dostavka=$dostavka->{ftp};
         $tpl->assign(
                   NAME_DOSTAVKA=>$name_dostavka,
                   ID_DOSTAVKA=>'ftp',
                   CHECK_ID_DOSTAVKA=>$checked
         );
         $tpl->parse("CATALOG_USER_DOSTAVKA_ROW",".CATALOG_USER_DOSTAVKA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  if($dostavka_email){
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{email};
         $tpl->assign(
                   NAME_DOSTAVKA=>$name_dostavka,
                   ID_DOSTAVKA=>'email',
                   CHECK_ID_DOSTAVKA=>$checked
         );
         $tpl->parse("CATALOG_USER_DOSTAVKA_ROW",".CATALOG_USER_DOSTAVKA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  

# my $zag="Выбор способа доставки";
 my $zag=slovo(45,$ref->{l}); #
 my $all_cost=$ref->{my_temp}->{all_cost}; 
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $all_cost=$all_cost-($all_cost*($skidka/100));
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_user' and id='$ref->{id_adres}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 if($ref_adres->{id}){
 $tpl->assign(
                   ID_ADRES=>$ref_adres->{id},
                   COUNTRY=>$ref_adres->{country},
                   POST_INDEX=>$ref_adres->{post_index},
                   REGION=>$ref_adres->{region},
                   CITY=>$ref_adres->{city},
                   FIO=>$ref_adres->{fio},
                   PHONE=>$ref_adres->{phone},
                   STREET=>$ref_adres->{street},
                   HOME=>$ref_adres->{home},
                   PLACE=>$ref_adres->{place},
                   DOP=>$ref_adres->{dop},
                   ID_ADRES=>$ref_adres->{id},
 );
         $tpl->parse("CATALOG_USER_ADRES_ROW",".CATALOG_USER_ADRES_ROW");
         $tpl->clear_href(1);
}
 $tpl->assign(
           CURENCY =>$curency,
           ALL_COST =>$all_cost,
           SKIDKA =>$skidka,
           ZAG  =>$zag,
           TITLE=>"$zag $ref->{user_db}->{template}->{assign}->{TITLE}",
           DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
           KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub check_oplata { # выбор способа оплаты
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id,skidka from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka)=$dbh->selectrow_array($sel_user);
 if(!$id_user){
#&view_info($ref); exit;
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }

 if(!$ref->{path_db}){print "<script>location.href='http://$host_name'</script>"; exit;}

 my $tpl={};
 $ref->{my_modul_ini}="catalog_user_oplata";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 #Выводим каталог товаров
 ($ref,$tpl)=list_basket($ref,$tpl);
 #Выводим каталог товаров
 my $predoplata=$ref->{user_db}->{data}->{params}->{predoplata}||'';
 my $postoplata=$ref->{user_db}->{data}->{params}->{postoplata}||'';
 my $checked="checked";
      my $oplata=$oplata_rus;
         $oplata=$oplata_eng if $ref->{l} eq '2';
  if($postoplata){
      my $name_postoplata=$oplata->{postoplata};
         $tpl->assign(
                   NAME_OPLATA=>$name_postoplata,
                   ID_OPLATA=>'postoplata',
                   CHECK_ID_OPLATA=>$checked
         );
         $tpl->parse("CATALOG_USER_OPLATA_ROW",".CATALOG_USER_OPLATA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  if($predoplata){
      my $name_predoplata=$oplata->{predoplata};
         $tpl->assign(
                   NAME_OPLATA=>$name_predoplata,
                   ID_OPLATA=>'predoplata',
                   CHECK_ID_OPLATA=>$checked
         );
         $tpl->parse("CATALOG_USER_OPLATA_ROW",".CATALOG_USER_OPLATA_ROW");
         $tpl->clear_href(1);
                 $checked="";
  }
  

# my $zag="Выбор способа оплаты";
 my $zag=slovo(46,$ref->{l}); #
 my $all_cost=$ref->{my_temp}->{all_cost}; 
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $all_cost=$all_cost-($all_cost*($skidka/100));
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_user' and id='$ref->{id_adres}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 if($ref_adres->{id}){
 $tpl->assign(
                   ID_ADRES=>$ref_adres->{id},
                   COUNTRY=>$ref_adres->{country},
                   POST_INDEX=>$ref_adres->{post_index},
                   REGION=>$ref_adres->{region},
                   CITY=>$ref_adres->{city},
                   FIO=>$ref_adres->{fio},
                   PHONE=>$ref_adres->{phone},
                   STREET=>$ref_adres->{street},
                   HOME=>$ref_adres->{home},
                   PLACE=>$ref_adres->{place},
                   DOP=>$ref_adres->{dop},
                   ID_ADRES=>$ref_adres->{id},
 );
         $tpl->parse("CATALOG_USER_ADRES_ROW",".CATALOG_USER_ADRES_ROW");
         $tpl->clear_href(1);
}

 $tpl->assign(
           ID_DOSTAVKA  =>$ref->{id_dostavka},
           CURENCY =>$curency,
           ALL_COST =>$all_cost,
           SKIDKA =>$skidka,
           ZAG  =>$zag,
                   TITLE=>"$zag $ref->{user_db}->{template}->{assign}->{TITLE}",
                   DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
                   KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub check_data { # Проверка данных пользователя
 my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id,skidka from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka)=$dbh->selectrow_array($sel_user);
 if(!$id_user){
#&view_info($ref); exit;
 print "  <HTML>  <body><script>location.href='/cgi-bin/view/catalog.cgi?a=view_info'</script>  </body></HTML>"; exit;
 }

 my $tpl={};
 $ref->{my_modul_ini}="catalog_user_check_data";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 #Выводим каталог товаров
 ($ref,$tpl)=list_basket($ref,$tpl);
 #Выводим каталог товаров
 my $name_oplata='';
 my $name_dostavka='';
  if ($ref->{id_oplata} eq 'postoplata' || $ref->{id_oplata} eq 'predoplata'){
                my $oplata=$oplata_rus;
                $oplata=$oplata_eng if $ref->{l} eq '2';
            $name_oplata=$oplata->{$ref->{id_oplata}};
         $tpl->assign(
                   NAME_OPLATA=>$name_oplata,
                   ID_OPLATA=>$ref->{id_oplata},
                   ID_DOSTAVKA=>$ref->{id_dostavka},
                   ID_ADRES=>$ref->{id_adres},
         );
         $tpl->parse("CATALOG_USER_CHECK_DATA_OPLATA_ROW",".CATALOG_USER_CHECK_DATA_OPLATA_ROW");
         $tpl->clear_href(1);
  }
  if ($ref->{id_dostavka} eq 'post' ||
                $ref->{id_dostavka} eq 'kurer' ||
                $ref->{id_dostavka} eq 'ftp' ||
                $ref->{id_dostavka} eq 'email'){
                my $dostavka=$dostavka_rus;
                $dostavka=$dostavka_eng if $ref->{l} eq '2';
            $name_dostavka=$dostavka->{$ref->{id_dostavka}};
         $tpl->assign(
                   NAME_DOSTAVKA=>$name_dostavka,
                   ID_DOSTAVKA=>$ref->{id_dostavka},
                   ID_ADRES=>$ref->{id_adres},
         );
         $tpl->parse("CATALOG_USER_CHECK_DATA_DOSTAVKA_ROW",".CATALOG_USER_CHECK_DATA_DOSTAVKA_ROW");
         $tpl->clear_href(1);
  }

# my $zag="Проверка данных";
 my $zag=slovo(47,$ref->{l}); #
 my $all_cost=$ref->{my_temp}->{all_cost}; 
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 $all_cost=$all_cost-($all_cost*($skidka/100));
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_user' and id='$ref->{id_adres}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 dbdisconnect($dbh);
 if($ref_adres->{id}){
 $tpl->assign(
                   ID_ADRES=>$ref_adres->{id},
                   COUNTRY=>$ref_adres->{country},
                   POST_INDEX=>$ref_adres->{post_index},
                   REGION=>$ref_adres->{region},
                   CITY=>$ref_adres->{city},
                   FIO=>$ref_adres->{fio},
                   PHONE=>$ref_adres->{phone},
                   STREET=>$ref_adres->{street},
                   HOME=>$ref_adres->{home},
                   PLACE=>$ref_adres->{place},
                   DOP=>$ref_adres->{dop},
                   ID_ADRES=>$ref_adres->{id},
 );
         $tpl->parse("CATALOG_USER_ADRES_ROW",".CATALOG_USER_ADRES_ROW");
         $tpl->clear_href(1);
}
 $tpl->assign(
           CURENCY =>$curency,
           ALL_COST =>$all_cost,
           SKIDKA =>$skidka,
           ZAG  =>$zag,
                   TITLE=>"$zag $ref->{user_db}->{template}->{assign}->{TITLE}",
                   DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
                   KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub order { #Отправка подтверждения  товаров (в этой версии подтверждения нет - заказ идет сразу), обнуление корзины и вывод информации, что заказ принят
my $ref=shift;
 my $dbh=dbconnect;
 my $sel_user="select id,skidka,name,f_name,l_name,email from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka,$name,$f_name,$l_name,$email)=$dbh->selectrow_array($sel_user);
 my $strcook=$ref->{basket_cook}->{value}->[0];
if(!$ref->{basket_cook}->{value}->[0]) {
  print "Content-type:text/html\r\n\r\n";
  &view_basket($ref); 
  exit;
 }
 my $text_basket='';
 my $text_adres='';
 my $text_top='';
 my $text_bottom='';
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 my ($zip,$number);
if ($id_user && $strcook){
 my @ar_cook=split /\|/,$strcook;
 my @ar_id=();
 my %hash_col='';
 for(my $i=0;$i<=$#ar_cook;$i++){
     my @ar_id_col=split/\=/,$ar_cook[$i];
     push @ar_id,$ar_id_col[0];
     $hash_col{$ar_id_col[0]}=$ar_id_col[1];
 }
 my $dop="and id='$ar_id[0]'";
 if($#ar_id>0){
 my $id_for_select=join(',',@ar_id);
 $id_for_select=~s/\,$//gi;
 $dop="and id in ($id_for_select)";
 }
    $number=$dbh->selectrow_array("select max(number) from basket_$ref->{prefix}");
    $number++;
 my $sel="select * from $ref->{db_prefix}_catalog where 1 $dop order by name";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $all_cost=0;
   my @chars=("A".."Z",0..9);
      $zip=join("", @chars[ map {rand @chars} (1..7)]);
    while(my $ref_catalog=$sth->fetchrow_hashref){
    my $cost=$ref_catalog->{cost}*$hash_col{$ref_catalog->{id}};
                 $all_cost=$all_cost+$cost;
$ref_catalog->{short}=~s/<br>/ /gi;
$text_basket.=qq[
-----------------------------------------------------------
$ref_catalog->{name}
$ref_catalog->{short}
кол-во:   $hash_col{$ref_catalog->{id}} 
стоимость:$cost $curency
-----------------------------------------------------------
];
   my $ins_basket="insert into basket_$ref->{prefix} (number,id_pol,id_adres,id_cat,id_zakaz,status,col,cost,data_reg,id_dostavka,id_oplata)
                                                       values (?,?,?,?,?,?,?,?,now(),?,?)
                                  ";
   $ref->{id_adres}=$ref->{id_adres} || '0';
   $ref->{id_adres}=$ref->{id_adres} || '0';
   my $sth2=$dbh->prepare($ins_basket);
      $sth2->execute($number,$id_user,$ref->{id_adres},$ref_catalog->{id},$zip,1,$hash_col{$ref_catalog->{id}},$cost,$ref->{id_dostavka},$ref->{id_oplata});
      $sth2->finish;
    }
    $sth->finish;
 $all_cost=$all_cost-($all_cost*($skidka/100));
$text_basket.=qq[______________________________
Персональная скидка: $skidka %
Общая сумма заказа: $all_cost $curency
];
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_user' and id='$ref->{id_adres}'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 if($ref_adres->{id}){
 $text_adres=qq[
Адрес получателя:
--------------------------------------------
$ref_adres->{fio}
$ref_adres->{country}, $ref_adres->{post_index},
г.$ref_adres->{city},
ул.$ref_adres->{street}, д.$ref_adres->{home}, кв.$ref_adres->{place}
email:$email
доп: $ref_adres->{dop}
--------------------------------------------
];
}

#Подтвердите, пожалуйста ваш заказ по ссылке
#http://$host_name/cgi-bin/view/catalog.cgi?a=update_order&email=$email&zip=$zip
#my $dost_pr="";
 $text_top=qq[
Здравствуйте, $l_name $name $f_name !
Вы сделали заказ в интернет магазине $host_name.
Ваш заказ $zip:

];
#  my $name_postoplata=$dostavka_rus->{$ref->{id_dostavka}};
 $text_bottom=qq[
Доставка: $dostavka_rus->{$ref->{id_dostavka}}
Оплата: $oplata_rus->{$ref->{id_oplata}}

Оплатить заказ вы можете следующими способом:
банковский перевод:
http://$host_name/cgi-bin/view/catalog.cgi?a=view_oplata&who=bank&zip=$zip&number=$number
почтовый перевод:
http://$host_name/cgi-bin/view/catalog.cgi?a=view_oplata&who=bank&zip=$zip&number=$number


Если вы не заказывали товары, либо не хотите заказывать товары пройдите по ссылке:
http://$host_name/cgi-bin/view/catalog.cgi?a=del_order&zip=$zip

Или авторизуйтесь на сайте, зайдите в раздел ваши заказы и удалите заказ
];
my $fromemail=$ref->{user_db}->{data}->{params}->{email}||$ref->{user}->{email};
my $subject="Ваш заказ #$zip в магазине $host_name";
my $text=$text_top.$text_adres.$text_basket.$text_bottom;
my $from=$fromemail;
my $name_project="Интернет магазин $host_name";
&send_mail($email,$subject,$text,$from,$name_project);

my $toemail=$ref->{user_db}->{data}->{params}->{email}||$ref->{user}->{email};
my $subject="Новый заказ #$zip в магазине $host_name";
my $text="Пользователь сделал новый заказ\n".$text_top.$text_adres.$text_basket.$text_bottom;
my $from='';
my $name_project="Интернет магазин $host_name";
&send_mail($toemail,$subject,$text,$from,$name_project);
} 
  $strcook='';
  my  $expires='+12M';
  my @ar=($strcook);
  my $c = new CGI::Cookie(
                        -name => "basket_cook",
                        -value => \@ar,
#                        -value => '',
                        -expires => $expires,
                        -path => "/",
                        -domain => "$host_name"
                        );
 print CGI::header(-cookie=>$c);
#               &view_basket($ref);
# print $ref->{up_banner}."
#  <HTML>
# <head>
# <title>Заказ оформлен</title>
# </head>
#  <body>
#<center>
#На адрес электронной почты, указанный вами при регистрации отправлено письмо со сылкой для подтверждения заказа
#<br>
#Неподтвержденные заказы рассматриваться не будут. <br>
#<b>Спасибо за покупку !</b><br>
#<a href='http://$host_name'>перейти на главную страницу</a>
#</center>
#  </body>
#</HTML>"; 
 my $tpl={};
 if(!$ref->{user_cat}->{id}){&view_info($ref); exit;}
 $ref->{my_modul_ini}="catalog_zakaz_success";
 $ref->{zag}="Оплата заказа";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)


my $text_message=qq[
<center>
<b>Ваш заказ принят</b>, для оплаты ипользуйте:
<br><br>
<li><a href="http://$host_name/cgi-bin/view/catalog.cgi?a=view_oplata&who=bank&zip=$zip&number=$number" target=_blank>банковский перевод</a>
<br><br>
<li><a href="http://$host_name/cgi-bin/view/catalog.cgi?a=view_oplata&who=bank&zip=$zip&number=$number" target=_blank>почтовый перевод</a>

<br>
<br>
<b>Спасибо за покупку !</b><br>
<a href='http://$host_name/base/view/catalog/&a=view_orders'>перейти на страницу заказов</a>
</center>
];
 $tpl->assign(
   ZAKAZ_SUCCESS=> $text_message
 );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############

}

sub update_order { # Подтверждение заказа
my $ref=shift;
  my $dbh=dbconnect;
 my $sel_user="select id from users_cat_$ref->{prefix} where email='$ref->{email}'";
 my ($id_user)=$dbh->selectrow_array($sel_user);
 my $upd=0;
 if($id_user){
  my $status=$dbh->selectrow_array("select status from basket_$ref->{prefix} where id_zakaz='$ref->{zip}' and id_pol='$id_user' limit 1");
  if(!$status){
  $upd=$dbh->do("update basket_$ref->{prefix} set status='1' where id_zakaz='$ref->{zip}' and id_pol='$id_user'");
  }
 }
 if($upd){
 my $dbh=dbconnect;
 my $all_cost=0;
 my $id_pol='';
 my $id_adres='';
 my $text_basket='';
 my $text_adres='';
 my $text_top='';
 my $text_bottom='';
 my $id_dostavka='';
 my $id_oplata='';
 my $sel_basket="select * from basket_$ref->{prefix} where id_zakaz='$ref->{zip}'";
 my $sth_b=$dbh->prepare($sel_basket);
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
  $sth_b->execute;
 while(my $ref_basket=$sth_b->fetchrow_hashref){
         my $sel="select * from $ref->{db_prefix}_catalog where id=$ref_basket->{id_cat}";
         my $sth=$dbh->prepare($sel);
     $sth->execute;
     my $ref_catalog=$sth->fetchrow_hashref;
     my $cost=$ref_basket->{cost};
     $all_cost=$all_cost+$cost;
$ref_catalog->{short}=~s/<br>/ /gi;
$text_basket.=qq[
-----------------------------------------------------------
$ref_catalog->{id}|$ref_basket->{col}x$ref_catalog->{name} | $cost $curency
$ref_catalog->{short}
-----------------------------------------------------------
];
    $sth->finish;
 $id_pol=$ref_basket->{id_pol};
 $id_adres=$ref_basket->{id_adres};
 $id_dostavka=$ref_basket->{id_dostavka};
 $id_oplata=$ref_basket->{id_oplata};
 }
 $sth_b->finish;
 my $sel_user="select id,skidka,name,f_name,l_name,email from users_cat_$ref->{prefix} where id='$id_pol'";
 my ($id_user,$skidka,$name,$f_name,$l_name,$email)=$dbh->selectrow_array($sel_user);
 $all_cost=$all_cost-($all_cost*($skidka/100));
$text_basket.=qq[------------------------------
Персональная скидка: $skidka %
Общая сумма заказа: $all_cost $curency
];
 my $sel="select * from users_adres_$ref->{prefix} where id_pol='$id_pol' and id='$id_adres'";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_adres=$sth->fetchrow_hashref||{};
    $sth->finish;
 if($ref_adres->{id}){
 $text_adres=qq[
Адрес получателя:
--------------------------------------------
$ref_adres->{fio}
$ref_adres->{country}, $ref_adres->{post_index},
 г.$ref_adres->{city},
 ул.$ref_adres->{street}, д.$ref_adres->{home}, кв.$ref_adres->{place}
--------------------------------------------
email: $email
Дополнительно: 
тел.: $ref_adres->{phone}
$ref_adres->{dop}
];
 }
 $text_top=qq[
Здравствуйте !
Пользователь  $l_name $name $f_name  cделал заказ в интернет магазине $host_name.
Заказ $ref->{zip}:

$text_adres
____________________________________________________________
];
      my $dostavka=$dostavka_rus;
        $dostavka=$dostavka_eng if $ref->{l} eq '2';
      my  $name_dostavka=$dostavka->{$id_dostavka};
      my $oplata=$oplata_rus;
        $oplata=$oplata_eng if $ref->{l} eq '2';
      my  $name_oplata=$oplata->{$id_oplata};
 $text_bottom=qq[
Доставка: $name_dostavka
Оплата: $name_oplata

Пройдите в администрирование каталога товаров и выберите ссылку Заказы
];
my $toemail=$ref->{user_db}->{data}->{params}->{email}||$ref->{user}->{email};
my $subject="Новый заказ #$ref->{zip} в магазине $host_name";
my $text=$text_top.$text_basket.$text_bottom;
my $from='';
my $name_project="Интернет магазин $host_name";
&send_mail($toemail,$subject,$text,$from,$name_project);

print $ref->{up_banner}.qq[
  <HTML>
 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
 <title>Подтверждение заказа</title>
 </head>
  <body>
<center>
Ваш заказ принят
<br>
<b>Спасибо за покупку !</b><br>
<a href='http://$host_name'>перейти на главную страницу</a>
</center>
  </body>
</HTML>
];

#$text_top <hr>
#$text_basket <hr>
#$text_bottom <hr>

}
else {
print $ref->{up_banner}.qq[
  <HTML>
 <head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
 <title>Подтверждение заказа</title>
 </head>
  <body>
<center>
Введен ошибочный код заказа, либо заказ уже подтвержден
<br>
<a href='http://$host_name'>перейти на главную страницу</a>
</center>
  </body>
</HTML>
];

}
}

sub del_order {
my $ref=shift;
 my $dbh=dbconnect;
 if(!$ref->{user_cook}->{value}->[0]){
  &view_info($ref);exit;
 }
 my $sel_user="select id,skidka,name,f_name,l_name,email from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_user,$skidka,$name,$f_name,$l_name,$email)=$dbh->selectrow_array($sel_user);
 my $upd=undef;
 if($id_user){
  $upd=$dbh->do("delete from basket_$ref->{prefix} where id_zakaz='$ref->{zip}' and id_pol='$id_user' and status!='2'");
 }
 if($upd>=1){
print $ref->{up_banner}.qq[
  <HTML>
 <head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
 <title>Удаление заказа</title>
 </head>
  <body>
<center>
Ваш заказ был удален
<br>
<b>Спасибо что воспользовались нашим магазином !</b>
<br>
<a href='http://$host_name'>перейти на главную страницу</a>
</center>
  </body>
</HTML>
];
 }
 else {
print $ref->{up_banner}.qq[
  <HTML>
 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
 <title>Удаление заказа</title>
 </head>
  <body>
<center>
Введен ошибочный код заказа, либо заказ уже подтвержден, либо такого заказа не существует
<br>
<a href='http://$host_name'>перейти на главную страницу</a>
</center>
  </body>
</HTML>
];

}
}

sub view_orders {
 my $ref=shift;
 my $dbh=dbconnect;
 if(!$ref->{user_cook}->{value}->[0]){
   &view_info($ref);exit;
 }
 my $sel_user="select id,skidka,name,f_name,l_name,email from users_cat_$ref->{prefix} where email='$ref->{user_cook}->{value}->[0]' and pass='$ref->{user_cook}->{value}->[1]'";
 my ($id_pol,$skidka,$name,$f_name,$l_name,$email)=$dbh->selectrow_array($sel_user);
 if(!$id_pol){
   &view_info($ref);exit;
 }

 my $tpl={};
 $ref->{my_modul_ini}="catalog_user_view_orders";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 #для перехода по страницам
 my $CountPage=5;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(distinct id_zakaz) from basket_$ref->{prefix} where id_pol='$id_pol'";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #для перехода по страницам
 my $sel="select * from basket_$ref->{prefix}
         where id_pol='$id_pol'
         group by id_zakaz
         order by data_reg desc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 my $cost_all=$dbh->selectrow_array("select sum(cost) from basket_$ref->{prefix} where id_pol='$id_pol'")||0;
  $tpl->assign(
             COUNT =>$count,
             COST_ALL =>$cost_all,
             CURENCY =>$curency
   );
 my $skidka=$ref->{user_cat}->{skidka}||0;
    $cost_all=$cost_all-($cost_all*($skidka/100));
    while(my $ref_basket=$sth->fetchrow_hashref){
             my ($data,$hour)=split / /,$ref_basket->{data_reg};
             my ($y,$m,$d)=split /\-/,$data;
                 my $data_pr="$d.$m.$y";
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
      my $status=$status_rus;
         $status=$status_eng if $ref->{l} eq '2';
                 if($ref_adres->{id}){
                        $fio=qq[<b>$ref_adres->{fio}</b><br>
                        $ref_adres->{country},
                        $ref_adres->{post_index},
                         г.$ref_adres->{city},
                         ул.$ref_adres->{street},
                         д.$ref_adres->{home},
                         кв.$ref_adres->{place},
                         тел. $ref_adres->{phone}
                ];
                }
                 my $col_pokupok=$dbh->selectrow_array("select sum(col) from basket_$ref->{prefix} where id_zakaz='$ref_basket->{id_zakaz}'")||0;
                 my $cost=$dbh->selectrow_array("select sum(cost) from basket_$ref->{prefix} where id_zakaz='$ref_basket->{id_zakaz}'")||0;
                    $cost=$cost-($cost*($skidka/100));
                 my $name_status=$status->{$ref_basket->{status}};
         $tpl->assign(
                                DATA    => $data_pr,
                                FIO    => $fio,
                                KOL    => $col_pokupok,
                                COST    => $cost,
                                NUMBER    => $ref_basket->{number},
                                CURENCY    => $curency,
                                NAME_STATUS    => $name_status,
                                ID_ZAKAZ      =>$ref_basket->{id_zakaz}
         );
         $tpl->parse("CATALOG_USER_VIEW_ORDERS_ROW",".CATALOG_USER_VIEW_ORDERS_ROW");
         $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
    #Переход по страницам
    my $host_name1="/cgi-bin/view/catalog.cgi?a=view_orders";
    my $perehod=&page_down($host_name1,$kol,$PageIn,$p_n,$CountPage);
    $tpl->assign (
            PEREHOD=>$perehod
    );
    #Переход по страницам
 my $zag="Ваши заказы";
 $tpl->assign(
                   SKIDKA =>$skidka,
                   ZAG  =>$zag,
                   TITLE=>"$zag $ref->{user_db}->{template}->{assign}->{TITLE}",
                   DESCRIPTION=>"$ref->{user_db}->{template}->{assign}->{DESCRIPTION} $zag",
                   KEYWORDS=>"$ref->{user_db}->{template}->{assign}->{KEYWORDS} $zag"
           );
 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############

}

sub view_oplata {
 my $ref=shift;
 if(!$ref->{user_cat}->{id}){&view_info($ref); exit;}
 my $dbh=dbconnect;
 my $tpl={};
 if($ref->{who} eq 'bank'){
   $ref->{my_modul_ini}="catalog_bank";
 }elsif($ref->{who} eq 'pochta'){
   $ref->{my_modul_ini}="catalog_pochta";
 }
 $ref->{index_ini}="index_simple";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)
 my $sel="select * from basket_$ref->{prefix}
         where id_pol='$ref->{user_cat}->{id}' and id_zakaz='$ref->{zip}' and number='$ref->{number}'
         group by id_zakaz
         ";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
 my $ref_basket=$sth->fetchrow_hashref;    
 if (!$ref_basket->{id}){print qq[<br><br><center>Error request</center>]; exit;}
 my $curency=$ref->{user_db}->{data}->{params}->{curency}||'$';
 my $cost_all=$dbh->selectrow_array("select sum(cost) from basket_$ref->{prefix} where id_pol='$ref->{user_cat}->{id}'")||0;
 my ($data,$hour)=split / /,$ref_basket->{data_reg};
 my ($y,$m,$d)=split /\-/,$data;
 my $data_pr="$d.$m.$y";
 my $sel_adres="select * from users_adres_$ref->{prefix} where id_pol='$ref_basket->{id_pol}'
                and id='$ref_basket->{id_adres}'";
 my $sth2=$dbh->prepare($sel_adres);
    $sth2->execute;
 my $ref_adres=$sth2->fetchrow_hashref||{};
    $sth2->finish;
 my $cost=$dbh->selectrow_array("select sum(cost) from basket_$ref->{prefix} where id_zakaz='$ref_basket->{id_zakaz}'")||0;
 my $skidka=$ref->{user_cat}->{skidka}||0;
    $cost=$cost-($cost*($skidka/100));
 my $toemail=$ref->{user_db}->{data}->{params}->{email}||$ref->{user}->{email};
    
 my $adres=qq[
                        $ref_adres->{country},
                        $ref_adres->{post_index},
                         г.$ref_adres->{city},
                         ул.$ref_adres->{street},
                         д.$ref_adres->{home},
                         кв.$ref_adres->{place}
         ];
 my $fio=$ref_adres->{fio};
    $fio=~s/\s+/ /gi;    
 my  $summa1=int($cost);
 my  $summa_kop="00";
     if($summa_kop=~/\.|\,/gi){
       $summa_kop=~s/^([0-9]+)\.|\,([0-9])$/$2/gi;
     }
 my  $summa_propis='';
     
     $summa_propis=propis($summa1);
 
    $tpl->assign(
             URL =>$host_name,
             SUMMA =>$cost,
             SUMMA1 =>$summa1,
             SUMMA_KOP =>$summa_kop,
             NUMBER =>$ref_basket->{number},
             CURENCY =>$curency,
             USER_NAME => $ref_adres->{fio},
             USER_NAME_EMAIL => $fio,
             USER_ADRES => $adres,
             DATE_REG =>$data_pr,
             EMAIL =>$toemail
    );

 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}
sub ok_authorize {
 my $ref=shift;
 my $tpl={};
 if(!$ref->{user_cat}->{id}){&view_info($ref); exit;}
 $ref->{my_modul_ini}="catalog_ok_authorize";
 $ref->{zag}="Успешная авторизация";
 #выводим начало (считываем параметры и вcе такое)
 ($tpl,$ref)=tplbegin($ref);
 #выводим начало (считываем параметры и все такое)

 ############
  tplend($ref,$tpl); #печатаем содержимое
 ############
}

sub propis { #Выводим цифровую запись числа в слова
 my  $slovo=shift;
 return $slovo;
}

1;