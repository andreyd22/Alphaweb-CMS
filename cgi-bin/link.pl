#!/usr/bin/perl

use CGI;

my $link=CGI::param('link');
 my $err;
  ($link, $err)=data_filter($link);
print "Content-type:text/html\r\n\r\n";
$link=~s/http:\/\///gi;
 print qq[
 <html>
 <head>
<META http-equiv="Refresh" content="0;URL=http://$link">
</head>
<body>
<center>http://$link</center>
</body>
</html>
 ];


sub data_filter{
use locale;
  my $data=shift||'';
  my $type=shift||'';
  my $err=0;
   #������ ������ - ������� ���, ��� �� ���������
    $data=~s/\%|\*|\&|\?|\||\"//gi; #������� ������� �������
#    $data=~=~s/[\|\-&\.\\\/\0]//gi;
    $data=~s/(<\w+?.*?>)+.*?(<\/\w+?.*?>)+//gi; #tags
    $data=~s/^\s+//gi;   #������� 
    $data=~s/\s+/ /gi;      # ������
    $data=~s/\s+$//gi;          # �������
 #����� ������ - ��������� ������ ��, ��� ��������� 
 if($type eq 'name'){
  $err=1 if $data!~/^[A-Za-z�-��-�0-9_\-\s]+$/gi;
 }elsif($type eq 'email'){   
   $err=1 if $data!~/^[_\.\w]+\@\w+\.\w+$/gi;
 }elsif($type eq 'tel'){
   $_=$data;
   $_=~s/\+|\(|\)|\-//gi;
   $err=1 if $_!~/^\d+([\s\d]*)$/gi;
 }
 no locale;
 return ($data,$err);
}
