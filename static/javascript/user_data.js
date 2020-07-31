window.onload = function() {
    window.addEventListener('visibilitychange', function() {
        var url = window.location.href;
        var length = url.length;
        var userid = '';
        var i;
        var j;
        for (i = 0; i < length; i++) {
            if (url[i] === '/' && url[i - 1] === 'a' && url[i - 2] === 't') {
                for (j = i; j < length; j++) {
                    userid = userid + url[j];
                }
                break;
            }
        }
        var useridurl = '/clear/temp/user/objects' + userid;

        var tempform = document.createElement('form');
        var input = document.createElement('input');

        tempform.setAttribute('action', useridurl);
        tempform.setAttribute('method', 'POST');
    
        input.setAttribute('type', 'hidden');
        input.setAttribute('name', 'NAME');
        input.setAttribute('value', 'LOGIN');

        tempform.appendChild(input);
        document.body.appendChild(tempform);

        tempform.submit();
    });

    
    window.addEventListener("unload", function() {
        var url = window.location.href;
        var length = url.length;
        var userid = '';
        var i;
        var j;
        for (i = 0; i < length; i++) {
            if (url[i] === '/' && url[i - 1] === 'a' && url[i - 2] === 't') {
                for (j = i; j < length; j++) {
                    userid = userid + url[j];
                }
                break;
            }
        }
        var useridurl = '/clear/temp/user/objects' + userid;
        navigator.sendBeacon(useridurl, 'LOGIN');
    });


};

