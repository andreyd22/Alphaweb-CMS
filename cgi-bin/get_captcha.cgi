#!/usr/bin/perl
#модуль доски объявлений
 use Data::Dumper;
 $|=1;
 use Modules::Constructor qw (Get_Param &set_captcha);
 use strict;
 my $ref=Get_Param||{};


# use JSON;
# my $json = new JSON; 
      ############### использование  json OOP ########
      #  $json_text   = $json->encode($perl_scalar); #
      #  $perl_scalar = $json->decode($json_text);   #
      ################################################
=r3
my $json_str2=qq[
[
    { "animal" : {"Cat2": "I cat"}, "message" : "Meow" },
    { "animal" : "Cat2", "message" : "Woof" },
    { "animal" : "Cow", "message" : "Moo" },
    { "animal" : "Duck", "message" : "Quack" },
    { "animal" : "Lion", "message" : "Roar" },
    { "animal" : "arg1", "message" : "1$arg1" },
    { "animal" : "arg2", "message" : "1$arg2" }
]
];
=cut

#	my $perl_ref = from_json($json_str2);
	# генерим картинку  captcha
	# $ref->{pass_hash} - содержит имя картинки
	$ref=set_captcha($ref);

	#делаем ссылку на массив, в котором содержатся ссылки на данные (имя => значение, имя2 => значение2)
	my $ref_captcha=[{"pass_hash"=>$ref->{pass_hash}}];
#	my $json_text = to_json($ref_captcha);
	my $json_text=qq[ [{"pass_hash":"$ref->{pass_hash}"}] ];
	#$json->encode($ref_captcha);

   # выводим Json данные ( строка json генерится из ссылки на массив ссылок)
   print "Content-type:text/html\r\n\r\n";
#   print Dumper($ref_captcha);
   print $json_text;
