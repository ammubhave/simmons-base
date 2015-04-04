/*!
 * jQuery Cookie Plugin v1.4.1
 * https://github.com/carhartl/jquery-cookie
 *
 * Copyright 2006, 2014 Klaus Hartl
 * Released under the MIT license
 */
(function (factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD
        define(['jquery'], factory);
    } else if (typeof exports === 'object') {
        // CommonJS
        factory(require('jquery'));
    } else {
        // Browser globals
        factory(jQuery);
    }
}(function ($) {

    var pluses = /\+/g;

    function encode(s) {
        return config.raw ? s : encodeURIComponent(s);
    }

    function decode(s) {
        return config.raw ? s : decodeURIComponent(s);
    }

    function stringifyCookieValue(value) {
        return encode(config.json ? JSON.stringify(value) : String(value));
    }

    function parseCookieValue(s) {
        if (s.indexOf('"') === 0) {
            // This is a quoted cookie as according to RFC2068, unescape...
            s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
        }

        try {
            // Replace server-side written pluses with spaces.
            // If we can't decode the cookie, ignore it, it's unusable.
            // If we can't parse the cookie, ignore it, it's unusable.
            s = decodeURIComponent(s.replace(pluses, ' '));
            return config.json ? JSON.parse(s) : s;
        } catch(e) {}
    }

    function read(s, converter) {
        var value = config.raw ? s : parseCookieValue(s);
        return $.isFunction(converter) ? converter(value) : value;
    }

    var config = $.cookie = function (key, value, options) {

        // Write

        if (arguments.length > 1 && !$.isFunction(value)) {
            options = $.extend({}, config.defaults, options);

            if (typeof options.expires === 'number') {
                var days = options.expires, t = options.expires = new Date();
                t.setTime(+t + days * 864e+5);
            }

            return (document.cookie = [
                encode(key), '=', stringifyCookieValue(value),
                options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
                options.path    ? '; path=' + options.path : '',
                options.domain  ? '; domain=' + options.domain : '',
                options.secure  ? '; secure' : ''
            ].join(''));
        }

        // Read

        var result = key ? undefined : {};

        // To prevent the for loop in the first place assign an empty array
        // in case there are no cookies at all. Also prevents odd result when
        // calling $.cookie().
        var cookies = document.cookie ? document.cookie.split('; ') : [];

        for (var i = 0, l = cookies.length; i < l; i++) {
            var parts = cookies[i].split('=');
            var name = decode(parts.shift());
            var cookie = parts.join('=');

            if (key && key === name) {
                // If second argument (value) is a function it's a converter...
                result = read(cookie, value);
                break;
            }

            // Prevent storing a cookie that we couldn't decode.
            if (!key && (cookie = read(cookie)) !== undefined) {
                result[name] = cookie;
            }
        }

        return result;
    };

    config.defaults = {};

    $.removeCookie = function (key, options) {
        if ($.cookie(key) === undefined) {
            return false;
        }

        // Must not alter options, thus extending a fresh object...
        $.cookie(key, '', $.extend({}, options, { expires: -1 }));
        return !$.cookie(key);
    };

}));



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

    function api_error_callback(x, status, error) {
        if (x.status == 403) {
            if ($.cookie('access_token') != undefined) {
                $.removeCookie('access_token');
                sim.login();
            } else {
                alert('Unable to login to Simmons API, please contact simmons-tech@mit.edu');
            }
        } else {
            console.error('API call failed: ' + status + ' ' + error);
        }
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
        }).error(api_error_callback);
    };

    this.people.get = function(username, success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/people/profile/' + encodeURIComponent(username),
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(api_error_callback);
    };

    this.people.get_fsof = function(success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/people/fifteen_seconds_of_frame',
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(api_error_callback);
    };

    this.people.me = function(success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/people/me',
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(api_error_callback);
    };

    /** ROOMING **/
    this.rooming = new function() { };
    this.rooming.taken = function(success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/rooming/taken',
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(api_error_callback);
    }
    this.rooming.occupants = function(success) {
        $.ajax({
            url: 'https://simmons-dev.mit.edu/api/rooming/occupants',
            dataType: 'json',
            beforeSend: setHeader
        }).done(function (data) {
            //console.log(data);
            success(data);
        }).error(api_error_callback);
    }
}
