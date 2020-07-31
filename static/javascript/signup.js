window.onload = function() {
    window.addEventListener('visibilitychange', function() {
        var url = window.location.href;
        var length = url.length;
        var userid = '';
        var i;
        var j;
        for (i = 0; i < length; i++) {
            if (url[i] === '/' && url[i - 1] === 'e' && url[i - 2] === 'v') {
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
        input.setAttribute('value', 'SIGNUP');

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
            if (url[i] === '/' && url[i - 1] === 'e' && url[i - 2] === 'v') {
                for (j = i; j < length; j++) {
                    userid = userid + url[j];
                }
                break;
            }
        }
        var useridurl = '/clear/temp/user/objects' + userid;
        navigator.sendBeacon(useridurl, 'SIGNUP');
    });

    
    document.getElementById('signup-button-back-to-log-in').addEventListener('click', function() {
        window.location.href = '/login';
    });


};

