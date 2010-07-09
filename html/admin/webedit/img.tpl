<HTML>
<TITLE>{$TITLE}</TITLE>
<HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
<LINK href="http://{$ADMIN_CSS}" rel=styleSheet type=text/css>
<script language="JavaScript1.2" src="http://{$ADMIN_JS}"></script>
{literal}

{/literal}
</HEAD>
<body bgcolor="#F6F6F6" text="#000000" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
{if $ToDo == "ModifyImage"}
{literal}
<script language=javascript>


var myPage = window.opener;

window.onload = setValues;

// var cellBgColor = myTable.selectedTD.bgColor;
var imageWidth = myPage.selectedImage.width;
var imageHeight = myPage.selectedImage.height;
var imageAlign = myPage.selectedImage.align;
var imageBorder = myPage.selectedImage.border;
var imageAltTag = myPage.selectedImage.alt;
var imageHspace = myPage.selectedImage.hspace;
var imageVspace = myPage.selectedImage.vspace;

function setValues() {

	imageForm.image_width.value = imageWidth;
	imageForm.image_height.value = imageHeight;

	if (imageBorder == "") {
		imageBorder = "0"
	}

	imageForm.border.value = imageBorder;
	imageForm.alt_tag.value = imageAltTag;
	imageForm.hspace.value = imageHspace;
	imageForm.vspace.value = imageVspace;
	// tableForm.cell_width.value = cellWidth;
	this.focus();
}

function doModify() {

	var error = 0;
	if (isNaN(imageForm.image_width.value) || imageForm.image_width.value < 0) {
		alert("Image Width must contain a valid, positive number")
		error = 1
		imageForm.image_width.select()
		imageForm.image_width.focus()
	} else if (isNaN(imageForm.image_height.value) || imageForm.image_height.value < 0) {
		alert("Image Height must contain a valid, positive number")
		error = 1
		imageForm.image_height.select()
		imageForm.image_height.focus()
	} else if (isNaN(imageForm.border.value) || imageForm.border.value < 0 || imageForm.border.value == "") {
		alert("Image Border must contain a valid, positive number")
		error = 1
		imageForm.border.select()
		imageForm.border.focus()
	} else if (isNaN(imageForm.hspace.value) || imageForm.hspace.value < 0) {
		alert("Horizontal Spacing must contain a valid, positive number")
		error = 1
		imageForm.hspace.select()
		imageForm.hspace.focus()
	} else if (isNaN(imageForm.vspace.value) || imageForm.vspace.value < 0) {
		alert("Vertical Spacing must contain a valid, positive number")
		error = 1
		imageForm.vspace.select()
		imageForm.vspace.focus()
	}

	if (error != 1) {
        	myPage.selectedImage.width = imageForm.image_width.value
			myPage.selectedImage.height = imageForm.image_height.value
			myPage.selectedImage.alt = imageForm.alt_tag.value
			myPage.selectedImage.border = imageForm.border.value
    
	if (imageForm.hspace.value != "") {
			myPage.selectedImage.hspace = imageForm.hspace.value
	} else {
			myPage.selectedImage.removeAttribute('hspace',0)
	}

	if (imageForm.vspace.value != "") {
			myPage.selectedImage.vspace = imageForm.vspace.value
	} else {
			myPage.selectedImage.removeAttribute('vspace',0)
	}

	if (imageForm.align[imageForm.align.selectedIndex].text != "None") {
       		myPage.selectedImage.align = imageForm.align[imageForm.align.selectedIndex].text
	} else {
       		myPage.selectedImage.removeAttribute('align',0)
	}
        
    window.close()
	}
}

function printAlign() {
	if ((imageAlign != undefined) && (imageAlign != "")) {
		document.write('<option selected>' + imageAlign)
		document.write('<option>None')
	} else {
		document.write('<option selected>None')
	}
}

function printvAlign() {
	if ((imagevAlign != undefined) && (imagevAlign != "")) {
		document.write('<option selected>' + imagevAlign)
		document.write('<option>None')
	} else {
		document.write('<option selected>None')
	}
}

document.onkeydown = function () { 
			if (event.keyCode == 13) {	// ENTER
				doModify()			
			}
}

document.onkeypress = onkeyup = function () { 				
	if (event.keyCode == 13) {	// ENTER
	event.cancelBubble = true;
	event.returnValue = false;
	return false;				
	}
};

</script>
{/literal}
<form name=imageForm>
<table width="100%" border="0" cellspacing="0" cellpadding="0">
   <tr>
	<td>&nbsp;</td>
	<td class="body">&nbsp;</td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	<td class="body">
	  <table width="98%" border="0" cellspacing="0" cellpadding="0" >
  		<tr>
		    <td class="heading1">&nbsp;&nbsp;Изменить данные изображения</td>
		</tr>
	  </table>
	</td>
  </tr>
  <tr>
	<td colspan="2"><img src="webedit_images/1x1.gif" width="1" height="10"></td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	<td class="body">  
		<table border="0" cellspacing="0" cellpadding="5" width="98%" class="bevel2">
		  <tr>
		    <td class="body" width="80">Alternate Text:</td>
			<td class="body" colspan="3">
			  <input type="text" name="alt_tag" size="50" class="Text220">
			</td>
		  </tr>
		  <tr>
			<td class="body" width="80">Image Width:</td>
			<td class="body">
			  <input type="text" name="image_width" size="3" class="Text50" maxlength="3">
		  </td>
			<td class="body" width="80">Image Height:</td>
			<td class="body">
			  <input type="text" name="image_height" size="3" class="Text50" maxlength="3">
			</td>
		  </tr>
		  <tr>
			<td class="body" width="80">Alignment:</td>
			<td class="body">
			  <SELECT class=text70 name=align>
			    <script>printAlign()</script>
			    <option>Baseline
			    <option>Top
			    <option>Middle
			    <option>Bottom
			    <option>TextTop
			    <option>ABSMiddle
			    <option>ABSBottom
			    <option>Left
			    <option>Right</option>
			  </select>
		  </td>
			<td class="body" width="80">Border:</td>
			<td class="body">
			  <input type="text" name="border" size="3" class="Text50" maxlength="3">
			</td>
		  </tr>
		  <tr>
			<td class="body" width="80">Horizontal Spacing:</td>
			<td class="body">
			  <input type="text" name="hspace" size="3" class="Text50" maxlength="3">
			</td>
			<td class="body" width="80">Vertical Spacing:</td>
			<td class="body">
			  <input type="text" name="vspace" size="3" class="Text50" maxlength="3">
			</td>
		  </tr>
		  
	    </table>
	</td>
  </tr>
  <tr>
	<td colspan="2"><img src="webedit_images/1x1.gif" width="1" height="10"></td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	<td>
	    <input type="button" name="modifyImage" value="Изменить" class="Text90" onClick="javascript:doModify();">
	<input type="button" name="Submit" value="Отмена" class="Text50" onClick="javascript:window.close()">
	</td>
  </tr>
</table>
</form>
{/if}

{if $ToDo == "InsertImage"}
{literal}
<script language=javascript>
function swEl(id)
{
	eval("obj = document.getElementById('"+id+"');");
	if(obj.style.display=='none') 
	{
		obj.style.display='block';
	}
	else 
	{
		obj.style.display='none';
	}
}

var myPage = window.opener;
function addLinkImg()
{  var image;
    image=document.imageLinkForm.link.value;
	myPage.selectImage(image);
	self.close();
} 
function SelectImage(ImageName) {
		window.opener.selectImage("{/literal}{$IMG_PATH_OUT}{literal}" + ImageName);
		self.close();
}

function SelectFile(FileName,size,ext) {
		window.opener.selectFile("{/literal}{$IMG_PATH_OUT}{literal}" + FileName,size,ext);
		self.close();
}
this.focus();
</script>
{/literal}

<table width="100%" border="0" cellspacing="4" cellpadding="4">
<tr align=center>
			<td>
				<a href='#1' class=bodylink  onclick="swEl('ul1')" >Добавить ссылку на изображение </a><img src="http://{$IMG_HTTP_ADMIN}button_blue_down.gif"  border="0" alt="">
			</td>
			<td>
				<a href='#2' class=bodylink  onclick="swEl('ul2')" >Добавить изображение или файл  </a><img src="http://{$IMG_HTTP_ADMIN}button_blue_down.gif"  border="0" alt="">
			</td>
			<td>
				<a href='#3' class=bodylink  onclick="swEl('ul3')" >Создать новую директорию </a><img src="http://{$IMG_HTTP_ADMIN}button_blue_down.gif"  border="0" alt="">
					<input type=hidden name=newdir value="">
			</td>
		</tr>
</table>

<div id=ul1 style="display:none;">
<form name=imageLinkForm>
    <table width="98%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
    <td>&nbsp;</td>
  </tr>
   <tr align=center>
   <td   class="body">
    <table width="98%" border="0" cellspacing="0" cellpadding="0" >
  		<tr>
		    <td class="heading1">Ссылка на изображение</td>
		</tr>
	  </table>
	</td>
  </tr>
  <tr align=center>
	<td >&nbsp;</td>
  </tr>
  <tr align=center>
	<td>  
		<table border="0" cellspacing="0" cellpadding="5" width="98%" class="bevel2">
		  <tr>
		    <td class="body" width="80">Ссылка:</td>
			<td class="body" >
			  <input type="text" name="link" size="50" class="Text220">
			</td>
		  </tr>
        </table>
    <td>
	</tr>
	<tr>
	<td>
	<br>
	 &nbsp;&nbsp;<input type="button"  value="Добавить ссылку" class="inp2" onClick="javascript:addLinkImg();">

	 &nbsp;<input type="button" name="Submit" value="Отмена" class="inp2" onClick="javascript:window.close()">
	</td>
	</tr>
	</table>
	</form>
</div>
<div id=ul2 style="display:none;">
<form name=imageAddForm method=post action="?ToDo=AddImage&dir={$DIR}" ENCTYPE=multipart/form-data>
    <table width="98%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
        <td > 
          <table width="98%" border="0" align="center" cellpadding="0" cellspacing="0">
            <tr>
              <td class="heading1">Добавить изображение или файл: </td>
            </tr>
            <tr>
              <td>&nbsp;</td>
            </tr>
          </table></td>
  </tr>
   <tr align=center>
   <td   class="body">
    <table width="98%" border="0" cellspacing="0" cellpadding="0" class="bevel1">
  		<tr>
		      <td class="titlecol2">&nbsp;&nbsp;(доп. форматы: {foreach from=$ext_array item=ext 
                key=key} {$key}, {/foreach})</td>
		</tr>
	  </table>
	</td>
  </tr>
  <tr align=center>
	<td >&nbsp;</td>
  </tr>
  <tr align=center>
	<td>  
		<table border="0" cellspacing="0" cellpadding="5" width="98%" class="bevel2">
		  <tr>
		    <td class="body" width="170">Изображение или файл:</td>
			<td class="body" >
			  <input type="file" name="img" size="50" class="Text220">
			</td>
		  </tr>
        </table>
    <td>
	</tr>
	<tr>
	<td>
	<br>
	 &nbsp;&nbsp;<input type="submit"  value="Добавить" class="inp2">
	 &nbsp;<input type="button" name="Submit" value="Отмена" class="inp2" onClick="javascript:window.close()">
	</td>
	</tr>
	</table>
	</form>
</div>
<div id=ul3 style="display:none;">
<form method="post" action='?ToDo=CreateNewFolder&dir={$DIR}'>
    <table width="98%" border="0" align="center" cellpadding="0" cellspacing="0">
      <tr>
	<td>&nbsp;</td>
	<td class="body">&nbsp;</td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	<td class="body">
	  <table width="100%" border="0" cellspacing="0" cellpadding="0" >
  		<tr>
		      <td  class="heading1">Создать новую директорию</td>
		</tr>
	  </table>
	</td>
  </tr>
  <tr>
	<td colspan="2">&nbsp;</td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	<td class="body">
    	  <table border="0" cellspacing="0" cellpadding="5" width="98%" class="bevel2">
		<tr>
		  <td class="body" width="200">Название новой директории:</td>
		  <td class="body">
			<input type=text name="newfoldername" class="Text220" >
		  </td>
		</tr>
	  </table>
	</td>
  </tr>
  <tr>
	<td colspan="2">&nbsp;</td>
  </tr>
  <tr>
	<td>&nbsp;</td>
	    <td> 
          <input type="submit" name="Submit" value="Создать" class="inp2">
	    &nbsp;<input type="button" name="Submit" value="Отмена" class="inp2" onClick="javascript:window.close()">
	</td>
  </tr>
</table>
</form>
</div>
{if $action_show_dir == 'open'}
	<br>
	<br>
	
<table border="0" cellspacing="1" cellpadding="0" width="98%" align=center>
  <tr bgcolor="#CCCCCC"> 
    <td width=30 height="25" >&nbsp;</td>
		
    <td width=27% align="center" class=text60>Имя файла</td>
		
    <td width=19% align="center" class=text60>Размер файла(bytes)</td>
		
    <td width=20% align="center" class=text60>Последнее изменение</td>
		
    <td width=30% colspan=3 align="center" class=text60>Действия</td>
	</tr>
	{foreach from=$name_dir item=dir key=key}
	<tr valign=top onMouseover="this.runtimeStyle.background ='#DDDDDD';" onMouseout="this.runtimeStyle.cssText ='';" class=fm2>
		<td width=20><img src='http://{$IMG_HTTP_ADMIN}icon_folder.gif' width=16 height=16></td>
		<td class=body>&nbsp;<a class=bodylink  href='?ToDo=InsertImage&dir={$current_dir}{$dir.file_name}'>{$dir.file_name}</a>
		<div id=ul{$key} style="display:none;" >
		<table  border="0" cellspacing="0" cellpadding="0">
			<form action='?ToDo=RenameDir&dir={$current_dir_if_del}' method=post>
			<INPUT TYPE="hidden" name='olddir'  value='{$dir.file_name}'>
			<tr>
				<td><INPUT TYPE="text" NAME="newdir" size=10 value='{$dir.file_name}'></td>
				<td>&nbsp;&nbsp;<INPUT  class=inp2 TYPE="submit" value='Rename'></td>
			</tr></form>
		</table>
		</div>
		</td>
		<td class=body>{$dir.file_size}</td>
		<td class=body>&nbsp;</td>
		<td><a href='#{$key}' class=bodylink  onclick="swEl('ul{$key}')" >Изменить</a></td>
		<td><a class=bodylink  href="?ToDo=DelDir&dir={$current_dir_if_del}&dirdel={$current_dir}{$dir.file_name}" onclick="return confirmLink(this,'dir')" title="Delete folder">Удалить</a></td>
	</tr>
	{/foreach}
</table>
{/if}




<table width="100%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td>&nbsp;</td>
  </tr>
   <tr align=center>
   <td   class="body">
    <table width="98%" border="0" cellspacing="0" cellpadding="0" class="bevel1">
  		<tr Valign=top>
		<form  method=GET>
		   <INPUT TYPE="hidden" name="ToDo" value='InsertImage'>
		    <td  class="titlecol2">&nbsp;&nbsp;Изображения и файлы №  /{$DIR}/ &nbsp;&nbsp;
			{if $action_dir == "open"}
				<select name=dir onchange=submit()>
				 <option value="">./
				 {$DIR_}
				</select>
			{/if}
			</td>
		 </form>
		</tr>
	  </table>
	</td>
  </tr>
  <tr align=center>
	<td >&nbsp;<div class=mess>{$erroe_format}</div><p></td>
  </tr>
  <tr align=center>
	<td>  
		<table border="0" cellspacing="0" cellpadding="5" width="98%" class="bevel2">
        {foreach from=$imgs item=img key=key}
		 {$img.tr_start}
		  <td {$img.colspan}>
		       <table border=0 cellspacing=1 cellpadding=1 width=100%>
				<tr>
					<td colspan=2 class=body>{if $img.ext_img != ""}<font color=blue>Файл:</font>{else}<font color=green>Изо:</font>{/if}&nbsp;<u>{$img.file_name}</u></td>
				</tr>
				<tr>
                {if $img.ext_img != ""}
				<td width=50><img border=1 src='{$img.ext_img}' width=90 height=90>&nbsp;</td>
                {else}
				<td width=50><img border=1 src='{$img.path}{$img.file_name}' width=90 height=90>&nbsp;</td>
				{/if}
				<td width=200>
				{if $img.ext_img != ""}
				  <a href=javascript:SelectFile("{$img.file_name}","{$img.file_sizeKb}","{$img.ext}") class=bodylink title="Insert image: '{$img.file_name}' into your page"><b>Insert</b></a>
				{else}
				<a href=javascript:SelectImage("{$img.file_name}") class=bodylink title="Insert image: '{$img.file_name}' into your page"><b>Insert</b></a>
				{/if}
				<br>
				<a href='?dir={$DIR}&ToDo=DelImage&file_name={$img.file_name}' class=bodylink title="Delete image: '{$img.file_name}'">Delete</a></td></tr><tr><td colspan=2 class=body><font color=red>Размер: </font>{$img.file_size} byte</td>
				</tr>
			</table>
		  </td>
		  {$img.tr}
        {/foreach}
        </table>
    <td>
	</tr>
</table>
<div class=mess>{$mess}</div>
{/if}

</body>
</html>