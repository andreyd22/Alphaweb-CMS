<style>
.gal {
float:left;
width: 130px;
height:150px;
padding:5px;
}
</style>
[%IF a=="" %]
[%IF tpl_top%]
<table width="100%"><tr><td>
[%INSERT $tpl_top%]
</td></tr></table>
<br><br>
[%END%]
<script src="/javascripts/prototype.js" type="text/javascript"></script>
<script src="/javascripts/scriptaculous.js?load=effects" type="text/javascript"></script>

<script type="text/javascript" src="/javascripts/lightbox.js"></script>
<link rel="stylesheet" href="/javascripts/lightbox.css" type="text/css" media="screen" />

[%i=0%]
[%IF perehod%]
<p align="center"><small>Страницы: </small>[%perehod%]</p>
<br><br>
[%END%]


<table align="center" width="100%"><tr><td>
<div class="floats">
[%FOREACH ref_data IN ar_data %]
    [%i=i+1%]

    <div style="float:left;width:90px;height:90px">
        <div class="ri" align="left">
	    <a href="/gallery/[%ref_data.idr%]/[%ref_data.id%].html"><img src="/base/gallery_image/[%ref_data.id%]-s.jpg"  class="ill2"></a>
	    <div align="left">
	    [%ref_data.name%]<br>
	    </div>
	</div>
        <div class="min"></div>
    </div>
[%END%]
</div>
</td></tr></table>


<br><br>
[%IF perehod%]
<p align="center"><small>Страницы: </small>[%perehod%]</p>
[%END%]


[%END%]


[%IF a=="full"%]
<script src="/javascripts/prototype.js" type="text/javascript"></script>
<script src="/javascripts/scriptaculous.js?load=effects" type="text/javascript"></script>

<script type="text/javascript" src="/javascripts/lightbox.js"></script>
<link rel="stylesheet" href="/javascripts/lightbox.css" type="text/css" media="screen" />
  <div align="center">
  <a href="/base/gallery_image/[%ref_data.id%].jpg" rel="lightbox[roadtrip]"><img src="/base/gallery_image/[%ref_data.id%]-m.jpg"></a>
  </div>

[%ref_data.opis%]
    
[%END%]
