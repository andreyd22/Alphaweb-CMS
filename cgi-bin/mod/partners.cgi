#!/usr/bin/perl
#модуль страниц партнеров
 $|=1;
 use lib "../";
 use Modules::Constructor_view;
 use Modules::Constructor;
 use strict;
 my $ref=Get_Param_view||{};
# my $ref=Get_Param;
 my $p=1;
#print qq[perf $ref->{prefix}];exit;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><title>Authorization error</title></HEAD>
    <body>
    <script>parent.location.href='/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes'</script>
    </body>
    </HTML>
     ";
 exit;
 }
#!!!Проверка sid пользователя!!!#
#!!!Проверка уровня доступа!!!
check_access($ref);
#!!!Проверка уровня доступа end!!!
 my $create_news=qq[
CREATE TABL `partners` (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY ,
`date_reg` DATETIME NULL ,
`name` VARCHAR( 255 ) NOT NULL ,
`short` TEXT NOT NULL ,
`opis` TEXT NOT NULL ,
`visible` TINYINT NOT NULL DEFAULT '0',
`link` VARCHAR( 255 ) NOT NULL ,
`typef` VARCHAR( 50 ) NOT NULL ,
`idr` varchar(50) NOT NULL default '0',

) ENGINE = MYISAM COMMENT = 'таблица партнеров'];      
my $dbh=dbconnect;
#my $col=$dbh->selectrow_array("select count(*) from $ref->{prefix}news");
if(!table_exists(qq[`partners`])){
 my $news=$dbh->do($create_news);
}

#print qq[$path_index];
 print "Content-type:text/html\r\n\r\n";
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);

 # кэшировать шаблоны
 # $ref->{cach}="yes";
 $ref->{index_tpl} = "index_admin.tpl"; 
 $ref->{tpl_}="partners_admin.tpl";
 $ref->{name_action}="Администрирование страниц актеров";
# $ref->{module_name}="anketa";
 if ($ref->{'a'} eq '') {$ref=list_partners($ref); } #Вывод списка анкет
 if ($ref->{'a'} eq 'edit_forma') {$ref=edit_forma($ref); } #Вывод редактора анкеты
 if ($ref->{'a'} eq 'save') {$ref=save($ref); } #сохранение информации
 if ($ref->{'a'} eq 'save_photo') {$ref=save_photo($ref); } #сохранение дополнительных фотографий
 if ($ref->{'a'} eq 'del_photo') {$ref=del_photo($ref); } #даление фотографии
 if ($ref->{'a'} eq 'del_partner') {$ref=del_partner($ref); } #даление анкеты с  фотографиями
 print_($ref);


sub list_partners {
 my $ref=shift;
 my $dbh=dbconnect;

 #переход по страницам
 my $CountPage=100;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $dop='';

 my $col="select count(*) from partners where 1 $dop";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 my $modp=$count%$CountPage;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 if(int($count/$CountPage)==$count/$CountPage){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}

 my $sel="select * from partners where idr='$ref->{id}' $dop order by sort desc, name, date_reg desc limit $off,$CountPage";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my @ar=();
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{date_reg};
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
	    $url1="/cgi-bin/mod/partners.cgi?slovo=$ref->{slovo}";
    }

    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;
    return $ref;
}

sub edit_forma {
 my $ref=shift;

 #Выводим новость
 my $dbh=dbconnect;
    if (!$ref->{id_partner}){
	$ref->{ref_data}=$ref;
	#$ref->{ref_data}->{id}="";
    }else{
 my $sel="select * from partners where id='$ref->{id_partner}'";
#print qq[id_news $ref->{id_news}];
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    $ref->{ref_data}=$sth->fetchrow_hashref||{};
    $sth->finish;
 }
 if($ref->{ref_data}->{ver}){$ref->{ver}=$ref->{ref_data}->{ver}}

    $ref->{ref_data}->{sort}=int($ref->{ref_data}->{sort});
    if($ref->{ref_data}->{sort}==0){$ref->{ref_data}->{sort}=50}
    my ($data,$time)=split / /,$ref->{ref_data}->{data_reg};
    my ($year,$month,$day)=split /-/,$data;
    my ($hour,$min,$sec)=split/:/,$time;

    $ref->{ref_data}->{name}=~s/\n/ /gi;
    $ref->{ref_data}->{name}=~s/\s+/ /gi;
    $ref->{ref_data}->{name}=~s/'/"/gi; #'

    $ref->{ref_data}->{opis}=~s/\n/ /gi;
    $ref->{ref_data}->{opis}=~s/\s+/ /gi;
    $ref->{ref_data}->{opis}=~s/'/"/gi; #'

    $ref->{ref_data}->{short}=~s/\n/ /gi;
    $ref->{ref_data}->{short}=~s/\s+/ /gi;
    $ref->{ref_data}->{short}=~s/'/"/gi; #'

    

 return $ref;
}

sub save {
    my $ref=shift;

     $ref->{visible}=0 if !$ref->{visible};
    if($ref->{id_partner}){
	 $ref->{update_status}=$ref->{dbh}->do("update partners set sort=?,name=?,short=?,opis=?,visible=?,link=?,idr=?
			where id=?",undef,($ref->{sort},$ref->{name},$ref->{short},$ref->{opis},$ref->{visible},$ref->{link},$ref->{id},$ref->{id_partner}));

    }else{
#			print qq[$ref->{insert_status} = $ref->{name},$ref->{short},$ref->{opis},$ref->{visible},$ref->{link},$ref->{id}]; exit;
	$ref->{insert_status}=$ref->{dbh}->do("insert into partners (date_reg,sort,name,short,opis,visible,link,idr) 
						    values (NOW(),?,?,?,?,?,?,?)
			",undef,($ref->{sort},$ref->{name},$ref->{short},$ref->{opis},$ref->{visible},$ref->{link},$ref->{id}));
			$ref->{id_partner}=$ref->{dbh}->last_insert_id(undef, undef, undef, undef);


    }
    $ref=save_photo($ref);


return $ref; 
}

sub save_photo {
my $ref=shift;
  #Берем массив фотографий
  my @ar_photo=CGI::param('upfile');
    #print qq[@ar_photo];
  for(my $i=0;$i<=$#ar_photo;$i++){
	if ($ar_photo[$i] && $ref->{id_partner})
	{
	        my $upfile=$ar_photo[$i];
		my $file='';
	        my @ar1=split /\\/,$upfile;
	        $file=$ar1[$#ar1];
	        my @ar2=split /\./,$file;
	        my $nmf=$ar2[0];
	        my $typef=$ar2[$#ar2];
	        my $d_f="";
	        my $num_foto=$i+1;
	        if($i>0){$d_f="-".$num_foto;}
	        if($typef!~/^jp(e){0,1}g|gif|png$/i){
	        	$ref->{mess}.=" Ошибка загрузки фото №$num_foto: К добавлению на портале принимают фото формата jpg,jpeg,gif. <br>"; 
	        	last
	        }else{
			$ref->{mess}.=" Фотография №$num_foto успешно загружена. <br>";
	        }
		# создаем директорию
		if(!-d "$ref->{path_root}/upload/partners_photo"){
    		    mkdir("$ref->{path_root}/upload/partners_photo",0777);
		}

		#print qq[$ref->{path_root}/upload/partners_photo]; exit;
	        my ($buf);
		my $file_photo="$ref->{id_partner}.$typef";
		my $file_photo_sm="$ref->{id_partner}-s.$typef";
		my $file_photo_pr="$ref->{id_partner}-m.$typef";
	        open A, "+>$ref->{path_root}/upload/partners_photo/$file_photo" || die $!;
	        binmode(A);
	        while (my $bytesread = read($upfile, $buf, 1024)) {
	         print A $buf;
		}
		close A;
	
		#chmod 0644, "../upload/catalog_photo/$file_photo";
		#magick('160',"$ref->{path_root}/upload/partners_photo/$file_photo","$ref->{path_root}/upload/partners_photo/$file_photo_sm"); 
		#chmod 0644, "../upload/catalog_photo/$file_photo_sm";
		magick('200',"$ref->{path_root}/upload/partners_photo/$file_photo","$ref->{path_root}/upload/partners_photo/$file_photo"); 
		#chmod 0644, "../upload/catalog_photo/$file_photo_pr";
		$ref->{upd_typef}=$ref->{dbh}->do("update partners set typef='$typef' where id='$ref->{id_partner}'");
		
	};
  };
return $ref;
}


sub del_photo {
my $ref=shift;
my $ref_partner=$ref->{dbh}->selectrow_hashref("select * from partners where id='$ref->{id_partner}'");
my $upd_partner=$ref->{dbh}->do("update partners set typef='' where id='$ref->{id_partner}'");
 del_1_photo($ref->{id_partner},$ref_partner->{typef});
return $ref;
}

sub del_partner {
my $ref=shift;
    del_1_photo($ref->{id_partner});
    $ref->{del_status}=$ref->{dbh}->do("delete from partners where id_ = ?", undef, ($ref->{id_partner}));


return $ref;
}

sub del_1_photo {
 my $id_photo=shift;
 my $typef=shift;
    if($id_photo){
	 unlink "$ref->{path_root}/upload/partners_photo/$id_photo.$typef";
	 unlink "$ref->{path_root}/upload/partners_photo/$id_photo-s.$typef";
    }
return 1;
}
1;