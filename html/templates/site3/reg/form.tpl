[%IF mess=='ok'%]<b style="color:red;padding:2px">Ваше сообщение доставлено! Наши менеджеры свяжутся с Вами в ближайшее время!</b><br /><br />[%END%]

<table border="0">
<form action="/reg/[%id%].html" method="POST">
[%FOREACH field IN ar_fields %]
<tr><td align="right" valign="top" height="40">[%field.name%]: </td><td valign="top">[%field.input%]</td></tr>
[%END%]
<tr><td>&nbsp;</td><td>&nbsp;</td></tr>
<tr><td align="right" valign="bottom">Введите число: </td><td>[%INSERT captcha.html%]<br><input type=text name=pass value=""></td></tr>
<tr><td></td><td><input type="submit" value="Отправить"></td></tr>
<input type="hidden" name="id" value="[%id%]">
<input type="hidden" name="a" value="reg">
</form>
</table>
