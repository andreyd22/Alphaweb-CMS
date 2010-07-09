#!/usr/bin/perl

print "content-type:text/html\r\n\r\n";
use CGI;
use strict;
 use lib "./";
 use Modules::Constructor qw(data_filter);

my $path=CGI::param('path');
my $title=CGI::param('title');
 my $err;
  ($path, $err)=data_filter($path);
  ($title, $err)=data_filter($title);
my $path_=$path;
   $path_=~s/http:\/\///gi;
my @ar_path=split /\//,$path_;
my $url=$ar_path[0];
print qq[<html>
<head><title>$title</title>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
<link href="/style.css" rel="stylesheet" type="text/css"></head>
<body topmargin=0 marginheight=0 leftmargin=0 marginwidth=0>
<h2>$title</h2>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="http://$url" onclick="print();return false;">Печать</a><br>
<center>
<img src="$path" title="$title" vspace=3>
<br><small><a href="javascript:window.close()">[закрыть окно]</a></small></center>
</body>
</html>];