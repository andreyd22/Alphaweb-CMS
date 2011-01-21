#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с регистрацией пользователей
 $|=1;
 use CGI qw(:standard);
 use CGI::Carp qw(fatalsToBrowser);
 use lib "../";
 use Modules::Constructor;
 use strict;
 print header(-type=>'text/html',-charset=>'windows-1251');
 my $ref=Get_Param;

#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print "
      <HTML><HEAD><title>Ошибка авторизации</title></HEAD>
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

if (!table_exists(qq[`$ref->{db_prefix}_reg_$ref->{id}`])){
   &create_reg_tbl($ref);
}

if ($ref->{a} eq ''){list_reg($ref)} #Выводим все записи зарегистрированных юзеров
if ($ref->{a} eq 'save_email'){save_email($ref)} #Сохраняем емайл адрес
if ($ref->{a} eq 'view'){view_reg($ref)} #Выводим форму редактирования регистрационной формы (Вопросы рег формы)
if ($ref->{a} eq 'save_reg'){save_reg($ref)} #Сохраняем информацию о рег форме (Вопросы)
if ($ref->{a} eq 'del'){del_all($ref)} #Удаляем всю информацию из бд зарегистрированных юзеров
if ($ref->{a} eq 'del_all'){del_all($ref)}
if ($ref->{a} eq 'edit_field'){edit_field($ref)}
if ($ref->{a} eq 'del_field'){del_field($ref)} #Удаляем поле по номеру
if ($ref->{a} eq 'block_list'){block_list($ref)} #Блокируем ip адреса


sub list_reg {
 my $ref=shift;
 my $mes='';
 if ($ref->{mes}){$mes=message($ref)}
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_reg.html.$ref->{l}",
            "row"=>"/constructor_reg_row.html.$ref->{l}",
            "cell"=>"/constructor_reg_cell.html.$ref->{l}"
         };

 my $user_db =$ref->{user_db};
 my $block_ip=$user_db->{data}->{$ref->{id}}->{params}->{block_ip}||'';
 my $name_r=$user_db->{data}->{$ref->{id}}->{name}||'';
 my $my_email=$user_db->{data}->{$ref->{id}}->{params}->{email}||'';

 my $title="Модуль обратной связи - $name_r"; # title 2

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

  $tpl->assign(
             EMAIL_OWNER=>$my_email,
             BLOCK_IP=>$block_ip,
             MESSAGE=>$mes,
             IDR_REG=>$ref->{id},
   );

open A, "$template_root$def->{cell}" || die $!;
#print qq[$template_root$def->{cell} ];
my @ar_cell=<A>;
close A;

my $cell=join('',@ar_cell);

 	my ($name_field,$name_field_lat,$type_field)= split /\&/,$user_db->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;

 if($#ar_name <=0){view_reg($ref); exit;}
        my $parse_cell='';
  my $dbh=dbconnect();
  my $sql="select * from `$ref->{db_prefix}_reg_$ref->{id}` order by `rg_date` desc";
#  print $sql;
  my $sth=$dbh->prepare($sql);
     $sth->execute;
  while (my $ref_reg=$sth->fetchrow_hashref){
       my $parse_cell='';
          for (my $t=0;$t<=$#ar_name;$t++){
            my $temp_cell=$cell;
            my $name_reg=$ref_reg->{"rg_$ar_name_lat[$t]"};
               $temp_cell=~s/\$\{NAME_REG\}/$name_reg/i;
               $temp_cell=~s/\$\{NAME_FIELD\}/$ar_name[$t]/i;
               $parse_cell.=$temp_cell;
         }
         $tpl->assign(
              CELLS=>$parse_cell,
              IP =>$ref_reg->{rg_ip},
              ID_DEL=>$ref_reg->{rg_id},
	      DATA=>$ref_reg->{rg_date}
         );

         $tpl->parse("ROW_REG",".row");
         $tpl->clear_href(1);
    }
   $sth->finish;
   dbdisconnect($dbh);

A:
 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}

sub view_reg {
 my $ref=shift;
 my $def={  "main"=>"/constructor.html.$ref->{l}",
            "text"=>"/constructor_reg_add.html.$ref->{l}",
            "row"=>"/constructor_reg_add_row.html.$ref->{l}"
          };
 my $mess = $ref->{mess}||'';
 if ($ref->{mes}) { $mess ||= message($ref)}
 my $title="Редактор формы регистрации"; #title 4

 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);

    $tpl->assign(IDR_REG	=> $ref->{id},
                 SID		=> $ref->{sid},
		 MESSAGE	=> $mess,
                );

 my $user_db =$ref->{user_db};

 if($user_db->{data}->{$ref->{id}}->{params}->{reg})
{

 	my ($name_field,$name_field_lat,$type_field)=
	split /\&/,$user_db->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;

	 for(my $pos=0;$pos<=$#ar_name;$pos++){
#		print qq[$ar_name_lat[$pos],];
	 	my ($type,$text_value) = split /\^/,$ar_type[$pos];
#	 	my %text_value = map { split /\~/,$_ } split /\$/,$text_value;
#	 	my $field_params = '';	 	
#	 	while (my ($text,$value) = each (%text_value))
		my @ar_text_value=split /\$/,$text_value;
	 	my $field_params = '';
		for (my $i=0; $i<=$#ar_text_value;$i++)
	 	{
			my ($text,$value)=split /\~/,$ar_text_value[$i];
	 		my $col = time()+$i;
	 		$field_params .= qq[
	 		<span id="fld_$ar_name_lat[$pos]$col">
	 		Текст:<input name="text" value="$text">&nbspЗначение:<input name="value" value="$value">
	 		<a href="#to_$ar_name_lat[$pos]" onclick="DelField('$ar_name_lat[$pos]$col');">Удалить</a><br>
	 		</span>
	 		];
	 	}
	 	$field_params = qq[<a href="#to_$ar_name_lat[$pos]" onclick="AddField('$ar_name_lat[$pos]');">Добавить варианты</a><br>].$field_params if $field_params ne '';
	 	my $sel_item = qq[select_item('$ar_name_lat[$pos]','$type');];
	   $tpl->assign(
	     POS     => $pos,
	     SEL_ITEM => $sel_item,
	     NAME_FIELD     => $ar_name[$pos],
	     NAME_FIELD_LAT => $ar_name_lat[$pos],
	     NAME_FIELD_LAT_OLD => $ar_name_lat[$pos],
	     TYPE_FIELD     => $type,
	     FIELD_PARAMS => $field_params,
	     IDR_REG    => $ref->{id},
	     SID         => $ref->{sid}
	   );
         $tpl->parse("ROW_REG_FIELD",".row");
         $tpl->clear_href(1);
	}
}

 $tpl->parse(TEXT => "text");
 $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}

sub save_reg { #Сохраняем информацию о рег форме (Вопросы)
 my $ref=shift;
    $ref->{zag}=~tr/'/"/; #'

 my $user_db =$ref->{user_db};

 my $pr_mes='19';

 if($ref->{save} eq 'ok')
{

	 $ref->{name_field}=~tr/,&|=/____/;
	 $ref->{name_field_lat}=~tr/,&|= /____/;


 	my ($name_field,$name_field_lat,$type_field)=
		split /\&/,$user_db->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;

	my @ar_text = CGI::param('text');
	my @ar_value = CGI::param('value');
	# формируем строку списка значений (выпадающий список, чекбоксы и т.д.)
	my $text_value = join("\$", map { qq{$ar_text[$_]~$ar_value[$_]} } (0..$#ar_text));

# print qq[$ref->{name_field_lat}&&$ref->{name_field}]; exit;
# print qq[$ref->{name_field_lat}&&$ref->{name_field}; @ar_text; @ar_value; text_value: $text_value]; exit;

# Проверяем есть ли такое поле
	 if ( grep {$ref->{name_field_lat} eq $_} @ar_name_lat)
	 {
		my $mess = qq[Поле с названием '$ref->{name_field_lat}' уже существует!];
		out_err_($ref,$mess); 
	 }
#
	 my $dbh=dbconnect();
	if ($ref->{name_field_lat}&&$ref->{name_field})
	{
#	 eval {
		my $add=$dbh->do(qq[ALTER TABLE `$ref->{db_prefix}_reg_$ref->{id}` ADD `rg_$ref->{name_field_lat}` VARCHAR( 250 )])
		#print qq[ALTER TABLE `reg_$ref->{id}` ADD `rg_$ref->{name_field_lat}` VARCHAR( 250 )  = $add ]; exit;

#	 } 
		 or out_err_($ref,$dbh->errstr);

		 push @ar_name,$ref->{name_field};
		 push @ar_name_lat,$ref->{name_field_lat};
		 push @ar_type,join("\^",($ref->{type_field},$text_value));

	}
	 dbdisconnect($dbh);

#
	 my $reg=join('&',(join('|',@ar_name),join('|',@ar_name_lat),join('|',@ar_type)));
	 $user_db->{data}->{$ref->{id}}->{params}->{reg}=$reg;
	 my $kind='params';
	 &store_db( $user_db,  $ref->{id}, $kind);
}
else{
$pr_mes='20';
}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
print qq[
<html>
<body>
<script>location.href="/cgi-bin/mod/reg.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&mes=$pr_mes&a=view"</script>
</body>
</html>];
  exit;
}

sub edit_field
{
	my $ref = shift;
	my $user_db = $ref->{user_db};
	my $pr_mes='19';
 if($ref->{save} eq 'ok')
{
	 $ref->{name_field}=~tr/,&|=/_/;
	 $ref->{name_field_lat}=~tr/,&|=/_/;

 	my ($name_field,$name_field_lat,$type_field)=
		split /\&/,$user_db->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;

	my @ar_text = CGI::param('text');
	my @ar_value = CGI::param('value');
	my $text_value = join("\$", map { qq{$ar_text[$_]~$ar_value[$_]} } (0..$#ar_text));
	
#	 print qq[$ref->{name_field_lat}&&$ref->{name_field}; @ar_text; @ar_value; text_value: $text_value]; exit;

	my $dbh = dbconnect();	
	if ( defined($ref->{'pos'}) )
	{
			my $drop = $dbh->do(qq[ALTER TABLE `$ref->{db_prefix}_reg_$ref->{id}` CHANGE `rg_$ref->{name_lat_old}` `rg_$ref->{name_field_lat}` VARCHAR( 250 )] )
		or 
			my $add = $dbh->do(qq[ALTER TABLE `$ref->{db_prefix}_reg_$ref->{id}` ADD `rg_$ref->{name_field_lat}` VARCHAR( 250 )]);


		 $ar_name[$ref->{'pos'}] = $ref->{name_field};
		 $ar_name_lat[$ref->{'pos'}] = $ref->{name_field_lat};
		 $ar_type[$ref->{'pos'}] = join("\^",($ref->{type_field},$text_value));

	}
	 dbdisconnect($dbh);

	 my $reg=join('&',(join('|',@ar_name),join('|',@ar_name_lat),join('|',@ar_type)));
	 $user_db->{data}->{$ref->{id}}->{params}->{reg}=$reg;

	 &store_db( $user_db,  $ref->{id});
}
	$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
	my $time=time;
	print qq[
	<html>
	<body>
	<script>location.href="/cgi-bin/mod/reg.cgi?sid=$ref->{sid}&l=$ref->{l}&id=$ref->{id}&mes=$pr_mes&a=view"</script>
	</body>
	</html>];
	  exit;
}

sub del_all {
 my $ref=shift;

if ($ref->{a} eq 'del_all'){
 open A, "+>$ref->{path_db}.$ref->{id}.info" || die $!;
 close A;

#
 my $dbh=dbconnect;
# eval {
	my $delete_all=$dbh->do(qq[delete from `$ref->{db_prefix}_reg_$ref->{id}`])
# } 
or out_err_($ref,$dbh->errstr);

 dbdisconnect($dbh);
#
}elsif($ref->{id_del}){
#
 my $dbh=dbconnect;
# eval {
	my $delete_id=$dbh->do(qq[delete from `$ref->{db_prefix}_reg_$ref->{id}` where rg_id='$ref->{id_del}'])
# } 
or out_err_($ref,$dbh->errstr);

 dbdisconnect($dbh);
#
}

my $pr_mes='19';
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub del_field {
 my $ref=shift;
my $pr_mes='19';

 my $user_db =$ref->{user_db};
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;

 	my ($name_field,$name_field_lat,$type_field)=
		split /\&/,$user_db->{data}->{$ref->{id}}->{params}->{reg};
	my @ar_name=split /\|/,$name_field;
	my @ar_name_lat=split /\|/,$name_field_lat;
	my @ar_type=split /\|/,$type_field;

# есть ли оно?
#print $ref->{name_field_lat};
# if ( !grep {$ref->{name_field_lat} eq $_} @{$ar_name_lat_href})
# {#
#	my $mess = qq[Поле с названием '$ref->{name_field_lat}' не существует!];
#	out_err_($ref,$mess);
# }

#
 splice @ar_name,$ref->{'pos'},1;
 splice @ar_name_lat,$ref->{'pos'},1;
 splice @ar_type,$ref->{'pos'},1;

 my $reg=join('&',(join('|',@ar_name),join('|',@ar_name_lat),join('|',@ar_type)));

 $user_db->{data}->{$ref->{id}}->{params}->{reg}=$reg;

 &store_db( $user_db,  $ref->{id});

 my $dbh = dbconnect();
# print qq[$reg]; exit;
# eval {
#print qq[ALTER TABLE `reg_$ref->{id}` DROP `rg_$ar_name_lat[$ref->{pos}]`]; exit;
#print qq[ALTER TABLE `reg_$ref->{id}` DROP `rg_$ref->{name_field_lat}`]; exit;
	my $del_fld=$dbh->do(qq[ALTER TABLE `$ref->{db_prefix}_reg_$ref->{id}` DROP `rg_$ref->{name_field_lat}`])
# };

#or out_err_($ref,$dbh->errstr)
;

 dbdisconnect($dbh);
#



my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub create_reg_tbl{
  my $ref=shift;
 my $user_db=$ref->{user_db};

 my @ar_name=();
 my @ar_name_lat=();
 my @ar_type=();

 if($user_db->{data}->{$ref->{id}}->{reg}->{name_field}){
 my $ar_name_href = $user_db->{data}->{$ref->{id}}->{reg}->{name_field}||{};
 my @ar_name=@$ar_name_href;
 my $ar_name_lat_href = $user_db->{data}->{$ref->{id}}->{reg}->{name_field_lat}||{};
 my @ar_name_lat=@$ar_name_lat_href;
 my $ar_type_href = $user_db->{data}->{$ref->{id}}->{reg}->{type_field}||{};
 my @ar_type=@$ar_type_href;
 }

my $tbl_fields=',';
for (my $i=0;$i<=$#ar_name_lat;$i++){
 my $type='varchar(250)';
   $type='text' if ($ar_type[$i] eq 'textarea');
  $tbl_fields.=qq[rg_$ar_name_lat[$i] $type,];
}
  chop $tbl_fields;
  my $dbh=dbconnect;
  my $create_tbl=qq[
CREATE TABLE `$ref->{db_prefix}_reg_$ref->{id}`(
 rg_id int not null auto_increment primary key,
 rg_ip varchar(20) not null,
 rg_date datetime not null
 $tbl_fields
)
];
  my $create=$dbh->do($create_tbl);

if (-e "$ref->{path_db}.$ref->{id}.info"){
open A, "$ref->{path_db}.$ref->{id}.info" || die $!;
my @ar_text=();
while(<A>){
 chomp;
 push @ar_text,$_;
}
close A;
 my $ar_name_href = $user_db->{data}->{$ref->{id}}->{reg}->{name_field_lat}||{};
 my @ar_name=@$ar_name_href;
     for(my $u=$#ar_text;$u>=0;$u--){
        my $parse_cell='';
        chomp($ar_text[$u]);
         my @ar_str=split/\|/,$ar_text[$u];
         my $insert='';
         my $values='';
          for(my $t=0;$t<=$#ar_str;$t++){
                if ($t<$#ar_str){
		$values.=qq['$ar_str[$t]',];
               $insert.=qq[rg_$ar_name[$t],];}
                elsif ($t==$#ar_str-1) {
		$values.=qq['$ar_str[$t]',];
               $insert.=qq[rg_ip,];}
		elsif($t==$#ar_str){
 		my @data;
		@data=get_data($ar_str[$t]);
		$values.=qq['$data[0]-$data[1]-$data[2] $data[3]:$data[4]:$data[5]',];
               $insert.=qq[rg_date,];}
          }
          chop $insert; chop $values;
          my $sql=qq[insert into `$ref->{db_prefix}_reg_$ref->{id}` ($insert) values($values)];
          my $ins=$dbh->do($sql);
  }
 unlink "$ref->{path_db}.$ref->{id}.info";
}
 dbdisconnect($dbh);
}

sub save_email {
 my $ref=shift;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
  my $user_db =$ref->{user_db};
my $pr_mes='19';
if($ref->{save} eq 'ok'){

      $user_db->{data}->{$ref->{id}}->{params}->{email}=$ref->{email_owner};
      my $kind='params';
      &store_db( $user_db,  $ref->{id}, $kind);

}else{$pr_mes='20';}

$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

sub out_err_
{ my ($ref,$err) = @_;
  $ref->{mess} = $err;
  view_reg($ref);
  exit;
}

sub block_list {
 my $ref=shift;
# use Storable;
# my $user_db = retrieve $ref->{path_db};
 my $user_db =$ref->{user_db};
 my $pr_mes='19';
 if($ref->{save} eq 'ok'){
  if(length($ref->{block_ip})<100){
    $user_db->{data}->{$ref->{id}}->{params}->{block_ip}=$ref->{block_ip};
    my $kind='params';
    &store_db($user_db,  $ref->{id}, $kind);
  }
 }else{$pr_mes='20';}
$ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
my $time=time;
 print qq[
  <HTML>
  <body>
  <script>location.href="$ref->{referrer}&mes=$pr_mes&$time"</script>
  </body>
  </HTML>
 ];
  exit;
}

1;