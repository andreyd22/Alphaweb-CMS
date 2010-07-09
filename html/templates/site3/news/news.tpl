
[%IF a=="" %]

[%FOREACH data IN ar_data %]

      <p>
        [%data.data_print%]&nbsp;&nbsp;&nbsp;<!--a href="/news/[%id%]/[%data.id%].html"--><b>[%data.zag%]</b><!--/a--></p>
        <p>
        [%data.short%]<BR><BR>
       <a href="/news/[%id%]/[%data.id%].html">Подробнее</a>
	</p>


[%END%]

[%perehod%]


[%END%]


[%IF a=="full"%]
<h1>[%ref_data.zag%]</h1>
[%ref_data.data_print%]<br>
<p>
<div>
[%ref_data.full_news%]
</div>
</p>
<p>&nbsp;</p>
<small><a href="/news/[%id%].html"><small>Архив</small></a></small>
[%END%]