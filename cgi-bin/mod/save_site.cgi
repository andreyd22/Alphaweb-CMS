#!/usr/bin/perl -w

$|=1;
 use Benchmark; 
 my $time1 = new Benchmark; 
 print "Content-type:text/html;Cache-control: no-cache, no-store;Pragma: no-cache;Expires: 0\r\n\r\n";
 print qq[<html><title></title><body>];
# сохраняем весь сайт - сжимаем сайт и высылаем ссылку на него                                                                                
 use lib "../";                                                                                       
 use Modules::Constructor_view;                                                                       
 use Modules::Constructor;                                                                            

 use strict;                                                                                          
 my $ref=Get_Param_view||{};                                                                          
 my $p=1;                                                                                             
#!!!Проверка sid пользователя!!!#                                                                     
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
#!!!Проверка sid пользователя!!!#                                                                     
#!!!Проверка уровня доступа!!!                                                                        
check_access($ref);                                                                                   
#!!!Проверка уровня доступа end!!!  

if($ref->{a} eq ''){

print qq[<h1>С помощью этого модуля вы можете сохранить весь сайт на локальный компьютер!</h1>
После окончания сохранения сайта - на емайл $ref->{root_mail} прийдет уведомление со ссылкой     
на файл архива <br><br>
<a href="/cgi-bin/mod/save_site.cgi?a=save">Сохранить offline версию сайта ?</a>
];
}
if($ref->{a} eq 'save'){

my $old=`ps ax|grep wget;`;

#print qq[$old]; exit;
if( $old=~m!\(cd $ref->{path_host}; wget -m!gi){
print qq[Процесс сохранения сайта уже запущен! Дождитесь уведомления на почту $ref->{root_mail}];
exit;
}

print qq[
<h1>После окончания сохранения сайта - на емайл $ref->{root_mail} прийдет уведомление со ссылкой 
на файл архива</h1>                                                                                   

];
if($ref->{path_host}=~/\*/gi){print "Неверный путь к директории"; exit;}
    chroot "$ref->{path_host}";
    my $commands=qq[cd $ref->{path_host};                                                             
wget -m -k -p $ref->{host_name};                                                            
tar cfz ./$ref->{host_name}.tar.gz ./$ref->{host_name};
echo 'Subject: Задание по сохранению сайта выполнено' >> ./temp.letter;
echo 'Сайт успешно сохранен и доступен по адресу                                                      
http://$ref->{host_name}/base/$ref->{host_name}.tar.gz' >> ./temp.letter;
echo 'Размер архива: ' >> ./temp.letter;
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

# дальше скрипт не работает! 
print qq[
<br>
Вы можете скачать сохраненную версию сайта по ссылке 
  <br><center>
<a href="http://$ref->{host_name}/base/$ref->{host_name}.tar.gz" target=_blank>http://$ref->{host_name}/base/$ref->{host_name}.tar.gz</a>
</center>
<h1>После окончания сохранения сайта - на емайл $ref->{root_mail} прийдет уведомление со ссылкой 
на файл архива</h1>                                                                                   
];     
} 

my $time2 = new Benchmark; 

my $timebenchmark = timediff($time1, $time2); 
print "<br><br><small>Time", timestr($timebenchmark), "</small><br><br></body></html>";