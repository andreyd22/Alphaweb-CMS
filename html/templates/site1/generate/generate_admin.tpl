<!--a href="/cgi-bin/mod/generate.cgi?a=edit_form">Создать новый контроллер</a-->
<a href="/cgi-bin/mod/generate.cgi"> Список доступных таблиц для генерации контроллеров</a>

<br><br>

[%IF a == ''%]
Здесь вы можете генерировать новые админ скрипты и скрипты вывода. Перед генерацией - создайте соотвествующую таблицу в базе данных<br><br>
<table>
<tr>[%inc=0%]
[%FOREACH name IN name_fields %]
<td><b>[%fields_comment.$inc||name%] ([%type_fields.$inc.Type%])</b></td>
[%inc=inc+1%]
[%END%]
</tr>
[%FOREACH ref_data IN ar_data %]
<tr>    
    [%FOREACH name IN name_fields %]
	<td valign="top"><a href="/cgi-bin/mod/generate.cgi?a=form_edit&table_name=[%ref_data.$name%]">[%ref_data.$name%]</td>
    [%END%]
</tr>
[%END%]
</table>

[%END%]

[%IF a == 'form_edit'%]
    <form action="/cgi-bin/mod/generate.cgi">
    Название таблицы: <input name="table_name" value="[%table_name%]"> <br>
    Название модуля: <input name="name" value="[%name%]"><br>
    Описание модуля: <input name="opis" value="[%opis%]"><br>
    <input type="submit" value="Генерировать контроллер и шаблоны"><br>
    <input type="hidden" name="a" value="generate">
    </form>
[%END%]


[%IF a == 'generate'%]
    [%IF status=='success'%]
	генерация прошла успешно
    [%END%]
    [%IF mess%]
	[%mess%]
    [%END%]
[%END%]