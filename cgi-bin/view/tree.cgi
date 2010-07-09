#!/usr/bin/perl
#модуль структуры сайта
 $|=1;
 use lib "../";
 use Modules::Constructor qw (Get_Param $host_name &check_auth);
 use Modules::Constructor_view;
 use strict;

 print "Content-type:text/html\r\n\r\n";
my $ref=Get_Param_view||{};

 $ref->{index_tpl} = "index.tpl"; 
 $ref->{tpl_}="tree.tpl";
 my $itt=0; 
    my @ar_tree=();
if ($ref->{'a'} eq '') {$ref=all_tree($ref);} #Вывод каталога

 print_($ref);


sub all_tree {
    my $ref=shift;

 #если есть верхняя часть выводим
 if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){

 	$ref->{tpl_top}="user_db.$ref->{id}.data";
 }
    $ref=make_tree($ref);

    $ref->{ar_data}=\@ar_tree;

return $ref;
}


sub make_tree {
my $ref=shift;
 # аварийный выход, если разделов > 250
 if($itt>250){print qq[exit!!! ]; return $ref}

 $ref->{id_parent} = '0' if !$ref->{id_parent};
 #переход по страницам
 my $sel="select * from structure where parent='$ref->{id_parent}' and (visible = 'tree1=1,menu1=1' or visible = 'tree1=1,menu1=') order by id_n";
 my $sth=$ref->{dbh}->prepare($sel);
 my $col = $sth->execute;
    #print qq[$sel<br>];
    if($col==0){return $ref;}
    $itt++;
    my $nbsp='';
    for (my $i=1;$i<$itt;$i++){
	$nbsp.="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    }
    while(my $ref_news=$sth->fetchrow_hashref){
	 #print qq[$ref_news->{name}<br>];
	 $ref_news->{nbsp} = $nbsp;
      	 push @ar_tree,$ref_news;
	 $ref->{id_parent}=$ref_news->{id};
	 $ref=make_tree($ref);
    }

    $sth->finish;

    return $ref;
}