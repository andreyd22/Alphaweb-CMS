#!/usr/bin/perl
#!!!Выводим первую страницу конструктора, где выводим все доступные модули
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
 my $err;
  ($ref->{l}, $err)=data_filter($ref->{l});
  ($ref->{mes}, $err)=data_filter($ref->{mes});
  ($ref->{a}, $err)=data_filter($ref->{a});

#     use Data::Dumper;
#     print Dumper($ref);
#     exit;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><META HTTP-EQUIV='Refresh' CONTENT='0;
    URL=/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes'></HEAD></HTML>
     ";
 exit;
 }
#!!!Проверка sid пользователя!!!#

if ($ref->{a} eq ''){main($ref)} #Выводим в фреймах меню и страницу о модулях загруженных по умолчанию 

sub main {
 my $ref=shift;
     my $def={  "main"=>"/constructor.html.$ref->{l}",
                "text"=>"/constructor_main.html.$ref->{l}",
                "modules"=>"/constructor_modules.html.$ref->{l}",
                "about_modules"=>"/constructor_about_modules.html.$ref->{l}"
        };
 my $title=slovo(31,$ref->{l}); #загруженные модули
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
 opendir DIR,"../mod" or die $!;
 my @ar_files=readdir(DIR);
 close DIR;
 my @ini_files=();

# use Storable;
# my $user_db = retrieve $ref->{path_db};
my $user_db={};
 $user_db->{mods}={};

 for (my $i=0;$i<=$#ar_files;$i++){
   if($ar_files[$i]=~/\.ini$/){
   push @ini_files,$ar_files[$i];
   }
 }
my $dbh=dbconnect();

if(!table_exists(qq[`mod_scrt`])){
 my $sql = qq[
CREATE TABLE `mod_scrt` (
`id` INT NOT NULL AUTO_INCREMENT ,
`script` VARCHAR( 25 ) NOT NULL ,
`name` VARCHAR( 100 ) NOT NULL ,
`name2` VARCHAR( 100 ) NOT NULL ,
`opis` VARCHAR( 250 ) ,
`opis2` VARCHAR( 250 ),
`status` VARCHAR( 25 ),
 PRIMARY KEY ( `id` ),
 UNIQUE KEY `id` (`id`)
) 
 ]; 
 my $create=$dbh->do($sql);
};

=r3
 opendir DIR,"../mod" or die $!;
 my @ar_files=readdir(DIR);
 close DIR;
  for (my $i=2;$i<=$#ar_files;$i++){
   if($ar_files[$i]=~/\.ini$/){
   push @ini_files,$ar_files[$i];
   }
  };
=cut

for(my $j=0;$j<=$#ini_files;$j++){
   open A, "../mod/$ini_files[$j]";
   my $str=<A>;
   chomp($str);
   close A;
   my ($script,$name,$name2,$opis,$opis2,$status)=split /\=/,$str;

   if ($status eq 'visible')
   {          $user_db->{mods}->{$script}=[$name,$name2];
           my $yes=$dbh->selectrow_array("select count(*) from mod_scrt where script='$script'");
	   if ($yes==0)
	   {	  	
		   my $sql="insert into mod_scrt (script,name,name2,opis,opis2,status) values (?,?,?,?,?,?)";
		   my $sth=$dbh->prepare($sql);
		   $sth->execute($script,$name,$name2,$opis,$opis2,$status);
		   $sth->finish;
	   };
     if($ref->{l}==1){
      $tpl->assign(
            NAME=>$name,
            OPIS=>$opis
      );
     }else{
      $tpl->assign(
            NAME=>$name2,
            OPIS=>$opis2
      );
     }
      $tpl->parse("MODULES",".modules");
      $tpl->clear_href(1);

   }

};

dbdisconnect($dbh);

# store $user_db, $ref->{path_db};

 $tpl->parse(MAIN=>"about_modules");
 $tpl->clear_href(1);
 $tpl->parse(TEXT=>"text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
#     use Data::Dumper;
#     print Dumper($user_db->{mods});
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear();
}
