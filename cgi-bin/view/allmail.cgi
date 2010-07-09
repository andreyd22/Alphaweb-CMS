#!/usr/bin/perl 
 $|=1;
 use lib "../";
 use Modules::Constructor qw (Get_Param dbconnect dbdisconnect $host_name
                              $path_index send_mail);
use CGI::Carp qw(fatalsToBrowser);
#use strict;
my $ref=Get_Param;
print "Content-type:text/html\r\n\r\n";
if($ref->{a} eq '' && $ref->{email}){
if($ref->{email}!~/^[0-9a-z\_\-\.]+\@[0-9a-z\-]+\.[0-9a-z]+$/i){
print qq[<script>alert('Введен неверный email адрес');history.go(-1)</script>];exit;
}
my $dbh=dbconnect();

my @chars=("A".."Z",0..9);
my $zip=join("", @chars[ map {rand @chars} (1..32)]);

my $ins="insert into user_sub (email,language,zip,ip) VALUES (?,?,?,?)";
my $sth=$dbh->prepare($ins);
my $ok=$sth->execute($ref->{email},"russian",$zip,$ref->{ip});
   $sth->finish;

if($ok==1){
   print qq[<script>alert('Ваш емайл добавлен в базу рассылки сайта $host_name');</script>];
}else{
   print qq[<script>alert('Данный емайл уже добавлен в базу рассылки сайта $host_name');</script>];
}

if($ref->{email} && $ok==1){
     my $text=qq[
Здравствуйте!
Ваш адрес добавлен в список рассылки сайта $host_name

Если вы не подписывались на новости пройдите по следующей ссылке:
http://$host_name/cgi-bin/allmail.cgi?a=delemail&email=$ref->{email}&zip=$zip
];
      my $subject=qq[Ваш адрес добавлен в базу рассылки проекта $host_name];
      &send_mail($ref->{email},$subject,$text);
}
}

if($ref->{a} eq 'delemail' && $ref->{email} && $ref->{zip}){
my $dbh=dbconnect();
my $del="select count(*) from user_sub where email=? and zip=?";
my $sth=$dbh->prepare($del);
	$sth->execute($ref->{email},$ref->{zip});
my $ok=$sth->fetchrow_array;	
print qq[...];
   $sth->finish;
if($ok>0){
my $del2="delete from user_sub where email=? and zip=?";
my $sth2=$dbh->prepare($del2);
my $ok2=$sth2->execute($ref->{email},$ref->{zip});
   $sth2->finish;
     my $text=qq[
Здравствуйте!
Ваш адрес удален из списка рассылки сайта $host_name 

];
      my $subject=qq[Ваш адрес удален из базы рассылки сайта $host_name];
      &send_mail($ref->{email},$subject,$text);

}

print qq[<script>alert('Ваш емайл удален из базы рассылки сайта $host_name');</script>];
}
print qq[<script>location.href="/";</script>];
1;