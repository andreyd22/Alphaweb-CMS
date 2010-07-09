#!/usr/bin/perl -w

$|=1;
 use Benchmark; 
 my $time1 = new Benchmark; 
 print "Content-type:text/html;Cache-control: no-cache, no-store;Pragma: no-cache;Expires: 0\r\n\r\n";
 print qq[<html><title></title><body>];
# ��������� ���� ���� - ������� ���� � �������� ������ �� ����                                                                                
 use lib "../";                                                                                       
 use Modules::Constructor_view;                                                                       
 use Modules::Constructor;                                                                            

 use strict;                                                                                          
 my $ref=Get_Param_view||{};                                                                          
 my $p=1;                                                                                             
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

if($ref->{a} eq ''){

print qq[<h1>� ������� ����� ������ �� ������ ��������� ���� ���� �� ��������� ���������!</h1>
����� ��������� ���������� ����� - �� ����� $ref->{root_mail} ������� ����������� �� �������     
�� ���� ������ <br><br>
<a href="/cgi-bin/mod/save_site.cgi?a=save">��������� offline ������ ����� ?</a>
];
}
if($ref->{a} eq 'save'){

my $old=`ps ax|grep wget;`;

#print qq[$old]; exit;
if( $old=~m!\(cd $ref->{path_host}; wget -m!gi){
print qq[������� ���������� ����� ��� �������! ��������� ����������� �� ����� $ref->{root_mail}];
exit;
}

print qq[
<h1>����� ��������� ���������� ����� - �� ����� $ref->{root_mail} ������� ����������� �� ������� 
�� ���� ������</h1>                                                                                   

];
if($ref->{path_host}=~/\*/gi){print "�������� ���� � ����������"; exit;}
    chroot "$ref->{path_host}";
    my $commands=qq[cd $ref->{path_host};                                                             
wget -m -k -p $ref->{host_name};                                                            
tar cfz ./$ref->{host_name}.tar.gz ./$ref->{host_name};
echo 'Subject: ������� �� ���������� ����� ���������' >> ./temp.letter;
echo '���� ������� �������� � �������� �� ������                                                      
http://$ref->{host_name}/base/$ref->{host_name}.tar.gz' >> ./temp.letter;
echo '������ ������: ' >> ./temp.letter;
du -sh ./$ref->{host_name}.tar.gz >> ./temp.letter;
cat ./temp.letter | /usr/sbin/sendmail $ref->{root_mail};                             
rm -f ./temp.letter;];
    $commands=~s/\n|\t|\r/ /gi;
    $commands=~s/\s+/ /gi;
   close(STDIN);
   close(STDERR);
   close(STDOUT);

   open(STDERR, ">/dev/null");
   open(STDOUT, ">/dev/null");
   open(STDIN, ">/dev/null");
    my $wget = `($commands) &`;

# ������ ������ �� ��������! 
print qq[
<br>
�� ������ ������� ����������� ������ ����� �� ������ 
  <br><center>
<a href="http://$ref->{host_name}/base/$ref->{host_name}.tar.gz" target=_blank>http://$ref->{host_name}/base/$ref->{host_name}.tar.gz</a>
</center>
<h1>����� ��������� ���������� ����� - �� ����� $ref->{root_mail} ������� ����������� �� ������� 
�� ���� ������</h1>                                                                                   
];     
} 

my $time2 = new Benchmark; 

my $timebenchmark = timediff($time1, $time2); 
print "<br><br><small>Time", timestr($timebenchmark), "</small><br><br></body></html>";