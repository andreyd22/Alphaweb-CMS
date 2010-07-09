#!/usr/bin/perl
#!!!Скрипт, отвечающий за работу с разделами сайта
 $|=1;
 use lib "../";
 use Modules::Constructor;
 use strict;
 print "Content-type:text/html\r\n\r\n";
 my $ref=Get_Param;
 $ref->{sid}=time;
#!!!Проверка sid пользователя!!!#
 my $mes=check_auth($ref);
 if($mes){
   print qq[
      <HTML><HEAD><title>authorization error</title></HEAD>
    <body>
    <script>parent.location.href="/cgi-bin/view.pl?a=mes&l=$ref->{l}&mes=$mes"</script>
    </body>
    </HTML>
     ];
 exit;
 }
#!!!Проверка sid пользователя!!!#
#!!!Проверка уровня доступа!!!
check_access($ref);
#!!!Проверка уровня доступа end!!!
if ($ref->{a} eq ''){edit_st($ref)} #Выводим форму для редактирования статьи (form insert new article)
if ($ref->{a} eq 'save'){save($ref)} #Сохраняем информацию

sub edit_st {
my $ref=shift;
      my $def={  
      		"main"=>"/constructor_document_editor_main_fck.html.$ref->{l}",
#                 "text"=>"/constructor_editor.html.$ref->{l}",
             };
     if($ref->{page} eq 'simple'){
	$def={  
      		"main"=>"/constructor_document_editor_main_simple.html.$ref->{l}",
#                 "text"=>"/constructor_editor.html.$ref->{l}",
             };
     }
 my $title=slovo(19,$ref->{l}); #Редактор документа 
 $ref->{def}=$def;
 $ref->{title}=$title;
 my $tpl=tplb($ref);
my $mes='';
if ($ref->{mes}){$mes=message($ref)}
open A, "$ref->{path_db}.$ref->{id}.data";
my @ar_text=<A>;
close A;
my $text=join('',@ar_text);

if($ref->{page} ne 'simple'){
   $text=~s/\n/ /gi;
   $text=~s/\s+/ /gi;
   $text=~s/'/"/gi; #'
}

 $tpl->assign(
             MESSAGE=>$mes,
             NAME_ST=>$ref->{user_db}->{data}->{$ref->{id}}->{name},
             DATA=>$text,
             HTTP_HOST=>$host_name,
             MOD=>$ref->{user_db}->{data}->{$ref->{id}}->{mod},
             ID=>$ref->{id}
             );
# $tpl->parse(TEXT => "text");
# $tpl->clear_href(1);
 $tpl->parse(CONTENT => "main");
 $tpl->clear_href(1);
 my $content = $tpl->fetch("CONTENT");
 print $$content;
 $tpl->clear_href(1);
 $tpl->clear();
}

sub save {
 my $ref=shift;
 my $pr_mes='19';
 if($ref->{save} eq 'ok'){
 open A, "+>$ref->{path_db}.$ref->{id}.data" or die $!;
 print A $ref->{content};
 close A;
 }
  
   if($ref->{save} ne 'ok'){$pr_mes='20';}
   $ref->{referrer}=~s/\&mes=19|\&mes=20//gi;
   my $time=time;
   my $sort=$ref->{user_db}->{data}->{sort}||{};
   my %sort=%$sort;
   my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
print qq[
  <HTML>
  <body>
  <script>
parent.load.location.href="/cgi-bin/view/$ref->{user_db}->{data}->{$ar_sort_key[0]}->{mod}.cgi?id=$ar_sort_key[0]&sid=$ref->{sid}";
location.href="$ref->{referrer}&mes=$pr_mes&rnd=$time"
</script>
  </body>
  </HTML>
 ];
  exit;
}