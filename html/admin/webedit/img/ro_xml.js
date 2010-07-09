function getXHTML(domSource) {
	var sb = new StringBuilder;
	copyNodeXHTML(domSource, sb);
	return sb.toString();
}

function getHTML(domSource) {
	return domSource.innerHTML;
}

var reComment = new RegExp();
reComment.compile("^<!--(.*)-->");

function fixAttribute(s) {
	return String(s).replace(/\&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/\"/g, "&quot;");
}

function fixText(s) {
	//return String(s).replace(/\&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;");
	return String(s).replace(/\&/g, "&amp;").replace(/>/g, "&gt;").replace(/</g, "&lt;").replace(/\u00A0/g, "&nbsp;");
}

var putReturnAfter = "html,p,table,tbody,tr,td,th,script,title,head,body,script,comment,style,ul,li,ol,meta,h1,h2,h3,h4,h5,h6,";

function copyNodeXHTML(sNode, sb) {
	var i=0;
	var newNode = null;
	var node;
	var sc = sNode.childNodes;
	var length = sc.length;
	for(i=0; i < length; i++){
		node = sc[i];

		switch(node.nodeType){
			case 1: //NODE_ELEMENT
				var name = node.nodeName;

				if (name == "!") {	// IE5.0 and IE5.5 are weird
					//this actually is a comment!
					//final character may not be a hyphen
					var found = reComment.exec(node.text);

					// Added by Eddie Machaalani to fix DTD bug
					if (found)
					{
						commentvalue = found[1];
						if (/-$/.test(commentvalue)) {
							commentvalue += " ";
						}
						//double hyphens must not occur in a comment
						commentvalue = commentvalue.replace(/--/g, "__");
						//newNode = targetdom.createComment(commentvalue);
						sb.append(node.text);
					}
					break;
				}
	
				if (node.scopeName == "HTML") {
					name = name.toLowerCase();
				}

				//newNode = targetdom.createElement(name);
				if (name == "html" && sb.length == 0) 
					sb.append("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n" +
				"\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n");
				sb.append("<" + name);

				var aAttributes = parseAttributes (sc(i).outerHTML);
			
				if (aAttributes.length > 0) {
					//copyAttributesXML(node, newNode, aAttributes);
					copyAttributesXHTML(node, sb, aAttributes);
				}

				if (node.canHaveChildren || node.hasChildNodes()) {
					sb.append(">");
					copyNodeXHTML(node, sb);				
					sb.append("</" + name + ">");
				} else if (name == "script") {
					//var secNode = targetdom.createCDATASection(node.text);
					sb.append(">" + node.text + "</" + name + ">");
					////var secNode = targetdom.createTextNode(node.text);
					//newNode.appendChild(secNode);
				} else if (name == "style") {
					//var secNode = targetdom.createCDATASection(node.innerHTML);
					////var secNode = targetdom.createTextNode(node.innerHTML);
					//newNode.appendChild(secNode);
					
					//if it begins with 2 enters or more, leave only one
					sb.append(">" + String(node.innerHTML).replace(/([$\r\n]+)/, "\r\n") + "</" + name + ">");
					
				} else if (name == "title") {
					//newNode.text = node.text;
					sb.append(">" + node.text + "</" + name + ">");
				} else if (name == "comment") {
					//newNode.text = node.innerHTML;
					sb.append(">" + node.innerHTML + "</" + name + ">");
				} else {
					sb.append(" />");
				}
				
				/* for readability */
				if (putReturnAfter.indexOf(name+","))
					sb.append("\n");
				
				break;
/*
			case 2: //NODE_ATTRIBUTE
				newNode = targetdom.createAttribute(node.nodeName);
				break;
*/
			case 3: //NODE_TEXT
				//newNode = targetdom.createTextNode(node.nodeValue);
				sb.append(fixText(node.nodeValue));
				break;
			case 4: //NODE_CDATA_SECTION 
				//newNode = targetdom.createCDATASection(node.nodeValue);
				sb.append("<![CDA" + "TA[\n" + node.nodeValue + "\n]" + "]>");
				break;
/*
			case 5: //NODE_ENTITY_REFERENCE 
				newNode = targetdom.createEntityReference(node.nodeName);
				break;
			case 6: //NODE_ENTITY 
				break;
			case 7: //NODE_PROCESSING_INSTRUCTION 
				newNode = targetdom.createProcessingInstruction("xml", node.nodeValue);
				break;
*/
			case 8: //NODE_COMMENT 
				//sb.append(node.text);
				if (/(^<\?xml)/.test(node.text) ) {
					sb.append(node.text);
					sb.append("\n");
				} else if (/(^<\!DOCTYPE)/.test(node.text) ) {
					//only the correct one
					sb.append("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"\n" +
				"\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n");
				} else {
					//final character may not be a hyphen
					var commentvalue = node.nodeValue;
					if (/-$/.test(commentvalue)) {
						commentvalue += " ";
					}
					//double hyphens must not occur in a comment
					commentvalue = commentvalue.replace(/\-\-/g, "__");
					sb.append("<!--" + commentvalue + "-->");
					//newNode = targetdom.createComment(commentvalue);
				}
				break;
			case 9: //NODE_DOCUMENT
				//newNode = targetdom.createElement("xml");
				sb.append ("<xml");
				
				var aAttributes = parseAttributes (sc(i).outerHTML);
			
				if (aAttributes.length > 0) {
					//copyAttributesXML(node, newNode, aAttributes);
					copyAttributesXHTML(node, sb, aAttributes);
				}

				//directly add all innerHTML
				//addXMLwoTag (newNode, "<root>" + node.innerHTML + "</root>"); 
				sb.append (">" + node.innerHTML + "</xml>"); 
				break;
			case 10: //NODE_DOCUMENT_TYPE 
				break;
			case 11: //NODE_DOCUMENT_FRAGMENT 
				//newNode = targetdom.createDocumentFragment();
				break;
/*			case 12: //NODE_NOTATION 
				break;
*/
			default:
				sb.append("<!--\nNot Supported:\n\n" + "nodeType: " + node.nodeType + "\nnodeName: " + node.nodeName + "\n-->");
		}

		/* helemaal naar voren halen 
		if (newNode != null){
			dNode.appendChild (newNode);
			if (node.hasChildNodes() && node.nodeType != 9) {
				copyNodeXML (node, newNode, targetdom);
			}
		}
		*/
		//sb.append("\n");

	}
}

function copyAttributesXHTML(sNode, sb, aAttributes){
	var i=0;
	var name, value;

	var length = aAttributes.length;
	for (i=0; i < length; i++){
	
		name = aAttributes[i];
		namelower = name.toLowerCase();
		
		switch(namelower) {
			case "style":
				value = sNode.style.cssText;
				// dNode.setAttribute(namelower, value.toLowerCase());
				sb.append(" " + namelower + "=\"" + fixAttribute(value) + "\"");
				break;		
			case "http-equiv":
				value = sNode.httpEquiv;
				//dNode.setAttribute(namelower, value);
				sb.append(" " + namelower + "=\"" + fixAttribute(value) + "\"");
				break;
			case "class":
				name = "className";
			default:
				value = sNode.getAttribute(name, 2);
				if (value==null)
					value = '';
				else
					//dNode.setAttribute(namelower, value);
					sb.append(" " + namelower + "=\"" + fixAttribute(value) + "\"");
				break;
			
		}
	}
}