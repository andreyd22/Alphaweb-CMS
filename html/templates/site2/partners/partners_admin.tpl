[%INCLUDE menu_partners.tpl%]

[%IF mess%]<center><b style="color:red">[%mess%]</b></center>[%END%]

[%IF a =='edit_forma'%]

<table width="100%" border="0">
<form action="/cgi-bin/mod/partners.cgi" method="post" name="form1" enctype="multipart/form-data">
[%IF ref_data.typef%]
<tr><td width="160">
<b>Загруженная главная фотография</b></td><td>
<img src="/upload/partners_photo/[%ref_data.id%].[%ref_data.typef%]?t=[%time%]"><br>
<a href="/cgi-bin/mod/partners.cgi?a=del_photo&id_partner=[%ref_data.id%]" onclick="return confirm('Удалить фотографию [%ref_data.name%]')">[x]</a>
</td>
<tr>
[%END%]
<td align="right" width="160">Заглавная Фотография </td><td>[%INSERT fileinput.tpl%]</td>
</tr>


<tr>
<td align="right" width="160">Имя</td><td><input name="name" value="[%ref_data.name%]"></td>
</tr>

<tr><td width="160">Краткое описание - выводится в списке</td><td></td></tr>
<tr><td colspan="3">

	<link href="/fckeditor/_samples/sample.css" rel="stylesheet" type="text/css" />
	<script type="text/javascript" src="/fckeditor/fckeditor.js"></script>

<script type="text/javascript">
<!--
// Automatically calculates the editor base path based on the _samples directory.
// This is usefull only for these samples. A real application should use something like this:
// oFCKeditor.BasePath = '/fckeditor/' ;	// '/fckeditor/' is the default value.
//var sBasePath = document.location.href.substring(0,document.location.href.lastIndexOf('_samples')) ;

var oFCKeditor = new FCKeditor( 'short' ) ;
oFCKeditor.BasePath	= /fckeditor/ ;
oFCKeditor.Height	= 250 ;
oFCKeditor.Value	= '[%ref_data.short%]' ;
oFCKeditor.Create() ;
//-->
</script>

</td></tr>

<tr><td width="160">Полное Описание</td><td></td></tr>
<tr><td colspan="3">


<script type="text/javascript">
<!--
// Automatically calculates the editor base path based on the _samples directory.
// This is usefull only for these samples. A real application should use something like this:
// oFCKeditor.BasePath = '/fckeditor/' ;	// '/fckeditor/' is the default value.
//var sBasePath = document.location.href.substring(0,document.location.href.lastIndexOf('_samples')) ;

var oFCKeditor2 = new FCKeditor( 'opis' ) ;
oFCKeditor2.BasePath	= /fckeditor/ ;
oFCKeditor2.Height	= 500 ;
oFCKeditor2.Value	= '[%ref_data.opis%]' ;
oFCKeditor2.Create() ;
//-->
</script>

</td></tr>

<tr>
<td align="right" width="160">Ссылка</td><td><input name="link" value="[%ref_data.link%]"></td>
</tr>

<tr>
<td>Видимый на сайте ?</td><td><input type="checkbox" name="visible" value="1"[%IF ref_data.visible%]checked[%END%]><input type="hidden" name="visible" value="0"></td>
</tr>

<tr>
<td align="right" width="160">Сортировка</td><td><input name="name" value="[%ref_data.sort||50%]" size="2">(чем больше цифра тем выше)</td>
</tr>

<tr>
<td colspan="2"><input type="submit" value="Сохранить"></td>
</tr>
<input type="hidden" name="id" value="[%id%]">
<input type="hidden" name="id_partner" value="[%IF ref_data.id != id%][%ref_data.id%][%END%]">
<input type="hidden" name="a" value="save">

</form>
</table>

</td></tr></table>

[%END%]


[%IF a == ''%]
<table>
[%FOREACH data IN ar_data %]

      <tr>
        <td>[%data.data_print%]</td>
	<td>
	<a href="/cgi-bin/mod/partners.cgi?id_partner=[%data.id%]&a=edit_forma&id=[%id%]">[%data.name%]</a></td>
	<td><a href="/cgi-bin/mod/partners.cgi?id_partner=[%data.id%]&a=edit_forma&id=[%id%]">[редактировать]</a></td>
	<td><a href="/cgi-bin/mod/partners.cgi?a=del_partner&id_partner=[%data.id%]&id=[%id%]" onclick="return confirm('Удалить [%data.name%]')">[x]</a></td>
    </tr>
[%END%]
</table>
[%perehod%]

[%END%]

[%IF a == 'edit_partner_sort'%]
Изменение сортировки прошло успешно!
[%END%]
[%IF  a== 'del_partner' %]
    [%IF del_status %] 
	Удаление прошло успешно!
    [%ELSE%]
	Удалить не удалось!
    [%END%]
[%END%]

[%IF  a=='del_photo'%]
     Удаление фотографии прошло успешно<br><br>
     <a href="[%referrer%]">Вернуться к редактированию</a>
[%END%]

[%IF  a=='edit_photo'%]
     Обновление фотографий галереи прошло успешно<br><br>
     <a href="[%referrer%]">Вернуться к редактированию</a>
[%END%]

[%IF  a=='del_photo_gal'%]
     Удаление фотографи из галереи прошло успешно<br><br>
     <a href="[%referrer%]">Вернуться к редактированию</a>
[%END%]

[%IF a == 'save'%]
    [%IF insert_status%]Сохранение прошло успешно [%END%]
    [%IF update_status%]Обновление прошло успешно <a href="[%referrer%]">Вернуться к редактированию</a>[%END%]
    

[%END%]

