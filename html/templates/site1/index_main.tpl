<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
<title>[%IF data.name%][%data.name%] | [%END%][%IF zag||name_zag_site%][%zag||name_zag_site%] | [%END%] ООО "Мэтр" - производство офисных кресел и офисной мебели, многоместные кресла, метеллическая мебель</title>
<style type="text/css">
<!--
td {
    font-size: 9px;
}
td {
    font-weight: bold;
}
.a {
    font-family: Tahoma;
    font-size: 16px;
    font-weight: bold;
    color: #930;
    text-decoration: none;
    border: none;
}
.a {
    text-align: center;
}
td {
    color: #930;
}
body table tr td table tr td {
    color: #000;
    text-align: center;
    font-size: 10px;
    font-weight: bold;
    font-family: Tahoma, Geneva, sans-serif;
}
td {
}

td {
		font: bold 12px Verdana, Arial, Helvetica, sans-serif;
		line-height: 18px;
}

a:link {
    color: #000;
}
body,td,th {
    color: #000;
}
a:visited {
    color: #000;
}
a:hover {
    color: #069;
}
a:active {
    color: #000;
}
h1 {font-size: 18px;}
-->
</style>

</head>
<body>
<table width="836" height="459" border="0" align="center">
  <tr>
    <td height="143" colspan="3"><table width="822" height="120" border="0">
        <tr>

          <td height="38" colspan="3" align="center"><img src="/images/1.jpg" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="839" height="34" /></td>
        </tr>
        <tr>
          <td width="197" rowspan="3"><img src="/images/meetr1.JPG" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="187" height="49" /></td>
          <td width="354" bgcolor="#FFFFFF">&nbsp;</td>
          <td width="280" bgcolor="#FFFFFF"><img src="/images/tel.JPG" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="279" height="47" /></td>
        </tr>
        <tr>
          <td colspan="2" bgcolor="#FFFFFF">&nbsp;</td>

        </tr>
        <tr>
          <td colspan="2" align="center" bgcolor="#FFFFFF">

[%inc = 0%]
[%FOREACH sub_menu IN main_menu_1('main') %]                                     
[%IF sub_menu.name != "" && sub_menu.visible=='tree1=1,menu1=1'%]
[%inc=inc+1%]
[%IF inc > 1 %] | [%END%]<a href="[%IF sub_menu.link%][%sub_menu.link%][%ELSE%]/[%sub_menu.module%]/[%sub_menu.id%].html[%END%]" title="[%sub_menu.zag%]">[%sub_menu.name%]</a> 
                                                                                       
[%END%]
                                                                                                    
[%END%]
        </tr>
        <tr>
          <td colspan="3" bgcolor="#8AA0B9">&nbsp;</td>
        </tr>
      </table></td>
  </tr>
  <tr>
    <td width="220" valign="top"><table width="213" height="100%" border="0">
      <tr>

        <td height="19" bgcolor="#8AA0B9">&nbsp;</td>
      </tr>
[%FOREACH sub_menu IN main_menu_1('cat') %]                                     
[%IF sub_menu.name != "" && sub_menu.visible=='tree1=1,menu1=1'%]
[%inc=inc+1%]
<tr>
        <td height="22" bgcolor="#EFEFEF"><a href="[%IF sub_menu.link%][%sub_menu.link%][%ELSE%]/[%sub_menu.module%]/[%sub_menu.id%].html[%END%]" title="[%sub_menu.zag%]">[%sub_menu.name%]</a> 
</td></tr>                                                                                       
[%END%]
                                                                                                    
[%END%]

      <tr>
        <td height="32" bgcolor="#FFFFFF"><img src="/images/mol.jpg" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="170" height="268" /></td>
      </tr>

      <tr>

        <td height="100%" bgcolor="#FFFFFF"><a href="http://kc.meetr.ru/" target="_blank"><img style="margin: 30px 0;" src="/images/180x150meetr.gif" border="0" /></a></td>
        </tr>
    </table></td>
    <td width="595" valign="top" align="left">
[%IF a == 'full'%]                                                                                    
<h2 align="right">[%zag||name_zag_site%]</h2>                                                         
[%ELSE%]                                                                                              
<h1 align="left">[%zag||name_zag_site%]</h1>                                                                       
[%END%]                                                                                               

[%is_images_cat%]
[%IF module_name == 'catalog'%]
    [%child_ids = child_ids("$id")%]
    [%IF child_ids != '' %]
	[%FOREACH data IN get_sql("select c.*,s.name as name_r from catalog_ as c, structure as s where s.id=c.idr and idr IN ($child_ids) group by idr")%]
<div id="kat_bl">
<div id="kat_ris"><a href="/catalog/[%data.idr%].html" title="[%data.name%]"><img src="/base/cat_image/[%data.id%]-s.[%data.img_end%]" border="0" align="middle"></a>
</div>
<div id="katalog_text" style="margin-bottom:-1px;">[%data.name_r%]</div>
</div>

	[%END%]
	<div style="clear:both">&nbsp;</div>	
	[%is_image_cat=1%]
    [%END%]
[%END%]

<div style="width:250px;float:left;margin-left:25px;margin-right:25px;margin-top:10px">               
    [%inc=0%]                                                                                         
    [%FOREACH sub_link IN sub_links(id) %]                                                            
[%IF sub_link.name != ""%]                                                                    
    [%inc=inc+1%]                                                                             
[%IF inc>1%]<br> [%END%]<a href="[%IF sub_link.link%][%sub_link.link%][%ELSE%]/[%sub_link.module%]/[%sub_link.id%].html[%END%]">[%sub_link.zag||sub_link.name%]</a>                  
    [%END%]                                                                                   
    [%END%]                                                                                           
    [%IF inc>0%]<p>&nbsp;</p>[%END%]                                                                  
</div>                                                                                                
<div style="clear:both"></div>                                                                                                      

[%IF $tpl_top%]                                                                                       
[%PROCESS $tpl_top%]                                                                                  
[%END%]                                                                                               

[%PROCESS $tpl_%]                                                                                                      

</td>
    <td width="12">&nbsp;</td>
  </tr>
  <tr>
    <td colspan="2"><table width="828" border="0">

      <tr>
        <td width="31" height="22">&nbsp;</td>
        <td width="161">&nbsp;</td>
        <td width="205" align="center" bgcolor="#8AA0B9">ДОСТАВКА</td>
        <td width="96">&nbsp;</td>
        <td width="130">&nbsp;</td>
        <td width="232" bgcolor="#8AA0B9">РЕЖИМ РАБОТЫ</td>
      </tr>

      <tr>
        <td>&nbsp;</td>
        <td><img src="/images/maprussia.gif" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="161" height="94" /></td>
        <td>По Москве и по МО - 500 рублей. От 30000 - бесплатно. Доставка в регионы</td>
        <td>&nbsp;</td>
        <td><img src="/images/118362m.jpg" alt="ООО &quot; МЭТР&quot; - производство офисных кресел и офисной мебели, многоместные кресла, металлическая мебель" width="98" height="94" /></td>
        <td><p>пн-пт</p>
          <p>с8.00 до 19.00</p></td>

      </tr>
      <tr>
        <td colspan="6" bgcolor="#EFEFEF">&nbsp;</td>
        </tr>
    </table></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td colspan="3">&nbsp;</td>

  </tr>
</table>
</body>
</html>
