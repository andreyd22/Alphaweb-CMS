#!/usr/bin/perl -w
=r
use Config;
print "Content-Type: text/plain\n\n";
print join "\n",
      map {$_.' => '.
           (defined $Config{$_}?
             ($Config{$_} eq ''?
               '[EMPTY STRING]':
               "'$Config{$_}'"):
             '[UNDEFINED]')}
      sort keys %Config;
=cut

use strict;
use threads;
 
sub f {
    my ($a, $t)=@_;
    open A, "+>./log.thread";
    print A "WAIT $a\n";
    sleep $t;
    print A "DONE $a\n";
    close A;
    return "RESULT $a\n";
}
 
my $kida = threads->create(\&f, 'A', 30);
#my $kidb = threads->create(\&f, 'B', 1);
 
print $kida->detach;
#print $kidb->join;