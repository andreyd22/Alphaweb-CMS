var	fixedX = -1;
var	fixedY = -1;
var startAt = 1;
var	crossobj, monthSelected, yearSelected, dateSelected, omonthSelected, oyearSelected, odateSelected, monthConstructed, yearConstructed, ctlToPlaceValue, ctlNow, dateFormat, nStartingYear
var	bPageLoaded=false
var	today = new	Date()
var	dateNow  = today.getDate()
var	monthNow = today.getMonth()
var	yearNow  = today.getYear()
var bShow = false;

/*** For language packs, month/day names should be changed here  ***/
var	monthName =	new Array("Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь","Ноябрь", "Декабрь")
var dayName = new Array("П","Вт","Ср","Ч","Пт","Сб","Вс")

if (dom)
{
	document.write ("<div onclick='bShow=true' id='calendar' class='div-style'>\n");
	document.write ("<table width='140' class='table-style'>\n");
	document.write ("<tr class='title-background-style' >\n");
	document.write ("	<td width='100%'>\n");
	document.write ("	<table width='100%'>\n");
	document.write ("		<tr>\n");
	document.write ("			<td class='title-style'>\n");
	document.write ("				<span id='caption'></span>\n");
	document.write ("			</td>\n");
	document.write ("		</tr>\n");
	document.write ("		</table>\n");
	document.write ("	</td>\n");
	document.write ("</tr>\n");
	document.write ("<tr>\n");
	document.write ("	<td width='100%' class='body-style'>\n");
	document.write ("		<span id='content'></span>\n");
	document.write ("	</td>\n");
	document.write ("</tr>");
	document.write ("</table>")
	document.write ("</div>");
}

function hideCalendar() {
	crossobj.visibility="hidden"
	showElement( 'SELECT' );
	showElement( 'APPLET' );
}

function padZero(num) {
	return (num	< 10)? '0' + num : num ;
}

function constructDate(d,m,y)
{
	sTmp = dateFormat
	sTmp = sTmp.replace	("dd","<e>")
	sTmp = sTmp.replace	("d","<d>")
	sTmp = sTmp.replace	("<e>",padZero(d))
	sTmp = sTmp.replace	("<d>",d)
	sTmp = sTmp.replace	("mmm","<o>")
	sTmp = sTmp.replace	("mm","<n>")
	sTmp = sTmp.replace	("m","<m>")
	sTmp = sTmp.replace	("<m>",m+1)
	sTmp = sTmp.replace	("<n>",padZero(m+1))
	sTmp = sTmp.replace	("<o>",monthName[m])
	return sTmp.replace ("yyyy",y)
}

function closeCalendar() {
	var	sTmp

	hideCalendar();
	ctlToPlaceValue.value = constructDate(dateSelected,monthSelected,yearSelected)
			getPrice();
}

function incMonth () {
	monthSelected++
	if (monthSelected>11) {
		monthSelected=0
		yearSelected++
	}
	constructCalendar()
}

function decMonth () {
	monthSelected--
	if (monthSelected<0) {
		monthSelected=11
		yearSelected--
	}
	constructCalendar()
}



/*** calendar ***/

function constructCalendar () {
	var dateMessage
	var	startDate =	new	Date (yearSelected,monthSelected,1)
	var	endDate = new Date (yearSelected,monthSelected+1,1);
	endDate = new Date (endDate	- (24*60*60*1000));
	numDaysInMonth = endDate.getDate()

	datePointer	= 0
	dayPointer = startDate.getDay() - startAt

	if (dayPointer < 0)
	{
		dayPointer = 6
	}

	sHTML = "<table width='100%' border='0' cellpadding='1' cellspacing='1' class='body-style'><tr>"

	for	(i=0; i<7; i++) {
		sHTML += "<td width='15' align='center'><B>"+ dayName[i]+"</B></td>"
	}
	sHTML +="</tr><tr>"

	for	( var i=1; i<=dayPointer;i++ )
	{
		sHTML += "<td>&nbsp;</td>"
	}

	for	( datePointer=1; datePointer<=numDaysInMonth; datePointer++ )
	{
		dayPointer++;
		sHTML += "<td width='15' align='center'>"

		var sStyle="normal-day-style"; //regular day

		if ((datePointer==dateNow)&&(monthSelected==monthNow)&&(yearSelected==yearNow)) //today
		{ sStyle = "current-day-style"; }

		//selected day
		if ((datePointer==odateSelected) &&	(monthSelected==omonthSelected) && (yearSelected==oyearSelected))
		{ sStyle += " selected-day-style"; }

		sHint = ""

		var regexp= /\"/g
		sHint=sHint.replace(regexp,"&quot;")

		sHTML += "<a class='"+sStyle+"' title=\"" + sHint + "\" href='javascript:dateSelected="+datePointer+";closeCalendar();'>" + datePointer + "</a>"
		if ((dayPointer+startAt) % 7 == startAt) {
			sHTML += "</tr><tr>"
		}
	}

	document.getElementById("content").innerHTML   = sHTML
	document.getElementById("spanMonth").innerHTML = monthName[monthSelected]
	document.getElementById("spanYear").innerHTML = yearSelected
}

function popUpCalendar(ctl,	ctl2, format) {
	var	leftpos=0
	var	toppos=0

  DocumentRegisterEvents();
	if (bPageLoaded)
	{
		if ( crossobj.visibility ==	"hidden" ) {
			ctlToPlaceValue = ctl2
			dateFormat=format;

			formatChar = " "
			aFormat = dateFormat.split(formatChar)
			if (aFormat.length<3)
			{
				formatChar = "/"
				aFormat = dateFormat.split(formatChar)
				if (aFormat.length<3)
				{
					formatChar = "."
					aFormat = dateFormat.split(formatChar)
					if (aFormat.length<3)
					{
						formatChar = "-"
						aFormat = dateFormat.split(formatChar)
						if (aFormat.length<3)
						{
							// invalid date format
							formatChar=""
						}
					}
				}
			}

			tokensChanged = 0
			if ( formatChar != "" )
			{
				// use user's date
				aData = ctl2.value.split(formatChar)

				for	(i=0;i<3;i++)
				{
					if ((aFormat[i]=="d") || (aFormat[i]=="dd"))
					{
						dateSelected = parseInt(aData[i], 10)
						tokensChanged ++
					}
					else if ((aFormat[i]=="m") || (aFormat[i]=="mm"))
					{
						monthSelected = parseInt(aData[i], 10) - 1
						tokensChanged ++
					}
					else if (aFormat[i]=="yyyy")
					{
						yearSelected = parseInt(aData[i], 10)
						tokensChanged ++
					}
					else if (aFormat[i]=="mmm")
					{
						for	(j=0; j<12;	j++)
						{
							if (aData[i]==monthName[j])
							{
								monthSelected=j
								tokensChanged ++
							}
						}
					}
				}
			}

			if ((tokensChanged!=3)||isNaN(dateSelected)||isNaN(monthSelected)||isNaN(yearSelected))
			{
				dateSelected = dateNow
				monthSelected = monthNow
				yearSelected = yearNow
			}

			odateSelected=dateSelected
			omonthSelected=monthSelected
			oyearSelected=yearSelected

			aTag = ctl
			do {
				aTag = aTag.offsetParent;
				leftpos += aTag.offsetLeft;
				toppos += aTag.offsetTop;
			} while(aTag.tagName!="BODY");

			crossobj.left = fixedX==-1 ? ctl.offsetLeft	+ leftpos :	fixedX
			crossobj.top = fixedY==-1 ?	ctl.offsetTop + toppos + ctl.offsetHeight +	2 :	fixedY
			constructCalendar (1, monthSelected, yearSelected);
			crossobj.visibility=(dom||ie)? "visible" : "show"
			
			hideElement( 'SELECT', document.getElementById("calendar") );
			hideElement( 'APPLET', document.getElementById("calendar") );			

			bShow = true;
		}
	}
	else
	{
		DateSelectorInit()
		popUpCalendar(ctl, ctl2, format)
	}
}

function DateSelectorInit()	{
	if (!ns4)
	{
		if (!ie) { yearNow += 1900	}

		crossobj=(dom)?document.getElementById("calendar").style : ie? document.all.calendar : document.calendar
		hideCalendar()

		monthConstructed=false;
		yearConstructed=false;

		sHTML1 = "<table width='100%' border='0' cellpadding='0' cellspacing='0'>\n";
		sHTML1 += "<tr>\n";
		sHTML1 += "	<td width='5'><span id='spanLeft' class='title-control-normal-style' onclick='javascript:decMonth()'>&lt;</span></td>\n";
		sHTML1 += "	<td width='100%' align='center'><span id='spanMonth' class='title-control-normal-style'></span>&nbsp;<span id='spanYear' class='title-control-normal-style'></span></td>\n";
		sHTML1 += "	<td width='5'><span id='spanRight' class='title-control-normal-style' onclick='incMonth()'>&gt;</span></td>\n";
		sHTML1 += "</tr>\n";
		sHTML1 += "</table>\n";

		document.getElementById("caption").innerHTML  = sHTML1

		bPageLoaded=true
	}
}

function DocumentRegisterEvents()
{
  document.onkeypress = function hideCalender_Trap1 () 
  {
	  if (event.keyCode == 27)
	  {
      hideCalendar();
	  }
  }

  document.onclick = function hideCalender_Trap2()
  {
	  if (!bShow)
	  {
      hideCalendar();
	  }
	  bShow = false
  }
}
