[%IF a==''%]

<style>
#katalog {
widht:auto;
height:auto;
}

#kat_bl {
float:left;
width:131px;
height:230px;
margin:7px;
padding:5px;
border: 1px solid #c1c8cf;
z-index: 100;
}

#kat_bl img {margin: 20px 0 0 0; z-index: 0;}

#kat_bl:hover {
float:left;
width:131px;
height:230px;
margin:7px;
padding:5px;
border: 1px solid #f4cf80;
background: #fff8e8;
}

#kat_ris {
width:130px;
height:180px;
}
#katalog_text {
margin: 35px 0 0 0;
padding: 2px 0;
background:#8aa0b9;
font: bold 13px Verdana, Arial, Helvetica, sans-serif;
color: #fff;
text-align: center;
}
</style>
<div style="clear:both"></div>
<div id="katalog">
[%FOREACH data IN ar_data %]

<div id="kat_bl">

<div id="kat_ris" align="center">[%IF data.img_cat%]
<a href="/catalog/[%data.idr%]/[%data.id%].html" title="[%data.name%]"><img src="/base/cat_image/[%data.id%]-s.[%data.img_end%]" border="0"></a>
[%END%]
</div>
<div id="katalog_text">[%data.name%]</div>

</div>

[%END%]
</div>
<table width="100%"><tr><td></td></tr></table>
[%perehod%]

[%END%]


[%IF a == 'full'%]
</style>

<script src="/javascripts/prototype.js" type="text/javascript"></script>
<script src="/javascripts/scriptaculous.js?load=effects" type="text/javascript"></script>

<script type="text/javascript" src="/javascripts/lightbox.js"></script>
<link rel="stylesheet" href="/javascripts/lightbox.css" type="text/css" media="screen" />

[%IF  mess == 'error_field'%]<b style="color:red">Поля, помеченные знаком *, обязательны для заполненя!</b>[%END%]
[%IF  mess == 'ok'%]<b style="color:green">Спасибо! Ваша заявка принята. Менеджер свяжется с вами в ближайшее время!</b>[%END%]
<h1 align="center">[%data.name%]</h1>

<div id="katalog" style="margin-left:10px;">

<div id="tovar_ris" style="margin-right:20px;">
<div style="float:left;margin-right:25px">[%IF img_cat%]<a href="/base/cat_image/[%data.id%].[%data.img_end%]" title="[%data.name%]" rel="lightbox[roadtrip]"><img src="/base/cat_image/[%data.id%]-m.[%data.img_end%]" border="0" align="left" class="img_cat"></a> [%END%]
<div id="tovar_cena" align="center" style="padding:10px;">[%data.cost||"<small>звоните, чтобы уточнить стоимость</small>"%] [%IF data.cost%]руб.[%END%]</div>
</div>
<div id="tovar_info">[%IF data.articul%]<div id="tovar_cena">[%data.articul%]</div>[%END%]
[%data.opis%]<br /><br /><br /><p align="right"><a href="/catalog/[%id%].html">Другие товары</a></p>
</div>
</div>


<!--a name="zakaz"></a>
<h3>Форма заказа</h3>
[%IF cook.users_cook.value%]
<form action="/catalog/[%id%]/[%id_cat%].html" method=post name="form_zakaz">
 <table>
   <tr>
    <td class="td123">Кол-во*:</td><td><input name=col value="[%col%]" id="col"></td>
   </tr>
   <tr>
    <td class="td123">Удобный способ оплаты:</td><td><input name=oplata value="[%oplata%]"></td>
   </tr>
   <tr>
    <td valign=top class="td123">Комментарий:</td><td><textarea name=comments cols=34 rows=5>[%comments%]</textarea></td>
   </tr>
   <tr>
    <td colspan=2 align=center><input type=submit value="Отправить заказ"></td>
   </tr>
 </table>
<input type=hidden name=a value="send">
<input type=hidden name=id_cat value="[%id_cat%]">
<input type=hidden name=id value="[%id%]">
</form>
[%ELSE%]
Для того чтобы сделать заказ, Вам необходимо пройти <a href="/users/users.html?a=forma">регистраци</a>.<br><br>Если вы уже зарегистрированы в системе, введите ваш логин и пароль в форме ниже.

[%IF mess=='error'%]<br><br><b style="color:red">Пользователь с такими данеными не зарегистрирован</b>[%END%]
<table>
<form action="/users/users.html" method="post">
<tr>
<td class="td123">Логин:</td> <td><input type="text" name="login"></td>
</tr><tr>
<td class="td123">Пароль:</td> <td><input name="pass" type="password"></td>
</tr>
<tr><td></td><td><input type="submit" value="Войти и продолжить заказ"></td><tr>
<input type="hidden" name="old_referrer" value="[%location%]">
<input type="hidden" name="a" value="auth_user">
</form>		
</table-->
[%END%]
[%END%]


[%IF a == 'form_order'%]
<script>

function OpenClose(name,act){
	var tek = document.getElementById(name).style.display;
	if(tek == 'block' || act == 'close'){
		document.getElementById(name).style.display='none';
	}
	if(tek == 'none' || act== 'open'){
		document.getElementById(name).style.display='block';
	}
}

</script>
<style>
.hdiv {
display:none;
position:absolute; 
}
</style>
[%IF cook.users_cook.value%]
<form action="/catalog/prod_milk.html" method=post name="form_zakaz">
<table cellspacing="0">
[%inc=0%]
[%FOREACH data_r IN ar_r %]
<tr><td class=td123><b><a href="#" onclick="OpenClose('cat[%inc%]','');return false;">+</a> [%data_r.name%]</b></td></tr>
<tr><td>
<table width="100%" cellspacing="0" cellpadding="2" id="cat[%inc%]" style="display:none;position:relative">
<tr>
    <td class="td123"><b>Наименование</b></td>
    <td class="td123"><b>Штрих код<b></td>
    <td class="td123"><b>ГОСТ<b></td>
    <td class="td123"><b>Кол-во<b></td>
</tr>
[%FOREACH data IN data_r.data %]
        <tr>
	    <td style="border-bottom:solid 1px" class=td123><a href="/catalog/[%data.1%]/[%data.0%].html"><b>[%data.2%]</b></a></td>
	    <td style="border-bottom:solid 1px;border-right:solid 1px;" class=td123>[%data.14||"&nbsp;"%]</td> 
	    <td style="border-bottom:solid 1px" class=td123>[%data.15||"&nbsp;"%]</td> 
	    <td style="border-bottom:solid 1px" width="7" class=td123><input name="col_[%data.0%]" value="0" size=1> </td>
	</tr>
[%END%]
</table>
</td></tr>
<tr><td>&nbsp;</td></tr>
[%inc=inc+1%]
[%END%]
</table>
 <table>
   <tr>
    <td class=td123>Удобный способ оплаты:</td><td><input name=oplata value="[%oplata%]"></td>
   </tr>
   <tr>
    <td valign=top class=td123>Комментарий:</td><td><textarea name=comments cols=34 rows=5>[%comments%]</textarea></td>
   </tr>
   <tr>
    <td colspan=2 align=center><input type=submit value="Отправить заказ"></td>
   </tr>
 </table>
<input type=hidden name=a value="send_order">
</form>
[%ELSE%]
Для того чтобы сделать заказ, Вам необходимо пройти <a href="/users/users.html?a=forma">регистраци</a>.<br><br>Если вы уже зарегистрированы в системе, введите ваш логин и пароль в форме ниже.

[%IF mess=='error'%]<br><br><b style="color:red">Пользователь с такими данеными не зарегистрирован</b>[%END%]
<table>
<form action="/users/users.html" method="post">
<tr>
<td class=td123>Логин:</td> <td><input type="text" name="login"></td>
</tr><tr>
<td class=td123>Пароль:</td> <td><input name="pass" type="password"></td>
</tr>
<tr><td></td><td><input type="submit" value="Войти и продолжить заказ"></td><tr>
<input type="hidden" name="old_referrer" value="[%location%]">
<input type="hidden" name="a" value="auth_user">
</form>		
</table>
[%END%]

[%END%]

[%IF a == 'send_order'%]
Ваша заявка принята! Мы свяжемся с вами в ближайшее время!
[%END%]
