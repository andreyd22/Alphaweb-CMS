var	ie = document.all
var	dom = document.getElementById
var	ns4 = document.layers

/* hides <select> and <applet> objects (for IE only) */
function hideElement( elmID, overDiv )
{
  	if (ie)
	{
        for( i = 0; i < document.all.tags( elmID ).length; i++ )
        {
			obj = document.all.tags( elmID )[i];
			if( !obj || !obj.offsetParent )
			{
				continue;
			}

			// Find the element's offsetTop and offsetLeft relative to the BODY tag.
			objLeft   = obj.offsetLeft;
			objTop    = obj.offsetTop;
			objParent = obj.offsetParent;

			while( objParent.tagName.toUpperCase() != "BODY" )
			{
				objLeft  += objParent.offsetLeft;
				objTop   += objParent.offsetTop;
				objParent = objParent.offsetParent;
			}

			objHeight = obj.offsetHeight;
			objWidth = obj.offsetWidth;

			if(( overDiv.offsetLeft + overDiv.offsetWidth ) <= objLeft );
			else if(( overDiv.offsetTop + overDiv.offsetHeight ) <= objTop );
			else if( overDiv.offsetTop >= ( objTop + objHeight ));
			else if( overDiv.offsetLeft >= ( objLeft + objWidth ));
			else
			{
				obj.style.visibility = "hidden";
			}
		}
	}
}

/*
 * unhides <select> and <applet> objects (for IE only)
 */
function showElement( elmID )
{
	if (ie)
	{
		for( i = 0; i < document.all.tags( elmID ).length; i++ )
		{
			obj = document.all.tags( elmID )[i];

			if( !obj || !obj.offsetParent )
			{
				continue;
			}

			obj.style.visibility = "";
		}
	}
}