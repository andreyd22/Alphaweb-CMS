package Modules::MysqlFunction;
$|=1;

# Отладочные функции
use CGI::Carp qw(fatalsToBrowser);
use Data::Dumper;
    use Data::Dumper;

use CGI;


require Exporter;

  @ISA = qw(Exporter);

# Items to export into callers namespace by default. Note: do not export
# names by default without a very good reason. Use EXPORT_OK instead.
# Do not simply export all your public functions/methods/constants.

# This allows declaration       use Modules::Constructor ':all';
# If you do not need this, moving things directly into @EXPORT or @EXPORT_OK
# will save memory.
#our  %EXPORT_TAGS = ( 'all' => [ qw( ) ] );

#our  @EXPORT_OK = ( @{ $EXPORT_TAGS{'all'} } );

  @EXPORT = qw(  &select_sql &insert_sql &update_sql &delete_sql  );

 $VERSION = '0.01';
# Preloaded methods go here.

 BEGIN { }

sub select_sql {
    my $ref	= shift; # ссылка на переменные
    my $tbl_name= shift; # название таблицы
    my $query	= shift; # запрос
    my $ar_vals	= shift; # переменные запроса
    my $is_type	= shift; # 1 - запрашивать названия полей
    my @vals = @$ar_vals;
    my @quote_vals=();
    for(my $i=0;$i<=$#vals;$i++){push @quote_vals,$ref->{dbh}->quote($vals[$i]);}
    my @ar=();

#    print qq[$query @vals];
    my $sth=$ref->{dbh}->prepare($query);
#    print qq[query: $query<br>vals: @quote_vals<br>];
    $sth->execute(@quote_vals);
    while(my $ref_data=$sth->fetchrow_hashref){
      	 push @ar,$ref_data;
    }
    my $names 		= $sth -> {NAME};
    #my $types 		= $sth -> {type};
    $sth->finish;

    # выбираем комментарии к столбцам
    my @ar_names=@$names;
    my @ar_comments=();
    my @ar_types=();
    if($tbl_name && $is_type){
    my ($nametbl_,$schema)=$ref->{dbh}->selectrow_array("show create table $tbl_name");
	for(my $i=0;$i<=$#ar_names;$i++){
	    my $comment='';
	    if($schema=~/\`$ar_names[$i]\`(.+?)COMMENT \'(.+?)\'/){
	    $comment=$2;
	    }
	    push @ar_comments,$comment;
	}
    # выбираем типы столбцов
    my $sth=$ref->{dbh}->prepare("show fields from $tbl_name");
    $sth->execute();
        while(my $ref_data=$sth->fetchrow_hashref){
		 $ref_data->{Type_short}=$ref_data->{Type};
		 $ref_data->{Type_short}=~s/(\(.+?\))//gi;
	  	 push @ar_types,$ref_data;
	}
	#print Dumper(\@ar_types);
    }
    
    return ($names,\@ar,\@ar_comments,\@ar_types);
}

sub insert_sql {
my $ref 	= shift;
my $tbl_name 	= shift;
my $not_update	= shift;
    my @ar_types=();
    # выбираем типы столбцов
    my $sth=$ref->{dbh}->prepare("show fields from $tbl_name");
    $sth->execute();
        while(my $ref_data=$sth->fetchrow_hashref){
	  	 push @ar_types,$ref_data;
	}
	#print qq[<b>$tbl_name</b><br><br>];
	my($keys_str,$values_vop);
	my @ar_values=();
	for(my $i=0;$i<=$#ar_types;$i++){
		#print qq[$ar_types[$i]->{Field} - $ar_types[$i]->{Type}<br>];
	    if ($ar_types[$i]->{Field} ne 'id' && $not_update!~/,$ar_types[$i]->{Field},/){
		$keys_str.="$ar_types[$i]->{Field},";
		if($ar_types[$i]->{Field} eq 'zip'){
		    $values_vop.="MD5($ref->{time}),";
		}
		else
		{
		    if($ar_types[$i]->{Type} =~ /date/ && !$ref->{$ar_types[$i]->{Field}}){
			$values_vop.="NOW(),";
		    }
		    else{
    			$values_vop.="?,";
			push @ar_values,$ref->{$ar_types[$i]->{Field}}||CGI::param($ar_types[$i]->{Field})||0;
		    }
		}
	    }
	}
	$keys_str=~s/,$//gi;$values_vop=~s/,$//gi;
    	my $insert_sql="insert into $tbl_name ($keys_str) values ($values_vop)";
	#print qq[$insert_sql @ar_values]; 
	$ref->{dbh}->do("$insert_sql",undef,@ar_values);

	my $id=$ref->{dbh}->last_insert_id(undef, undef, undef, undef);

return $id;
}

sub update_sql {
my $ref 	= shift;
my $tbl_name 	= shift;
my $id 		= shift;
my $not_update	= shift;

    my @ar_types=();

    # выбираем типы столбцов
    my $sth=$ref->{dbh}->prepare("show fields from $tbl_name");
    $sth->execute();
        while(my $ref_data=$sth->fetchrow_hashref){
	  	 push @ar_types,$ref_data;
	}
	my($keys_str,$values_vop);
	my @ar_values=();
	for(my $i=0;$i<=$#ar_types;$i++){
	    if ($ar_types[$i]->{Field} ne 'id' && $not_update!~/,$ar_types[$i]->{Field},/){ #not_update - строка с запрещенными для обновления полями
		if($ar_types[$i]->{Field} eq 'zip'){
		#print qq[$ar_types[$i]->{Field}<br>];
		    $keys_str.="$ar_types[$i]->{Field}=MD5(?),";
    		    push @ar_values,time;
		}
		elsif($ar_types[$i]->{Type} =~ /date/ && !$ref->{$ar_types[$i]->{Field}}){
		    $keys_str.="$ar_types[$i]->{Field}=NOW(),";
		}
		else{
		    $keys_str.="$ar_types[$i]->{Field}=?,";
    		    push @ar_values,$ref->{$ar_types[$i]->{Field}}||CGI::param($ar_types[$i]->{Field})||0;
		}
	    }
	}
	$keys_str=~s/,$//gi; push @ar_values,$id;
	my $insert_sql="update $tbl_name set $keys_str where id=?";
	#print $insert_sql." --- ".$not_update;
	my $upd=$ref->{dbh}->do($insert_sql,undef,@ar_values);
return $upd;
}

sub delete_sql {
my $ref 	= shift;
my $tbl_name 	= shift;
my $id		= shift;
    my $del=$ref->{dbh}->do("delete from $tbl_name where id=?",undef,($id));
return $del;
}

 END { }
1;