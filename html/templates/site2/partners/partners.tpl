[%IF a == ''%]

<table width="100%" cellpadding="10">

[%FOREACH data IN ar_data %]
<tr><td valign="top" width="10%">[%IF data.typef%]<a href="/partners/[%data.idr%]/[%data.id%].html"><img align="left" src="/upload/partners_photo/[%data.id%].[%data.typef%]"></a>[%END%]</td><td valign="top" width="90%">
[%data.short%]
<a class="dop" href="/partners/[%data.idr%]/[%data.id%].html">Подробнее</a>
</td></tr>
[%END%]
</table>

[%IF perehod%]
<table width="100%">
<tr><td align="center">
Страницы: [%perehod%]
</td></tr></table>
[%END%]

[%END%]

[%IF a == 'full'%]
<h1>[%ref_data.name%]</h1>

<table width="100%" cellpadding="10">
<tr><td valign="top" width="10%">[%IF ref_data.typef%][%IF ref_data.link%]<a class="dop" href="http://[%ref_data.link%]">[%END%]<img align="left" src="/upload/partners_photo/[%ref_data.id%].[%ref_data.typef%]">[%IF ref_data.link%]</a>[%END%][%END%]

</td><td valign="top" width="90%">
[%ref_data.opis%]

[%IF ref_data.link%]Обязательно зайдите на сайт: <a class="dop" href="http://[%ref_data.link%]">[%ref_data.link%]</a>[%END%]
</td></tr>
</table>
<p align="right"><a href="/partners/[%ref_data.idr%].html">Партнеры</a></p>
[%END%]