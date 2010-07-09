#!/usr/bin/perl 
#!!!Менеджер пользователей системы
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 use MySQL::Backup;
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
if(!$ref->{admin_ref}->{grant}){
print "Content-type:text/html\r\n\r\n";
print qq[<center>У вас недостаточно прав на это действие</center>]; exit;
}
if ($ref->{a} eq 'backup'){backup($ref)} #Выдаем файл структуры


sub backup {
 my $ref=shift;
# print "Content-Type: multipart/x-mixed-replace;boundary=boundary\n\n";
print "Content-Type: application/x-perl; Content-Disposition: attachment; filename=users_db\n\n";
#open A, "$ref->{path_db}";
# while(<A>){
#my $dbh=&dbconnect;

#my $sql=qq[select * from structure];
#my $sth=$dbh->prepare($sql);
# $sth->execute;
#while (){
# my @ref_st=$sth->dump_results;
# print join(',',@ref_st);
  #}
#  $sth->finish;
#  dbdisconnect($dbh);
# close A; 
}