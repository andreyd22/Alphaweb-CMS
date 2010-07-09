<HTML>
  <HEAD>
    <TITLE>
      [%name_action%] AlphaWeb CMS
    </TITLE>
   <script type="text/javascript" src="/admin/scripts.js"></script>
  <LINK rel="stylesheet" type="text/css" href="/admin/style.css?t=[%time%]">
  </HEAD>
  <BODY bgcolor="#F5F5F5">
    <TABLE width="100%" border="0" cellpadding="0" cellspacing="0" height="100%">

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
<li><a href="/cgi-bin/mod/auth.cgi?sid=[%time%]&l=1" target=_top>Вход в конструктор</a><br>
<li><a href="/cgi-bin/mod/file_viewer.pl?sid=[%time%]&l=1">Загрузка файлов</a><br>
<li><a href="/cgi-bin/mod/about.cgi?sid=[%time%]&l=1">Помощь</a><br>
<li><a href="/index.html" target=_top>Главная страница</a><br>
</ul>
</td>

</tr>
<tr><td align=right><a href="/cgi-bin/view.pl?a=logout&t=[%time%]" title="Выход из системы" target=_top>[logout]</a></td></tr>
</table>
  </td>
  </tr>

                                  </DIV>
                                </TD>
                              </TR>
                              <TR>

                                <TD bgcolor="#e2e2e2" align="left" class="bl">
                                  &nbsp;<b>[%name_action%]</b>
                                </TD>
                                                          </TR>
                            </TABLE>
</td></tr>
      <TR>
         <TD bgcolor="#ffffff" class="miniwh" height="100%" valign="top">
<table width="100%" height="100%"><tr><td>&nbsp;</td><td height="100%" valign="top">
                                  <DIV class="smallbl">

<!--Вывод дерева разделов с последующей сортировкой -->
[%PROCESS $tpl_%]
<!--Вывод дерева разделов с последующей сортировкой -->
</td></tr></table>

                                  </DIV>
                                </TD>

                              </TR>

          <TR>
        <TD height="4" class="minibl" align="center"><iframe src="http://alphaweb.ru/cgi-bin/copyright.cgi" width="100%" scrolling="no" frameborder="0" align="center" hspace="0" vspace="0" marginheight="0" marginwidth="0"></iframe></TD>
      </TR>
    </TABLE>
  </BODY>
</HTML>

