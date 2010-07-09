"""
FCKeditor - The text editor for Internet - http://www.fckeditor.net
Copyright (C) 2003-2008 Frederico Caldeira Knabben

== BEGIN LICENSE ==

Licensed under the terms of any of the following licenses at your
choice:

 - GNU General Public License Version 2 or later (the "GPL")
   http://www.gnu.org/licenses/gpl.html

 - GNU Lesser General Public License Version 2.1 or later (the "LGPL")
   http://www.gnu.org/licenses/lgpl.html

 - Mozilla Public License Version 1.1 or later (the "MPL")
   http://www.mozilla.org/MPL/MPL-1.1.html

== END LICENSE ==

This is the integration file for Python.
"""

import cgi
import os
import re
import string

def escape(text, replace=string.replace):
    """Converts the special characters '<', '>', and '&'.

    RFC 1866 specifies that these characters be represented
    in HTML as &lt; &gt; and &amp; respectively. In Python
    1.5 we use the new string.replace() function for speed.
    """
    text = replace(text, '&', '&amp;') # must be don