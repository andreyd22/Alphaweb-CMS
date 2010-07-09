#!/usr/bin/perl
#модуль вывода советов
 use Data::Dumper;
 $|=1;
 use Modules::Constructor qw (Get_Param);
 use strict;
 my $ref=Get_Param||{};
    
      use Encode 'from_to';
    

   print "Content-type:text/html\r\n\r\n";
    if ($ref->{id_sovet}){
	$ref->{dop_id}="and id!='$ref->{id_sovet}'"
    }
   my $count=$ref->{dbh}->selectrow_array("select count(*) from news where idr='sovet' $ref->{dop_id}");
    
   my $t=int(rand($count));
    
   my $ref_sovet=$ref->{dbh}->selectrow_hashref("select * from news where idr='sovet' $ref->{dop_id} limit $t,1");    
   #<a href="/news/sovet/$ref_sovet->{id}.html">Узнать подробнее</a>
   my $str = qq[<h1>$ref_sovet->{zag}</h1>
<p>$ref_sovet->{short}</p> 

    <form id="sendF">
    <input type="hidden" name="id_sovet" value="$ref_sovet->{id}" id="id_sovet">
    </form>
    ];
      from_to($str, "windows-1251", "utf-8");

    print $str;
