#!/usr/bin/perl

use strict;
use warnings;
use lib '/opt/local/perl5';
use DBI;
use DBD::MySQL;
use Image::Magick;

my $dbh=DBI->connect(
  "DBI:mysql:database=mysql;host=127.0.0.1",
    "root",
      ""
      ) || die "Error connecting to database: $!\n";
      
      my $sth = $dbh->prepare("SELECT * FROM user");
      
      $sth->execute();
      
      while (my $ref = $sth->fetchrow_arrayref) {
        print $ref->[1] . "\n";
        }
        
        exit;