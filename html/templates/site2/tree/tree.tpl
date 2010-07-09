
[%IF a=="" %]

[%FOREACH data IN ar_data %]

        <p>[%data.nbsp%]<a href="/[%data.module%]/[%data.id%].html" title="[%data.description%]">[%data.name%]</a></p>

[%END%]


[%END%]
