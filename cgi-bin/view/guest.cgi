#!/usr/bin/perl
#модуль гостевой книги

 $|=1;
 use lib "../";
 use Modules::Constructor qw (dbconnect dbdisconnect page_down $host_name  &get_structure &check_captcha);
 use Modules::Constructor_view;
 use strict;

 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param_view||{};
   # uze vuzuvaem structuru iz Get_Param dla konkretnogo razdela
   #$ref=get_structure($ref);

 # кэшировать шаблоны
 # $ref->{cach}="yes";
 $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 
 $ref->{tpl_}="guest.tpl";

 if ($ref->{'a'} eq '') {$ref=list_guest($ref); } #Вывод документа
 if ($ref->{'a'} eq 'insert') {&insert_record($ref); } #добавляем запись

 print_($ref);


sub list_guest {
 my $ref=shift;

 my $col_records=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{col_records}||10;
 my $dbh=dbconnect;
 #переход по страницам
 my $CountPage=$col_records;
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 my $col="select count(*) from guest where idu='$ref->{user}->{id}' and idr='$ref->{id}' and answer!=''";
 my $count=$dbh->selectrow_array($col);
 my $kol;
 if($count%$CountPage==0){$kol=int($count/$CountPage);}else{$kol=int($count/$CountPage)+1;}
 #переход по страницам
         my $message='';
         $message=qq[Ваш вопрос был отправлен.] if $ref->{mess} eq 'ok';
 my $sel="select * from guest where idu='$ref->{user}->{id}' and idr='$ref->{id}' order by data_reg desc limit $off,$CountPage";

 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my @ar=();
    while(my $ref_guest=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_guest->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;

    	    $year=substr($year,2,2);
         
            $ref_guest->{data_print}="$day.$month.$year";

            $ref_guest->{name}=CGI::escapeHTML($ref_guest->{name});
            $ref_guest->{email}=CGI::escapeHTML($ref_guest->{email});
            $ref_guest->{subject}=CGI::escapeHTML($ref_guest->{subject});
            $ref_guest->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_guest->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_guest->{record}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_guest->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_guest->{record}=~s/\|\|===brake===\|\|/<br>/gi;
            $ref_guest->{answer}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_guest->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_guest->{answer}=~s/\|\|===brake===\|\|/<br>/gi;
                       $ref_guest->{record}=~s/ http:\/\/(.+?) /<a href="$1">$1<\/a>/gi;
                       $ref_guest->{answer}=~s/ http:\/\/(.+?) /<a href="$1">$1<\/a>/gi;

      	 push @ar,$ref_guest;
		
    }
    $ref->{ar_data}=\@ar;

    $sth->finish;
    #sереход по страницам
    my $url1=$ref->{location};
    $url1=~s/&{0,1}p_n=([0-9]+)?//gi;

    if($ref->{slovo}){
	    #sереход по страницам c поиска
	    $url1="/guest/$ref->{id}.html?id_r=$ref->{id_r}&slovo=$ref->{slovo}";
    }

    my $perehod=&page_down($url1,$kol,$PageIn,$p_n,$CountPage);
    $ref->{perehod}=$perehod;

	return $ref;
}

sub insert_record { #Добавляем запись в гостевую
 my $ref=shift;
 my $block_ip=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{block_ip}||'';
 $block_ip=~s/^\s+|\s+$//gi;
 $block_ip=~s/\s+/ /gi;
 my @ar= split / /,$block_ip;
 my $ok=grep $ref->{ip}=~$_, @ar;
 if(!$ref->{name}||!$ref->{record}){
 print qq[
 <html><head><title>Fill required fields</title></head>
 <body>
 <script>alert('Заполните обязательные поля!');history.go(-1)</script>
 </body>
 </html>
 ];
 exit;
 }
 elsif($ok!=0){
 print qq[
 <html><head><title>Ip is blocked</title></head>
 <body>
 <script>alert('Ip is blocked');location.href="$ref->{referrer}"</script>
 </body>
 </html>
 ];
 exit;
 }
 else{
  my $mod_razdel=$ref->{user_db}->{data}->{$ref->{id}}->{mod}||'';
 if($mod_razdel eq 'guest'){
  if(check_captcha($ref)==0&&1==2){
  print "<html><head><title></title></head><body>
    <script>alert('Введите корректный код!');history.go(-1)</script>
    </body></html>"; 
    exit;
  } 
  my $dbh=dbconnect;
    $ref->{subject}='' if !$ref->{subject};
  my $ins="insert into guest (idu,idr,data_reg,name,subject,email,record,ip) values (?,?,now(),?,?,?,?,?)";
  my $sth=$dbh->prepare($ins);
     $sth->execute($ref->{user}->{id},$ref->{id},$ref->{name},$ref->{subject},$ref->{email},$ref->{record},$ref->{ip});  
     $sth->finish;
     dbdisconnect($dbh);


my $email_owner=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{email}||'';
if($email_owner){
my $text=qq[
You have new mesage 

ФИО: $ref->{name}
Тема: $ref->{subject}
Email: $ref->{email}
Вопрос:
 $ref->{record}

Страница:
http://$host_name/guest/$ref->{id}/

-----------------
Для ответа на этот вопрос:
1. зайдите в систему администрирования: http://$host_name/admin/
2. В левом меню выберите раздел вопросов и ответов
3. Заполните поле "Ваш ответ" и нажмите "Ответить"
];
 my $subject=qq[New message $ref->{user_doman}];
 &send_mail($email_owner,$subject,$text);
}
 }
 print qq[
 <html><head><title>Record was added</title></head>
 <body>
 <script>location.href="/guest/$ref->{id}.html?mess=ok"</script>
 </body>
 </html>
 ];
 exit;
 }
}
1;