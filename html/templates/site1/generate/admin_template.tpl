<a href="/cgi-bin/mod/[%module_name%].cgi">Список записей</a> ::

<a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit">Добавить новую запись</a>
[%IF a == ''%]

<table width="100%">
<tr>[%inc=0%]
[%FOREACH name IN name_fields %]
	    [%IF type_fields.$inc.Type != 'text'%]
<td><a href="/cgi-bin/mod/[%module_name%].cgi?order_name=[%name%]&asc=[%IF  asc=='asc'%]desc[%ELSE%]asc[%END%]"><b>[%fields_comment.$inc||name%]</b></a>
 <!--([%type_fields.$inc.Type%])-->
</td>
	    [%END%]
[%inc=inc+1%]
[%END%]
</tr>
    [%FOREACH ref_data IN ar_data %]
    <tr>    
	[%inc=0%]
	[%FOREACH name IN name_fields %]
	    [%IF type_fields.$inc.Type != 'text'%]
    	    <td valign="top"><a href="/cgi-bin/mod/[%module_name%].cgi?a=form_edit&id=[%ref_data.id%]">[%ref_data.$name%]</td>
	    [%END%]
	[%inc=inc+1%]
        [%END%]
	<td><a href="/cgi-bin/mod/[%module_name%].cgi?a=del&id=[%ref_data.id%]" onclick="return confirm('Действительно удалить запись №[%ref_data.id%]?')">[x]</a></td>
    </tr>
    [%END%]
</table>

[%END%]


[%IF a == 'form_edit' %]
<script type="text/javascript" src="/js/tools/calendar/calendar_stuff.js"></script>
<script type="text/javascript" src="/js/tools/calendar/calendar_mini.js"></script>

<script type="text/javascript" src="/js/tools/calendar/lang/calendar-en.js"></script>
<link rel="stylesheet" href="/js/tools/calendar/calendar-mos.css" type="text/css" />	

	<link href="/fckeditor/_samples/sample.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript" src="/fckeditor/fckeditor.js"></script>
<fieldset>
<legend>[%IF !ref_data.id%]Добавление нового элемента в [%module_name%][%ELSE%]Редактирование #[%ref_data.id%] в [%module_name%][%END%]</legend>
<table width="100%">
[%inc=0%]
<form action="/cgi-bin/mod/[%module_name%].cgi" method="post" name="form1">
[%FOREACH name IN name_fields %]
[%IF name != 'id'%]
<tr><td valign="top" width="10%"><b>[%fields_comment.$inc||name%]</b></td>
<td valign="top" width="90%">
 [%name_field=type_fields.$inc.Field%]
 [%value_field = ref_data.$name_field%]

 [%foreign_table=is_field_foreign("$name")%]
 [%IF foreign_table%]
<select name="[%name%]">
[%FOREACH data IN get_sql("select * from $foreign_table")%]
    <option value="[%data.id%]" [%IF data.id==ref_data.$name%]SELECTED[%END%]>[%data.name%]
[%END%]
</select>

 [%ELSIF type_fields.$inc.Type_short == 'varchar'%]
    <input type="text" name="[%name_field%]" value="[%ref_data.$name_field%]">

[%ELSIF type_fields.$inc.Type_short == 'date'%]

<input name="[%name_field%]"  id="[%name_field%]" value="[%ref_data.$name_field%]" readonly style="width:80px">
 <input type="image" src="/js/tools/calendar/img.gif" onclick="return showCalendar('[%name_field%]', 'y/mm/dd');" />

[%ELSIF type_fields.$inc.Type_short == 'datetime'%]

<input name="[%name_field%]"  id="[%name_field%]" value="[%ref_data.$name_field%]" style="width:80px">
 <input type="image" src="/js/tools/calendar/img.gif" onclick="return showCalendar('[%name_field%]', 'y/mm/dd 00:00');" />


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
</fieldset>
</form>
[%END%]


[%IF a == 'save' %]<br><br>
    [%IF update_status%]
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