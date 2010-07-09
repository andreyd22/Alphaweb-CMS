<HTML> 
<TITLE>WebEdit Professional - Point. Click. Edit.</TITLE>
<HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1251">
<link rel="stylesheet" href="webedit.css" type="text/css">
</HEAD>

<body bgcolor="#FFFFFF" text="#000000" leftmargin="0" topmargin="0" marginwidth="0" marginheight="0">
{literal}
<script language=javascript>
	function RemoveLink() {
		if (window.opener.foo.document.selection.type == "Control")
		{
			selectedImage = window.opener.foo.document.selection.createRange()(0);
			selectedImage.width = selectedImage.width
			selectedImage.height = selectedImage.height
		}

		window.opener.foo.document.execCommand("Unlink");
		window.opener.foo.focus();
		self.close();
	}

	function InsertLinkSec(link)
	{
		 document.getElementById("link").value=link;
	} 


	function InsertPopUp()
	{	
		var strLink;
		var error=0;
		var link=document.PopUpForm.link.value;
		var width=document.PopUpForm.width.value;
		var height=document.PopUpForm.height.value;
		var sel=window.opener.foo.document.selection.createRange();
		var selTxt=sel.htmlText;

		if (isNaN(width) || width < 0 || width == "") {
			 	alert("Width must contain a valid, positive number")
				document.PopUpForm.width.select()
				document.PopUpForm.width.focus()
				error = 1
		} else if (isNaN(height) || height < 0 || height == "") {
			 	alert("Height must contain a valid, positive number")
				document.PopUpForm.height.select()
				document.PopUpForm.height.focus()
				error = 1
		}
		else if (link == "") {
			 	alert("Link must contain a valid")
				document.PopUpForm.link.select()
				document.PopUpForm.link.focus()
				error = 1
		}
		if(link != "/")link="/" + link + "/";
		if (error != 1) {
			strLink="<a href='{/literal}{if $name_sec != ""}/{$name_sec}/{else}/{/if}{literal}#' onclick=popUP('" + link + "'," + height + "," + width +",'','') >" + selTxt + "</a>";
			//alert(strLink);
			sel.pasteHTML( strLink );
			self.close();
		}

	} 

</script>
{/literal}
<br><br>
<div align=center class="heading1">POP_UP Manager</div>
<FORM METHOD=POST name=PopUpForm>
	<table width="50%" border="0" cellspacing="2" cellpadding="2" align=center class="bevel2">
	<tr>
	  <td class="body">Высота:</td>
	  <td class="body"><INPUT TYPE="text" NAME="height" size=5 value=100></td>
	</tr>
	<tr>
	  <td class="body">Ширина:</td>
	  <td class="body"><INPUT TYPE="text" NAME="width" size=5 value=100></td>
	</tr>
	<tr>
	  <td class="body">Ссылка на POP_UP раздел:</td>
	  <td class="body"><INPUT id='link' TYPE="text" NAME="link" size=10></td>
	</tr>
	<tr>
	  <td colspan="2" height="10"><img src="webedit_images/1x1.gif" width="1" height="10"></td>
	</tr>
	<tr>
	  <td class="body" colspan=2 align=center>
	       <input type="button" name="insertPopUp" value="Insert Pop_Up" class="Text90" onClick="javascript:InsertPopUp();">&nbsp;
		    <input type="button" name="removeLink" value="Remove Link" class="Text90" onClick="javascript:RemoveLink();">&nbsp;
		   <input type=button name="Cancel" value="Cancel" class="Text70" onClick="javascript:window.close()">
		  </td>
	</tr>
	<tr>
   </table>
  </form>
<br>
{if $action == "show_tree"}
{literal}
<script>

</script>
{/literal}
<table width="96%" border="0" cellspacing="0" cellpadding="0" class="bevel1" align=center>
		  <tr>
			<td>&nbsp;&nbsp;Ссылка на POP_UP раздел</td>
		  </tr>
</table>
<br>
<table border="0" cellspacing="0" cellpadding="5" width="96%" class="bevel2" align=center>
<tr ><td >
 {$tree}
 </td></tr>
</table>
</form>
{/if}

<!-- ВЫВОД СООБЩЕНИЙ -->
<div align=center class=mess>{$MESS}</div>
</body>
</html>