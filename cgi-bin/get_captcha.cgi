#!/usr/bin/perl
#������ ����� ����������
 use Data::Dumper;
 $|=1;
 use Modules::Constructor qw (Get_Param &set_captcha);
 use strict;
 my $ref=Get_Param||{};


# use JSON;
# my $json = new JSON; 
      ############### �������������  json OOP ########
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
	# ������� ��������  captcha
	# $ref->{pass_hash} - �������� ��� ��������
	$ref=set_captcha($ref);

	#������ ������ �� ������, � ������� ���������� ������ �� ������ (��� => ��������, ���2 => ��������2)
	my $ref_captcha=[{"pass_hash"=>$ref->{pass_hash}}];
#	my $json_text = to_json($ref_captcha);
	my $json_text=qq[ [{"pass_hash":"$ref->{pass_hash}"}] ];
	#$json->encode($ref_captcha);

   # ������� Json ������ ( ������ json ��������� �� ������ �� ������ ������)
   print "Content-type:text/html\r\n\r\n";
#   print Dumper($ref_captcha);
   print $json_text;
