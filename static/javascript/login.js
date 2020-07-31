window.onload = function() {
    document.getElementById('login-loginbutton').addEventListener('click', function() {
        var username = document.getElementById('login-usernamecontent').value;
        var email = document.getElementById('login-emailcontent').value;
        var password = document.getElementById('login-passwordcontent').value;
        if (username != '' && email != '' && password != '') {
            var login_form = document.getElementById('login-form');
            login_form.setAttribute('action', '/login');
            login_form.setAttribute('method', 'POST');
            login_form.submit();
        }
        else {
            alert('Please complete all Entries');
        }
    });


    document.getElementById('login-signupbutton').addEventListener('click', function() {
        var username = document.getElementById('login-usernamecontent').value;
        var email = document.getElementById('login-emailcontent').value;
        var password = document.getElementById('login-passwordcontent').value;
        if (username != '' && email != '' && password != '') {
            var login_form = document.getElementById('login-form');
            login_form.setAttribute('action', '/signup');
            login_form.setAttribute('method', 'POST');
            login_form.submit();
        }
        else {
            alert('Please complete all Entries');
        }
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
        if (userid != '') {
            navigator.sendBeacon(useridurl, 'EITHER');
        }
    });


};

