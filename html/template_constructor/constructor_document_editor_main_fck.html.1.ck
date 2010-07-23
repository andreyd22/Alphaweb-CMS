<html>
<head>
 <title></title>
</head>
<link rel="stylesheet" href="/admin/style.css" type="text/css">
<link rel="stylesheet" href="/admin/webedit/webedit.css" type="text/css">
<body bgcolor="#F5F5F5">
    <TABLE width="100%" border="0" cellpadding="0" cellspacing="0">
<tr><td>
                            <TABLE cellpadding="2" cellspacing="0" border="0" width="100%">
                              <TR>
                                <TD bgcolor="#ffffff" class="smallbl" align="left">
                                  <DIV class="smallbl">
                                                                        $USER_MENU
                                  </DIV>
                                </TD>
                              </TR>
                              <TR>
                                <TD bgcolor="#e2e2e2" align="left" class="bl">
                                  &nbsp;
                                </TD>
                                                          </TR>
                            </TABLE>
</td></tr>
      <TR>
         <TD bgcolor="#ffffff" class="miniwh" align="left">
                  <!--ВЕРХНЯЯ ЧАСТЬ С МЕНЮ КОНЕЦ-->

<table width=100%>
<tr>
<td>
<table cellspacing=3 cellpadding=3>
<tr>
<td>::<a href="/cgi-bin/mod/razdels.cgi?sid=${SID}&l=${LANG}&id=${ID}&a=add">Свойства раздела</a>:: 
 ::<a href="/cgi-bin/mod/${MOD}.cgi?sid=${SID}&l=${LANG}&id=${ID}"><b>Администрирование (спец. свойства)</b></a>:: 
 ::<a href="/cgi-bin/mod/razdels.cgi?sid=${SID}&l=${LANG}&idp=${ID}&a=add"><b>Добавить подраздел к этому разделу</b></a>::
</td>
</tr>
</table>
</td>
</tr>
<tr><td><center><b style="color:red">${MESSAGE}</b></center><hr></td></tr>
</table>
<TABLE cellSpacing=0 cellPadding=0 width="100%" align=center border=0>
<form action="/cgi-bin/mod/document.cgi" method="post">
<input type="hidden" name="a" value="save" />
<input type="hidden" name="sid" value="${SID}" />
<input type="hidden" name="id" value="${ID}" />
<input type="hidden" name="l" value="${LANG}" />
<tr><td align="center">Редактирование текста раздела: ${NAME_ST} </td>
<tr><td>
    <script type="text/javascript" src="/ckfinder/ckfinder.js"></script>
    <script type="text/javascript" src="/ckeditor/ckeditor.js"></script>
    <script type="text/javascript" src="/ckeditor/_samples/sample.js"></script>
<textarea name="content" id="content">${DATA}</textarea>  
    <script type="text/javascript">

// This is a check for the CKEditor class. If not defined, the paths must be checked.
if ( typeof CKEDITOR == 'undefined' )
{
    document.write(
	'<strong><span style="color: #ff0000">Error</span>: CKEditor not found</strong>.' +
	'This sample assumes that CKEditor (not included with CKFinder) is installed in' +
	'the "/ckeditor/" path. If you have it installed in a different place, just edit' +
	'this file, changing the wrong paths in the &lt;head&gt; (line 5) and the "BasePath"' +
	'value (line 32).' ) ;
}
else
{
    var editor = CKEDITOR.replace( 'content' );
    //editor.setData( '<p>Just click the <b>Image</b> or <b>Link</b> button, and then <b>&quot;Browse Server&quot;</b>.</p>' );

    // Just call CKFinder.SetupCKEditor and pass the CKEditor instance as the first argument.
    // The second parameter (optional), is the path for the CKFinder installation (default = "/ckfinder/").
    CKFinder.setupCKEditor( editor, '/ckfinder/' ) ;

    // It is also possible to pass an object with selected CKFinder properties as a second argument.
    // CKFinder.SetupCKEditor( editor, { BasePath : '../../', RememberLastFolder : false } ) ;
}
</script>

<br><br>
<input type=submit value="Сохранить">
                                </TD>
                              </TR></form>

          <TR>
        <TD height="4" class="minibl" align="center"> Copyright &copy;  <a href="http://alphaweb.ru" class=bl target=_blank>Alphaweb</a>, 2004-2008 </TD>
      </TR>
    </TABLE>
  </BODY>
</HTML>
