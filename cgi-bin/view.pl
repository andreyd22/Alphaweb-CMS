#!/usr/bin/perl
####!!! ����������� ������������� �������
#use Storable;
use Modules::Constructor qw (dbconnect dbdisconnect $host_name data_filter Get_Param);
use strict;
my $ref=Get_Param;
 my $err;
  ($ref->{l}, $err)=data_filter($ref->{l});
  ($ref->{mes}, $err)=data_filter($ref->{mes});
  ($ref->{mess}, $err)=data_filter($ref->{mess});
  ($ref->{a}, $err)=data_filter($ref->{a});
##�������� �� ������������� ������� 
my $dbh=dbconnect();
my $col=$dbh->selectrow_array("select count(*) from admin_groups");
if($col<=0){
 #COMMENT = '������� ������������� ������� AlphaWeb';
 my $sql = qq[
CREATE TABLE `admin_groups` (
`id` INT NOT NULL AUTO_INCREMENT ,
`login` VARCHAR( 25 ) NOT NULL ,
`pass` VARCHAR( 32 ) NOT NULL ,
`name` VARCHAR( 100 ) NOT NULL ,
`opis` VARCHAR( 255 ) NOT NULL ,
`add_razdel` TINYINT DEFAULT '0' NOT NULL ,
`edit_design` TINYINT DEFAULT '0' NOT NULL ,
`grant` TINYINT DEFAULT '0' NOT NULL ,
`email` VARCHAR( 150 ) NOT NULL ,
`status` TINYINT DEFAULT '1' NOT NULL ,
 PRIMARY KEY ( `id` ),
 UNIQUE KEY `login` (`login`)
) 
 ]; #��������� ������������ � ������� ������� � ������� 123
 my $ins=qq[
INSERT INTO `admin_groups` 
 VALUES (1, 'admin', md5(123), '�������������', '�������� ������� �������, ����� ��������� �������������', 1, 1, 1, '', 1)
 ];
 my $drop=$dbh->do("drop table admin_groups");
 my $create=$dbh->do($sql);
 my $ins=$dbh->do($ins);
 if($ins!=1){
print "Content-type:text/html\r\n\r\n";
print qq[
<html>
<head>
 <title>������ ����������� ��</title>
</head>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css">
<body>
<br><br><center><b>��������� ����������� MySql</b>
<br><br>
</center>
</body>
</html>
];  exit;
 }            
# print qq[
#  Processing... <br>
#  drop $drop ok <br>
#  create: $create  ok <br>
#  ins $ins ok
# ];
}
    dbdisconnect($dbh);

if($ref->{a} eq 'auth'){ &auth($ref);}
elsif($ref->{a} eq 'logout'){ &logout($ref);}
else{
print "Content-type:text/html\r\n\r\n"; &main($ref);
}

sub main { #������� ����� �����������
 my $ref=shift;
 my $mess='';

 if($ref->{mess}||$ref->{mes}) {$mess="������ �����������";}
 if($ref->{mess} eq 'rus_error'){$mess="����� � ������ ������ ���� � ��������� ��������� � ��� ��������";}
 if($ref->{mess} eq 'logout_ok'){$mess="";}
 if($ref->{mess} eq 'error'){$mess="������ �����������";}
 if($ref->{mess} eq 'disc_full'){$mess="�� ������� ������������ ����� ($ref->{free_all_size} byte) ��� ������ �������
                                <br>���������� � ������ ��������� ������ ��������";}
 print qq[
<html> 
 <head>
  <title>����������� ������������</title>
 </head>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css">
 <body>
 <br><br><br><br><br>
  <table bgcolor=#EEEEEE width=320 align=center>
   <tr bgcolor=#FFFFFF>
    <td align=center colspan=2><b>����������� ������������<b></td>
   </tr><form action="/cgi-bin/view.pl" method=post>
   <tr>
    <td align=center colspan=2><b style="color:red">$mess</b></td>
   </tr>
   <tr bgcolor=#FFFFFF><td><b>�����:</b></td><td><input name=login value="$ref->{login}"></td></tr>
   <tr bgcolor=#FFFFFF><td><b>������:</b></td><td><input name=pass type=password></td></tr>
   <tr bgcolor=#FFFFFF><td align=center colspan=2><input type="submit" value="��������������"></td></tr>
   <input type=hidden name=a value="auth">
   <tr> 
    <td colspan=2><p>��� �������� ������ � �������� ��������� ������� 
    <b style="color:red">Internet Explorer 6.0</b>, � ����� �� ����� ���������� ������ ���� �������� ��������� 
    <b style="color:red">cookie</b> � <b style="color:red">JavaScript</b></p></td>
   </tr>
  </table></form>
 </body>
</html> 
 ];
 }
sub auth { #�����������
 my $ref=shift;
#  my  $expires='+1h'; #������ ��� �� ������ ���� ��������
  if(!$ref->{login}||!$ref->{pass}||$ref->{login}!~/[a-z0-9\,\.\[\;\']+/gi||$ref->{pass}!~/[a-z0-9\,\.\[\;\']+/gi){
   print "Content-type:text/html\r\n\r\n"; 
   $ref->{mess}="rus_error";
   &main($ref); exit;}
   my $dbh=dbconnect();
   my $sel="select count(*) from admin_groups where login=? and pass=md5(?)";
   my $sth=$dbh->prepare($sel);
 	$sth->execute($ref->{login},$ref->{pass});
   my $count=$sth->fetchrow_array();
	$sth->finish;
   dbdisconnect($dbh);
 #  print "Content-type:text/html\r\n\r\n"; 
#    print qq[$count];
  if($count==1){
   my @ar=($ref->{login},$ref->{pass});
   my $time=time;
   my $c = new CGI::Cookie(
                        -name => "admin_groups",
                        -value => \@ar,
#                        -expires => $expires,
#                        -path => "/",
#                        -domain => "$host_name"
                        );
  print CGI::header(-cookie=>$c, -charset=> 'win-1251'); 
#exit;
  #������ ��������� �� ����� ��������� ���� ������
  print qq[
   <html>
    <head><title>�������� �����������</title></head>
    <body>
    <script>location.href="/cgi-bin/mod/auth.cgi?time=$time"</script>
    </body>
   </html>
  ];
 }else{
   print "Content-type:text/html\r\n\r\n"; 
   $ref->{mess}='error';
   &main($ref); exit;
 }
}
sub logout {
   my @ar=('','');
   my $c = new CGI::Cookie(
                        -name => "admin_groups",
                        -value => \@ar,
#                        -expires => $expires,
                        -path => "/",
                        -domain => "$host_name"
                        );
  print CGI::header(-cookie=>$c); 
  #������ ��������� �� ����� ��������� ���� ������
  print qq[
   <html>
    <head><title>�� ����� �� �������</title></head>
    <body>
    <script>location.href="/cgi-bin/view.pl"</script>
    </body>
   </html>
  ];

}