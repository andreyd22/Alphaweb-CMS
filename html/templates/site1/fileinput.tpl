 <style type="text/css">
        #File1
        {
            position: absolute;
        }
        .customFile
        {
            width: 219px;
            margin-left: -140px;
            cursor: default;
            height: 21px;
            z-index: 2;
            filter: alpha(opacity: 0);
            opacity: 0;
        }
        .fakeButton
        {
            position: absolute;
            z-index: 1;
            width: 85px;
            height: 21px;
            background: url(/javascripts/fileinput/images/button.jpg) no-repeat left top;
            float: left;
        }
       
        .blocker
        {
            position: absolute;
            z-index: 3;
            width: 150px;
            height: 21px;
            background: url(/javascripts/fileinput/images/transparent.gif);
            margin-left: -155px;
        }
        #FileName
        {
            position: absolute;
            height: 15px;
            margin-left: 90px;
            font-family: Verdana;
            font-size: 8pt;
            color: Gray;
            margin-top: 2px;
            padding-top: 1px;
            padding-left: 19px;
        }
        #activeBrowseButton
        {
            background: url(/javascripts/fileinput/images/button_active.jpg) no-repeat left top;
            display: none;
        }
    </style>
    <div id="wrapper">
        <input id="File1" type="file" name="upfile"/> 
    </div>
<br><br>
    <script type="text/javascript">
        window.onload = WindowOnLoad;
        var fileInput = document.getElementById('File1');
        var fileName = document.createElement('div');
        fileName.style.display = 'none';
        fileName.style.background = 'url(/javascripts/fileinput/images/icons.png)';
        var activeButton = document.createElement('div');
        var bb = document.createElement('div');
        var bl = document.createElement('div');
        function WindowOnLoad()
        {
            var wrap = document.getElementById('wrapper');
            fileName.setAttribute('id','FileName');
            activeButton.setAttribute('id','activeBrowseButton');
            fileInput.value = '';
            fileInput.onchange = HandleChanges;
            fileInput.onmouseover = MakeActive;
            fileInput.onmouseout = UnMakeActive;
            fileInput.className = 'customFile';
            bl.className = 'blocker';
            bb.className = 'fakeButton';
            activeButton.className = 'fakeButton';
            wrap.appendChild(bb);
            wrap.appendChild(bl);
            
            wrap.appendChild(activeButton);
            
            wrap.appendChild(fileName);
           
            
        };
        function HandleChanges()
        {
            file = fileInput.value;
	    //alert(file);
            reWin = /.*\\(.*)/;
            var fileTitle = file.replace(reWin, "$1"); //выдираем название файла
            reUnix = /.*\/(.*)/;
            fileTitle = fileTitle.replace(reUnix, "$1"); //выдираем название файла
            fileName.innerHTML = fileTitle;
            
            var RegExExt =/.*\.(.*)/;
            var ext = fileTitle.replace(RegExExt, "$1");//и его расширение
            
            var pos;
            if (ext){
                switch (ext.toLowerCase())
                {
                    case 'doc': pos = '0'; break;
                    case 'bmp': pos = '16'; break;                       
                    case 'jpg': pos = '32'; break;
                    case 'jpeg': pos = '32'; break;
                    case 'png': pos = '48'; break;
                    case 'gif': pos = '64'; break;
                    case 'psd': pos = '80'; break;
                    case 'mp3': pos = '96'; break;
                    case 'wav': pos = '96'; break;
                    case 'ogg': pos = '96'; break;
                    case 'avi': pos = '112'; break;
                    case 'wmv': pos = '112'; break;
                    case 'flv': pos = '112'; break;
                    case 'pdf': pos = '128'; break;
                    case 'exe': pos = '144'; break;
                    case 'txt': pos = '160'; break;
                    default: pos = '176'; break;
                };
                fileName.style.display = 'block';
                fileName.style.background = 'url(/javascripts/fileinput/images/icons.png) no-repeat 0 -'+pos+'px';
            };
            
        };
        function MakeActive()
        {
           activeButton.style.display = 'block';
        };
        function UnMakeActive()
        {
            activeButton.style.display = 'none';
        };
    </script>
