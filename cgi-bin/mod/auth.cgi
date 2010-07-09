#!/usr/bin/perl
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
  $ref->{sid}=time;
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
  print "Нет главного шаблона "; exit;
}

#!!!Проверка sid пользователя!!!#
$ref->{sid}=time;
if ($ref->{a} eq ''){auth($ref)} #Выводим в фреймах меню и страницу о модулях загруженных по умолчанию 


sub auth {
    my $ref=shift;
#     use Data::Dumper;
#     print Dumper(%users);
     print qq[
<html>
<head>
<title>Web builder - create your own web site</title>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=WINDOWS-1251">
</head>
<script>
var name = navigator.appName;
//var ver  = navigator.appVersion;
var ver  = navigator.userAgent;
//alert('Вы используете браузер '+ver+'\\nДля корректной работы используйте Microsoft Internet Explorer 5.5 и выше');
</script>
<FRAMESET rows="*,0" border=0>
<FRAMESET cols="250,*" border=0>
    <FRAME src="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}" name='menu'>
    <FRAME src="/cgi-bin/mod/about.cgi?sid=$ref->{sid}&l=$ref->{l}" name='main'>
  <NOFRAMES>
    <P>Links</P>
    <UL>
      <LI><A href="/cgi-bin/mod/menu.cgi?sid=$ref->{sid}&l=$ref->{l}">MENU</A></LI>
      <LI><A href="/cgi-bin/mod/about.cgi?sid=$ref->{sid}&l=$ref->{l}">Default page</A></LI>
    </UL>
  </NOFRAMES>
</FRAMESET>
    <FRAME src="" name='load'>
</FRAMESET>
</html>
     ];
}

