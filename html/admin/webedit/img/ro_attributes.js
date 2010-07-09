var reStart = new RegExp();
reStart.compile("^[\\s\\n]*<(?:\\w*:)?(\\w+)");

var reXMLNS = new RegExp();
reXMLNS.compile("^[\\s\\n]*(?:<\?xml:namespace.*/>)");

var reAttribute = new RegExp();
//reAttribute.compile("^[\\s\\n]*([\\w|-]+)");
//an atribute can have a namespace
reAttribute.compile("^[\\s\\n]*(?:\\w*:)?([\\w|-]+)");

//three kinds: " ' or nothing
var reAttributevalue1 = new RegExp();
reAttributevalue1.compile("^'[^']*'"); //'...'
var reAttributevalue2 = new RegExp();
reAttributevalue2.compile("^\"[^\"]*\""); //"..."
var reAttributevalue3 = new RegExp();
reAttributevalue3.compile("^[^>=\'\"\\n\\s]*"); // ...

var reAttributeis = new RegExp();
reAttributeis.compile("^([\\s\\n]*=[\\s\\n]*)");

var reTagClose = new RegExp();
reTagClose.compile("^[\\s\\n]*/?>");

var reWord = new RegExp();
reWord.compile("\\w"); //alphanumeric and _

var reWhite = new RegExp();
reWhite.compile("(\\n|\\s)"); //whitespace

var reAttrValue = new RegExp();
reAttrValue.compile("[^>=\'\"\\n\\s]") //anything except whitespace and  >'"=

function parseAttributes (sHTML) {

	var i=0;
	var len = sHTML.length;
	var attributes = "";
	var position = "start";
	var tagname = "";
	
	var aAttribs = new Array();
	
	var tag = "";
	var arr;
	Loop:
	for (i=0;i<len;i++) {
		char = sHTML.charAt(i);
		sstring = sHTML.substr(i,len);
		switch (position) {
			case "start":
				arr = reStart.exec(sstring);
				if (arr != null) {
					tag = arr[1]; //(misses one character!)
					position = "attribute";
					i += arr[0].length - 1;
					break;
				}
				arr = reXMLNS.exec(sstring);
				if (arr != null) {
					position = "start";
					i += arr[0].length - 1;
					break;
				}
				break;
			case "attribute":
				arr = reTagClose.exec(sstring);
				if (arr != null) {
					//done..
					break Loop;
				} 
				arr = reAttribute.exec(sstring);
				if (arr != null) {
					aAttribs[aAttribs.length] = arr[1];
					i += arr[0].length - 1;
					position = "attributeis";
				} 
				break;
			case "attributeis":
				arr = reAttributeis.exec(sstring);
				if (arr != null) {
					i += arr[0].length - 1;
					position = "beforeattrvalue";
				} else {
					//attribute has no value, next..
					position = "attribute";
					i--; //what happens if this char is a > character, it is skipped, therefore: i--;
				}
				break;
			case "beforeattrvalue":
				if (reWhite.test(char)) {
					//just continue
				} else if (char == "\"") {
					arr = reAttributevalue2.exec(sstring);
					if (arr != null) {
						i += arr[0].length - 1;
						position = "attribute";
					} 
				} else if (char == "'") {
					arr = reAttributevalue1.exec(sstring);
					if (arr != null) {
						i += arr[0].length - 1;
						position = "attribute";
					}
				} else {
					arr = reAttributevalue3.exec(sstring);
					if (arr != null) {
						i += arr[0].length - 1;
						position = "attribute";
					} 
				}
				break;
		}
	}
	return aAttribs;
}