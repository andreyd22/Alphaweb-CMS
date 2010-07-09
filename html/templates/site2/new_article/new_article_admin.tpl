<a href="/cgi-bin/mod/[%module_name%].cgi">Список записей</a> ::

<a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit">Добавить новую запись</a>
[%IF a == ''%]

<table width="100%">
<tr>[%inc=0%]
[%FOREACH name IN name_fields %]
<td><b>[%fields_comment.$inc||name%] ([%type_fields.$inc.Type%])</b></td>
[%inc=inc+1%]
[%END%]
</tr>
    [%FOREACH ref_data IN ar_data %]
    <tr>    
	[%FOREACH name IN name_fields %]
    	    <td valign="top"><a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit&id=[%ref_data.id%]">[%ref_data.$name%]</td>
        [%END%]
	<td><a href="/cgi-bin/mod/[%module_name%].cgi?a=del&id=[%ref_data.id%]" onclick="return confirm('Действительно удалить запись №[%ref_data.id%]?')">[x]</a></td>
    </tr>
    [%END%]
</table>

[%END%]


[%IF a == 'form_edit' %]
	<link href="/javascripts/date/dateselector.css" rel="stylesheet" type="text/css">
	<script type="text/javascript" src="/javascripts/date/popup_lib.js"></script>
	<script type="text/javascript" src="/javascripts/date/dateselector.js"></script>

	<script type="text/javascript" src="/javascripts/date/prototype.js"></script>

	<link href="/fckeditor/_samples/sample.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript" src="/fckeditor/fckeditor.js"></script>
<table width="100%">
[%inc=0%]
<form action="/cgi-bin/mod/[%module_name%].cgi" method="post" name="form1">
[%FOREACH name IN name_fields %]
[%IF name != 'id'%]
<tr><td valign="top" width="10%"><b>[%fields_comment.$inc||name%]</b></td>
<td valign="top" width="90%">
 [%name_field=type_fields.$inc.Field%]
 [%value_field = ref_data.$name_field%]

 [%IF type_fields.$inc.Type_short == 'varchar'%]

    <input type="text" name="[%name_field%]" value="[%ref_data.$name_field%]">

[%ELSIF type_fields.$inc.Type_short == 'date'%]

[%IF ref_data.$name_field == ''%]
<script type="text/javascript">
var day = new Date();
month = 1 + day.getMonth();
year = day.getYear();
if(year<1000){year=year+1900}
today = day.getDate() + '.' + month + '.' + year;
document.write('<input type="text" name="[%name_field%]" id="date_date_afisha"'+ 'value="' + today + '" readonly style="width:80px">');
</script>
[%ELSE%]
<input name="[%name_field%]" value="[%ref_data.$name_field%]" readonly style="width:80px">
[%END%]
<img onclick="popUpCalendar(this, form1.[%name_field%], 'dd.mm.yyyy');" height=18 hspace=3 src="/javascripts/date/date_selector.gif" width=16 border=0></td></tr>


[%ELSIF type_fields.$inc.Type_short == 'datetime'%]

[%IF ref_data.$name_field == ''%]
<script type="text/javascript">
var day = new Date();
month = 1 + day.getMonth();
year = day.getYear();
if(year<1000){year=year+1900}
today = day.getDate() + '.' + month + '.' + year;
document.write('<input type="text" name="[%name_field%]" id="date_date_afisha"'+ 'value="' + today + '00:00:00" style="width:100px">');
</script>
[%ELSE%]
<input name="[%name_field%]" value="[%ref_data.$name_field%]" style="width:100px">
[%END%]
<img onclick="popUpCalendar(this, form1.[%name_field%], 'yyyy.mm.dd 00:00:00');" height=18 hspace=3 src="/javascripts/date/date_selector.gif" width=16 border=0></td></tr>

 [%ELSIF type_fields.$inc.Type_short == 'int'%]
    <input type="text" name="[%name_field%]" value="[%ref_data.$name_field%]" size="2">



 [%ELSIF type_fields.$inc.Type_short == 'int'%]
    <input type="text" name="[%name_field%]" value="[%ref_data.$name_field%]" size="2">


 [%ELSIF type_fields.$inc.Type_short == 'text'%]


<script type="text/javascript">
<!--
// Automatically calculates the editor base path based on the _samples directory.
// This is usefull only for these samples. A real application should use something like this:
// oFCKeditor.BasePath = '/fckeditor/' ;	// '/fckeditor/' is the default value.
//var sBasePath = document.location.href.substring(0,document.location.href.lastIndexOf('_samples')) ;

var oFCKeditor_[%name_field%] = new FCKeditor( '[%name_field%]' ) ;
oFCKeditor_[%name_field%].BasePath	= /fckeditor/ ;
oFCKeditor_[%name_field%].Height	= 250 ;
oFCKeditor_[%name_field%].Value	= '[%trim_for_visual("$value_field")%]' ;
oFCKeditor_[%name_field%].Create() ;
//-->
</script>

 [%ELSE%]
    <input type="text" name="[%name_field%]" value='[%trim_for_visual("$value_field")%]'>

 [%END%]

</td>
</tr>
[%END%]
[%inc=inc+1%]
[%END%]

<tr>
<td colspan="2"><input type="submit" value="Сохранить"></td>
<input type="hidden" name="a" value="save">
<input type="hidden" name="id" value="[%ref_data.id%]">
</tr>
</table>

[%END%]


[%IF a == 'save' %]
    [%IF update_status%]<br><br>
	Обновление прошло успешно. <br><br><a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit&id=[%id%]">Вернуться к редактированию</a>
    [%ELSIF id %]
	Сохранени прошло успешно. <br><br><a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit&id=[%id%]">Вернуться к редактированию</a>
    [%ELSE%]
	Что то пошло не так. Обратитесь к разработчикам.
    [%END%]
[%END%]


[%IF a == 'del' %]<br><br>
    [%IF delete_status%]
	Удаление прошло успешно. <br><br><a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit">Добавить новую запись</a>
    [%ELSE%]
	Что то пошло не так. Обратитесь к разработчикам.
    [%END%]
[%END%]