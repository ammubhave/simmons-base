sim = new function () { 
    var clientid;
    var is_authenticated = false;

    this.init = function(options) {
        if (!('clientid' in options)) {
            console.error('clienid is a required argument to Simmons.init()');
            return;
        }

        clientid = options['clientid'];
    };

    this.login = function() {
        if ($.cookie('access_token') == undefined && window.location.hash.indexOf('access_token') == -1) {
            var link = 'https://simmons-dev.mit.edu/api/o/authorize/?response_type=token&client_id=' + clientid + '&redirect_uri=' + encodeURIComponent(window.location.href);
            window.location = link;
        } else if ($.cookie('access_token') == undefined) {
            var access_token = window.location.hash.substr(window.location.hash.indexOf('access_token') + 13);
            access_token = access_token.substr(0, access_token.indexOf('&'));
            //console.log(access_token);
            $.cookie('access_token', access_token);
        }
        //parent.location.hash = '';
        history.pushState("", document.title, parent.location.pathname + parent.location.search);
        // var state = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 8);
        // var link = 'https://simmons-dev.mit.edu/api/o/authorize/?response_type=token&state=' + state + '&client_id=' + clientid;
        // $.ajax({
        //     url: link,
        // }).done(function(data,status,xhr) {
        //     console.log(data);
        //     console.log(status);
        //     console.log(xhr);
        // });
    };

    function setHeader(xhr) {
        xhr.setRequestHeader('Authorization', 'Bearer ' + $.cookie('access_token'));
    }

    this.people = new function() { };
    this.people.all = function(success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/people/full',
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(function(x, status, error) {
            if (x.status == 403) {
                $.removeCookie('access_token');
                sim.login();
            }
        });
    };
}
