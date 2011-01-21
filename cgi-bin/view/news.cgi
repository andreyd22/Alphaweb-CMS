#!/usr/bin/perl
#модуль новостной ленты
 $|=1;
 use lib "../";
 use Modules::Constructor qw (dbconnect dbdisconnect page_down);
 use Modules::Constructor_view;
 use strict;
#print qq[$path_index];
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param_view||{};
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);

 # кэшировать шаблоны
 # $ref->{cach}="yes";
# $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 
 $ref->{index_tpl} = "index.tpl"; 
 $ref->{tpl_}="news.tpl";


 if ($ref->{'a'} eq '') {$ref=list_news($ref); } #Вывод документа
 if ($ref->{'a'} eq 'full') {$ref=full_news($ref); } #Вывод документа

 print_($ref);


sub list_news {
 my $ref=shift;
 #если есть верхняя часть выводим
 if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){

 	$ref->{tpl_top}="user_db.$ref->{id}.data";
 }

 my $col_records=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{col_records}||10;
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=$col_records;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||$ref->{p_n}||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from $ref->{db_prefix}_news where idu='$ref->{user}->{id}' and idr='$ref->{id}'";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
 my $sel="select * from $ref->{db_prefix}_news where idu='$ref->{user}->{id}' and idr='$ref->{id}' order by data_reg desc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my @ar=();
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
#         my $data_print="$day/$month/$year $hour:$min";
 	    $year=substr($year,2,2);
         
         $ref_news->{data_print}="$day.$month.$year";
      	 push @ar,$ref_news;
		
    }
    $ref->{ar_data}=\@ar;

    $sth->finish;
    #sереход по страницам
    my $url1=$ref->{location};
    $url1=~s/&{0,1}p_n=([0-9]+)?//gi;

    if($ref->{slovo}){
	    #sереход по страницам c поиска
	    $url1="/news/$ref->{id}.html?id_r=$ref->{id_r}&slovo=$ref->{slovo}";
    }

    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;

    return $ref;
}

sub full_news {
 my $ref=shift;
 my $tpl={};

 #Выводим новость
 my $dbh=dbconnect;
 my $sel="select * from $ref->{db_prefix}_news where id='$ref->{data_id}' and idu='$ref->{user}->{id}' and idr='$ref->{id}'";
#print qq[id_news $ref->{id_news}];
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    $ref->{ref_data}=$sth->fetchrow_hashref||{};
    $sth->finish;
    my ($data,$time)=split / /,$ref->{ref_data}->{data_reg};
    my ($year,$month,$day)=split /-/,$data;
    my ($hour,$min,$sec)=split/:/,$time;
#    my $data_print="$day/$month/$year $hour:$min";
    $ref->{ref_data}->{data_print}="$day.$month.$year";
    my $back=$ref->{referrer};
    $back="/$ref->{user_db}->{data}->{$ref->{id}}->{lang}/$ref->{id}/";
 #Выводим ключевики
 $ref->{title}=$ref->{ref_data}->{title} if $ref->{ref_data}->{title};
 $ref->{keywords}=$ref->{ref_data}->{keywords};
 $ref->{description}=$ref->{ref_data}->{description};

 return $ref;
}
1;