[%BLOCK begin_main_block%]
<table border="0" cellspacing="10" cellpadding="10">
[%END%]
[%BLOCK end_main_block%]
</table>
[%END%]

[%BLOCK begin_row_block%]
<tr>
[%END%]
[%BLOCK end_row_block%]
</tr>
[%END%]

[%BLOCK begin_col_block%]
<td align="left" valign="top">
[%END%]
[%BLOCK end_col_block-%]
</td>
[%END%]

[%BLOCK block_content-%]
<!-- Начало блока заполнения -->
[%ret_data=get_hash(data.$idx.params)%]
   <img alt="[%data.$idx.short%]" src="/base/cat_image/[%data.$idx.id%]-150.jpg" border=0  width="100" height="100"></td>
   <td valign="top"><h5>[%data.$idx.short%]</h5>
   [%IF data.$idx.opis%]<span><a href="/cat_show_det/msv_ohl/[%data.$idx.id%]">Подробно...</a></span>[%END%]
   <h4>[%data.$idx.cost%]&nbsp;[%ret_data.curency%].&nbsp;[%data.$idx.mera%].</h4>   	  
<!-- Конец блока заполнения -->
[%idx=idx + 1%]
[%END%]

[%PROCESS begin_main_block%]
[%idx=0%]
  [%FOREACH col=[1..tot_col]%]
  [%IF !data.$idx%]
	<!--[%PROCESS end_main_block%]-->
	[%LAST%]
  [%END%]  	
    [%PROCESS begin_row_block%]
	[%FOREACH row=[1..tot_row]%]
		[%PROCESS begin_col_block%]
    	  	[%PROCESS block_content%]
		[%PROCESS end_col_block%]
    	[%END%]
    [%PROCESS end_row_block%]  	
  [%END%]
[%PROCESS end_main_block%]
