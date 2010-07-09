#!/usr/bin/perl
#модуль новостной ленты
 $|=1;
 use lib "../";
 use Modules::Constructor qw (&dbconnect &dbdisconnect &check_captcha &data_filter &send_mail);
 use Modules::Constructor_view;
 use strict;

 my $ref=Get_Param_view||{};

 # кэшировать шаблоны
 # $ref->{cach}="yes";
 $ref->{index_tpl} = $ref->{user_db}->{data}->{$ref->{id}}->{index_ini}; 
 $ref->{tpl_}="form.tpl";

 print CGI::header(-type=>'text/html',-charset=>'windows-1251');

 if ($ref->{'a'} eq '') {$ref=&main($ref); } #Вывод документа
 if ($ref->{'a'} eq 'reg') {&reg($ref); } #Вывод документа

 print_($ref);


 exit;

sub main {
 my $ref=shift;

# my $mess="";
# if($ref->{mess} eq 'ok'){$ref->{mess}="Спасибо! Ваше сообщение доставлено! Мы свяжемся с Вами в ближайшее время.";}
 #если есть верхняя часть выводим
 if(-e $ref->{path_root}."/db/user_db.$ref->{id}.data"){

 	$ref->{tpl_top}="user_db.$ref->{id}.data";
 }

 if($ref->{user_db}->{data}->{$ref->{id}}->{params}->{reg})
 {
 	my ($name_field,$name_field_lat,$type_field)=
	split /\&/,$ref->{user_db}->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;
	my @ar_fields=();
  for(my $pos=0;$pos<=$#ar_name;$pos++){
	 	my ($type,$text_value) = split /\^/,$ar_type[$pos];
#	print $type."=".$text_value."<br>";
		my @ar_text_value=split /\$/,$text_value;
#	 	my %text_value = map { split /\~/,$_ } split /\$/,$text_value;
	 	my $field_params = '';
#	while (my ($text,$value) = each(%text_value))
	for (my $i=0; $i<=$#ar_text_value;$i++)
	{
		my ($text,$value)=split /\~/,$ar_text_value[$i];
		$field_params .= qq[<option value="$value">$text</option>] if $type eq 'select';
		$field_params .= qq[<input type="$type" name="$ar_name_lat[$pos]" value="$value ($text)" >&nbsp;$text <br>] if $type ne 'select';
	}
   my $input = qq[<input type=text name="$ar_name_lat[$pos]" style="width:250px" value="$ref->{$ar_name_lat[$pos]}">] if $type eq 'text';
   $input = qq[<textarea name="$ar_name_lat[$pos]" cols=25 rows=7  style="width:250px">$ref->{$ar_name_lat[$pos]}</textarea>] if $type eq 'textarea';
   $input = qq[<select name="$ar_name_lat[$pos]" style="width:250px">$field_params</select>] if $type eq 'select';
   $input = $field_params if ($type eq 'checkbox' || $type eq 'radio');
   
   push @ar_fields,{'name' => $ar_name[$pos], 'input' => $input};
  }
$ref->{ar_fields}=\@ar_fields;
 }
return $ref;
}

sub reg {
   my $ref=shift;
 my $block_ip=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{block_ip}||'';
 $block_ip=~s/^\s+|\s+$//gi;
 $block_ip=~s/\s+/ /gi;
 my @ar= split / /,$block_ip;
 my $ok=grep $ref->{ip}=~$_, @ar;
 if($ok!=0){
 print qq[
 <script>alert('You ip was blocked');location.href="$ref->{referrer}"</script>];
 exit;
 }
 #print $ref->{message};
 if($ref->{user_db}->{data}->{$ref->{id}}->{params}->{reg}){

  if(check_captcha($ref)==0 && $ref->{who} ne 'flash'){
  $ref->{mess2}=  "
    Неверно введен номер. Пожалуйста, нажмите \"обновить картинку\", если цифры на картинке не обновились!"; 
   $ref=main($ref);
    return $ref;
    #$ref->{mess2}='Неверно введен номер. Пожалуйста, нажмите \"обновить картинку\", если цифры на картинке не обновились!';
    #$ref->{id}=;
    #return $ref;
    exit;
  } 

 	my ($name_field,$name_field_lat,$type_field)=
		split /\&/,$ref->{user_db}->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;
    my $str_mail="\n";
    my $insert='';
    my $values = '';
    my @params=();
    for(my $pos=0;$pos<=$#ar_name_lat;$pos++){
#     my $temp=CGI::param($ar_name_lat[$pos]);
	my @temp_=CGI::param($ar_name_lat[$pos]);
	my $temp='';
	if($#temp_>1){
		for(my $i=0;$i<=$#temp_;$i++){$temp.=qq[$temp_[$i], ];}
	  $temp=~s/\, //gi;
	}
	else{$temp=CGI::param($ar_name_lat[$pos])||''}
	if($temp eq ''){print qq[<script>alert('Все поля обязательны для заполнения!');history.go(-1)</script>]; exit;}

     my $err;($temp,$err)=data_filter($temp);
        $str_mail.="$ar_name[$pos]: $temp\n";
        $insert.=qq[`rg_$ar_name_lat[$pos]`,];
        $values.=qq[?,];
        push @params,$temp;
    }
    #$str_mail=~s/\(.+?^\)\)//gi;
    #print qq[$insert <br> $str_mail];
    #chop $insert; chop $values;
    $insert.=qq[rg_ip,rg_date];
    my $data=time;
    $values.=qq['$ref->{ip}',FROM_UNIXTIME('$data')];
    my $sql=qq[insert into `reg_$ref->{id}` ($insert) values($values)];
    use Data::Dumper;
#   print "<!--\nsql=".$sql."\n".Dumper(\@params)."\n-->";
   my $dbh=dbconnect();
   my $sth = $dbh->prepare($sql) ;

#   eval { $sth->execute(@params) } or die $sth->errstr;
    $sth->execute(@params) or die $sth->errstr;
	$sth->finish;
    dbdisconnect($dbh);
     my $email_owner=$ref->{user_db}->{data}->{$ref->{id}}->{params}->{email}||$ref->{root_mail};
     if($email_owner)
     {
     	my $text=qq[$str_mail];
      	my $subject=qq[Вам заявка (страница "$ref->{id}")];
      	$text=qq[$text \nФорма: $ref->{user_db}->{data}->{$ref->{id}}->{name}\nhttp://$ref->{host_name}/reg/$ref->{id}.html\n];
      	&send_mail($email_owner,$subject,$text,$ref->{email}||$ref->{root_mail});
     }
 }
 print qq[<script>alert('Спасибо! Ваше сообщение успешно доставлено');location.href="/reg/$ref->{id}.html?mess=ok"</script>];

}
  
1;  