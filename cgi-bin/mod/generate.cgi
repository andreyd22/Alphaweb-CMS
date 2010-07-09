#!/usr/bin/perl
#��������� ����� ������������ �� ������� ������� (���. ������������ �������:
# ������� ��� ������ ������������
#���������� (insert_sql), ���������� (update_sql), �������� (delete_sql) � ������ ������ (select_sql) �� ������ ��)
 $|=1;
 use lib "../";
 use Modules::Constructor_view;
 use Modules::Constructor;
 use strict;
 my $ref=Get_Param_view||{};
# my $ref=Get_Param;
 my $p=1;
#print qq[perf $ref->{prefix}];exit;
#!!!�������� sid ������������!!!#
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
#!!!�������� sid ������������!!!#
#!!!�������� ������ �������!!!
check_access($ref);
#!!!�������� ������ ������� end!!!
 print "Content-type:text/html\r\n\r\n";

 $ref->{index_tpl} = "index_admin.tpl"; 
 $ref->{tpl_}="generate_admin.tpl";
 $ref->{name_action}="������������� ����� ������������";
# $ref->{module_name}="anketa";
 if ($ref->{'a'} eq '') {$ref=view_tables($ref); } #����� ������ ���� ������
 if ($ref->{'a'} eq 'form_edit') {$ref=form_edit($ref); } #����� ����� ����� ������� ��� ��������� �������� � �������� ���������� � ������ ������
 if ($ref->{'a'} eq 'generate') {$ref=generate($ref); } #���������
 print_($ref);

 sub view_tables {
    my $ref=shift;

    my $tbl_name="";
    my $query="show tables";
#    my $query="select * from new_article";
#    my $query="show fields from new_article";

    ($ref->{name_fields},$ref->{ar_data},$ref->{fields_comment},$ref->{type_fields})=select_sql($ref,$tbl_name,$query,[],1);

    #use Data::Dumper;
    #print Dumper($ref->{ar_data});
	
    return $ref;
 }
 sub form_edit {
    my $ref=shift;
    return $ref;
 }

 sub generate {
    my $ref=shift;
    # �������� - �������
    my $tpl_file_admin_source="$ref->{path_root}/templates/generate/admin_template.tpl";
    my $tpl_file_view_source="$ref->{path_root}/templates/generate/view_template.tpl";
    my $cgi_file_admin_source="$ref->{path_root}/templates/generate/admin.cgi";
    my $cgi_file_view_source="$ref->{path_root}/templates/generate/view.cgi";
    
    # ���� ������������ �������
    my $tpl_dir="$ref->{path_root}/templates/$ref->{table_name}";
    my $tpl_file_admin="$ref->{path_root}/templates/$ref->{table_name}/$ref->{table_name}_admin.tpl";
    my $tpl_file_view="$ref->{path_root}/templates/$ref->{table_name}/$ref->{table_name}.tpl";
    my $cgi_file_admin="$ref->{path_cgi}/mod/$ref->{table_name}.cgi";
    my $cgi_file_view="$ref->{path_cgi}/view/$ref->{table_name}.cgi";
    my $ini_file="$ref->{path_cgi}/mod/$ref->{table_name}.ini";

    my @ar_files=($tpl_file_admin,$tpl_file_view,$cgi_file_admin,$cgi_file_view,$ini_file);
	if(!&table_exists("`$ref->{table_name}`")){
	    $ref->{mess}="������� $ref->{table_name} �� ����������";
	    return $ref;
	}
	if(!$ref->{name} || !$ref->{opis} || !$ref->{table_name}){
	    $ref->{mess}="��� ���� ������ ���� ���������";
	    return $ref;
	}
	if(-d $tpl_dir){
	    $ref->{mess}.="����� �������� $tpl_dir ��� ����������<br>";
	}else{
            mkdir_($tpl_dir);
	}

	for(my $i=0;$i<=$#ar_files;$i++){
	    if(-e $tpl_file_admin){
		$ref->{mess}.="���� $ar_files[$i] ��� ����������<br>";
		return $ref;
	    }else{

	    }
	}
	open A, "+>$ini_file";
	print A "$ref->{table_name}.cgi=$ref->{name}=$ref->{table_name}=$ref->{opis}=You can create news archive=visible";
	close A;
	my $cmd = `cp $tpl_file_admin_source $tpl_file_admin`;
	print qq[����� ������ ������ $cmd $tpl_file_admin_source $tpl_file_admin_source<br>];

	my $cmd2 = `cp $tpl_file_view_source $tpl_file_view`;
	print qq[������ ������ ������ $cmd2 $tpl_file_view_source $tpl_file_view_source<br>];

	my $cmd3 = `cp $cgi_file_admin_source $cgi_file_admin`;
	chmod 0755, "$cgi_file_admin";
	print qq[����� ������ ������ $cmd3 $cgi_file_admin_source $cgi_file_admin<br>];

	my $cmd4 = `cp $cgi_file_view_source $cgi_file_view`;
	chmod 0755, "$cgi_file_view";
	print qq[������ ������ ������ $cmd4 $cgi_file_view_source $cgi_file_view<br>];
    $ref->{status}="success";
    return $ref;
}