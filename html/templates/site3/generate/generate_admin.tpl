<!--a href="/cgi-bin/mod/generate.cgi?a=edit_form">������� ����� ����������</a-->
<a href="/cgi-bin/mod/generate.cgi"> ������ ��������� ������ ��� ��������� ������������</a>

<br><br>

[%IF a == ''%]
����� �� ������ ������������ ����� ����� ������� � ������� ������. ����� ���������� - �������� �������������� ������� � ���� ������<br><br>
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
    �������� �������: <input name="table_name" value="[%table_name%]"> <br>
    �������� ������: <input name="name" value="[%name%]"><br>
    �������� ������: <input name="opis" value="[%opis%]"><br>
    <input type="submit" value="������������ ���������� � �������"><br>
    <input type="hidden" name="a" value="generate">
    </form>
[%END%]


[%IF a == 'generate'%]
    [%IF status=='success'%]
	��������� ������ �������
    [%END%]
    [%IF mess%]
	[%mess%]
    [%END%]
[%END%]