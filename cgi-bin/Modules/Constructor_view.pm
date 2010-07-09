package Modules::Constructor_view;
$|=1;
#use 5.008; #!!!!!!!!!!!!!
#use strict;
#use warnings; #!!!!!!!!!!!!
#use Apache::Reload; #!!!!!!!!
use CGI;

if($path_to_lib ne ""){
	use lib "$path_to_lib"; 
}

# Object initialization:
#use CGI::Session;
#называем сессию SID
#CGI::Session->name("SID");

use Modules::Constructor qw (&Get_Param dbconnect dbdisconnect store_db $host_name 
			    &check_auth get_data_from_cook $path_db $path $path_host 
			    &select_sql &insert_sql &update_sql 
			    &delete_sql $domain_config);
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

  @EXPORT = qw( &main_menu_2 &main_menu_1 &sub_menu_2 &link_view &includes 
  	&print_ &Get_Param_view &Main_Id rotate &select_sql &insert_sql &update_sql &delete_sql &get_city_by_ip &get_country_by_ip &insert_into_services &insert_into_city_anketa
	&is_block_ip_by_country
	);

 $VERSION = '0.02';
# Preloaded methods go here.
 my $t=1;
 my $u=1;
 my $k=1;
 my $y=1;

BEGIN {
}

sub Get_Param_view {
	my $ref=Get_Param;
	$ref->{main_menu_1}=\&main_menu_1;
	$ref->{include_news}=\&include_news;
	$ref->{child_ids}=\&child_ids;
#	$ref->{include_vote}=\&include_vote;
#	$ref->{include_guest}=\&include_guest;
#	$ref->{include_gal}=include_gal($ref);
#	$ref->{random_gal}=random_gal($ref);
#	$ref->{sub_menu}=\&sub_menu;
#	$ref->{path_links}=path_links($ref);
	$ref->{sub_links}=link_view($ref);
#	$ref->{MainID}=Main_Id($ref);
#	$ref->{set_banner}=\&rotate;
	$ref->{trim_for_visual}=\&trim_for_visual;
	$ref->{get_sql}=\&get_sql;

	$ref->{is_field_foreign}=\&is_field_foreign;
	$ref->{set_country}=\&set_country;
	$ref->{set_block_country}=\&set_block_country;
	#$ref->{get_country_by_ip}=get_country_by_ip($ref);
	$ref=check_role($ref);
	return $ref
}
sub child_ids {
my $id=shift;
my $ref={};
   $ref->{dbh}=dbconnect;
   $tbl_name='structure';
   $query="select id from structure where parent='$id'";
my ($name_fields,$ar_data,$fields_comment,$type_fields)=select_sql($ref,$tbl_name,$query,[],0);
my @ar_data_=@$ar_data;
my $res_ids="";
#use Data::Dumper;
#print Dumper($ar_data);
for (my $i=0;$i<=$#ar_data_;$i++){
    $res_ids.="'$ar_data_[$i]->{id}',";
}
$res_ids=~s/,$//gi;
return $res_ids
} 


# Проверка доступа
sub check_role {
        my $ref=shift;

        if(!$ref->{cook}->{SID}){ return $ref}

        # Сессии в базе
        my $dbh=$ref->{dbh};
        my $s = CGI::Session -> load ( "driver:mysql", undef , { Handle => $dbh } )  or die CGI::Session->errstr();

        # Сессии в файле
        #my $s = CGI::Session -> load ("driver:db_file", undef, {FileName=>'../../tmp/sessions.db'});

        if ( !$s->is_expired && !$s->is_empty ) {

                $ref->{user_cook}=$s->param("~profile");
		$ref->{user_cook}->{summa}=$ref->{dbh}->selectrow_array("select SUM(summa) from cashier where users_id='$ref->{user_cook}->{id}'");
	    
		#print qq[select SUMMA(summa) from cashier where users_id='$ref->{user_cook}->{id}'];

        }
        else{
                #$ref->{user_cook}='';
                $s->clear();
                $s->delete();
        }
        return $ref
}

sub is_block_ip_by_country {
my $block_country=shift; # разделитель стран |
my $ref=shift;

my $country_user=get_country_by_ip($ref);

my @ar_cntu=split /\s/, $country_user;
$country_user=$ar_cntu[0];
$country_user=~s/(,|\.)$//gi;

#print qq[<!--$block_country--> <!--$country_user $ref->{ip}-->];
if($block_country=~/$country_user/){return "block_this_ip"}

return undef;
}

sub get_country_by_ip {
#use Geo::IP;
my $ref=shift;
my $ip=shift;
my $ipaddr=$ip||$ref->{ip};
#my $gi = Geo::IP->open("/usr/local/share/GeoIP/GeoIP.dat", GEOIP_STANDARD);

#return $gi->country_name_by_addr( $ipaddr );
return 1;
}


sub get_city_by_ip {
#use Geo::IP;
my $ref=shift;
my $ip=shift;
my $ipaddr=$ip||$ref->{ip};
#my $gi = Geo::IP->open("/usr/local/share/GeoIP/GeoLiteCity.dat", GEOIP_STANDARD);

# my $record = $gi->record_by_addr($ipaddr);
# return $record->city;

=r1
  print $record->country_code,
        $record->country_code3,
        $record->country_name,
        $record->region,
        $record->region_name,
        $record->city,
        $record->postal_code,
        $record->latitude,
        $record->longitude,
        $record->time_zone,
        $record->area_code,
    $record->continent_code,
        $record->metro_code;
=cut
return 1
}

sub insert_into_services {
my $ref=shift;
if($ref->{anketa_id}){
my $del = $ref->{dbh}->do("delete from services_anketa where anketa_id=$ref->{anketa_id}");

my @ar_services_id=CGI::param('services_id');

for (my $i=0;$i<=$#ar_services_id;$i++){
    my $ins=$ref->{dbh}->do("insert into services_anketa (anketa_id,services_id) values (?,?)",undef,($ref->{anketa_id},$ar_services_id[$i]));
}
}

}

sub insert_into_city_anketa {
my $ref=shift;
if($ref->{anketa_id}){
my $del = $ref->{dbh}->do("delete from city_anketa where anketa_id=$ref->{anketa_id}");

my @ar_city_id=CGI::param('city_id');

for (my $i=0;$i<=$#ar_city_id;$i++){
    my $ins=$ref->{dbh}->do("insert into city_anketa (anketa_id,city_id) values (?,?)",undef,($ref->{anketa_id},$ar_city_id[$i]));
}
}

}

sub set_country {
my $country=shift;
my $str=qq[<option value="">Choose you country</option><option value="Afghanistan">Afghanistan</option><option value="Albania">Albania</option><option value="Algeria">Algeria</option><option value="American Samoa">American Samoa</option><option value="Andorra">Andorra</option><option value="Angola">Angola</option><option value="Anguilla">Anguilla</option><option value="Antigua">Antigua</option><option value="Antilles">Antilles</option><option value="Argentina">Argentina</option><option value="Armenia">Armenia</option><option value="Aruba">Aruba</option><option value="Ascension Island">Ascension Island</option><option value="Australia">Australia</option><option value="Austria">Austria</option><option value="Azerbaijan">Azerbaijan</option><option value="Bahamas">Bahamas</option><option value="Bahrain">Bahrain</option><option value="Bangladesh">Bangladesh</option><option value="Barbados">Barbados</option><option value="Barbuda">Barbuda</option><option value="Belarus">Belarus</option><option value="Belgium">Belgium</option><option value="Belize">Belize</option><option value="Benin">Benin</option><option value="Bermuda">Bermuda</option><option value="Bhutan">Bhutan</option><option value="Bolivia">Bolivia</option><option value="Botswana">Botswana</option><option value="Brazil">Brazil</option><option value="Brunei">Brunei</option><option value="Bulgaria">Bulgaria</option><option value="Burkina Faso">Burkina Faso</option><option value="Burundi">Burundi</option><option value="Cambodia">Cambodia</option><option value="Cameroon">Cameroon</option><option value="Canada">Canada</option><option value="Canary Islands">Canary Islands</option><option value="Cayman Islands">Cayman Islands</option><option value="Chad">Chad</option><option value="Chile, Rep. of">Chile, Rep. of</option><option value="China">China</option><option value="Christmas Island">Christmas Island</option><option value="Colombia">Colombia</option><option value="Comoros">Comoros</option><option value="Cook Islands">Cook Islands</option><option value="Costa Rica">Costa Rica</option><option value="Croatia">Croatia</option><option value="Cuba">Cuba</option><option value="Cyprus">Cyprus</option><option value="Czech Rep.">Czech Rep.</option><option value="Denmark">Denmark</option><option value="Diego Garcia">Diego Garcia</option><option value="Djibouti">Djibouti</option><option value="Dominica">Dominica</option><option value="Dominican Rep.">Dominican Rep.</option><option value="Ecuador">Ecuador</option><option value="Egypt">Egypt</option><option value="El Salvador">El Salvador</option><option value="Eritrea">Eritrea</option><option value="Estonia">Estonia</option><option value="Ethiopia">Ethiopia</option><option value="Faeroe Islands">Faeroe Islands</option><option value="Falkland Islands">Falkland Islands</option><option value="Fiji">Fiji</option><option value="Finland">Finland</option><option value="France">France</option><option value="French Antilles">French Antilles</option><option value="French Guiana">French Guiana</option><option value="French Polynesia">French Polynesia</option><option value="Gabon">Gabon</option><option value="Gambia">Gambia</option><option value="Georgia">Georgia</option><option value="Germany">Germany</option><option value="Ghana">Ghana</option><option value="Gibraltar">Gibraltar</option><option value="Greece">Greece</option><option value="Greenland">Greenland</option><option value="Grenada">Grenada</option><option value="Guadeloupe">Guadeloupe</option><option value="Guatemala">Guatemala</option><option value="Guinea">Guinea</option><option value="Guinea-Bissau">Guinea-Bissau</option><option value="Guyana">Guyana</option><option value="Haiti">Haiti</option><option value="Honduras">Honduras</option><option value="Hong Kong">Hong Kong</option><option value="Hungary">Hungary</option><option value="Iceland">Iceland</option><option value="India">India</option><option value="Indonesia">Indonesia</option><option value="Iraq">Iraq</option><option value="Ireland">Ireland</option><option value="Israel">Israel</option><option value="Italy">Italy</option><option value="Jamaica">Jamaica</option><option value="Japan">Japan</option><option value="Jordan">Jordan</option><option value="Kazakhstan">Kazakhstan</option><option value="Kenya">Kenya</option><option value="Kiribati">Kiribati</option><option value="Korea, North">Korea, North</option><option value="Korea, South">Korea, South</option><option value="Kuwait">Kuwait</option><option value="Kyrgyzstan">Kyrgyzstan</option><option value="Laos">Laos</option><option value="Latvia">Latvia</option><option value="Lebanon">Lebanon</option><option value="Lesotho">Lesotho</option><option value="Liberia">Liberia</option><option value="Liechtenstein">Liechtenstein</option><option value="Lithuania">Lithuania</option><option value="Luxembourg">Luxembourg</option><option value="Macau">Macau</option><option value="Madagascar">Madagascar</option><option value="Malawi">Malawi</option><option value="Malaysia">Malaysia</option><option value="Maldives">Maldives</option><option value="Mali">Mali</option><option value="Malta">Malta</option><option value="Marshall Islands">Marshall Islands</option><option value="Martinique">Martinique</option><option value="Mauritania">Mauritania</option><option value="Mauritius">Mauritius</option><option value="Mayotte Island">Mayotte Island</option><option value="Mexico">Mexico</option><option value="Moldova, Rep. of">Moldova, Rep. of</option><option value="Monaco">Monaco</option><option value="Mongolia">Mongolia</option><option value="Montserrat">Montserrat</option><option value="Morocco">Morocco</option><option value="Mozambique">Mozambique</option><option value="Myanmar">Myanmar</option><option value="Namibia">Namibia</option><option value="Nauru">Nauru</option><option value="Nepal">Nepal</option><option value="Netherlands">Netherlands</option><option value="Nevis">Nevis</option><option value="New Caledonia">New Caledonia</option><option value="New Zealand">New Zealand</option><option value="Nicaragua">Nicaragua</option><option value="Niger">Niger</option><option value="Nigeria">Nigeria</option><option value="Niue">Niue</option><option value="Norfolk Island">Norfolk Island</option><option value="Norway">Norway</option><option value="Oman">Oman</option><option value="Pakistan">Pakistan</option><option value="Palau">Palau</option><option value="Panama">Panama</option><option value="Papua New Guinea">Papua New Guinea</option><option value="Paraguay">Paraguay</option><option value="Peru">Peru</option><option value="Philippines">Philippines</option><option value="Poland">Poland</option><option value="Portugal">Portugal</option><option value="Puerto Rico">Puerto Rico</option><option value="Qatar">Qatar</option><option value="Reunion Island">Reunion Island</option><option value="Romania">Romania</option><option value="Rota Island">Rota Island</option><option value="Russian Federatio">Russian Federation</option><option value="Rwanda">Rwanda</option><option value="Saint Lucia">Saint Lucia</option><option value="Saipan Island">Saipan Island</option><option value="San Marino">San Marino</option><option value="Saudi Arabia">Saudi Arabia</option><option value="Scotland">Scotland</option><option value="Senegal">Senegal</option><option value="Seychelles">Seychelles</option><option value="Sierra Leone">Sierra Leone</option><option value="Singapore">Singapore</option><option value="Slovakia">Slovakia</option><option value="Slovenia">Slovenia</option><option value="Solomon Islands">Solomon Islands</option><option value="Somalia">Somalia</option><option value="South Africa">South Africa</option><option value="Spain">Spain</option><option value="Sri Lanka">Sri Lanka</option><option value="St. Helena">St. Helena</option><option value="St. Kitts">St. Kitts</option><option value="Sudan">Sudan</option><option value="Suriname">Suriname</option><option value="Swaziland">Swaziland</option><option value="Sweden">Sweden</option><option value="Switzerland">Switzerland</option><option value="Syrian Arab Rep.">Syrian Arab Rep.</option><option value="Taiwan">Taiwan</option><option value="Tajikistan">Tajikistan</option><option value="Tanzania">Tanzania</option><option value="Thailand">Thailand</option><option value="Tinian Island">Tinian Island</option><option value="Togo">Togo</option><option value="Tokelau">Tokelau</option><option value="Tonga">Tonga</option><option value="Tunisia">Tunisia</option><option value="Turkey">Turkey</option><option value="Turkmenistan">Turkmenistan</option><option value="Tuvalu">Tuvalu</option><option value="Uganda">Uganda</option><option value="Ukraine">Ukraine</option><option value="United Kingdom">United Kingdom</option><option value="Uruguay">Uruguay</option><option value="USA">USA</option><option value="Uzbekistan">Uzbekistan</option><option value="Vanuatu">Vanuatu</option><option value="Vatican City">Vatican City</option><option value="Venezuela">Venezuela</option><option value="Viet Nam">Viet Nam</option><option value="Wales">Wales</option><option value="Western Samoa">Western Samoa</option><option value="Yemen">Yemen</option><option value="Yugoslavia">Yugoslavia</option><option value="Zambia">Zambia</option><option value="Zimbabwe">Zimbabwe</option>];

$str=~s/value=\"$country\"\>/value=\"$country\" selected=\"selected\">/gi;
return $str;
}

sub set_block_country {
my $country=shift;
my @ar_block_country=();
if(!$country){
@ar_block_country=CGI::param('block_country');
}else{
$country=~s/|$//gi;
@ar_block_country=split /\|/,$country;
}
my $str=qq[<option value="">Block you anketa by country</option><option value="Afghanistan">Afghanistan</option><option value="Albania">Albania</option><option value="Algeria">Algeria</option><option value="American Samoa">American Samoa</option><option value="Andorra">Andorra</option><option value="Angola">Angola</option><option value="Anguilla">Anguilla</option><option value="Antigua">Antigua</option><option value="Antilles">Antilles</option><option value="Argentina">Argentina</option><option value="Armenia">Armenia</option><option value="Aruba">Aruba</option><option value="Ascension Island">Ascension Island</option><option value="Australia">Australia</option><option value="Austria">Austria</option><option value="Azerbaijan">Azerbaijan</option><option value="Bahamas">Bahamas</option><option value="Bahrain">Bahrain</option><option value="Bangladesh">Bangladesh</option><option value="Barbados">Barbados</option><option value="Barbuda">Barbuda</option><option value="Belarus">Belarus</option><option value="Belgium">Belgium</option><option value="Belize">Belize</option><option value="Benin">Benin</option><option value="Bermuda">Bermuda</option><option value="Bhutan">Bhutan</option><option value="Bolivia">Bolivia</option><option value="Botswana">Botswana</option><option value="Brazil">Brazil</option><option value="Brunei">Brunei</option><option value="Bulgaria">Bulgaria</option><option value="Burkina Faso">Burkina Faso</option><option value="Burundi">Burundi</option><option value="Cambodia">Cambodia</option><option value="Cameroon">Cameroon</option><option value="Canada">Canada</option><option value="Canary Islands">Canary Islands</option><option value="Cayman Islands">Cayman Islands</option><option value="Chad">Chad</option><option value="Chile, Rep. of">Chile, Rep. of</option><option value="China">China</option><option value="Christmas Island">Christmas Island</option><option value="Colombia">Colombia</option><option value="Comoros">Comoros</option><option value="Cook Islands">Cook Islands</option><option value="Costa Rica">Costa Rica</option><option value="Croatia">Croatia</option><option value="Cuba">Cuba</option><option value="Cyprus">Cyprus</option><option value="Czech Rep.">Czech Rep.</option><option value="Denmark">Denmark</option><option value="Diego Garcia">Diego Garcia</option><option value="Djibouti">Djibouti</option><option value="Dominica">Dominica</option><option value="Dominican Rep.">Dominican Rep.</option><option value="Ecuador">Ecuador</option><option value="Egypt">Egypt</option><option value="El Salvador">El Salvador</option><option value="Eritrea">Eritrea</option><option value="Estonia">Estonia</option><option value="Ethiopia">Ethiopia</option><option value="Faeroe Islands">Faeroe Islands</option><option value="Falkland Islands">Falkland Islands</option><option value="Fiji">Fiji</option><option value="Finland">Finland</option><option value="France">France</option><option value="French Antilles">French Antilles</option><option value="French Guiana">French Guiana</option><option value="French Polynesia">French Polynesia</option><option value="Gabon">Gabon</option><option value="Gambia">Gambia</option><option value="Georgia">Georgia</option><option value="Germany">Germany</option><option value="Ghana">Ghana</option><option value="Gibraltar">Gibraltar</option><option value="Greece">Greece</option><option value="Greenland">Greenland</option><option value="Grenada">Grenada</option><option value="Guadeloupe">Guadeloupe</option><option value="Guatemala">Guatemala</option><option value="Guinea">Guinea</option><option value="Guinea-Bissau">Guinea-Bissau</option><option value="Guyana">Guyana</option><option value="Haiti">Haiti</option><option value="Honduras">Honduras</option><option value="Hong Kong">Hong Kong</option><option value="Hungary">Hungary</option><option value="Iceland">Iceland</option><option value="India">India</option><option value="Indonesia">Indonesia</option><option value="Iraq">Iraq</option><option value="Ireland">Ireland</option><option value="Israel">Israel</option><option value="Italy">Italy</option><option value="Jamaica">Jamaica</option><option value="Japan">Japan</option><option value="Jordan">Jordan</option><option value="Kazakhstan">Kazakhstan</option><option value="Kenya">Kenya</option><option value="Kiribati">Kiribati</option><option value="Korea, North">Korea, North</option><option value="Korea, South">Korea, South</option><option value="Kuwait">Kuwait</option><option value="Kyrgyzstan">Kyrgyzstan</option><option value="Laos">Laos</option><option value="Latvia">Latvia</option><option value="Lebanon">Lebanon</option><option value="Lesotho">Lesotho</option><option value="Liberia">Liberia</option><option value="Liechtenstein">Liechtenstein</option><option value="Lithuania">Lithuania</option><option value="Luxembourg">Luxembourg</option><option value="Macau">Macau</option><option value="Madagascar">Madagascar</option><option value="Malawi">Malawi</option><option value="Malaysia">Malaysia</option><option value="Maldives">Maldives</option><option value="Mali">Mali</option><option value="Malta">Malta</option><option value="Marshall Islands">Marshall Islands</option><option value="Martinique">Martinique</option><option value="Mauritania">Mauritania</option><option value="Mauritius">Mauritius</option><option value="Mayotte Island">Mayotte Island</option><option value="Mexico">Mexico</option><option value="Moldova, Rep. of">Moldova, Rep. of</option><option value="Monaco">Monaco</option><option value="Mongolia">Mongolia</option><option value="Montserrat">Montserrat</option><option value="Morocco">Morocco</option><option value="Mozambique">Mozambique</option><option value="Myanmar">Myanmar</option><option value="Namibia">Namibia</option><option value="Nauru">Nauru</option><option value="Nepal">Nepal</option><option value="Netherlands">Netherlands</option><option value="Nevis">Nevis</option><option value="New Caledonia">New Caledonia</option><option value="New Zealand">New Zealand</option><option value="Nicaragua">Nicaragua</option><option value="Niger">Niger</option><option value="Nigeria">Nigeria</option><option value="Niue">Niue</option><option value="Norfolk Island">Norfolk Island</option><option value="Norway">Norway</option><option value="Oman">Oman</option><option value="Pakistan">Pakistan</option><option value="Palau">Palau</option><option value="Panama">Panama</option><option value="Papua New Guinea">Papua New Guinea</option><option value="Paraguay">Paraguay</option><option value="Peru">Peru</option><option value="Philippines">Philippines</option><option value="Poland">Poland</option><option value="Portugal">Portugal</option><option value="Puerto Rico">Puerto Rico</option><option value="Qatar">Qatar</option><option value="Reunion Island">Reunion Island</option><option value="Romania">Romania</option><option value="Rota Island">Rota Island</option><option value="Russian Federation">Russian Federation</option><option value="Rwanda">Rwanda</option><option value="Saint Lucia">Saint Lucia</option><option value="Saipan Island">Saipan Island</option><option value="San Marino">San Marino</option><option value="Saudi Arabia">Saudi Arabia</option><option value="Scotland">Scotland</option><option value="Senegal">Senegal</option><option value="Seychelles">Seychelles</option><option value="Sierra Leone">Sierra Leone</option><option value="Singapore">Singapore</option><option value="Slovakia">Slovakia</option><option value="Slovenia">Slovenia</option><option value="Solomon Islands">Solomon Islands</option><option value="Somalia">Somalia</option><option value="South Africa">South Africa</option><option value="Spain">Spain</option><option value="Sri Lanka">Sri Lanka</option><option value="St. Helena">St. Helena</option><option value="St. Kitts">St. Kitts</option><option value="Sudan">Sudan</option><option value="Suriname">Suriname</option><option value="Swaziland">Swaziland</option><option value="Sweden">Sweden</option><option value="Switzerland">Switzerland</option><option value="Syrian Arab Rep.">Syrian Arab Rep.</option><option value="Taiwan">Taiwan</option><option value="Tajikistan">Tajikistan</option><option value="Tanzania">Tanzania</option><option value="Thailand">Thailand</option><option value="Tinian Island">Tinian Island</option><option value="Togo">Togo</option><option value="Tokelau">Tokelau</option><option value="Tonga">Tonga</option><option value="Tunisia">Tunisia</option><option value="Turkey">Turkey</option><option value="Turkmenistan">Turkmenistan</option><option value="Tuvalu">Tuvalu</option><option value="Uganda">Uganda</option><option value="Ukraine">Ukraine</option><option value="United Kingdom">United Kingdom</option><option value="Uruguay">Uruguay</option><option value="USA">USA</option><option value="Uzbekistan">Uzbekistan</option><option value="Vanuatu">Vanuatu</option><option value="Vatican City">Vatican City</option><option value="Venezuela">Venezuela</option><option value="Viet Nam">Viet Nam</option><option value="Wales">Wales</option><option value="Western Samoa">Western Samoa</option><option value="Yemen">Yemen</option><option value="Yugoslavia">Yugoslavia</option><option value="Zambia">Zambia</option><option value="Zimbabwe">Zimbabwe</option>];
for(my $i=0;$i<=$#ar_block_country;$i++){
    my $tmp_block_country=$ar_block_country[$i];
    $str=~s/value=\"$tmp_block_country\"\>/value=\"$tmp_block_country\" selected=\"selected\">/i;
}
return $str;
}

sub is_field_foreign {
my $name_field=shift;
if($name_field=~/^(.+?)\_id$/){return $1;} else {return 0;}
}

sub get_sql {
my $query=shift;
my $ref={};
    $ref->{dbh}=dbconnect;
my $tpl_name='';
my ($name_fields,$ar_data,$fields_comment,$type_fields)=select_sql($ref,$tbl_name,$query,[],0);
return $ar_data;

}

sub trim_for_visual {
my $str=shift;

    $str=~s/\n/ /gi;
    $str=~s/\s+/ /gi;
    $str=~s/'/"/gi; #'

return $str;
}

sub random_gal {

 my $ref=shift;
 my $dbh=dbconnect;
 my $ref_random_gal=$dbh->selectrow_hashref("select * from gallery_ where konkurs_number='8' order by RAND() limit 1");	

 return $ref_random_gal;
#};

#return {};
}

#### пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
sub rotate
{
 my $place=shift;
 my $dbh=dbconnect;
 my $ref_banner=$dbh->selectrow_hashref("select * from banners where place='$place' order by RAND() limit 1");	
    return $ref_banner;

}



sub Main_Id { #пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅ
    my $ref=shift;
    my $id_p='main';
    my $last=$ref->{id};
    
    my $dbh=&dbconnect;

#    my $ll=$dbh->selectrow_array("select parent from structure where id='$last'");
    $ref->{lang}='ru' if !$ref->{lang};
    my $ll=$last;
    while ($ll ne $id_p)
    {
	$last=$ll;
      	$ll=$dbh->selectrow_array("select parent from structure where id='$last'");
	#print qq[$ll = $last<br>];
	if ($ll eq 'main' || !$ll){return $last;}
    };
    
return $ll;
}

sub path_links { # строим хлебные крошки (путь к странице)
        my $ref=shift;
	my $ref_link=$ref->{dbh}->selectrow_hashref("select * from structure where id='$ref->{id}' limit 1");
	my @ar_menu=();
	my $inc=0;
	while($ref_link->{parent} ne '0'){
    	    $ref_link=$ref->{dbh}->selectrow_hashref("select * from structure where id='$ref_link->{parent}' limit 1");
	    unshift @ar_menu, $ref_link;
	    $inc++;
	    if($inc>100){return \@ar_menu}
	}

return \@ar_menu;
}


sub main_menu_1 { #пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
	my $parent_id=shift || "main";
	my $dbh=dbconnect();
	my $sth=$dbh->prepare("select * from structure where parent='$parent_id' order by sort_id asc");
#print qq[$parent_id];
	$sth->execute;
	my @ar_menu=();
	while (my $ref_s=$sth->fetchrow_hashref)
	{
	    my $key=$ref_s->{id};
	    if($ref_s->{visible}=~/menu1=1/)
	    {
		my $count=$dbh->selectrow_array("select count(*) from structure where parent='$key'");
		$ref_s->{count_subs}=$count;	
		push @ar_menu,$ref_s;
	    }
	}
	$sth->finish;
	
	return 	\@ar_menu;
}

sub sub_menu { #пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_ пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_пїЅпїЅ_

        my $parent=shift;
	my $dbh=dbconnect();
	my $sth=$dbh->prepare("select * from structure where parent='$parent' order by sort_id asc");
	my $count=$sth->execute;

	my @sub_menu=();
	while (my $ref_s=$sth->fetchrow_hashref)
	{
	    my $key=$ref_s->{id};
	    if($ref_s->{visible}=~/menu1=1/)
	    {
		push @sub_menu,$ref_s;
	    }
	}
	$sth->finish;
	
	return 	\@sub_menu;
}

sub link_view {
    my $ref=shift;
        my $sort=$ref->{user_db}->{data}->{sort}||{};
        my $parent=$ref->{user_db}->{data}->{parent}||{};

    my %sort=%$sort;
    my %parent=%$parent;

    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    my $key_for_select='';
    my $dbh=dbconnect();

    #пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ

    if ($ref->{user_db}->{data}->{$ref->{id}}->{link_view} eq 'empty'){ #пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
	my @ar_menu=();
       return \@ar_menu;
    }
    if ($ref->{user_db}->{data}->{$ref->{id}}->{link_view} eq 'child'){ #пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
	my $sth=$dbh->prepare("select * from structure where parent='$ref->{id}' order by sort_id asc");
	$sth->execute;
	my @ar_menu=();
	    #print qq[select * from structure where parent='$ref->{id}' order by sort_id asc<br>];
	while (my $ref_s=$sth->fetchrow_hashref)
	{
		my $key=$ref_s->{id};
	    if($ref_s->{visible}=~/menu1=1/)
	    {
	       	push @ar_menu,$ref_s;
	    }
	}
	$sth->finish;
	
	return 	\@ar_menu;
    }
    if ($ref->{user_db}->{data}->{$ref->{id}}->{link_view} eq 'similary'){ #пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ
       $key_for_select=$parent{$ref->{id}};
	my $sth=$dbh->prepare("select * from structure where parent='$key_for_select' order by sort_id asc");
	$sth->execute;
	my @ar_menu=();
	while (my $ref_s=$sth->fetchrow_hashref)
	{
		my $key=$ref_s->{id};
	    if($ref_s->{visible}=~/menu1=1/)
		{
	       	push @ar_menu,$ref_s;
	    }
	}
	$sth->finish;
	
	return 	\@ar_menu;
    }

    if ($ref->{user_db}->{data}->{$ref->{id}}->{link_view} eq 'parent'){ #пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ

	my $sth=$dbh->prepare("select * from structure where parent='$ref->{id}' order by sort_id asc");
	$sth->execute;
	my @ar_menu=();
	while (my $ref_s=$sth->fetchrow_hashref)
	{
		my $key=$ref_s->{id};
	    if($ref_s->{visible}=~/menu1=1/)
		{
	       	push @ar_menu,$ref_s;
	    }
	}
	$sth->finish;
	
	return 	\@ar_menu;

   }

   #$ref->{link_view}=\@ar_link_view;
}

sub includes {
 my $ref=shift;
 my $tpl=shift;
 my $include_id=$ref->{user_db}->{data}->{$ref->{id}}->{include_id}||{};
 my $include_col=$ref->{user_db}->{data}->{$ref->{id}}->{include_col}||{};
 my @ar_include_id=@$include_id;
 my @ar_include_col=@$include_col;
# @ar_include_id[4]='important';
# @ar_include_col[4]='1';
 my $t=0;
        my $def={  
         "INCLUDES_ROW"=>"/includes.tpl",
         "INCLUDES_ROW1"=>"/includes1.tpl",
         "INCLUDES_ROW2"=>"/includes2.tpl",
         "INCLUDES_ROW3"=>"/includes3.tpl",
         "INCLUDES_ROW4"=>"/includes4.tpl",
        };
        $tpl->define(%$def);
 for(@ar_include_id){
    my $mod=$ref->{user_db}->{data}->{$ar_include_id[$t]}->{mod}||'';
    my $col=$ar_include_col[$t];
    my $num=$ref->{user_db}->{data}->{$ref->{id}}->{include_num}->[$t];
    if($mod eq 'document'){
        $tpl=include_document($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'news'){
        $tpl=include_news($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'guest'){
        $tpl=include_guest($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'catalog'){
        $tpl=include_catalog($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'vote'){
        $tpl=include_vote($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'gallery'){
        $tpl=include_gallery($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
    elsif($mod eq 'article'){
        $tpl=include_article($ref,$ar_include_id[$t],$tpl,$col,$num);
        }
  $t++;
 }
return $tpl;
}
sub include_vote { #пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
 my $id=shift;
 my $col=shift || '10';
# my $col=1;
 my $dbh=dbconnect;
 my $sel="select * from vote where idr='$id' and status=1  order by data_reg desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#print qq[ $sel];
    my @ar_vote=();
    while(my $ref_vote=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_vote->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day/$month/$year $hour:$min";

        my $sel_otvet="select * from otvet where id_vote='$ref_vote->{id}'";
        my $sth2=$dbh->prepare($sel_otvet);
        my $col_otvet=$sth2->execute();
        my $sum=$dbh->selectrow_array("select sum(count) from otvet where id_vote='$ref_vote->{id}'");
	    my @ar_otvet=();
        while(my $ref_otvet=$sth2->fetchrow_hashref){
               $vote_rows.=$tmp_row;
		push @ar_otvet,$ref_otvet;
        }
        $sth2->finish;
	$ref_vote->{otvets}=\@ar_otvet;
	push @ar_vote,$ref_vote;
    }
    $sth->finish;
    return \@ar_vote;

}
sub include_document { #пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
 my $ref=shift;
 my $id=shift;
 my $tpl=shift;
 my $col=shift || '';
 my $num=shift || '';
 my $k=0;
    my $sort=$ref->{user_db}->{data}->{sort}||{};
    my $parent=$ref->{user_db}->{data}->{parent}||{};

    my %sort=%$sort;
    my %parent=%$parent;

    my @ar_sort_key=sort{$sort{$a}<=>$sort{$b}} keys %sort;
    my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};

     foreach my $key (@ar_sort_key){
      if($parent{$key} eq $id){
#!!!        && $ref->{user_db}->{data}->{$key}->{visible}->{menu1} eq '1' #!!! пїЅпїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ
        my $link=$ref->{user_db}->{data}->{$key}->{link}||"/$ref->{user_db}->{data}->{$key}->{lang}/$key/";
        if($k!=0){
         $zag='';
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>'',
                ZAG_IMG=>''
                );
        }
        else{
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>$zag,
                ZAG_IMG=>$ref->{zag_img}
                );
        }
        $tpl->assign(
                INCLUDES_NAME=>$ref->{user_db}->{data}->{$key}->{name},
                INCLUDES_TEXT=>$ref->{user_db}->{data}->{$key}->{description},
                LINK=>$link
        );
        $tpl->parse("INCLUDES_ROW$num",".INCLUDES_ROW$num");
        $tpl->clear_href(1);
        $k++;
        if($k==$col){return $tpl}
     }
    }

 return $tpl;
}

sub include_news {
 my $id=shift;
 my $col=shift || '10';
 my $dbh=dbconnect;
 my $sel="select id,idr,data_reg,zag,short,full_news from news where 
 idr='$id' and data_reg<=now() order by data_reg desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    my @ar=();
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day.$month.$year";
	 $year=substr($year,2,2);
	 my @ar_month=('','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря');
         
        $ref_news->{data_print}="$day.$month.$year";

	 $ref_news->{data_y}=$year;
	 $ref_news->{data_d}=int($day);
	 $ref_news->{data_m}=$month;
	 $ref_news->{data_month}=$ar_month[$month];
	push @ar,$ref_news;
    }
    $sth->finish;
 dbdisconnect($dbh);
 return \@ar;
}
sub include_guest {
 my $id=shift;
 my $col=shift || '10';
 my $dbh=dbconnect;
 my $sel="select * from guest where 
 idr='$id' and data_reg<=now() order by data_reg desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    my @ar=();
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day.$month.$year";
	 $year=substr($year,2,2);
	 my @ar_month=('','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря');
         
        $ref_news->{data_print}="$day.$month.$year";

	 $ref_news->{data_y}=$year;
	 $ref_news->{data_d}=int($day);
	 $ref_news->{data_m}=$month;
	 $ref_news->{data_month}=$ar_month[$month];

=r1
            $ref_news->{name}=CGI::escapeHTML($ref_guest->{name});
            $ref_news->{email}=CGI::escapeHTML($ref_guest->{email});
            $ref_news->{subject}=CGI::escapeHTML($ref_guest->{subject});
            $ref_news->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_news->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_news->{record}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_news->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_news->{record}=~s/\|\|===brake===\|\|/<br>/gi;
            $ref_news->{answer}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_news->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_news->{answer}=~s/\|\|===brake===\|\|/<br>/gi;
=cut
	push @ar,$ref_news;
    }
    $sth->finish;
 dbdisconnect($dbh);
 return \@ar;
}

sub include_gal {
 my $ref=shift;
 #переход по страницам
# my $sel="select g.*, s.name as name_r from gallery_$ref->{prefix} as g, structure as s where g.idr=s.id order by date_reg desc, id desc limit 4";
 my $sel="select g.*, s.name as name_r from gallery_$ref->{prefix} as g, structure as s where g.idr=s.id order by RAND() limit 4";
 my $sth=$ref->{dbh}->prepare($sel);
    $sth->execute;
    my $inc=0; my $i=0;
    my @ar=();
    while(my $ref_catalog=$sth->fetchrow_hashref){
         $ref_catalog->{name}=~tr/"'/``/;
         $ref_catalog->{opis}=~tr/"'/``/; #'
         $ref_catalog->{opis}=~s/\n|\r/<br>/gi; 
         $inc++;$i++;
    	 my $alt="$ref_catalog->{name} / $zag $ref->{user_db}->{template}->{assign}->{TITLE}";
         $alt=~s/"/'/gi; $alt=~s/\s+/ /gi; $alt=~s/^\s+|\s+$//gi; $alt=~s/^\/|\/$//gi; #'"
      	 push @ar,$ref_catalog;
		
    }
    $sth->finish;
 return \@ar;
}

sub include_article {
 my $ref=shift;
 my $id=shift;
 my $tpl=shift;
 my $col=shift || '10';
 my $num=shift || '';

 my $dbh=dbconnect;
 my $sel="select * from article where idr='$id' and data_reg<=now() order by data_reg desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    while(my $ref_news=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_news->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
#         my $data_print="$day/$month/$year $hour:$min";
         my $data_print="$day.$month.$year";
#        $zag=qq[
#<tr>
#<td height=20 background="/tmp_img/im_r9_c2.jpg" class="z"><img src="/tmp_img/im_r9_c3.jpg" width="11" height="20" hspace="10" align="absmiddle" />$zag</td>
#</tr>
#        ];

                if($r==0){
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>$zag,
                ZAG_IMG=>$ref->{zag_img}
                        );
                 $r=1;
                }else {
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>''
                        );
                }
        my $link=$ref->{user_db}->{data}->{$id}->{link}||"/$ref->{user_db}->{data}->{$id}->{lang}/$id/doc$ref_news->{id}.html";
        $ref_news->{short}=~s/<img(.+?)>//gi;
        $tpl->assign(
                INCLUDES_DATA=>$data_print ,
                INCLUDES_NAME=>$ref_news->{zag},
                INCLUDES_TEXT=>$ref_news->{short},
                LINK=>$link
        );
        $tpl->parse("INCLUDES_ROW$num",".INCLUDES_ROW$num");
        $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
 return $tpl;
}

sub include_catalog {
 my $ref=shift;
 my $id=shift;
 my $tpl=shift;
 my $col=shift || '10';
 my $num=shift || '';
#print qq[ok2 $col];
$ref->{prefix}=$ref->{user_doman};
$ref->{prefix}=~s/\-|\./_/gi;
$ref->{prefix}='';

 my $dbh=dbconnect;
#print qq[news include id = $id <br>];
 my $sel="select * from catalog_$ref->{prefix} where  
  idr='$id' order by id desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    while(my $ref_catalog=$sth->fetchrow_hashref){
        my $img_cat="";
         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}-s.jpg"){
          $img_cat=qq[<a target=_blank href="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}.jpg">
        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/cat_image/$ref_catalog->{id}-s-50.jpg" border=0 align=center hspace=5 vspace=5 width=50></a>];
         }
#         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}.jpg"){
#          $img_cat=qq[<a target=_blank href="http://$ref->{user_doman}/docs/cat_image/$ref_catalog->{id}.jpg">
#        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE} full screen" src="http://$ref->{user_doman}/docs/cat_image/$ref_catalog->{id}.jpg" border=0 align=center hspace=5 vspace=5 width=50></a>];
#         }
#        $zag=qq[
#<tr>
#<td height=20 background="/tmp_img/im_r9_c2.jpg" class="z"><img src="/tmp_img/im_r9_c3.jpg" width="11" height="20" hspace="10" align="absmiddle" />$zag</td>
#</tr>
#        ];
                if($r==0){
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>$zag,
                ZAG_IMG=>$ref->{zag_img}
                        );
                 $r=1;
                }else {
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>''
                        );
                }
        my $link=$ref->{user_db}->{data}->{$id}->{link}||"/$ref->{user_db}->{data}->{$id}->{lang}/$id/cat$ref_catalog->{id}.html";
        $tpl->assign(
                INCLUDES_NAME=>$ref_catalog->{name},
                INCLUDES_TEXT=>$ref_catalog->{short},
                INCLUDES_IMG=>$img_cat,
                LINK=>$link
        );
        $tpl->parse("INCLUDES_ROW$num",".INCLUDES_ROW$num");
        $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
 return $tpl;
}

sub include_gallery {
 my $ref=shift;
 my $id=shift;
 my $tpl=shift;
 my $col=shift || '10';
 my $num=shift || '';
#print qq[ok2 $col];
$ref->{prefix}=$ref->{user_doman};
$ref->{prefix}=~s/\-|\./_/gi;
$ref->{prefix}='';

 my $dbh=dbconnect;
#print qq[news include id = $id <br>];
 my $sel="select * from gallery_$ref->{prefix} where  
  idr='$id' order by sort asc, id desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    while(my $ref_gal=$sth->fetchrow_hashref){
        my $img_cat="";
        $ref_gal->{name}=~tr/"'/``/;
         if(-e "$ref->{path_host}/gallery_image/$ref_gal->{id}-s.jpg"){
          $img_cat=qq[<a href="#" onclick="win_gallery('http://$ref->{user_doman}/gallery_image/$ref_gal->{id}.jpg','$ref_gal->{name}',$ref_gal->{width},$ref_gal->{height}); return false;">
        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE}" src="http://$ref->{user_doman}/gallery_image/$ref_gal->{id}-s-50.jpg" border=0 align=center hspace=5 vspace=5 width=50></a>];
         }
#         if(-e "$ref->{path_host}/cat_image/$ref_catalog->{id}.jpg"){
#          $img_cat=qq[<a target=_blank href="http://$ref->{user_doman}/docs/cat_image/$ref_catalog->{id}.jpg">
#        <img alt="$ref_catalog->{name} $zag $ref->{user_db}->{template}->{assign}->{TITLE} full screen" src="http://$ref->{user_doman}/docs/cat_image/$ref_catalog->{id}.jpg" border=0 align=center hspace=5 vspace=5 width=50></a>];
#         }
#        $zag=qq[
#<tr>
#<td height=20 background="/tmp_img/im_r9_c2.jpg" class="z"><img src="/tmp_img/im_r9_c3.jpg" width="11" height="20" hspace="10" align="absmiddle" />$zag</td>
#</tr>
#        ];
                if($r==0){
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>$zag,
                ZAG_IMG=>$ref->{zag_img}
                        );
                 $r=1;
                }else {
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>'',
                ZAG_IMG=>''
                        );
                }
        my $link=$ref->{user_db}->{data}->{$id}->{link}||"/$ref->{user_db}->{data}->{$id}->{lang}/$id/gal$ref_gal->{id}.html";
        $tpl->assign(
                INCLUDES_DATA=>'',
                INCLUDES_NAME=>$ref_gal->{name},
                INCLUDES_TEXT=>$ref_gal->{short},
                INCLUDES_IMG=>$img_cat,
                LINK=>$link
        );
        $tpl->parse("INCLUDES_ROW$num",".INCLUDES_ROW$num");
        $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
 return $tpl;
}

sub include_guest_old {
 my $ref=shift;
 my $id=shift;
 my $tpl=shift;
 my $col=shift || '10';
 my $num=shift || '';

 my $dbh=dbconnect;
#print qq[news include id = $id <br>];
 my $sel="select * from guest where idu='7' 
 and idr='$id' order by data_reg desc limit $col";
 my $r=0;
 my $sth=$dbh->prepare($sel);
 my $count=$sth->execute;
#        $tpl->clear_href(1);
my $zag=$ref->{user_db}->{data}->{$id}->{zag}||$ref->{user_db}->{data}->{$id}->{name};
    while(my $ref_guest=$sth->fetchrow_hashref){
         my ($data,$time)=split / /,$ref_guest->{data_reg};
         my ($year,$month,$day)=split /-/,$data;
         my ($hour,$min,$sec)=split/:/,$time;
         my $data_print="$day/$month/$year $hour:$min";
            $ref_guest->{name}=CGI::escapeHTML($ref_guest->{name});
            $ref_guest->{email}=CGI::escapeHTML($ref_guest->{email});
            $ref_guest->{subject}=CGI::escapeHTML($ref_guest->{subject});
            $ref_guest->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_guest->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_guest->{record}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_guest->{record}=CGI::escapeHTML($ref_guest->{record});
            $ref_guest->{record}=~s/\|\|===brake===\|\|/<br>/gi;
            $ref_guest->{answer}=~s/\n/\|\|===brake===\|\|/gi;
            $ref_guest->{answer}=CGI::escapeHTML($ref_guest->{answer});
            $ref_guest->{answer}=~s/\|\|===brake===\|\|/<br>/gi;
#        $zag=qq[
#<tr>
#<td height=20 background="/tmp_img/im_r9_c2.jpg" class="z"><img src="/tmp_img/im_r9_c3.jpg" width="11" height="20" hspace="10" align="absmiddle" />$zag</td>
#</tr>
#        ];
                if($r==0){
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>$zag,
                ZAG_IMG=>$ref->{zag_img}
                        );
                 $r=1;
                }else {
        $tpl->assign(
                INCLUDES_NAME_RAZDEL=>'',
                ZAG_IMG=>''
                        );
                }
        my $link=$ref->{user_db}->{data}->{$id}->{link}||"/$ref->{user_db}->{data}->{$id}->{lang}/$id";
        $tpl->assign(
                INCLUDES_NAME=>"$data_print $ref_guest->{name} <b> $ref_guest->{subject}</b>",
                INCLUDES_TEXT=>"$ref_guest->{record}<blockquote><hr>$ref_guest->{answer}</blockquote>",
                                LINK=>$link
        );
        $tpl->parse("INCLUDES_ROW$num",".INCLUDES_ROW$num");
        $tpl->clear_href(1);
    }
    $sth->finish;
 dbdisconnect($dbh);
 return $tpl;
}

# пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
sub print_ {

my $ref=shift;
	use Template;
         # some useful options (see below for full list)
         my $config = {};
         if($ref->{module_name}){
         	$ref->{path_module_template}=":$ref->{path_root}/templates/$domain_config->{$host_name}->{'folder'}/$ref->{module_name}/";
         }
         if($ref->{cach} eq "yes"){
	    $config = {
             INCLUDE_PATH => "$ref->{path_root}/templates/$domain_config->{$host_name}->{'folder'}/:$ref->{path_root}/db/$domain_config->{$host_name}->{'folder'}/$ref->{path_module_template}",  	# or list ref
             INTERPOLATE  => 0,               	# expand "$var" in plain text
             POST_CHOMP   => 1,               	# cleanup whitespace
             EVAL_PERL    => 0,               	# evaluate Perl code blocks
    	     COMPILE_DIR  => "$ref->{path_root}/templates/$domain_config->{$host_name}->{'folder'}/ext/", 		#   Root of directory in which compiled template files should be written (default: undef - don't compile).
	     COMPILE_EXT  => '.ext',		#           Filename extension for compiled template files (default: undef - don't compile)

            };
         
         }else{
            $config = {
             INCLUDE_PATH => "$ref->{path_root}/templates/$domain_config->{$host_name}->{'folder'}/:$ref->{path_root}/db/$domain_config->{$host_name}->{'folder'}/$ref->{path_module_template}",  	# or list ref
             INTERPOLATE  => 0,               	# expand "$var" in plain text
             POST_CHOMP   => 1,               	# cleanup whitespace
             EVAL_PERL    => 0,               	# evaluate Perl code blocks
            };
         }
	 #print qq[$ref->{path_root}/templates/:$ref->{path_root}/db/$ref->{path_module_template}];
         # create Template object
         my $Template = Template->new($config);

	# пїЅпїЅпїЅпїЅпїЅпїЅ, пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ
	my $tpl='index.tpl'; 
	if($ref->{index_tpl}){$tpl=$ref->{index_tpl}}
	if($ref->{v} eq 'print'){$tpl="index_print.tpl"}
	$ref->{tpl_}="default.tpl" if !$ref->{tpl_};
	# пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ
	# print qq[$tpl , $ref->{tpl_}];
	$Template->process($tpl, $ref) || die $Template->error();
#	print qq[$ref->{tpl_}]; exit;
#########################################################################
# пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ.
# пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ. 
# пїЅ.пїЅ. пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅпїЅ пїЅ пїЅпїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅ пїЅпїЅпїЅпїЅпїЅпїЅпїЅ.
#########################################################################
#print $output;
}

END {}
1;
__END__
# Below is stub documentation for your module. You'd better edit it!

=head1 NAME

Modules::Constructor_view - Perl extension for blah blah blah

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

Copyright 2009 by Andreyd dmitrichev@gmail.com

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself. 

=cut
