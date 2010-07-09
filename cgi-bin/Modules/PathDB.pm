package Modules::PathDB;
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

  @EXPORT = qw(     
		$domain_config $host_name $path_cgi $path_root $db_host $db_user $db_pass $db_name $path_to_lib
    		);

 $VERSION = '0.02';

 BEGIN
{
	  $host_name	= $ENV{'HTTP_HOST'};
	  $host_name=~s/^www\.//gi;
	  
	  $domain_config = {
	    'site1.local' => {	'folder' => 'site1', 
				'root_mail'=>'dmitrichev@gmail.com', 
				'post_mail' => 'dmitrichev@gmail.com',
				'project' => 'Alphaweb CMS 1' 
			    },
	    'site2.local' => {	'folder' => 'site2', 
				'root_mail'=>'dmitrichev@gmail.com', 
				'post_mail' => 'dmitrichev@gmail.com',
				'project' => 'Alphaweb CMS 2'
			    },
	    'site3.local' => {	'folder' => 'site3', 
				'root_mail'=>'dmitrichev@gmail.com', 
				'post_mail' => 'dmitrichev@gmail.com',
				'peoject' => 'AlphaWeb CMS 3' 
			    }
	  };

	  $path_cgi	= "$ENV{'DOCUMENT_ROOT'}/../cgi-bin";
	  $path_root	= "$ENV{'DOCUMENT_ROOT'}";
	  $path_to_lib	= "$path_cgi/Modules" || "./" ;  # путь к модулям, если стоят в отдельной папке

	  $db_host	= "localhost";
	  $db_name 	= "alphawebcms";
	  $db_user 	= "root";
	  $db_pass	= "";

}

END {}
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

Copyright 2008 by Andreyd dmitrichev@gmail.com

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself. 

=cut
