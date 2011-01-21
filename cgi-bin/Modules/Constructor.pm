package Modules::Constructor;
$|=1;
#use 5.008; #!!!!!!!!!!!!!
#use strict;
#use warnings; #!!!!!!!!!!!!

#use Apache::Reload; #!!!!!!!! Почему то пишет в логи что не может загрузить этот модуль/ Решил проблем использованием startup.pl
use Modules::PathDB qw ($domain_config $path_cgi $path_root $path_to_lib $db_host $db_user $db_pass $db_name $host_name);
# Отладочные функции

use Modules::MysqlFunction;

use CGI::Carp qw(fatalsToBrowser);
use Data::Dumper;

#use Apache::Reload; #!!!!!!!! Почему то пишет в логи что не может загрузить этот модуль/ Решил проблем использованием startup.pl
use CGI;
# Object initialization:
if($path_to_lib ne ""){
	use lib "$path_to_lib"; 
}
#use CGI::Session;
#называем сессию SID
#CGI::Session->name("SID");

use FastTemplate;

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

  @EXPORT = qw(     &check_status &check_access &store_db &data_filter &table_exists
                    &Get_Param &dbconnect &dbdisconnect &send_mail &sel_mag
                    &get_data_from_sid &get_data_from_cook &user_menu &get_sid &get_idu &tplb
                    &check_auth &get_data &page_down &encoder &magick
                    &size_img &resize_img &write_on_picture &mkdir_
                    $path_admin_template $path_admin_preview 
                    $path  $path_host
                    %visible %link_view $color_option $size_option $font_option
                    $type_option $sel_host $razdel_option_e $razdel_option_r $path_db
                    @ar_sum $template_root &get_structure
                    %lang_tpl &slovo &message $host_name &check_captcha &set_captcha &composit_img &crop_img
		    &magick_width_only
		    &select_sql &insert_sql &update_sql &delete_sql &get_url $domain_config
);

 $VERSION = '0.02';
# Preloaded methods go here.
our ($path,$root_mail,$post_mail,$project,$time_out,$path_host,%visible,%link_view,$path_template_site, $phone_number,
$path_admin_preview, $path_db, $color_option, $size_option, $font_option, $type_option, $sel_host,
$razdel_option_e,$razdel_option_r,$template_root,@ar_sum,@ar_plan,@ar_name_plan,$dostavka_rus, $dostavka_eng, $oplata_rus, $oplata_eng, $status_rus,$status_eng,
%lang_tpl,$dbh_, $domain_config
);

 BEGIN
{
$template_root=$path_root."/template_constructor";

$color_option=qq[<option value="#F0F8FF" style="BACKGROUND-COLOR:#F0F8FF">alicemblue<option value="#FAEBD7" style="BACKGROUND-COLOR:#FAEBD7">antiquewhite<option value="#7FFFD4" style="BACKGROUND-COLOR:#7FFFD4">aquamarine<option value="#F0FFFF " style="BACKGROUND-COLOR:#F0FFFF ">azure<option value="#F5F5DC" style="BACKGROUND-COLOR:#F5F5DC">beige<option value="#FFE4C4" style="BACKGROUND-COLOR:#FFE4C4">bisque<option value="#000000" style="BACKGROUND-COLOR:#000000">black<option value="#FFEBCD" style="BACKGROUND-COLOR:#FFEBCD">blanchedalmond<option value="#0000FF" style="BACKGROUND-COLOR:#0000FF">blue<option value="#8A2BE2" style="BACKGROUND-COLOR:#8A2BE2">blueviolet<option value="#A52A2A" style="BACKGROUND-COLOR:#A52A2A">brown<option value="#DEB887" style="BACKGROUND-COLOR:#DEB887">burlywood<option value="#5F9EA0" style="BACKGROUND-COLOR:#5F9EA0">cadetblue<option value="#7FFF00" style="BACKGROUND-COLOR:#7FFF00">chartreuse<option value="#D2691E" style="BACKGROUND-COLOR:#D2691E">chocolate<option value="#FF7F50" style="BACKGROUND-COLOR:#FF7F50">coral<option value="#6495ED" style="BACKGROUND-COLOR:#6495ED">cornflowerblue<option value="#FFF8DC" style="BACKGROUND-COLOR:#FFF8DC">cornsilk<option value="#DC143C" style="BACKGROUND-COLOR:#DC143C">crimson<option value="#00FFFF" style="BACKGROUND-COLOR:#00FFFF">cyan<option value="#00008B" style="BACKGROUND-COLOR:#00008B">darkblue<option value="#008B8B" style="BACKGROUND-COLOR:#008B8B">darkcyan<option value="#B8860B" style="BACKGROUND-COLOR:#B8860B">darkgoldenrod<option value="#A9A9A9" style="BACKGROUND-COLOR:#A9A9A9">darkgray<option value="#006400" style="BACKGROUND-COLOR:#006400">darkgreen<option value="#BDB76B" style="BACKGROUND-COLOR:#BDB76B">darkkhaki<option value="#8B008B" style="BACKGROUND-COLOR:#8B008B">darkmagenta<option value="#556B2F" style="BACKGROUND-COLOR:#556B2F">darkolivegreen<option value="#FF8C00" style="BACKGROUND-COLOR:#FF8C00">darkorange<option value="#9932CC" style="BACKGROUND-COLOR:#9932CC">darkochid<option value="#8B0000" style="BACKGROUND-COLOR:#8B0000">darkred<option value="#E9967A" style="BACKGROUND-COLOR:#E9967A">darksalmon<option value="#8FBC8F" style="BACKGROUND-COLOR:#8FBC8F">darkseagreen<option value="#483D8B" style="BACKGROUND-COLOR:#483D8B">darkslateblue<option value="#2F4F4F" style="BACKGROUND-COLOR:#2F4F4F">darkslategray<option value="#00CED1" style="BACKGROUND-COLOR:#00CED1">darkturquoise<option value="#9400D3" style="BACKGROUND-COLOR:#9400D3">darkviolet<option value="#FF1493" style="BACKGROUND-COLOR:#FF1493">deeppink<option value="#00BFFF" style="BACKGROUND-COLOR:#00BFFF">deepskyblue<option value="#696969" style="BACKGROUND-COLOR:#696969">dimgray<option value="#1E90FF" style="BACKGROUND-COLOR:#1E90FF">dodgerblue<option value="#B22222" style="BACKGROUND-COLOR:#B22222">firebrick<option value="#FFFAF0" style="BACKGROUND-COLOR:#FFFAF0">floralwhite<option value="#228B22" style="BACKGROUND-COLOR:#228B22">forestgreen<option value="#FF00FF" style="BACKGROUND-COLOR:#FF00FF">fushsia<option value="#DCDCDC" style="BACKGROUND-COLOR:#DCDCDC">gainsboro<option value="#F8F8FF" style="BACKGROUND-COLOR:#F8F8FF">ghostwhite<option value="#FFD700" style="BACKGROUND-COLOR:#FFD700">gold<option value="#DAA520" style="BACKGROUND-COLOR:#DAA520">goldenrod<option value="#808080" style="BACKGROUND-COLOR:#808080">gray<option value="#008000" style="BACKGROUND-COLOR:#008000">green<option value="#ADFF2F" style="BACKGROUND-COLOR:#ADFF2F">greenyellow<option value="#F0FFF0" style="BACKGROUND-COLOR:#F0FFF0">honeydew<option value="#FF69B4" style="BACKGROUND-COLOR:#FF69B4">hotpink<option value="#CD5C5C" style="BACKGROUND-COLOR:#CD5C5C">indiandred<option value="#4B0082" style="BACKGROUND-COLOR:#4B0082">indigo<option value="#FFFFF0" style="BACKGROUND-COLOR:#FFFFF0">ivory<option value="#F0E68C" style="BACKGROUND-COLOR:#F0E68C">khaki<option value="#E6E6FA" style="BACKGROUND-COLOR:#E6E6FA">lavender<option value="#FFF0F5" style="BACKGROUND-COLOR:#FFF0F5">lavenderblush<option value="#7CFC00" style="BACKGROUND-COLOR:#7CFC00">lawngreen<option value="#FFFACD" style="BACKGROUND-COLOR:#FFFACD">lemonchiffon<option value="#ADD8E6" style="BACKGROUND-COLOR:#ADD8E6">ligtblue<option value="#F08080" style="BACKGROUND-COLOR:#F08080">lightcoral<option value="#E0FFFF" style="BACKGROUND-COLOR:#E0FFFF">lightcyan<option value="#FAFAD2" style="BACKGROUND-COLOR:#FAFAD2">lightgoldenrodyellow<option value="#90EE90" style="BACKGROUND-COLOR:#90EE90">lightgreen<option value="#D3D3D3" style="BACKGROUND-COLOR:#D3D3D3">lightgrey<option value="#FFB6C1" style="BACKGROUND-COLOR:#FFB6C1">lightpink<option value="#FFA07A" style="BACKGROUND-COLOR:#FFA07A">lightsalmon<option value="#20B2AA" style="BACKGROUND-COLOR:#20B2AA">lightseagreen<option value="#87CEFA" style="BACKGROUND-COLOR:#87CEFA">lightscyblue<option value="#778899" style="BACKGROUND-COLOR:#778899">lightslategray<option value="#B0C4DE" style="BACKGROUND-COLOR:#B0C4DE">lightsteelblue<option value="#FFFFE0" style="BACKGROUND-COLOR:#FFFFE0">lightyellow<option value="#00FF00" style="BACKGROUND-COLOR:#00FF00">lime<option value="#32CD32" style="BACKGROUND-COLOR:#32CD32">limegreen<option value="#FAF0E6" style="BACKGROUND-COLOR:#FAF0E6">linen<option value="#FF00FF" style="BACKGROUND-COLOR:#FF00FF">magenta<option value="#800000" style="BACKGROUND-COLOR:#800000">maroon<option value="#66CDAA" style="BACKGROUND-COLOR:#66CDAA">mediumaquamarine<option value="#0000CD" style="BACKGROUND-COLOR:#0000CD">mediumblue<option value="#BA55D3" style="BACKGROUND-COLOR:#BA55D3">mediumorchid<option value="#9370DB" style="BACKGROUND-COLOR:#9370DB">mediumpurple<option value="#3CB371" style="BACKGROUND-COLOR:#3CB371">mediumseagreen<option value="#7B68EE" style="BACKGROUND-COLOR:#7B68EE">mediumslateblue<option value="#00FA9A" style="BACKGROUND-COLOR:#00FA9A">mediumspringgreen<option value="#48D1CC" style="BACKGROUND-COLOR:#48D1CC">mediumturquoise<option value="#C71585" style="BACKGROUND-COLOR:#C71585">mediumvioletred<option value="#191970" style="BACKGROUND-COLOR:#191970">midnightblue<option value="#F5FFFA" style="BACKGROUND-COLOR:#F5FFFA">mintcream<option value="#FFE4E1" style="BACKGROUND-COLOR:#FFE4E1">mistyrose<option value="#FFE4B5" style="BACKGROUND-COLOR:#FFE4B5">moccasin<option value="#FFDEAD" style="BACKGROUND-COLOR:#FFDEAD">navajowhite<option value="#000080" style="BACKGROUND-COLOR:#000080">navy<option value="#FDF5E6" style="BACKGROUND-COLOR:#FDF5E6">oldlace<option value="#808000" style="BACKGROUND-COLOR:#808000">olive<option value="#6B8E23" style="BACKGROUND-COLOR:#6B8E23">olivedrab<option value="#FFA500" style="BACKGROUND-COLOR:#FFA500">orange<option value="#FF4500" style="BACKGROUND-COLOR:#FF4500">orengered<option value="#DA70D6" style="BACKGROUND-COLOR:#DA70D6">orchid<option value="#EEE8AA" style="BACKGROUND-COLOR:#EEE8AA">palegoldenrod<option value="#98FB98" style="BACKGROUND-COLOR:#98FB98">palegreen<option value="#AFEEEE" style="BACKGROUND-COLOR:#AFEEEE">paleturquose<option value="#DB7093" style="BACKGROUND-COLOR:#DB7093">palevioletred<option value="#FFEFD5" style="BACKGROUND-COLOR:#FFEFD5">papayawhop<option value="#FFDAB9" style="BACKGROUND-COLOR:#FFDAB9">peachpuff<option value="#CD853F" style="BACKGROUND-COLOR:#CD853F">peru<option value="#FFC0CB" style="BACKGROUND-COLOR:#FFC0CB">pink<option value="#DDA0DD" style="BACKGROUND-COLOR:#DDA0DD">plum<option value="#B0E0E6" style="BACKGROUND-COLOR:#B0E0E6">powderblue<option value="#800080" style="BACKGROUND-COLOR:#800080">purple<option value="#FF0000" style="BACKGROUND-COLOR:#FF0000">red<option value="#BC8F8F" style="BACKGROUND-COLOR:#BC8F8F">rosybrown<option value="#4169E1" style="BACKGROUND-COLOR:#4169E1">royalblue<option value="#8B4513" style="BACKGROUND-COLOR:#8B4513">saddlebrown<option value="#FA8072" style="BACKGROUND-COLOR:#FA8072">salmon<option value="#F4A460" style="BACKGROUND-COLOR:#F4A460">sandybrown<option value="#2E8B57" style="BACKGROUND-COLOR:#2E8B57">seagreen<option value="#FFF5EE" style="BACKGROUND-COLOR:#FFF5EE">seashell<option value="#A0522D" style="BACKGROUND-COLOR:#A0522D">sienna<option value="#C0C0C0" style="BACKGROUND-COLOR:#C0C0C0">silver<option value="#87CEEB" style="BACKGROUND-COLOR:#87CEEB">skyblue<option value="#6A5ACD" style="BACKGROUND-COLOR:#6A5ACD">slateblue<option value="#708090" style="BACKGROUND-COLOR:#708090">slategray<option value="#FFFAFA" style="BACKGROUND-COLOR:#FFFAFA">snow<option value="#00FF7F" style="BACKGROUND-COLOR:#00FF7F">springgreen<option value="#4682B4" style="BACKGROUND-COLOR:#4682B4">steelblue<option value="#D2B48C" style="BACKGROUND-COLOR:#D2B48C">tan<option value="#008080" style="BACKGROUND-COLOR:#008080">teal<option value="#D8BFD8" style="BACKGROUND-COLOR:#D8BFD8">thistle<option value="#FF6347" style="BACKGROUND-COLOR:#FF6347">tomato<option value="#40E0D0" style="BACKGROUND-COLOR:#40E0D0">turquose<option value="#EE82EE" style="BACKGROUND-COLOR:#EE82EE">violet<option value="#F5DEB3" style="BACKGROUND-COLOR:#F5DEB3">wheat<option value="#FFFFFF" style="BACKGROUND-COLOR:#FFFFFF">white<option value="#F5F5F5" style="BACKGROUND-COLOR:#F5F5F5">whitesmoke<option value="#FFFF00" style="BACKGROUND-COLOR:#FFFF00">yellow<option value="#9ACD32" style="BACKGROUND-COLOR:#9ACD32">yellowgreen
];

$time_out=600;#Time out наступает через 100 минут
  


%visible=(menu1 =>['Меню','Menu'],
          tree1 =>['Карта','Tree']); # Где отображать раздел
%link_view=( 
            empty    =>['не отображать ссылок','Not to show',], 
            child    =>['на подразделы','to subsections',], 
            similary =>['на смежные разделы','to inter-sections'], 
            parent   =>['на родительский раздел','to parent section'] 
            ); # Where to show the section
%lang_tpl=(
            'ru' => 'Русскоязычная версия',
#            'en' => 'Англоязычная версия',
          ); #Главные шаблоны для страниц сайта

}

$dbh_=dbconnect_global();

my $dbh=dbconnect();



sub get_url {
my $url=shift;
my $noproxy=shift;
    my $rnd_time_out=(1..3)[rand(3)];
    #print "rnd timeout: $rnd_time_out \n";
    sleep($rnd_time_out);
  #use LWP::UserAgent;

    my $status="";
    my $it=0;
    $ua = LWP::UserAgent->new;
    $ua->agent("Mozilla/5.0 (Windows; U; Windows NT 10.3; ru; rv:1.8.0.2) Gecko/20060308 Firefox/2.5.0.4 Beta");
    $ua->timeout('30');


    my $req = HTTP::Request->new(GET => $url);

    #print qq[new request \n];

    my $res = $ua->request($req);

    #print qq[request send ... \n];

    $status = $res->status_line;

    #print qq[status line: $status ... \n];

  # Check the outcome of the response
  if ($res->is_success) {
        #print "Успешно закачен файл! \n";
      return $res->content; #decoded_content;
  }
  else {
        #print "ОШИБКА ЗАКАЧКИ! \n";
      return $res->status_line, "\n";
  }


}


sub trim{

    return undef if( !defined($_[0]) );

    my $str = $_[0];

    if( ref( $str ) eq 'ARRAY' ){

        my @str = map{

            $_ =~ s/^\s*//s;
            $_ =~ s/\s*$//s;
            $_;

        } @$str;

        return @str;

    }elsif( ref( $str ) eq 'HASH' ){

        my %str = %$str;

        foreach my $key ( keys(%str) ){

            $str{ $key } =~ s/^\s*//s;
            $str{ $key } =~ s/\s*$//s;

        }

        return %str;

    }elsif( wantarray() ){

        my @str = map{

            $_ =~ s/^\s*//s;
            $_ =~ s/\s*$//s;
            $_;

        } @_;

        return @str;

    }elsif( defined( wantarray() ) ){

        $str =~ s/^\s*//s;
        $str =~ s/\s*$//s;

        return $str;

    }

}

sub get_structure {
my $param_ref=shift;
my $user_db={};
my $where="";
if($param_ref->{id}=~/^[A-Z0-9\-\_]+$/i){$where=" and  id='$param_ref->{id}'";}
my $sth_st=$dbh->prepare("select * from structure where domain = '$host_name' $where order by sort_id asc, name");
$sth_st->execute();
while (my $ref_st=$sth_st->fetchrow_hashref)
{
	 $user_db->{data}->{$ref_st->{id}}->{access}=$ref_st->{access};
	 $user_db->{data}->{$ref_st->{id}}->{index_ini}=$ref_st->{index_ini}||"index_document.tpl";
	 $user_db->{data}->{$ref_st->{id}}->{lang}=$ref_st->{lang};
	 $user_db->{data}->{$ref_st->{id}}->{link}=$ref_st->{link};
	 $user_db->{data}->{$ref_st->{id}}->{mod}=$ref_st->{module};
	 $user_db->{data}->{parent}->{$ref_st->{id}}=$ref_st->{parent}||'0';
	 $user_db->{data}->{sort}->{$ref_st->{id}}=$ref_st->{sort_id}||'0';
	 $user_db->{data}->{$ref_st->{id}}->{name}=$ref_st->{name};
	 $user_db->{data}->{$ref_st->{id}}->{zag}=$ref_st->{zag};
	 $user_db->{data}->{$ref_st->{id}}->{keywords}=$ref_st->{keywords};
	 $user_db->{data}->{$ref_st->{id}}->{description}=$ref_st->{description};
	 $user_db->{data}->{$ref_st->{id}}->{link_view}=$ref_st->{link_view};
	 my @vis=split /,/, $ref_st->{visible};
	 for ($i=0; $i<=$#vis; $i++){
		 my @vis1=split /=/, $vis[$i];
        	 $user_db->{data}->{$ref_st->{id}}->{visible}->{$vis1[0]}=$vis1[1];
         };
	 if($ref_st->{params}){
	 my @pr=split /,/, $ref_st->{params};
	 	for ($i=0; $i<=$#pr; $i++){
		 my @pr1=split /=/, $pr[$i];
        	 $user_db->{data}->{$ref_st->{id}}->{params}->{$pr1[0]}=$pr1[1];
         	};
     	}

 my @in_id=split /\|/, $ref_st->{include_id};
 my @in_col=split /\|/, $ref_st->{include_col};
 my @in_num=split /\|/, $ref_st->{include_num};

 for(my $pos=0;$pos<=4;$pos++){
	 $user_db->{data}->{$ref_st->{id}}->{include_id}->[$pos]=$in_id[$pos];
	 $user_db->{data}->{$ref_st->{id}}->{include_col}->[$pos]=$in_col[$pos];
 	$user_db->{data}->{$ref_st->{id}}->{include_num}->[$pos]=$in_num[$pos];
 }

};
$sth_st->finish;
$sth_st=$dbh->prepare("select * from mod_scrt");

$sth_st->execute;
while (my $ref_st=$sth_st->fetchrow_hashref)
{
	$user_db->{mods}->{$ref_st->{script}}=[$ref_st->{name},$ref_st->{name2}];
};
$sth_st->finish;

my $sth=$dbh->prepare("select * from template_info");
$sth->execute;
while (my $t_ref=$sth->fetchrow_hashref)
{
	$user_db->{template}->{assign}->{$t_ref->{t_alias}}=$t_ref->{t_value}
};
$sth->finish;

    if($param_ref->{id}){
		$param_ref->{zag_site}=$user_db->{data}->{$param_ref->{id}}->{zag};

		$param_ref->{name_zag_site}=$user_db->{data}->{$param_ref->{id}}->{name};

	  	$param_ref->{keywords_site}=qq[$user_db->{data}->{$param_ref->{id}}->{keywords}];
	    $param_ref->{keywords_site}||=$param_ref->{name_zag}||$param_ref->{zag};
		$param_ref->{description_site}=qq[$user_db->{data}->{$param_ref->{id}}->{description}];
	    $param_ref->{description_site}=$param_ref->{name_zag}||$param_ref->{zag} if ! $param_ref->{description_site};

    }
    $param_ref->{user_db}=$user_db;
    return $param_ref;  	
}

# Принимаем параметры
#______________________________________________________________________________________________________________
sub  Get_Param {
     my @params = CGI::param();
        @params = trim(@params);

     my $param_ref = {};

     foreach (@params) {

         my @temp = CGI::param($_);

         if( $#temp>1 ){

              $param_ref->{$_}=[@temp]

         }else{

              $param_ref->{$_} = CGI::param($_) || ''

         }

     }
     #Строим диспатчер в зависимости от строки запроса
     if($param_ref->{dispatch}=~/^([A-Z0-9\-\_^_p]+)\_p([0-9]+)\.html$/i){
		 $param_ref->{id}=$1;
		 $param_ref->{p_n}=$2;
		 if($param_ref->{id}!~/^[a-zA-Z0-9\_\-]+$/i){$param_ref->{id}="main"}
     }
     #Строим диспатчер в зависимости от строки запроса
     elsif($param_ref->{dispatch}=~/^([A-Z0-9\_\-]+)\.html$/i){
		 $param_ref->{id}=$1;
		 if($param_ref->{id}!~/^[a-zA-Z0-9\_\-]+$/i){$param_ref->{id}="main"}
     }
     #Строим диспатчер в зависимости от строки запроса
     elsif($param_ref->{dispatch}=~/^([A-Z0-9\_\-]+)\.html(.+?)$/i){
		 $param_ref->{id}=$1;
		 my $str=$2;
		 $str=~s/^\?//gi;
		 my @ar_p=split/\&/,$str;
		for(my $i=0;$i<=$#ar_p;$i++){
		    my($nm,$vl)=split/\=/,$ar_p[$i];
		    $param_ref->{$nm}=$vl;
		}
		 if($param_ref->{id}!~/^[a-zA-Z0-9\_\-]+$/i){$param_ref->{id}="main"}
     }
     elsif($param_ref->{dispatch}=~/^([A-Z0-9\_\-]+)\/([A-Z0-9\_\-]+)\.html$/i){
		 $param_ref->{id}=$1;
		 $param_ref->{data_id}=$2;
		 $param_ref->{id_cat}=$2;
		 $param_ref->{a}="full";
		 if($param_ref->{id}!~/^[a-zA-Z0-9\_\-]+$/i){$param_ref->{id}="main"}
     }

     my $host_name_ = $ENV{'HTTP_HOST'};
        $host_name_ =~s/^www\.//;

     my $host_name_site =$host_name_||$host_name;
        #$host_name_ = "www.".$host_name_;

	$param_ref->{l}=1 if !$param_ref->{l}; # Язык для самого конструктора
	$param_ref->{'ip'}=$ENV{'REMOTE_ADDR'}; #ip-адрес пользователя
	$param_ref->{'script_name'}=$ENV{'SCRIPT_NAME'}; # имя вызывающего Скрипт
         if($param_ref->{script_name}=~/([A-Z0-9\_]+)\.([A-Z]+)$/i){
			$param_ref->{module_name}=$1;
         }else{
			$param_ref->{module_name}="document";
         }
	$param_ref->{'path_cgi'} = $path_cgi;
	$param_ref->{'phone_number'}=$phone_number;  #телефон главный
	$param_ref->{'post_mail'}=$domain_config->{$host_name}->{'post_mail'};  #емайл для почты
	$param_ref->{'root_mail'}=$domain_config->{$host_name}->{'root_mail'};  #емайл для почты рутовый
	$param_ref->{'host_name'}=$host_name_;  #имя сайта
	$param_ref->{'host_name_now'}=$ENV{'HTTP_HOST'};  #имя сайта
	$param_ref->{'referrer'}=$ENV{'HTTP_REFERER'}; # предыдущая страница
	$param_ref->{'location'}=$ENV{'REQUEST_URI'}; # текущас строка запроса
	#Путь к каталогу пользователя
	$param_ref->{path_host}=$path_root."/base/$domain_config->{$host_name}->{'folder'}";
	#путь пользователя для цмс (все файлы в папке base, выше залезть нельзя)
	$param_ref->{user_doman}=$host_name."/base/$domain_config->{$host_name}->{'folder'}";
	$param_ref->{db_prefix}="$domain_config->{$host_name}->{'folder'}";
	#Истинный урл пользователя
	$param_ref->{user_url}=$host_name;
	#Путь к базе данных пользователя
	$param_ref->{path_root}=$path_root;

	$param_ref->{path_db}=$path_root."/db/$domain_config->{$host_name}->{'folder'}/user_db";
	$param_ref->{path_db1}=$path_root."/db";
 	$param_ref->{path_template}=$path_root."/templates/$domain_config->{$host_name}->{'folder'}";
 	$param_ref->{path_to_db}=$path_root."/db/$domain_config->{$host_name}->{'folder'}";
 	$param_ref->{path_template_img}=$path_root."/images";
 	$param_ref->{user}->{id}=7;
 	$param_ref->{dbh}=dbconnect();
 	$param_ref->{prefix}=""; #Префикс для таблиц
 
 my $size_use=10240;
 $size_use = sprintf "%.1f", $size_use;
 $param_ref->{user}->{size}=1000;
 $param_ref->{size_use}=$size_use;
 my $free_size=($param_ref->{user}->{size}*1024)-$size_use;
 if($free_size>0){$param_ref->{save}='ok';}else{$param_ref->{save}="not";}

 $param_ref->{"time"}=time; #время


#my $col=$dbh->selectrow_array("select count(*) from structure");
if(!table_exists(qq[`structure`])){

 my $sql = qq[
CREATE TABLE `structure` (
`id_n` INT NOT NULL AUTO_INCREMENT ,
`id` VARCHAR( 25 ) NOT NULL ,
`parent` VARCHAR( 25 ) NOT NULL ,
`name` VARCHAR( 250 ) NOT NULL ,
`zag` VARCHAR( 250 ) ,
`keywords` VARCHAR( 250 ),
`description` VARCHAR( 250 ),
`access`  VARCHAR( 250 ) NOT NULL,
`index_ini` VARCHAR( 250 ) NOT NULL ,
`lang` varchar(2)  NOT NULL ,
`link` varchar(255)  NOT NULL ,
`module` varchar(255)  NOT NULL ,
`sort_id` INT(5)  NOT NULL ,
`link_view` varchar(255)  NOT NULL ,
`include_id` varchar(255)  NOT NULL ,
`include_col` varchar(255)  NOT NULL ,
`include_num` varchar(255)  NOT NULL , 
`visible` varchar(255)  NOT NULL ,
`domain` varchar(255)  NOT NULL ,
`params` text default '',
 PRIMARY KEY ( `id_n` ),
 UNIQUE KEY `id_domain` (`id`,`domain`)
) 
 ]; 
 my $create=$dbh->do($sql);
};

=m
#__________________________________________________________________________
# Раскоментировать блок если нужно восстан структуру из стар user_db
#   при переходе на лайт вершон
#__________________________________________________________________________
 if (-e "$param_ref->{path_db}"){
#print "$param_ref->{path_db}";
  use Storable;
  my $user_db_old= retrieve $param_ref->{path_db};
  #my @ar_id=();
  if ($user_db_old->{data}){
# my $dbh1=dbconnect;
 #print $user_db_old->{data};
   my $ar_id_href=$user_db_old->{data}||{};
   my @ar_id=keys %$ar_id_href;
   for (my $i=0;$i<=$#ar_id;$i++){
     my $sql='';
     my $ex=$dbh->selectrow_array("select count(*) from structure where id='$ar_id[$i]'");
     if ($ex<=0) {
	 $sql=qq[insert into structure (id) values ('$ar_id[$i]')];
	my $sth=$dbh->prepare($sql);
	 $sth->execute;
	 $sth->finish;
       &store_db($user_db_old,$ar_id[$i]);
    }
   }
   #dbdisconnect($dbh1);
   }	
 }
=cut


#create captcha_img
if(!table_exists(qq[`template_info`])){
my $sql=qq[
CREATE TABLE `captcha_img` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `file_name` char(32) COLLATE cp1251_bin NOT NULL,
  `kod` char(4) COLLATE cp1251_bin NOT NULL,
   `ip` char(15) COLLATE cp1251_bin NOT NULL,
  `time_reg` bigint(20) NOT NULL DEFAULT '0',
PRIMARY KEY (`id`),
KEY `file_name_to_ip` (`file_name`,`ip`)
) ENGINE=MyISAM  DEFAULT CHARSET=cp1251 COLLATE=cp1251_bin COMMENT='captcha for forms' AUTO_INCREMENT=1 ;
];      
 my $create=$dbh->do($sql);
}


if(!table_exists(qq[`template_info`])){

 my $sql = qq[
CREATE TABLE `template_info` (
`id_n` INT NOT NULL AUTO_INCREMENT ,
`t_alias` VARCHAR( 50 ) NOT NULL ,
`t_value` TEXT,
`t_value_eng` TEXT,
 PRIMARY KEY ( `id_n` )
) 
 ]; 
 my $create=$dbh->do($sql);
};

if(!table_exists(qq[`mod_scrt`])){
 my $sql = qq[
CREATE TABLE `mod_scrt` (
`id` INT NOT NULL AUTO_INCREMENT ,
`script` VARCHAR( 25 ) NOT NULL ,
`name` VARCHAR( 100 ) NOT NULL ,
`name2` VARCHAR( 100 ) NOT NULL ,
`opis` VARCHAR( 250 ) ,
`opis2` VARCHAR( 250 ),
`status` VARCHAR( 25 ),
 PRIMARY KEY ( `id` ),
 UNIQUE KEY `id` (`id`)
) 
 ]; 
 my $create=$dbh->do($sql);
};

#считываем структуру end
 #считываем куки
  use CGI::Cookie;
  my $cook=fetch CGI::Cookie();
     $param_ref->{cook}=$cook;
#считываем куки end
#Забираем админовские даные
   $admin_ref={};
   if(ref($param_ref->{cook}->{admin_groups}) eq 'CGI::Cookie'){
   $dbh=dbconnect();
   my $sel="select * from admin_groups where login=? and pass=md5(?)";
   my $sth=$dbh->prepare($sel);
      $sth->execute($param_ref->{cook}->{admin_groups}->{value}->[0],$param_ref->{cook}->{admin_groups}->{value}->[1]);
      $admin_ref=$sth->fetchrow_hashref();
      $sth->finish;
   
	#Забираем админовские даные end
	 $param_ref->{admin_ref}=$admin_ref;
   }
    #if($param_ref->{id}){
       $param_ref=get_structure($param_ref);
    #}
 return $param_ref; # Возвращаем ссылку на хеш параметров
}
# Принимаем параметры конец
sub sel_mag
{
	my ($option_mag,$all_mag);
	$option_mag = qq[<option value=''>Выбрать...</option>];
	my $sel = qq[select `id`,`number` from `magazine`];
	my $sth = $dbh->prepare($sel);
	$sth->execute();
	while (my $ref_m = $sth->fetchrow_hashref)
	{
		$option_mag .= qq[<option value='$ref_m->{id}'>$ref_m->{number}</option>];
	}
	$sth->finish;
	
	
	return ($option_mag,$all_mag);
}
#______________________________________________________________________________________________________________
# Сохраняем user_db
#______________________________________________________________________________________________________________
sub store_db {
  my $user_db=shift;
  my $id=shift;
  my $kind=shift;

if (!$kind) {
  #my $exists=$dbh->selectrow_array(qq[select count(*) from structure where id='$id']);
  #if ($exists<=0) {$dbh->do(qq[insert into structure (id) values('$id')]);}

  #Внести квотирование кавычек = \'   : $user_db->{data}->{$id}->{access}=~s/\'/\\\'/gi;
  
  my $access=qq[access='$user_db->{data}->{$id}->{access}'];
  my $index_ini=qq[index_ini='$user_db->{data}->{$id}->{index_ini}'];
  my $lang=qq[lang='$user_db->{data}->{$id}->{lang}'];
  my $link=qq[link='$user_db->{data}->{$id}->{link}'];
  my $mod=qq[module='$user_db->{data}->{$id}->{mod}'];
  my $parent=qq[parent='$user_db->{data}->{parent}->{$id}'];
  my $sort_id=qq[sort_id='$user_db->{data}->{sort}->{$id}'];
  my $name=qq[name='$user_db->{data}->{$id}->{name}'];
  my $zag=qq[zag='$user_db->{data}->{$id}->{zag}'];
  my $keywords=qq[keywords='$user_db->{data}->{$id}->{keywords}'];
  my $description=qq[description='$user_db->{data}->{$id}->{description}'];
  my $link_view=qq[link_view='$user_db->{data}->{$id}->{link_view}'];

      my $vis=$user_db->{data}->{$id}->{visible};
      my %vis=%$vis;
      my @vis_names=keys %vis;
    my $visible=qq[visible='];
      for (my $i=0;$i<=$#vis_names;$i++){$visible.=qq[$vis_names[$i]=$vis{$vis_names[$i]},];}
     if (chop $visible eq "'") {$visible.=qq[''];}else{$visible.="'";};

      my $par=$user_db->{data}->{$id}->{params};
      my %par=%$par;
      my @par_names=keys %par;
	  my $params=qq[params='];
      for (my $i=0;$i<=$#par_names;$i++){$params.=qq[$par_names[$i]=$par{$par_names[$i]},];}
      if (chop $params eq "'") {$params.=qq[''];}else{$params.="'";};

 my $in__id=$user_db->{data}->{$id}->{include_id};
 my @in__id=@$in__id;
 my $in_id="include_id='".join ('|',@in__id)."'";
 my $in__col=$user_db->{data}->{$id}->{include_col};
 my @in__col=@$in__col;
 my $in_col="include_col='".join ('|',@in_col)."'";
 my $in__num=$user_db->{data}->{$id}->{include_num};
 my @in__num=@$in__num;
 my $in_num="include_num='".join ('|',@in__num)."'";

 my $sql=qq[update structure set $access, $index_ini, $lang, $link, $mod, 
	$parent, $sort_id, $name, $zag, $keywords, $description, $link_view, 
	$visible, $params, $in_id, $in_col, $in_num where id='$id'];
 my $sth=$dbh->prepare($sql);
 $sth->execute;
 $sth->finish;

}elsif ($kind eq 'params') {

      my $par=$user_db->{data}->{$id}->{params};
      my %par=%$par;
      my @par_names=keys %par;
    my $params='';
      for (my $i=0;$i<=$#par_names;$i++){$params.=qq[$par_names[$i]=$par{$par_names[$i]},];}
      chop $params;
    $params=qq[params='$params'];
  my $sql=qq[update structure set $params where id='$id'];
  my $sth=$dbh->prepare($sql);
 $sth->execute;
 $sth->finish;

}elsif ($kind eq 'visible') {

      my $vis=$user_db->{data}->{$id}->{visible};
      my %vis=%$vis;
      my @vis_names=keys %vis;
    my $visible='';
      for (my $i=0;$i<=$#vis_names;$i++){$visible.=qq[$vis_names[$i]=$vis{$vis_names[$i]},];}
      chop $visible;
     $visible=qq[visible='$visible'];
  my $sql=qq[update structure set $visible where id='$id'];
  my $sth=$dbh->prepare($sql);
 $sth->execute;
 $sth->finish;

}elsif ($kind eq 'include') {

 my $in__id=$user_db->{data}->{$id}->{include_id};
 my @in__id=@$in__id;
 my $in_id="include_id='".join ('|',@in__id)."'";
 my $in__col=$user_db->{data}->{$id}->{include_col};
 my @in__col=@$in__col;
 my $in_col="include_col='".join ('|',@in_col)."'";
 my $in__num=$user_db->{data}->{$id}->{include_num};
 my @in__num=@$in__num;
 my $in_num="include_num='".join ('|',@in__num)."'";
 my $sql=qq[update structure set $in_id, $in_col, $in_num where id='$id'];
 my $sth=$dbh->prepare($sql);
 $sth->execute;
 $sth->finish;
}
elsif ($kind eq 'template') {

   open A, "$path_root/template_site/assign.ini";
   print qq[$path_root/template_site/assign.ini];
   my @lines=<A>;
   close A;
   my @ar_opis=();
   my @ar_type=();
   my @ar_name_alias=();
   my $j=0;

   my $del=$dbh->do("TRUNCATE TABLE `template_info`");

   for(@lines){
    $lines[$j]=~s/\n|\r//gi;
        chomp($lines[$j]);
    my ($alias,$value,$opis,$value_eng,$opis_eng,$type)=split /\=/,$lines[$j];

	$sql=qq[insert into template_info (t_alias,t_value) values (?,?)];

	my $sth=$dbh->prepare($sql);
	$sth->execute($alias,$user_db->{template}->{assign}->{$alias});
	$sth->finish;

     $j++;
   }

}
 
};
# Сохраняем user_db конец
#______________________________________________________________________________________________________________
# Резервное копирование базы структуры
#______________________________________________________________________________________________________________
sub backup_db{
  my $struc=$mb->create_structure();
  my $data= $mb->data_backup();
  my $res=$struc."\n".$data;
  return $res;
}
#______________________________________________________________________________________________________________
# Проверка существования таблицы в базе
# return 0 == table not exists
# 	 1 == table exists
#______________________________________________________________________________________________________________
sub table_exists{
  my $tbl_name=shift||'';
  my $err=0;
  if ($tbl_name ne ''){
     my @tables = map { $_ =~ s/.*\.//; $_ } $dbh->tables();
     my %tables_href = map { $_ => $_ }  @tables;

     $err=1 if $tables_href{$tbl_name};
        #print join(/,/,keys %tables)."<br>",join(/,/,values %tables),"$tbl_name=".$err;
	#print '<br>%tables='.$tables{$tbl_name};exit;
    
  }
 return $err;
}
#______________________________________________________________________________________________________________
#Фильтр входных данных для форм
#______________________________________________________________________________________________________________
sub data_filter{
use locale;
  my $data=shift||'';
  my $type=shift||'';
  my $err=0;
   #черный список - убирать все, что не разрешено
    $data=~s/\%|\*|\&|\?|\||\"//gi; #Удаляем опасные символы
#    $data=~=~s/[\|\-&\.\\\/\0]//gi;
    $data=~s/(<\w+?.*?>)+.*?(<\/\w+?.*?>)+//gi; #tags
    $data=~s/^\s+//gi;   #Удаляем 
    $data=~s/\s+/ /gi;      # лишние
    $data=~s/\s+$//gi;          # пробелы
 #Белые списки - оставлять только то, что разрешено 
 if($type eq 'name'){
  $err=1 if $data!~/^[A-Za-zА-Яа-я0-9_\-\s]+$/gi;
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
#______________________________________________________________________________________________________________
# Коннект с базой
#______________________________________________________________________________________________________________
sub dbconnect_global{
#  use Apache::DBI;
  #use lib "/opt/local/lib/perl5";
  use DBI;
  my $user=$db_user;
  my $pass=$db_pass;
  my $host=$db_host;
  my $dbname=$db_name;
  my $flag=0;
  my $dbh = DBI->connect("DBI:mysql:$dbname:$host",$user,$pass,{ PrintError =>0,RaiseError=>0}) or $flag=1;   # || die "Can't connect: $DBI::errstr\n"; #
    $dbh->do("set names cp1251");
  if($flag){
   print qq[
<html>
<head>
<title>Can't connect to database</title>
</head>
<body>
<center>
Sorry, can't connect to database. Server is busy<br><br>
<a href="http://$host_name">$host_name</a>
</center>
</body>
</html>
]; #'
   exit;
  }
  return $dbh;
 }
# конец Коннект с базой
#______________________________________________________________________________________________________________
#______________________________________________________________________________________________________________
# Дисконнект с базой
sub dbdisconnect_global{
  my $dbh=shift;
  $dbh->disconnect if $dbh;
  return 1;
}

# Коннект с базой
#______________________________________________________________________________________________________________
sub dbconnect{
  return $dbh_;
}
# конец Коннект с базой
#______________________________________________________________________________________________________________
#______________________________________________________________________________________________________________
# Дисконнект с базой
sub dbdisconnect{
  return 1;
  my $dbh=shift;
}

# Конец Дисконнект с базой
#______________________________________________________________________________________________________________
# отправка почты
#______________________________________________________________________________________________________________
sub send_mail_() { 
 my $email=shift; my $subject=shift; my $text=shift;  #use Mail::Sendmail;
 my $from=shift;
 my $name_project=shift;
 $from=$post_mail if !$from;
 $name_project=$project if !$name_project;
 my %mail = ( From         => "$name_project<$from>",
           Subject        => "$subject",
           Organization   => '',
           'Content-type'  => 'text/plain; charset=koi8-r',
           'Content-Transfer-Encoding' => '8bit',
           To             => "$email",
           Message        => "$text",
#                  SMTP                   =>'192.168.1.80'
         );
        sendmail(%mail) or warn $Mail::Sendmail::error;
}
# отправка почты конец
#______________________________________________________________________________________________________________

# отправка почты /usr/sbin/sendmail простой вариант
#______________________________________________________________________________________________________________
sub send_mail() { 
my $email=shift; my $subject=shift; my $text=shift;
my $from=shift;
my $name_project=shift;
my $how=shift || 'text';
$from=$post_mail if !$from;
$name_project=$project if !$name_project;
my $mail_prog = '/usr/sbin/sendmail';

my $content_type="Content-Type: text/plain; charset=\"Windows-1251\"\n";
my $content_transfer="Content-Transfer-Encoding: 8bit\n";

if($how eq 'html'){
    $content_type="Content-Type: text/html; charset=\"Windows-1251\"\n";
    $content_transfer="Content-Transfer-Encoding: 8bit\n";
    $text=qq[<html><head><title>$subject</title></head><body>$text</body></html>];
}

open MAIL, "|$mail_prog $email" || die $!;
print MAIL "To: $email\n";
print MAIL "From: $name_project <$from>\n";
print MAIL "Subject: $subject\n";
print MAIL "MIME-Version: 1.0\n";
print MAIL $content_type;
print MAIL $content_transfer;
print MAIL  $text;
close MAIL;
#print qq[ok $email];exit;
1;
}
sub send_mail_old {
   my ($mail,$subject,$text,$path_root_attach)=@_;
   my @ar_f=split /\//,$path_root_attach;
   my $file=$ar_f[$#ar_r];
#   use lib "/home/fesserr3/mylib/MIME-Lite";
#   use MIME::Lite;
### Create a new multipart message:
$msg = MIME::Lite->new(
       From    =>"$project<$post_mail>",
       To      =>$mail,
       Subject =>$subject,
       Type    =>'TEXT',
       Data    =>$text
       );
if($path_root_attach){
### Attach a part:
$msg->attach(Type     =>'AUTO',
             Path     =>$path_root_attach,
             Filename =>$file
             );
}
MIME::Lite->send("sendmail", "/usr/sbin/sendmail -t -oi -oem");
$msg->send;
return 1;
}



sub get_data_from_sid { #Получаем все данные о пользователе по sid
 return undef;
 my $sid=shift;
 my $idu=$dbh->selectrow_array("select idu from session where sid=?",undef,($sid));
 my $sel="select * from users where id='$idu'";
 my $sth=$dbh->prepare($sel);
        $sth->execute();
 my $ref_users_data=$sth->fetchrow_hashref; #Ссылка на все значения всех полей таблицы users
        $sth->finish;    
 
    if($ref_users_data){return $ref_users_data}else{return 0;}
}

sub get_data_from_cook { #Проверяем доступ пользователя по куку
 my $ref=shift;
 my $idu=$dbh->selectrow_array("select id from users where login=? and pass=?",undef,($ref->{cook}->{mod_user_cook}->{value}->[0],$ref->{cook}->{mod_user_cook}->{value}->[1]));
 if(!$idu){return 0;}
 my $sel="select * from users where id='$idu'";
 my $sth=$dbh->prepare($sel);
        $sth->execute();
 my $ref_users_data=$sth->fetchrow_hashref; #Ссылка на все значения всех полей таблицы users
        $sth->finish;    
 
    if($ref_users_data){
        return $ref_users_data}else{return 0;}
}

sub get_data_from_idu {
 return undef;
 my $idu=shift;
 my $sel="select * from users where id='$idu'";
 my $sth=$dbh->prepare($sel);
        $sth->execute();
 my $ref_users_data=$sth->fetchrow_hashref||''; #Ссылка на все значения всех полей таблицы users
        $sth->finish;
 
    if($ref_users_data){ return $ref_users_data}else{return 0;}
}


sub check_auth {#Это новый вариант авторизации для многопользовательской CMS
   my $ref=shift;
   #если нет кука - сразу выдаем ошибку
   if(ref($ref->{cook}->{admin_groups}) ne 'CGI::Cookie'){return 1;}
   my $sel="select * from admin_groups where login=? and pass=md5(?) and status=1";
   my $sth=$dbh->prepare($sel);
      $sth->execute($ref->{cook}->{admin_groups}->{value}->[0],$ref->{cook}->{admin_groups}->{value}->[1]);
   my $admin_ref=$sth->fetchrow_hashref();
      $sth->finish;
   #если авториация не проходит - выдаем 1, иначе выдаем пустоту
   if(!$admin_ref->{id}){return 1}else{return undef;}
}

sub check_status { #Проверка статуса пользователя, если неактивный - 
                   #выкидываем на страницу отказа дальнейших действий. 
                   #(Поставил проверку в проверку авторизации) 
                   #Здесь выкидываем при неправильном доступе к спец разделам
 my $ref=shift;
 my $mess="error";
 my $flag=1;
 if(!$ref->{admin_ref}->{grant}&&$ref->{who} eq 'grant'){$mess="grant_error";$flag=0}
 if(!$ref->{admin_ref}->{add_razdel}&&$ref->{who} eq 'add_razdel'){$mess="add_razdel_error";$flag=0}
 if(!$ref->{admin_ref}->{edit_design}&&$ref->{who} eq 'edit_design'){$mess="edit_design_error";$flag=0;}
 if(!$flag){
  print qq[
   <html>
   <head><title>Доступ закрыт</title></head>
   <body>
    <script>location.href="/cgi-bin/mod/manager.cgi?a=message&mess=$mess"</script>
   </body>
   </html>
  ];
 }
}

sub check_access {#проверяем доступ к разделу, рекрсивно ищем самый высший раздел, 
                  #где проставлены права пользователя. Т.е. назначив главный раздел - 
                  #автоматом доступ к подразделам
 my $ref=shift;
 my $flag=0;
 if($ref->{admin_ref}->{login} eq 'admin'){$flag=1}else{
 my $id_sub_menu=$ref->{id};
 if($ref->{idr}){
 my $mod=$ref->{user_db}->{data}->{$ref->{idr}}->{mod};
 $id_sub_menu=$ref->{idr} if  $mod eq 'news' || $mod eq 'article';
 }
 if($id_sub_menu){
  #Проходим вверх для обнаружения у родителей прав доступа авторизованного пользователя
#  my $p_parent=$ref->{user_db}->{data}->{parent}->{$id_sub_menu}; #выбираем предпоследний id
  my $col=100; #максимум 100 проходов (чтобы не было бесконечного цикла)
  while($id_sub_menu ne '0' && $id_sub_menu ne '')
  {
    if($ref->{user_db}->{data}->{$id_sub_menu}->{access} eq $ref->{admin_ref}->{login}){$flag=1;last;}
    $id_sub_menu=$ref->{user_db}->{data}->{parent}->{$id_sub_menu}; 
    $col++;
    last if $col==100; #выходим если цилк слишком большой (надеюсь циклить не буит :-))
  }
 }
 }
 if(!$flag){
  print qq[
   <html>
   <head><title>Доступ к данному разделу закрыт</title></head>
   <body>
    <script>location.href="/cgi-bin/mod/manager.cgi?a=message&mess=error"</script>
   </body>
   </html>
  ];
 
 }
}

sub tplb {
 my $ref=shift;
 my $def=$ref->{def};
 my $tpl = new CGI::FastTemplate();
 $tpl->set_root($template_root);
# $tpl->set_root("../virtual/template");
 $tpl->no_strict();
 $tpl->define(%$def);
 $tpl=user_menu($ref,$tpl);
 $tpl->assign(
              LANG => $ref->{l},
              TITLE => $ref->{title},
              SID => $ref->{sid}
             );
 return $tpl;
}
sub user_menu {
 my $ref=shift;
 my $tpl=shift;
if(1==1){
 $tpl->define(user_menu=>"/user_menu.html.$ref->{l}");
 my $size_use_kbyte=$ref->{size_use}/1024;
# my $all_size=$ref->{user}->{size}*1024;
 my $all_size=$ref->{user}->{size};
    $size_use_kbyte = sprintf "%.1f", $size_use_kbyte;
 my $size_persent_use=0;
 if($all_size){
  $size_persent_use=($size_use_kbyte/$all_size)*100;
}
    $size_persent_use = sprintf "%.0f", $size_persent_use;
    my $name_u=$ref->{admin_ref}->{name};
    if(length($name_u)>25){$name_u=substr $name_u,0,25; $name_u="$name_u...";}
 my ($year,$mon,$mday,$hour,$min,$sec)=get_data($ref->{user}->{time_end});
 my $time_end="$mday-$mon-$year $hour:$min";
    $time_end="$year-$mon-$mday $hour:$min" if ($ref->{l} eq '2');
    if (!$ref->{user}->{time_end}){$time_end="N/A"}
    my $plan="Alphaweb.ru";
    if($ref->{user}->{size}==160){$plan="Lite";}
    my $limit=$ref->{user}->{size}*1024;
    if($ref->{free_all_size} && $ref->{free_all_size}<$limit){ #Если места на сервере мало - выкидываем на  страницу с уведомлением
     print qq[
<html>
<head>
 <title>Недостаточно места</title>
</head>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css">
<body>
<br><br><center><b>Обратитетсь в службу поддержки хостинга</b>
<br><br>
<script>parent.location.href="/cgi-bin/view.pl?mess=disc_full"</script>
<a href="http://www.alphaweb.ru" target=_blank>AlhaWeb CMS</a>
</center>
</body>
</html>
     ];
    }
 $tpl->assign(
              LANG => $ref->{l},
              SID => $ref->{sid},
              NAME_U => $name_u,
              LOGIN => $ref->{user}->{login},
              HOST_NAME => $host_name,
              SIZE=>$all_size,
              USE_SIZE=>$size_use_kbyte,
              BYTE_PERSENT_USE=>$size_persent_use,
              TIME_END=>$time_end,
              PLAN=>$plan
             );
 }else{
 $tpl->define(user_menu=>"/login.html.$ref->{l}");
 $tpl->assign(
              LANG => $ref->{l},
              HOST_NAME => $sel_host
                );
 }
 $tpl->parse(USER_MENU=>"user_menu");
 $tpl->clear_href(1);
return $tpl;
}


sub get_idu { #Получаем id пользователя по логину и паролю
 return 1;
 my $ref=shift;
 my $idu=undef;
 if ($ref->{login}&&$ref->{pass}&&$ref->{sel_host}){
        $idu=$dbh->selectrow_array("select id from users where login=? and pass=? and status=1 and domen=?",undef,($ref->{login},$ref->{pass},$ref->{sel_host}));
    if ($idu){return $idu}else{return undef}
 
 }else{ return undef}
}
sub get_sid { #получаем sid пользователя по idu /создаем новую сессию
 return 1;
 my $idu=shift;
 my $ref=shift;
 my $time_now=time;
 my $res_time=$time_now-$time_out;
 my $del=$dbh->do("delete from session where time<$res_time");
 my $del_session=$dbh->do("delete from session where idu=?",undef,($ref->{idu}));#Удаляем сессии пользователя с таким же id
    A:
    my @chars = ( "A" .. "Z", "a" .. "z", 0 .. 9);
    my $sid = join("", @chars[ map { rand @chars } ( 1 .. 32 ) ]);
    my $ins=$dbh->do("insert into session (sid,idu,time,ip) values (?,?,?,?)",undef,($sid,$idu,time,$ref->{ip}));
    if ($ins==0){goto A;}
     else{return $sid; }
 
 
}

sub get_data {#Возвращает массив текущей даты 
 my $time=shift||time;
 my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=localtime($time);
 $mon++;
# print qq[($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)];
 $year+=1900;
#if ($mon<10){$mon=qq[0$mon]};
#if ($mday<10){$mon=qq[0$mday]};
 return ($year,$mon,$mday,$hour,$min,$sec);
}

#################Печать страничек снизу начало
sub page_down {
 my ($host_name,$kol,$PageIn,$p_n,$CountPage)=@_;
 $CountPage=$CountPage||25;
 my ($mnprt,$PageInn,$konn,$str_kn,$first_s,$first_sk,$str_k,$PageIne,$kone,$str);
 $PageIn=int($p_n/$CountPage)+1;
 if ($kol>=1){
 #--------странички внизу (начало)
 if($PageIn>1){
  $PageInn=$PageIn-1;
  $konn=$PageInn*$CountPage-1;
  $str_kn=$konn+1;
  my $link="$host_name&p_n=$konn";
  if($host_name=~/\.html$/){
  	  my $host_name2=$host_name;
	  $host_name2=~s/\_p([0-9]+)\.html$//gi;
	  $host_name2=~s/\.html$//gi;
	  $link=$host_name2."_p$konn.html";
  }
  $mnprt.= qq[ <a href="$link">&lt;&lt; 1..$str_kn</a>&nbsp;&nbsp;];
 }
 $first_s=($PageIn-1)*$CountPage;
 $first_sk=$first_s+$CountPage-1;
 if ($first_sk>=$kol){
 	$first_sk=$kol-1;
 }

 for (my $i=$first_s;$i<=$first_sk&&$first_sk>=1;$i++){
 $str=$i+1;
  if ($i==$p_n){
  	$mnprt.= qq[<b>[$str]</b> ];
  }else{
	 my $link="$host_name&p_n=$i";
	 if($host_name=~/\.html$/){
	 	my $host_name2=$host_name;
		$host_name2=~s/\_p([0-9]+)\.html$//gi;
		$host_name2=~s/\.html$//gi;
	  	$link=$host_name2."_p$i.html";
	  }
  	$mnprt.= qq[<a href="$link">$str</a> ];
  }
 }
 $PageIne=$PageIn+1;
 $kone=$PageIn*$CountPage;
 $str_k=$kone+1;
  if ($kol>$CountPage && $str_k<$kol){
  	  my $link="$host_name&p_n=$kone";
	  if($host_name=~/\.html$/){
  		  my $host_name2=$host_name;
		  $host_name2=~s/\_p([0-9]+)\.html$//gi;
		  $host_name2=~s/\.html$//gi;
		  $link=$host_name2."_p$kone.html";
	  }
  	$mnprt.= qq[ &nbsp;&nbsp;<a href="$link">$str_k..$kol &gt;&gt;</a>];
  }
 }
return $mnprt;
}
 #--------странички внизу (конец)

#################Печать страничек снизу конец

sub encoder {
my $enstring=shift; my $cfrom=shift; my $cto=shift;
my %codefunk=(
win=>"\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF\xF0\xF1\xF2\xF3\xF4\xF5\xF6\xF7\xF8\xF9\xFA\xFB\xFC\xFD\xFE\xFF",
koi=>"\xE1\xE2\xF7\xE7\xE4\xE5\xF6\xFA\xE9\xEA\xEB\xEC\xED\xEE\xEF\xF0\xF2\xF3\xF4\xF5\xE6\xE8\xE3\xFE\xFB\xFD\xFF\xF9\xF8\xFC\xE0\xF1\xC1\xC2\xD7\xC7\xC4\xC5\xD6\xDA\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD2\xD3\xD4\xD5\xC6\xC8\xC3\xDE\xDB\xDD\xDF\xD9\xD8\xDC\xC0\xD1",
iso=>"\xB0\xB1\xB2\xB3\xB4\xB5\xB6\xB7\xB8\xB9\xBA\xBB\xBC\xBD\xBE\xBF\xC0\xC1\xC2\xC3\xC4\xC5\xC6\xC7\xC8\xC9\xCA\xCB\xCC\xCD\xCE\xCF\xD0\xD1\xD2\xD3\xD4\xD5\xD6\xD7\xD8\xD9\xDA\xDB\xDC\xDD\xDE\xDF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF",
dos=>"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8A\x8B\x8C\x8D\x8E\x8F\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9A\x9B\x9C\x9D\x9E\x9F\xA0\xA1\xA2\xA3\xA4\xA5\xA6\xA7\xA8\xA9\xAA\xAB\xAC\xAD\xAE\xAF\xE0\xE1\xE2\xE3\xE4\xE5\xE6\xE7\xE8\xE9\xEA\xEB\xEC\xED\xEE\xEF",

koi_lc=>"tr/\xB3\xE0-\xFF/\xA3\xC0-\xDF/", koi_uc=>"tr/\xA3\xC0-\xDF/\xB3\xE0-\xFF/",
win_lc=>"tr/\xA8\xC0-\xDF/\xB8\xE0-\xFF/", win_uc=>"tr/\xB8\xE0-\xFF/\xA8\xC0-\xDF/",
alt_lc=>"tr/\xF0\x80-\x9F/\xF1\xA0-\xAF\xE0-\xEF/", alt_uc=>"tr/\xF1\xA0-\xAF\xE0-\xEF/\xF0\x80-\x9F/",
iso_lc=>"tr/\xA1\xB0-\xCF/\xF1\xD0-\xEF/", iso_uc=>"tr/\xF1\xD0-\xEF/\xA1\xB0-\xCF/",
dos_lc=>"tr/\x80-\x9F/\xA0-\xAF\xE0-\xEF/", dos_uc=>"tr/\xA0-\xAF\xE0-\xEF/\x80-\x9F/",
mac_lc=>"tr/\xDD\x80-\xDF/\xDE\xE0-\xFE\xDF/", mac_uc=>"tr/\xDE\xE0-\xFE\xDF/\xDD\x80-\xDF/"
);

if (!$enstring or !$cfrom or !$cto) {return 0}
else {
    if ($cfrom ne "" and $cto ne "lc" and $cto ne "uc") {
       $_=$enstring;$cfrom=$codefunk{$cfrom};$cto=$codefunk{$cto};
       eval "tr/$cfrom/$cto/"; return $_;
    }
    elsif (($cfrom ne "") and ($cto eq "lc" or $cto eq "uc")) {
       $_=$enstring; $cfrom=$codefunk{"$cfrom\_$cto"};
       eval $cfrom; return $_;
    }
}
return $enstring;
}

sub magick { #уменьшение картинки
#use Image::Magick;
my $size=shift;
my $path_root_i=shift;
my $path_root_new=shift;

my $d=Image::Magick->new;
$d->ReadImage("$path_root_i");

my $width  = $d->Get('columns');
my $height = $d->Get('rows');
my ($width_new,$height_new);
my $new=$d->Clone();
if($width>$height){ 				# если ширина больше высоты 

    my $prop   = ($size/$width);
    $width_new  = int($width*$prop);
    $height_new = int($height*$prop);
    if($height_new>$size){ 			#  Если все же высота не умещается в указанный размер size уменьшаем ещё польше
	my $prop = ($size/$height_new);
	$width_new = int($width_new*$prop);
	$height_new = int($height_new*$prop);
    }
}else{						# Если у нас высота больше ширины
    my $prop   = ($size/$height);
    $width_new  = int($width*$prop);
    $height_new = int($height*$prop);
    if($width_new>$size){ 			#  Если все же высота не умещается в указанный размер size уменьшаем ещё польше
	my $prop = ($size/$width_new);
	$width_new = int($width_new*$prop);
	$height_new = int($height_new*$prop);
    }
}
    $new->Resize(width=>$width_new, height=>$height_new);

#my $prop   = ($height/$width);
#if($width>$height){$prop   = ($width/$height);}
#my $h_new  = int($width_n*$prop);
#if($width<$height)
#    {$new->Resize(height=>$h_new, width=>$width_n);}
#else{$new->Resize(width=>$width_n, height=>$h_new);}
#if($width>$height){$prop   = ($width/$height);}
#my $h_new  = int($width_n*$prop);
#if($width<$height)
#    {$new->Resize(height=>$h_new, width=>$width_n);}
#else{$new->Resize(width=>$width_n, height=>$h_new);}
$new->Comment("$host_name");

$new->Write("$path_root_new");
}

sub magick_width_only { #уменьшение картинки
#use Image::Magick;
my $size=shift;
my $path_root_i=shift;
my $path_root_new=shift;

my $d=Image::Magick->new;
$d->ReadImage("$path_root_i");

my $width  = $d->Get('columns');
my $height = $d->Get('rows');
my $new=$d->Clone();
    $size = $width if $width < $size;
    my $prop   = ($size/$width);
    my $h_new  = int($height*$prop);
    $new->Resize(width=>$size, height=>$h_new);

$new->Comment("$host_name");

$new->Write("$path_root_new");
}

sub resize_img { # не помню уже чем отличается эта функция отпредыдущей
my $width_n=shift;
my $path_root_i=shift;
my $path_root_new=$path_root;
   $path_root_new=~s/\.(.+?)$//i;
   my $ext=$1;
   $path_root_new.="-".time.".$ext";
my $d=Image::Magick->new;
$d->ReadImage("$path_root_i");

my $width  = $d->Get('columns');
my $height = $d->Get('rows');
my $prop   = ($width_n/$width);
#my $prop   = ($height/$width);
my $new=$d->Clone();

my $h_new  = int($height*$prop);
$new->Resize(width=>$width_n, height=>$h_new);
$new->Comment("$host_name");
#$new->Annotate(
#                  fill  => 'Black',
#                  font      => 'Times-Roman',
#                  pointsize => '10',
#                  gravity   => 'right',
#                  text      => "ioniz.ru"
#);

$new->Write("$path_root_new");
return $path_root_new;
}

sub crop_img {

my $size=shift;
my $path_root_i=shift;
my $path_root_new=shift;
my $size_h=shift;
#use Image::Magick;
my $image = Image::Magick->new; #новый проект
my $x = $image->Read($path_root_i); #открываем файл
my ($ox,$oy)=$image->Get('base-columns','base-rows'); #определяем ширину и высоту изображения
my $nx=int(($ox/$oy)*$size); #вычисляем ширину, если высоту сделать 150
$image->Resize(geometry=>geometry, width=>$nx, height=>$size); #Делаем resize (изменения размера)
if($size_h){
if($nx > 200) { #Если ширина получилась больше 200
   my $nnx = int(($nx-200)/2); #Вычисляем откуда нам резать
   $image->Crop(x=>$nnx, y=>0); #Задаем откуда будем резать
   $image->Crop('200x150'); #С того места вырезаем 200х150
}
}
$x = $image->Write($path_root_new); #Сохраняем изображение.

return 1;
}

sub composit_img {

my $path_root_i=shift;
my $path_root_i_new=shift;
my $path_to_copyright =shift;

#use Image::Magick;
my $image = Image::Magick->new; #новый проект
my $image2 = Image::Magick->new; #новый проект
my $x = $image->Read($path_root_i); #открываем файл
my $y = $image2->Read($path_to_copyright); #открываем файл

print "Composite...\n logo size:".$image2->Get('columns')."<br> image size: ".$image->Get('columns')."<br>";
#$example=$model->Clone();
#$example->Label('Composite');
my $x1 = $image->Composite(image=>$image2,compose=>'Over',geometry=>'+1+1',gravity=>'Center' );
#push(@$images,$example);
#print qq[<br>warning: $x1<br>];
$x = $image->Write($path_root_i_new); #Сохраняем изображение.
#use Data::Dumper;
#print Dumper($y);exit;
}

sub size_img {
my $path_root_i=shift;
#use Image::Magick;
my $d=Image::Magick->new;
$d->ReadImage("$path_root_i");
my $ref={};
my $width  = $d->Get('columns');
my $height = $d->Get('rows');
$ref->{width}=$width;
$ref->{height}=$height;
return $ref;
}

sub write_on_picture {
my $path_root_img=shift;
my $font=shift || 'Times-Roman';
my $color=shift || 'black';
my $size_text=shift || 40;
my $gravity=shift || 'Center';
my $text=shift || $host_name;
my $d=Image::Magick->new;
my $status=$d->ReadImage("$path_root_img");
my $new=$d->Clone();
warn "Error read JPEG: $status" if $status;
my @fonts = $d->QueryFont();

$font   =~ s/\W//g;

$new->Annotate(
                  fill  => 'Black',
                  font      => $font,
                  pointsize => '10',
                  gravity   => $gravity,
                  text      => $text
);
$new->Write("$path_root_img");
return 1;
}

sub koi2utf{
    my($str)=@_;
        $_=$str;
            s/Ј/1105/g;         s/і/1025/g;     s/ю/1102/g;     s/а/1072/g;
        s/б/1073/g;     s/ц/1094/g;     s/д/1076/g;     s/е/1077/g;
        s/ф/1092/g;     s/г/1075/g;     s/х/1093/g;     s/и/1080/g;
        s/й/1081/g;     s/к/1082/g;     s/л/1083/g;     s/м/1084/g;
        s/н/1085/g;     s/о/1086/g;     s/п/1087/g;     s/я/1103/g;
        s/р/1088/g;     s/с/1089/g;     s/т/1090/g;     s/у/1091/g;
        s/ж/1078/g;     s/в/1074/g;     s/ь/1100/g;     s/ы/1099/g;
        s/з/1079/g;     s/ш/1096/g;     s/э/1101/g;     s/щ/1097/g;
        s/ч/1095/g;     s/ъ/1098/g;     s/Ю/1070/g;     s/А/1040/g;
        s/Б/1041/g;     s/Ц/1062/g;     s/Д/1044/g;     s/Е/1045/g;
        s/Ф/1060/g;     s/Г/1043/g;     s/Х/1061/g;     s/И/1048/g;
        s/Й/1049/g;     s/К/1050/g;     s/Л/1051/g;     s/М/1052/g;
        s/Н/1053/g;     s/О/1054/g;     s/П/1055/g;     s/Я/1071/g;
        s/Р/1056/g;     s/С/1057/g;     s/Т/1058/g;     s/У/1059/g;
        s/Ж/1046/g;     s/В/1042/g;     s/Ь/1068/g;     s/Ы/1067/g;
        s/З/1047/g;     s/Ш/1064/g;     s/Э/1069/g;     s/Щ/1065/g;
        s/Ч/1063/g;     s/Ъ/1066/g;
    return $_;
}
sub mkdir_ {
my $path_root_mk=shift;
mkdir $path_root_mk,'755';
chmod 0755, $path_root_mk;
return 1;
}

sub message {
  my $ref=shift;
  my $i=$ref->{mes} || '';
  my $lang=$ref->{l};
  my $mess;
  $mess->{1}->[0]=qq[Не все поля заполнены];
  $mess->{2}->[0]=qq[Not all the required fields are filled];
  $mess->{1}->[1]=qq[Домен уже занят];
  $mess->{2}->[1]=qq[Sorry, this domain has been already registered];
  $mess->{1}->[2]=qq[Домен может состоять только из латиских букв, цифр и символа -.<br>Домен должен содержать не менне 3-х и не более 25 символов];
  $mess->{2}->[2]=qq[Domain name can contain Latin letters, figures and "-" symbol only.<br>Not less than 3 and not more than 25 characters.];
  $mess->{1}->[3]=qq[Неверный формат e-mail];
  $mess->{2}->[3]=qq[Incorrect email];
  $mess->{1}->[4]=qq[E-mail содержит недопустимые символы];
  $mess->{2}->[4]=qq[E-mail contains incorrect symbols];
  $mess->{1}->[5]=qq[Пароли не совпадают];
  $mess->{2}->[5]=qq[Passwords are not the same];
  $mess->{1}->[6]=qq[пароль должен содержать не менее 5-ти символов];
  $mess->{2}->[6]=qq[Your password should contain not less than 5 characters];
  $mess->{1}->[9]=qq[Неверный код];
  $mess->{2}->[9]=qq[Incorrect code];
  $mess->{1}->[10]=qq[Пароль содержит недопустимые символы];
  $mess->{2}->[10]=qq[The password contains incorrect symbols];
  $mess->{1}->[11]=qq[Пароль был выслан !];
  $mess->{2}->[11]=qq[The password has been sent];
  $mess->{1}->[12]=qq[Неверный логин. Нет пользователя с таким логином.];
  $mess->{2}->[12]=qq[Incorrect login. There is no user with this login.];
  $mess->{1}->[13]=qq[Информация изменена];
  $mess->{2}->[13]=qq[The information has been changed];
  $mess->{1}->[14]=qq[Неверный пароль !];
  $mess->{2}->[14]=qq[Incorrect password];
  $mess->{1}->[15]=qq[Неверный логин/пароль!<br>Возможно Вы не подтвердили регистрацию или не зарегистрированы];
  $mess->{2}->[15]=qq[Incorrect login/password!<br>Maybe you should confirm your registration or you haven't registered yet.]; #'
  $mess->{1}->[16]=qq[Неверная сессия];
  $mess->{2}->[16]=qq[Wrong session];
  $mess->{1}->[17]=qq[Session time out];
  $mess->{2}->[17]=qq[Session time out];
  $mess->{1}->[18]=qq[Попытка доступа с другого ip адреса];
  $mess->{2}->[18]=qq[Attempt to access from another IP-address];
  $mess->{1}->[19]=qq[Информация сохранена];
  $mess->{2}->[19]=qq[The information has been saved];
  $mess->{1}->[20]=qq[Информация не может быть сохранена. У вас недостаточно свободного места];
  $mess->{2}->[20]=qq[The information can't be saved. You don't have enough free space.];
  $mess->{1}->[21]=qq[Название сайта не должно превышать 35 символов];
  $mess->{2}->[21]=qq[The name of your site should not exceed 35 characters.];
  $mess->{1}->[22]=qq[Описание сайта не должно превышать 255 символов];
  $mess->{2}->[22]=qq[The description of your site should not exceed 255 characters.];
  $mess->{1}->[23]=qq[Сайт временно закрыт за неуплату];
  $mess->{2}->[23]=qq[The site is temporarily closed for non-payment];
  $mess->{1}->[24]=qq[Сайт не найден];
  $mess->{2}->[24]=qq[The page can't be found.]; #'
  $mess->{1}->[25]=qq[Не все поля заполнены];
  $mess->{2}->[25]=qq[Not all the required fields are filled];
  return $mess->{$lang}->[$i];
}

sub slovo {
  my $i=shift||'';
  my $lang=shift||1;
  my $mess;
  $mess->{1}->[0]=qq[];
  $mess->{2}->[0]=qq[];
  $mess->{1}->[1]=qq[Ошибка авторизации - ];
  $mess->{2}->[1]=qq[Authorization error];
  $mess->{1}->[2]=qq[Помощь - ];
  $mess->{2}->[2]=qq[Help - ];
  $mess->{1}->[3]=qq[404 Документ не найден - ];
  $mess->{2}->[3]=qq[404 The page is not found];
  $mess->{1}->[4]=qq[Условия хостинга - ];
  $mess->{2}->[4]=qq[Hosting conditions];
  $mess->{1}->[5]=qq[Каталог сайтов - ];
  $mess->{2}->[5]=qq[Sites catalog];
  $mess->{1}->[6]=qq[Выбор шаблона для сайта - ];
  $mess->{2}->[6]=qq[Choice of site templates];
  $mess->{1}->[7]=qq[Изменение контактной информации - ];
  $mess->{2}->[7]=qq[Edit the contact info];
  $mess->{1}->[8]=qq[Пользовательское соглашение  - ];
  $mess->{2}->[8]=qq[User's agreement];
  $mess->{1}->[9]=qq[Регистрация 1 шаг. Заполните форму - ];
  $mess->{2}->[9]=qq[Registration. Step 1. Fill the form - ];
  $mess->{1}->[10]=qq[Регистрация 2 шаг. Подтвердите регистрацию - ];
  $mess->{2}->[10]=qq[Registration. Step 2. Confirm the registration.];
  $mess->{1}->[11]=qq[Регистрация 3 шаг. Регистрация завершена - ];
  $mess->{2}->[11]=qq[Registration. Step 3. The registration is finished.];
  $mess->{1}->[12]=qq[Напоминание пароля - ];
  $mess->{2}->[12]=qq[Password reminder - ];
  $mess->{1}->[13]=qq[Пароль был выслан - ];
  $mess->{2}->[13]=qq[The password has been sent.];
  $mess->{1}->[14]=qq[Управление файлами: ];
  $mess->{2}->[14]=qq[Files management];
  $mess->{1}->[15]=qq[Продление хостинга -  ];
  $mess->{2}->[15]=qq[Hosting prolongation];
  $mess->{1}->[16]=qq[Расширенный редактор:  ];
  $mess->{2}->[16]=qq[Advanced editor];
  $mess->{1}->[17]=qq[Простой редактор:  ];
  $mess->{2}->[17]=qq[Simple editor];
  $mess->{1}->[18]=qq[Доступ разрешен  ];
  $mess->{2}->[18]=qq[ok];
  $mess->{1}->[19]=qq[Редактор документа - ];
  $mess->{2}->[19]=qq[Document editor];
  $mess->{1}->[20]=qq[Гоствеая :: Редактируем шапку :: ];
  $mess->{2}->[20]=qq[Guestbook :: Edit the top :: ];
  $mess->{1}->[21]=qq[Гостевая книга :: ];
  $mess->{2}->[21]=qq[Guestbook];
  $mess->{1}->[22]=qq[Новости :: Редактируем шапку ];
  $mess->{2}->[22]=qq[News :: Edit the top ];
  $mess->{1}->[23]=qq[Новости :: ];
  $mess->{2}->[23]=qq[News :: ];
  $mess->{1}->[24]=qq[Свойства раздела :: ];
  $mess->{2}->[24]=qq[Section properties :: ];
  $mess->{1}->[25]=qq[Сортировка разделов -  ];
  $mess->{2}->[25]=qq[Sections sorting - ];
  $mess->{1}->[26]=qq[Переопределение родительского раздела - ];
  $mess->{2}->[26]=qq[Parent section redefinition - ];
  $mess->{1}->[27]=qq[Визуальная настройка параметров шаблонов - ];
  $mess->{2}->[27]=qq[Visual setting of template parameters - ];
  $mess->{1}->[28]=qq[Ручная настройка шаблонов - ];
  $mess->{2}->[28]=qq[Manual setting of templates - ];
  $mess->{1}->[29]=qq[Редактор шаблона ::  ];
  $mess->{2}->[29]=qq[Template editor :: ];
  $mess->{1}->[30]=qq[Карта сайта -  ];
  $mess->{2}->[30]=qq[Site map - ];
  $mess->{1}->[31]=qq[Загруженные модули -  ];
  $mess->{2}->[31]=qq[Uploaded modules - ];
  $mess->{1}->[32]=qq[Редактировать содержимое раздела ];
  $mess->{2}->[32]=qq[Edit document];
  $mess->{1}->[33]=qq[Вернуться к настройкам раздела ];
  $mess->{2}->[33]=qq[Back to section properties];
  $mess->{1}->[34]=qq[Удалите сначала все подразделы ];
  $mess->{2}->[34]=qq[Delete all sub section first];
  $mess->{1}->[35]=qq[Удаление раздела ];
  $mess->{2}->[35]=qq[Delete section];
  $mess->{1}->[36]=qq[Раздел удален];
  $mess->{2}->[36]=qq[Section was deleted];
  $mess->{1}->[37]=qq[Интернет магазин - редактор шапки];
  $mess->{2}->[37]=qq[e-Shop];
  $mess->{1}->[38]=qq[Интернет магазин - товары];
  $mess->{2}->[38]=qq[e-Shop];
  $mess->{1}->[39]=qq[Интернет магазин - export/import excel];
  $mess->{2}->[39]=qq[e-Shop - export/import excel];
  $mess->{1}->[40]=qq[Интернет магазин - пользователи];
  $mess->{2}->[40]=qq[e-Shop - users];
  $mess->{1}->[41]=qq[Корзина];
  $mess->{2}->[41]=qq[Basket];
  $mess->{1}->[42]=qq[Авторизация / Регистрация];
  $mess->{2}->[42]=qq[Authorization / registration];
  $mess->{1}->[43]=qq[Выбор адреса доставки];
  $mess->{2}->[43]=qq[Choose adres];
  $mess->{1}->[44]=qq[Добавление/редактирование адреса доставки];
  $mess->{2}->[44]=qq[];
  $mess->{1}->[45]=qq[Выбор способа доставки];
  $mess->{2}->[45]=qq[];
  $mess->{1}->[46]=qq[Выбор способа оплаты];
  $mess->{2}->[46]=qq[];
  $mess->{1}->[47]=qq[Проверка данных];
  $mess->{2}->[47]=qq[];
  $mess->{1}->[48]=qq[Галлерея фотографий];
  $mess->{2}->[48]=qq[Photo gallery];

#'
  if($i){return $mess->{$lang}->[$i];}else{return "";}
}

# Проверяем правильность вписанной картинки
# $ref->{pass} - то что ввел пользователь
# $ref->{pass_hash} - то что передается в форме - закодированное паролем ($ref->{key}) число $ref->{pass}
sub check_captcha { 
 	my $ref=shift;

 	# СЕКРЕТНЫЙ КЛЮЧ ДЛЯ ПОДПИСИ РЕАЛЬНОГО ЧИСЛА НА КАРТИНКЕ
 	my $key=$ref->{key};

 	# директория хранения картинок
 	my $tempdir = "$ref->{path_root}/img/pics";

	# флаг успешного прохождения проверок (1 - успех, 0 - неудача)
	my $flag=1;

 	# подключаем библиотеку Digest::MD5
 	use Digest::MD5 qw(md5_hex);
  	if (md5_hex($key."|".$ref->{pass}) ne $ref->{pass_hash} || !-e "$tempdir/$ref->{pass_hash}.png")
  	{
  		 $flag=0;
  	}
  	my $del=$ref->{dbh}->do("delete from captcha_img where ip=? and file_name=?",undef, ($ref->{ip},$ref->{pass_hash}));
  	# если ничего не удалили из базы - неудача
	if($del==0){$flag=0}
	
	# удаляем записи в базе, время создания которых больше 5 минут
	my $time_min=time-300;
	my $del_all=$ref->{dbh}->do("delete from captcha_img where time_reg<$time_min");

	# Удаляем временные файлы
	# сохраняем директорию чистой, без записей в cron и доп скриптов очистки
	opendir TMPDIR, "$tempdir"; 
	my @alltmpfiles = readdir TMPDIR;

	foreach my $oldtemp (@alltmpfiles) {

		my $age = 0;
		$age = (stat("$tempdir/$oldtemp"))[9];
		# if age is more than 300 seconds or 5 minutes	
		if ((time - $age) > 300){unlink "$tempdir/$oldtemp";}
	
	}

	# удаляем запрашиваемый файл - чистим директорию
	unlink "$ref->{path_root}/img/pics/$ref->{pass_hash}.png";

	return $flag;
}

# записываем в общую переменную данные по картинке
# $ref->{pass_img} - код самой картинки
# $ref->{pass_hash} - закодированное ключом число с картинки
# также записываем в базу ip адрес и закодированное имя картинки
sub set_captcha {

	my $ref=shift;

	# СЕКРЕТНЫЙ КЛЮЧ ДЛЯ ПОДПИСИ РЕАЛЬНОГО ЧИСЛА НА КАРТИНКЕ
	my $key=$ref->{key};

	use Digest::MD5 qw(md5_hex);
	#use ImagePwd;

	my $obj = ImagePwd->new(len=>4, height=>40, width=>140,	
							fixed=>0, rot=>25, quality=>60, cell=>3, 
							f_min=>19, f_max=>25, 
							bgcolor=>'#FFFCCC', 
							color => '#000000'
							);
	$obj->fonts([$ref->{path_root}.'/fonts/arial.ttf'],[$ref->{path_root}.'/fonts/cour.ttf'],[$ref->{path_root}.'/fonts/verdana.ttf']);
	my @arr_letter=('1','2','3','4','5','6','7','8','9','5');
	my $size=$#arr_letter;

	my $approve=""; 
	for (my $i=0; $i<=3; $i++)
	{
		my $t=int(rand($size+1));
		$approve.=$arr_letter[$t];

	};
	$ref->{pass_hash}=md5_hex($key."|".$approve);
#	print qq["$ref->{path_root}/img/pics/$ref->{pass_hash}.png"]; exit;

	my $img = $obj->password($approve); 
   	$img = $obj->ImagePassword();

	binmode STDOUT;
	$img->Write("$ref->{path_root}/img/pics/$ref->{pass_hash}.png");

	# записываем в базу имя картинки, ip и время добавления
	my $ins=$ref->{dbh}->do("insert into captcha_img (file_name,kod,ip,time_reg) values (?,?,?,?)", undef, ($ref->{pass_hash},$approve,$ref->{ip},time));
	return $ref;
}   

END {dbdisconnect_global($dbh_)}
1;
__END__
# Below is stub documentation for your module. You'd better edit it!

=head1 NAME

Modules::Constructor - Perl extension for blah blah blah

=head1 SYNOPSIS

  use Modules::Constructor;
  blah blah blah

=head1 ABSTRACT

  This should be the abstract for Modules::Constructor.
  The abstract is used when making PPD (Perl Package Description) files.
  If you don't want an ABSTRACT you should also edit Makefile.PL to
  remove the ABSTRACT_FROM option.

=head1 DESCRIPTION

Stub documentation for Modules::Constructor, created by h2xs. It looks like the
author of the extension was negligent enough to leave the stub
unedited.

Blah blah blah.

=head2 EXPORT

None by default.



=head1 SEE ALSO

Mention other useful documentation such as the documentation of
related modules or operating system documentation (such as man pages
in UNIX), or any relevant external documentation such as RFCs or
standards.

If you have a mailing list set up for your module, mention it here.

If you have a web site set up for your module, mention it here.

=head1 AUTHOR

Andrey Dmitrichev, <lt>dmitrichev@gmail.com<gt>

=head1 COPYRIGHT AND LICENSE

Copyright 2003-2009 by Andreyd dmitrichev@gmail.com

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself. 

=cut
