[%IF a=="" %]
    <table width="100%" border="0" cellspacing="2" cellpadding="2">

[%FOREACH data IN ar_data %]

      <tr>
        <td class="news-date">[%data.data_print%]</td>
        <td width="743" class="news-zag">[%data.subject%]</td>
      </tr>
      <tr>
        <td colspan="2" class="news-text">
        [%data.record%]<br>
	 <small>�����������: [%data.name%]</small>
	</td>
     </tr>
[%IF data.answer%]
      <tr>
	<td>&nbsp;</td>
        <td class="news-text">
        [%data.answer%]
	 <p align="right">�������������</p>
	</td>
     </tr>
[%END%]

[%END%]

    </table>

[%perehod%]
<br><br>
<b>�������� ������</b>
<TABLE align=center border=0><FORM ACTION="/cgi-bin/view/guest.cgi" method=post>
<TR><TD width=100><b>���� ���*:</b></TD><TD width=250><INPUT TYPE=TEXT NAME=name style="width:150" value="[%name%]"></TD></TR>
<TR><TD width=100><b>��� E-mail*:</b></TD><TD width=250><INPUT TYPE=TEXT NAME=email style="width:150" value="[%email%]"></TD></TR>
<TR><TD width=100><b>����/���������*:</b></TD><TD width=250><INPUT TYPE=TEXT NAME=subject style="width:150" value="[%subject%]"></TD></TR>
<TR><TD colspan=2><b>�����*:</b></TD></TR>
<TR><TD colspan=2><TEXTAREA NAME=record rows=5 cols=35 style="width:250">[%record%]</TEXTAREA></TD></TR>
<tr><td colspan="2"><b>������� �����</b><input type=text name=pass value="">[%INSERT captcha.html%]</td></tr>
<INPUT TYPE=HIDDEN name=id value="[%id%]">
<INPUT TYPE=HIDDEN name=a value="insert">
<TR><TD align=center><input type=submit value="���������"></TD>
<TD align=center><input type=reset value="��������"></TD></TR>
</TABLE> </form>

[%END%]
