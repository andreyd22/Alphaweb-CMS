<HTML>
  <HEAD>
    <TITLE>
      Сортировка разделов [%name_action%]
    </TITLE>
   <script type="text/javascript" src="/admin/scripts.js"></script>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css">
  </HEAD>
  <BODY bgcolor="#F5F5F5">
    <TABLE width="100%" border="0" cellpadding="0" cellspacing="0">

<tr><td>
                            <TABLE cellpadding="2" cellspacing="0" border="0" width="100%">
                              <TR>
                                <TD bgcolor="#ffffff" class="smallbl" align="left">
                                  <DIV class="smallbl">
                                                                           <tr>
   <td>
  <table cellspacing=0 width=100%>
  <tr><td class=td_y></td><td class=td_ygol_r>&nbsp;&nbsp;<b class=y>МЕНЮ</b> <b>ПОЛЬЗОВАТЕЛЯ</b></td></tr>

  </table>
  </td>
  </tr>
  <tr>
  <td class=td_simple>
<table width=100%>
<tr><td>
Здравствуйте, Администратор <br>
Домен: <b>[%host_name%]</b> (<b><a href="http://[%host_name%]" target=_blank>Просмотр сайта</a></b>)<br>

     <table align=center width=100% cellspacing=0 cellpadding=0>
     <tr>
        <td colspan=5>
            <table width="1%" bgcolor="blue" border=0>
            <tr><td style='font-size:1px;'>&nbsp;</td></tr>
            </table>
        </td></tr>

        <tr>
        <td align=center style="font-size:4px;">|</td>
        <td align=center style="font-size:4px;" width=50%></td>
        <td align=center style="font-size:4px;">|</td>
        <td align=center style="font-size:4px;" width=50%></td>
        <td align=center style="font-size:4px;">|</td>
        </tr>

        <tr>
        <td>0%</td>
        <td width=50%></td>
        <td>50%</td>
        <td width=50%></td>
        <td>100%</td>
        </tr>

     </table>
</td></tr>
<tr>
<td><ul>
<li><a href="/cgi-bin/mod/auth.cgi?sid=1213865429&l=1" target=_top>Вход в конструктор</a><br>
<li><a href="/cgi-bin/mod/file_viewer.pl?sid=1213865429&l=1">Загрузка файлов</a><br>
<li><a href="/cgi-bin/mod/about.cgi?sid=1213865429&l=1">Помощь</a><br>
<li><a href="/index.html" target=_top>Главная страница</a><br>
</ul>
</td>

</tr>
<tr><td align=right><a href="/cgi-bin/view.pl?a=logout" title="Выход из системы" target=_top>[logout]</a></td></tr>
</table>
  </td>
  </tr>

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
         <TD bgcolor="#ffffff" class="miniwh" align="center">
                                  <DIV class="smallbl">

                                  <!--Вывод дерева разделов с последующей сортировкой -->
<table width=100%> <tr><td>
<br>
</td></tr>
<tr><td>
<form action='/cgi-bin/mod/razdels.cgi' method=post>
<input type='submit' value='Поменять сортировку'>
<table width=100%>

<tr>
<!--Вывод всех ссылок в меню конструктора админ-->
<tr bgcolor=#EFEFEF>
<td nowrap>
<table cellspacing=0 cellpadding=0>
<tr>

<td width=1 nowrap>&nbsp;</td><td>-<a href="/cgi-bin/mod/document.cgi?sid=1213865429&id=main&l=1" class=link1 target=main>Главная</a></td>
</tr>
</table>
</td><!--Ссылка на редактирование информации модуля-->
<!--td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=main&position=" title='Вверх' target=main><img src="/img/icons/icon_moveup.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=main&position=" title='Вниз' target=main><img src="/img/icons/icon_movedown.gif" border=0></a></td-->
<td width=30 align=center><input style='width:30px' type='text' name=sort_id value='1'><input type='hidden' name=sort_id_id value='main'></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=view_sort&id=main" title='Поменять родительский раздел' target=main><img src="/img/icons/icon_acls.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&idp=main" title='Добавить подраздел' target=main><img src="/img/icons/icon_add.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&id=main" title='Свойства раздела' target=main><img src="/img/icons/icon_properties.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=del&id=main" title='Удалить раздел' onclick="return Delete(2,'Главная');" target=main><img src="/img/icons/delete.gif" border=0></a></td>
</tr>
<!--Вывод всех ссылок в меню конструктора админ-->
<!--Вывод всех ссылок в меню конструктора админ-->
<tr bgcolor=#EFEFEF>
<td nowrap>

<table cellspacing=0 cellpadding=0>
<tr>
<td width=11 nowrap>&nbsp;</td><td>-<a href="/cgi-bin/mod/document.cgi?sid=1213865429&id=about&l=1" class=link2 target=main>О компании</a></td>
</tr>
</table>
</td><!--Ссылка на редактирование информации модуля-->
<!--td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=about&position=" title='Вверх' target=main><img src="/img/icons/icon_moveup.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=about&position=" title='Вниз' target=main><img src="/img/icons/icon_movedown.gif" border=0></a></td-->
<td width=30 align=center><input style='width:30px' type='text' name=sort_id value='1'><input type='hidden' name=sort_id_id value='about'></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=view_sort&id=about" title='Поменять родительский раздел' target=main><img src="/img/icons/icon_acls.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&idp=about" title='Добавить подраздел' target=main><img src="/img/icons/icon_add.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&id=about" title='Свойства раздела' target=main><img src="/img/icons/icon_properties.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=del&id=about" title='Удалить раздел' onclick="return Delete(2,'О компании');" target=main><img src="/img/icons/delete.gif" border=0></a></td>
</tr>
<!--Вывод всех ссылок в меню конструктора админ-->
<!--Вывод всех ссылок в меню конструктора админ-->

<tr bgcolor=#EFEFEF>
<td nowrap>
<table cellspacing=0 cellpadding=0>
<tr>
<td width=11 nowrap>&nbsp;</td><td>-<a href="/cgi-bin/mod/news.cgi?sid=1213865429&id=news_our&l=1" class=link2 target=main>Новости</a></td>
</tr>
</table>
</td><!--Ссылка на редактирование информации модуля-->
<!--td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=news_our&position=" title='Вверх' target=main><img src="/img/icons/icon_moveup.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=sort&id=news_our&position=" title='Вниз' target=main><img src="/img/icons/icon_movedown.gif" border=0></a></td-->
<td width=30 align=center><input style='width:30px' type='text' name=sort_id value='2'><input type='hidden' name=sort_id_id value='news_our'></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=view_sort&id=news_our" title='Поменять родительский раздел' target=main><img src="/img/icons/icon_acls.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&idp=news_our" title='Добавить подраздел' target=main><img src="/img/icons/icon_add.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=add&id=news_our" title='Свойства раздела' target=main><img src="/img/icons/icon_properties.gif" border=0></a></td>
<td width=30 align=center><a href="/cgi-bin/mod/razdels.cgi?sid=1213865429&l=1&a=del&id=news_our" title='Удалить раздел' onclick="return Delete(2,'Новости');" target=main><img src="/img/icons/delete.gif" border=0></a></td>
</tr>

<!--Вывод всех ссылок в меню конструктора админ-->

</tr>
<input type=hidden name=l value='1'>
<input type=hidden name=sid value='1213865429'>
<input type=hidden name=a value='change_sort'>
</table>
<input type='submit' value='Поменять сортировку'>
</td></tr>
</table>
</form>

<!--Вывод дерева разделов с последующей сортировкой -->

                                  </DIV>
                                </TD>

                              </TR>

          <TR>
        <TD height="4" class="minibl" align="center"><iframe src="http://alphaweb.ru/cgi-bin/copyright.cgi" width="100%" scrolling="no" frameborder="0" align="center" hspace="0" vspace="0" marginheight="0" marginwidth="0"></iframe></TD>
      </TR>
    </TABLE>
  </BODY>
</HTML>

