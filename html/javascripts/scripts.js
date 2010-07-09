// JavaScript Document
function MM_changeProp(objId,x,theProp,theValue) { //v9.0
  var obj = null; with (document){ if (getElementById)
  obj = getElementById(objId); }
  if (obj){
    if (theValue == true || theValue == false)
      eval("obj."+theProp+"="+theValue);
    else eval("obj."+theProp+"='"+theValue+"'");
  }
}

IE = (document.all);
NC = (document.layers);
Opera = (document.getElementById);

function getHeight() {
if (IE || Opera) send = document.body.clientHeight;
if (NC) send = window.innerHeight;
return send;
}

function getWidth() {
if (IE || Opera) send = document.body.clientWidth;
if (NC) send = window.innerWidth;
return send;
}


function putLayer() {
	widthBrowser = getWidth();
	if(widthBrowser < 1030) { 
		MM_changeProp('all_c','','className','page_small','DIV')
	};
	else {
	MM_changeProp('all_c','','className','none','DIV')
	};
}

