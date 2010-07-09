#!/usr/bin/perl
#модуль документов
 print "Content-type:text/html\r\n\r\n";
 $|=1;
 use lib "../";
 use Modules::Constructor_view;

 #use strict;
 use CGI::Carp qw(fatalsToBrowser);
# print qq[lang  OK]; exit;

 my $ref=Get_Param_view||{};

   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);

  #если есть верхн€€ часть выводим
  if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){
	 $ref->{tpl_}="$ref->{module_name}.tpl";
	 $ref->{tpl_text}="user_db.$ref->{id}.data";
  }


 # кэшировать шаблоны
 # $ref->{cach}="yes";
 #print qq[$ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; ];
 #print qq[$ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; ];
 $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 

 #use Data::Dumper;
 #print Dumper($ref);


 print_($ref);


#1;