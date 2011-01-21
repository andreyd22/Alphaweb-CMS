#!/usr/bin/perl
#модуль новостной лентыgallery view
 $|=1;
 use lib "../";
 use Modules::Constructor qw (dbconnect dbdisconnect page_down $host_name  &get_structure);
 use Modules::Constructor_view;
 use strict;
#print qq[$path_index];
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param_view||{};
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);

 # кэшировать шаблоны
 # $ref->{cach}="yes";
 $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 
 $ref->{tpl_}="gallery.tpl";

 if ($ref->{'a'} eq '') {$ref=list_gal($ref); } #Вывод документа
 if ($ref->{'a'} eq 'full') {$ref=full_gal($ref); } #Вывод документа

 print_($ref);


sub list_gal { #вывод элементов каталога (самих товаров)
 my $ref=shift;

 my $col_records=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{col_records}||25;
 my $col_rows=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{col_rows}||'3';
 my $zag=$ref->{user_db}->{data}->{$ref->{id}}->{zag}||$ref->{user_db}->{data}->{$ref->{id}}->{name};
 my $dbh=dbconnect;

 #если есть верхняя часть выводим
 if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){

 	$ref->{tpl_top}="user_db.$ref->{id}.data";
 }

 #переход по страницам
 my $CountPage=$col_records;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||$ref->{p_n}||0;
 my $off=$p_n*$CountPage;
 my $dop='';
 if($ref->{slovo}){
  $ref->{slovo}=~s/\%//gi;
  $ref->{slovo}=~s/^\s+//gi;
  $ref->{slovo}=~s/\s+$//gi;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
 $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(opis) like upper('%$ref->{slovo}%'))];
 }
 if ($ref->{author}){
 $dop.="and author='$ref->{author}'";
 }
 my $dop_r="and idr='$ref->{id}'";
 $dop_r="and idr != 'portfolio'" if $ref->{id} eq 'template';
 my $col="select count(*) from $ref->{db_prefix}_gallery where 1 $dop_r $dop";

 my $count=$dbh->selectrow_array($col);
 my $kol;
 my $order='order by sort asc, id desc';
    $order='order by id desc' if $ref->{sort} eq 'data';
    $order='order by name' if $ref->{sort} eq 'name';
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
 my $sel="select * from $ref->{db_prefix}_gallery where 1 $dop_r $dop $order limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $inc=0; my $i=0;
    my @ar=();
    while(my $ref_catalog=$sth->fetchrow_hashref){
         $ref_catalog->{name}=~tr/"'/``/;
         $ref_catalog->{opis}=~tr/"'/``/; #'
         $ref_catalog->{opis}=~s/\n|\r/<br>/gi; 
         $inc++;$i++;
    	 my $alt="$ref_catalog->{name} / $zag $ref->{user_db}->{template}->{assign}->{TITLE}";
         $alt=~s/"/'/gi; $alt=~s/\s+/ /gi; $alt=~s/^\s+|\s+$//gi; $alt=~s/^\/|\/$//gi; #'"
	 
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
	    $url1="/gallery/$ref->{id}.html?id_r=$ref->{id_r}&slovo=$ref->{slovo}";
    }

    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;
return $ref;
}

sub full_gal {
 my $ref=shift;
 #Выводим каталог товаров
 my $dbh=dbconnect();
 my $sel="select g.*,s.name as name_r from $ref->{db_prefix}_gallery as g, structure as s  where g.id='$ref->{data_id}' and g.idr=s.id";
    #print qq[$sel];
 my $sth=$dbh->prepare($sel);
    $sth->execute();
 $ref->{ref_data}=$sth->fetchrow_hashref;
 dbdisconnect($dbh);
  $ref->{zag}=$ref->{user_db}->{data}->{$ref->{id}}->{zag}||$ref->{user_db}->{data}->{$ref->{id}}->{name};
# my $alt="$ref->{ref_data}->{name} / $zag / $ref->{user_db}->{template}->{assign}->{TITLE}";
#    $alt=~s/"/'/gi; $alt=~s/\s+/ /gi; $alt=~s/^\s+|\s+$//gi; $alt=~s/^\/|\/$//gi; #'"
 if(-e "$ref->{path_host}/gallery_image/$ref->{ref_data}->{id}-1.jpg"){
    $ref->{ref_data}->{foto_1}=1;
 }
 if(-e "$ref->{path_host}/gallery_image/$ref->{ref_data}->{id}-2.jpg"){
    $ref->{ref_data}->{foto_2}=1;
 }

 $ref->{title}=$ref->{ref_data}->{name};
 #переход по страницам
# my $sel="select * from $ref->{db_prefix}_gallery where idr='$ref->{ref_data}->{idr}' and id!='$ref->{ref_data}->{id}' order by date_reg desc, id desc limit 6";
 my $sel="select * from $ref->{db_prefix}_gallery where idr='$ref->{ref_data}->{idr}' and id!='$ref->{ref_data}->{id}' order by RAND() limit 6";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $inc=0; my $i=0;
    my @ar=();
    while(my $ref_catalog=$sth->fetchrow_hashref){
         $ref_catalog->{name}=~tr/"'/``/;
         $ref_catalog->{opis}=~tr/"'/``/; #'
         $ref_catalog->{opis}=~s/\n|\r/<br>/gi; 
         $inc++;$i++;
	 
      	 push @ar,$ref_catalog;
		
    }
    $ref->{ar_data}=\@ar;
    $sth->finish;

 #Выводим каталог товаров
return $ref;
}

1;