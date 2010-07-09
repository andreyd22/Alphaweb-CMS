#!/usr/bin/perl

use Modules::Constructor qw(Get_Param get_structure);
#use strict;

my $ref=Get_Param;
#use Data::Dumper;
$ref=get_structure($ref);

my $mod=$ref->{user_db}->{data}->{$ref->{id}}->{mod};
my $lang_now=$ref->{user_db}->{data}->{$ref->{id}}->{lang};
my $mods=$ref->{user_db}->{mods};
my %mods=%$mods;
use CGI qw(:standard); 
my $flg=0; #ставим флаг, что такого модуля нет.
#print "Content-type:text/html\r\n\r\n";
foreach my $key (keys(%mods)){ #Проходим по хешу всех модулей
   my $key1=$key;
   $key1=~s/\.cgi$//gi;
   if($key1 eq $mod){$flg=1;last;}
}
if($ref->{lang}||(!$ref->{lang}&&!$lang_now)){
   my $all_lang="ru en de fr it";
   my @ar= split / /,$all_lang;
   my $ok=grep $ref->{lang}=~$_, @ar;
  if(!$ok){
  print header (-type => 'text/html; charset=windows-1251',-status => '404 Not Found');
#print "Content-type:text/html\r\n\r\n";
#print qq[ok1 <br>]; exit;
        	  print "<script>location.href='/error404$ref->{lang}.html'</script>"; 
  exit;}
}
if(!$ref->{id}||!$mod||!$flg||($ref->{lang}&&$ref->{lang} ne $lang_now)){
		print "Content-type:text/html\r\n\r\n";
  		print "<script>location.href='/error404$ref->{lang}.html'</script>"; 
	 	exit;
 
 }


eval {
$SIG{ALRM} = sub { die "alarm time out\n" };
alarm 5;
require "./view/$mod.cgi";

};

if ( $@ eq "alarm time out\n" ){
 print "Content-type:text/html\r\n\r\n";
 print "<center> Извините сервер перегружен. <br> Повторите запрос через минуту!</center>";
 exit;
}

exit;
1;