
 function Sure(dir,file,sid) {
  if (confirm("�� �������, ��� ������ ������� ����/����������?\n"+' '+dir+''+file)) {
   return true;  
  }
  else {return false;}
 }


 function Delete(name,target) {
 var text;
 if(name==1){
   text='�� ������� ��� ������ ������� �������:'+target
 }
 if (name==2){
   text='�� �������, ��� ������ ������� ������ '+target+' ?\n��� �������� ������� ��� ����������� ���������� ����� �������';
 }
 if (name==3){
   text='���� �� �������� ��� �������, �� ��� ����������� ���������� ����� ������������� �������\n���� �� ������ ��������� ������ � ������� �� ������� ��� ���!';
 }
 if(name==4){
   text='�� ������� ��� ������ ������� ���������:'+target
 }
 if(name==5){
   text='�� ������� ��� ������ ��������� ��� �������:'+target
 }
  if (confirm(text)) {
   return true;  
  }
  else {return false;}
 }

function paste_img(file,name){
// alert(name);
 opener.document.getElementById(name).value=file;
 window.close();
}
function set_value(textObject,newValue,who){
 var name2="link"+textObject;
 eval ("document.assign." + textObject + ".value=newValue;");
 if(who==1){
 eval("document.all." + name2 + ".style.color=newValue");
 }
 if(who==2){
 eval("document.all." + name2 + ".style.fontSize=newValue");
 }
 if(who==3){
 eval("document.all." + name2 + ".bgColor=newValue");
 }
 if(who==4){
 eval("document.all." + name2 + ".style.fontFamily=newValue");
 }
 if(who==5){
 eval("document.all." + name2 + ".style.textDecoration=newValue");
 }
}

function getCookie(name) {
        var prefix = "" + name + "="
        var cookieStartIndex = document.cookie.indexOf(prefix)
        if (cookieStartIndex == -1)
                return null
        var cookieEndIndex = document.cookie.indexOf(";", cookieStartIndex + prefix.length)
        if (cookieEndIndex == -1)
                cookieEndIndex = document.cookie.length
        return unescape(document.cookie.substring(cookieStartIndex + prefix.length, cookieEndIndex))
}
 function win_assign(sid,name_form) {
   window.open('/cgi-bin/mod/img_viewer.pl?sid='+sid+'&name_form='+name_form+'','select_img_assign_123','width=450,height=450,status=no,toolbar=no,menubar=no,resizable=yes,scrollbars=yes,location=no');
   return false;
 }

  function win(url) {
 //alert(sid);
   window.open(url,'select_img_assign','width=450,height=450,status=no,toolbar=no,menubar=yes,resizable=yes,scrollbars=yes,location=no');
   return false;
 }
 function win_gallery(url,title,width,height) {
   width=width+23;
   height=height+25;
   url_new='/cgi-bin/full_img.pl?path='+url+'&title='+title;
   window.open(url_new,'open_img','width='+width+',height='+height+',status=no,toolbar=no,menubar=no,resizable=yes,scrollbars=1,location=no,border=thin,top=0,left=0,help=0');
   return false;
 }
