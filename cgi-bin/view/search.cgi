#!/usr/bin/perl
#������ ������ �� �����
 $|=1;
 use lib "../";
 use locale;
 use POSIX qw(locale_h);
 setlocale(LC_ALL, 'ru_RU.CP1251');
 use Modules::Constructor qw (&Get_Param &dbconnect &dbdisconnect &page_down $host_name 
                              &check_auth &encoder &send_mail &table_exists
                              &slovo);
 use Modules::Constructor_view;
 use strict;
use CGI::Carp qw(fatalsToBrowser);
my $time=time;
my $ref=Get_Param_view||{};
 print "Content-type:text/html\r\n\r\n";

 $ref->{index_tpl} = "index.tpl"; 
 $ref->{tpl_}="search.tpl";

if ($ref->{'a'} eq '') {$ref=all_catalog($ref);} #����� ��������

 print_($ref);

sub all_catalog { #����� ���������� ����������
 my $ref=shift;
 #������� �� ���������
 my $CountPage=25; # ���������� ������� �� ��������
 my $PageIn=CGI::param('PageIn')||1;
 my $p_n=CGI::param('p_n')||0;
 my $off=$p_n*$CountPage;
 if($ref->{slovo}){
  $ref->{slovo}=~s/\%|\*|\&|\?|\||\///gi;
  $ref->{slovo}=~s/^\s+//gi;
  $ref->{slovo}=~s/\s+$//gi;
 }
 my $search_all;my $count_all=0;my $gal='';my $slovo=$ref->{slovo};my $ok=0;
if($slovo=~/^[A-Z�-�a-z�-�0-9\s\-\_]+$/gi) {$ok=1;
#print qq[�������];
}
if(!$ref->{slovo}||length($ref->{slovo})<=3||$ok!=1)
{$ref->{mess}=qq[������� �������� ����� ��� ������. ����� ������ ��������� �� ����� <b style="color:red">4 ��������</b>]; return $ref;} #���� �� ������ ����� ��� ������
 #������� ���������� ������
 my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
if($ref->{type} eq 'catalogue'){
 #������ ����� �� ��������
 my ($ref_data,$count)=list_search_catalog($ref); #�������� � ������ ��� �� �������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }

}
else
{
 my ($ref_data,$count)=list_search_document($ref); #���� �� ��������� ����� ��� ����������
     use Data::Dumper;
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
if(table_exists(qq[`news`])){
 #������ ����� �� ��������
 my ($ref_data,$count)=list_search_news($ref); #�������� � ������ ��� ������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
}
if(table_exists(qq[`gallery_`])){
 #������ ����� �� ���������
 my ($ref_data,$count)=list_search_gallery($ref); #�������� � ������ ��� �� �������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
}
if(table_exists(qq[`article`])){
 #������ ����� �� ��������
 my ($ref_data,$count)=list_search_article($ref); #�������� � ������ ��� ������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
}
if(table_exists(qq[`guest_`])){
 #������ ����� �� ��������/�������
 my ($ref_data,$count)=list_search_guest($ref); #�������� � ������ ��� ���������� � �������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
}
if(table_exists(qq[`catalog`])){
 #������ ����� �� ��������
 my ($ref_data,$count)=list_search_catalog($ref); #�������� � ������ ��� �� �������� �� ����������� ������
    my $ar_link_new=$ref_data->{ar_link};my $ar_name_new=$ref_data->{ar_name};my $ar_opis_new=$ref_data->{ar_opis};my $ar_keywords_new=$ref_data->{ar_keywords};
    if($count>0){
    push @ar_link,@$ar_link_new;push @ar_name,@$ar_name_new;push @ar_opis,@$ar_opis_new;push @ar_keywords,@$ar_keywords_new;
    $count_all+=$count;
    }
}
}

 my $kol;
 if($count_all%$CountPage==0){$kol=int($count_all/$CountPage);}else{$kol=int($count_all/$CountPage)+1;}
my $inc=0;
          for(my $i=$off;$inc<=$CountPage and $i<=$count_all and $ar_link[$i] ne '';$i++){
          $inc++;
            $ref->{ar_data}[$inc]={
		name => $ar_name[$i],
        	opis=>$ar_opis[$i],
        	link=>$ar_link[$i],
        	keywords=>$ar_keywords[$i]
	    };
          }

    #������� �� ���������
    my $host_name1="/search/$ref->{id}.html?slovo=$ref->{slovo}";
     $ref->{perehod}=&page_down($host_name1,$kol,$PageIn,$p_n,$CountPage);

 my $zag=" �����";

return $ref;
}

sub list_search_document { #����� ��������� ������ ��� ���������� (������ �� ���� ���������)
 my $ref=shift;
 my $dbh=dbconnect;
my $dop=qq[and (upper(zag) like upper('%$ref->{slovo}%') or upper(name) like upper('%$ref->{slovo}%')
 or upper('description') like upper('$ref->{slovo}') or upper('keywords') like upper('$ref->{slovo}'))];


 my $sel="select * from structure where visible='tree1=1,menu1=1' $dop";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_struct=$sth->fetchrow_hashref){

	
          my $pr_link="/$ref_struct->{module}/$ref_struct->{id}.html";
          if ($ref_struct->{link}){$pr_link=$ref_struct->{link};}

          my $search_str=$ref_struct->{name}." ".$ref_struct->{zag}." ".$ref_struct->{description}." ".$ref_struct->{keywords};
	 my $opis=$ref_struct->{description};
         if(!$ref_struct->{description}){
         ##��������� ���� � ������� ��� ��������������� ������ 
         open A, "$ref->{path_db}.$ref_struct->{id}.data"||'';
         my @file=<A>;
         close A;
         $opis=join('',@file);
         ##��������� ���� � �������
          if($opis){
          $opis=~s/<([.+?^\/>])>/ /gi;
          $opis=~s/<\/(.+?)>/ /gi;
          $opis=substr $opis, 0, 200; #�������� ������ 200 ��������
          $opis.="...";
          }
         }
          
          $search_str=~s/<(.+?)>/ /gi;
          $search_str=~s/\s+/ /gi;
          $search_str=~s/^\s+|\s+$//gi;
          $search_str=~s/\s+/ /gi;
          my @ar= split / /,$search_str;
          my $ok=0;
            if($search_str=~/$ref->{slovo}/i){$ok=1}
             if($ok!=0){
             $ref_struct->{name}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             $ref_struct->{zag}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             $ref_struct->{description}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             $ref_struct->{keywords}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             $opis=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_struct->{name};
             push @ar_opis,$opis."<p align=\"left\"><small>��������</small></p>";
             push @ar_keywords,$ref_struct->{keywords};
            }

    }
    $sth->finish;
my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
    };
 my $count=$#ar_link;
    $count++;
return ($ref_data,$count);

}


sub list_search_news { #����� ��������� ������ ��� �������� 
 my $ref=shift;
 my $dbh=dbconnect;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
my $dop=qq[and (upper(zag) like upper('%$ref->{slovo}%') or upper(short) like upper('%$ref->{slovo}%'))];
 my $dop_r="";
# if($ref->{id}){$dop_r="and idr='$ref->{id}'";}
# my $col="select count(*) from news where 1 $dop_r $dop";
# my $count=$dbh->selectrow_array($col);
 my $kol;
 my $order='order by id desc';
#    $order='order by name' if $ref->{sort} eq 'name';
 #������� �� ���������
 my $sel="select * from news where 1 $dop_r $dop $order";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_news=$sth->fetchrow_hashref){
             $ref_news->{zag}=~s/<(.+?)>//gi;
             $ref_news->{short}=~s/<(.+?)>//gi;
             if($ref_news->{zag}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi || $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi)
                {1}else{next;}
#             if($ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi){1}else{next;}
#             $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             my $pr_link="/news/$ref_news->{idr}/$ref_news->{id}.html";
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_news->{zag};
             push @ar_opis,$ref_news->{short}; #."<p align=right>�������</p>";
             push @ar_keywords,'';
             $count++;
    }
    $sth->finish;
 dbdisconnect($dbh);
 my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
 }  ;
return ($ref_data,$count);
}

sub list_search_gallery { #����� ��������� ������ ��� ���������
 my $ref=shift;
 my $dbh=dbconnect;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
 my $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(opis) like upper('%$ref->{slovo}%'))];
 my $dop_r="";
# if($ref->{id}){$dop_r="and idr='$ref->{id}'";}
# my $col="select count(*) from news where 1 $dop_r $dop";
# my $count=$dbh->selectrow_array($col);
 my $kol;
 my $order='order by date_reg desc, id desc';
#    $order='order by name' if $ref->{sort} eq 'name';
 #������� �� ���������
 my $sel="select * from gallery_ where 1 $dop_r $dop $order";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_news=$sth->fetchrow_hashref){
             $ref_news->{name}=~s/<(.+?)>//gi;
             $ref_news->{opis}=~s/<(.+?)>//gi;
             if($ref_news->{name}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi || $ref_news->{opis}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi)
                {1}else{next;}
#             if($ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi){1}else{next;}
#             $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             my $pr_link="/gallery/$ref_news->{idr}/$ref_news->{id}.html";
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_news->{name};
             push @ar_opis,$ref_news->{opis}."<p align=\"left\"><small>���������</small></p>";
             push @ar_keywords,'';
             $count++;
    }
    $sth->finish;
 dbdisconnect($dbh);
 my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
 }  ;
return ($ref_data,$count);
}

sub list_search_article { #����� ��������� ������ ��� ������
 my $ref=shift;
 my $dbh=dbconnect;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
 my $dop=qq[and (upper(zag) like upper('%$ref->{slovo}%') or upper(short) like upper('%$ref->{slovo}%'))];
 my $dop_r="";
# if($ref->{id}){$dop_r="and idr='$ref->{id}'";}
# my $col="select count(*) from news where 1 $dop_r $dop";
# my $count=$dbh->selectrow_array($col);
 my $kol;
 my $order='order by id desc';
#    $order='order by name' if $ref->{sort} eq 'name';
 #������� �� ���������
 my $sel="select * from article where 1 $dop_r $dop $order";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_news=$sth->fetchrow_hashref){
             $ref_news->{zag}=~s/<(.+?)>//gi;
             $ref_news->{short}=~s/<(.+?)>//gi;
             if($ref_news->{zag}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi || $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi)
                {1}else{next;}
#             if($ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi){1}else{next;}
#             $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             my $pr_link="/article/$ref_news->{idr}/$ref_news->{id}.html";
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_news->{zag};
             push @ar_opis,$ref_news->{short}; #."<p align=right>�������</p>";
             push @ar_keywords,'';
             $count++;
    }
    $sth->finish;
 dbdisconnect($dbh);
 my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
 }  ;
return ($ref_data,$count);
}

sub list_search_guest { #����� ��������� ������ ��� ��������/�������
 my $ref=shift;
 my $dbh=dbconnect;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
my $dop=qq[and (upper(subject) like upper('%$ref->{slovo}%') or upper(record) like upper('%$ref->{slovo}%'))];
 my $dop_r="and answer!=''";
 my $kol;
 my $order='order by id desc';
 #������� �� ���������
 my $sel="select * from guest where 1 $dop_r $dop $order";
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_news=$sth->fetchrow_hashref){
             $ref_news->{subject}=~s/<(.+?)>//gi;
             $ref_news->{record}=~s/<(.+?)>//gi;
             if($ref_news->{subject}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi || $ref_news->{record}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi)
                {1}else{next;}
#             if($ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi){1}else{next;}
#             $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
#             my $pr_link="/consult$ref_news->{id}.html";
             my $pr_link="/guest/$ref_news->{idr}/$ref_news->{id}.html";
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_news->{subject};
             push @ar_opis,$ref_news->{record}; #."<p align=right>�������</p>";
             push @ar_keywords,'';
             $count++;
    }
    $sth->finish;
 dbdisconnect($dbh);
 my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
 }  ;
return ($ref_data,$count);
}

sub list_search_catalog { #����� ��������� ������ ��� ��������
 my $ref=shift;
 my $dbh=dbconnect;
  # $dop=qq[and MATCH(name,short,opis) AGAINST('$ref->{slovo}')];
 my $dop=qq[and (upper(name) like upper('%$ref->{slovo}%') or upper(short) like upper('%$ref->{slovo}%'))];
 my $dop_r=qq[];
 my $kol;
 my $order='order by id desc';
 #������� �� ���������
 my $sel="select * from catalog_$ref->{prefix} where 1 $dop_r $dop $order";
# print qq[$sel]; exit;
 my $sth=$dbh->prepare($sel);
    $sth->execute;
    my $count=0;
    my (@ar_link,@ar_name,@ar_opis,@ar_keywords); #������� ��� �������� ���� ����������� ������ �� ���������
    while(my $ref_news=$sth->fetchrow_hashref){
             $ref_news->{name}=~s/<(.+?)>//gi;
             $ref_news->{short}=~s/<(.+?)>//gi;
             if($ref_news->{name}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi || $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi)
                {1}else{next;}
#             if($ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi){1}else{next;}
#             $ref_news->{short}=~s/$ref->{slovo}/<b>$ref->{slovo}<\/b>/gi;
             my $pr_link="/catalog/$ref_news->{idr}/$ref_news->{id}.html";
             push @ar_link,$pr_link;                       
             push @ar_name,$ref_news->{name};
             push @ar_opis,$ref_news->{short}; #."<p align=right>�������</p>";
             push @ar_keywords,'';
             $count++;
    }
    $sth->finish;
 dbdisconnect($dbh);
 my $ref_data={
 'ar_link'=>\@ar_link,
 'ar_name'=>\@ar_name,
 'ar_opis'=>\@ar_opis,
 'ar_keywords'=>\@ar_keywords,
 }  ;
return ($ref_data,$count);
}

1;