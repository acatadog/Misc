/*!
 * 一些类似于思路来自于python的工具函数
 * write by penghuawei
 */

pyurllib = {
    parse: {
        urlencode: function (a) {
            var s = [];

            if ( a.constructor == Array ) {
                for ( var i = 0; i < a.length; i++ )
                    s.push( a[i].name + "=" + encodeURIComponent( a[i].value ) );
            } else {
                for ( var j in a )
                    s.push( j + "=" + encodeURIComponent( a[j] ) );
            }
            return s.join("&");
        },

        urlparse: function (url) {
            var obj = { 
                protocol : '' ,  /* http */
                auth : null,
                origin: '',  /* http://localhost:8080 */
                host : '' ,  /* localhost:8080 */
                port : '' ,  /* 8080 */
                hostname : '' ,  /* localhost */
                hash : null,
                search : '',  /* ?a=index&t=article */
                query : '',  /* a=index&t=article */
                pathname : '',  /* /one */
                path : '',  /* /one?a=index&t=article */
                href : url  /* http://localhost:8080/one?a=index&t=article */
            };

            var reg = /(^(file|gopher|news|nntp|telnet|http|ftp|https|ftps|sftp):\/\/(.+?)(:\d+)*?)(\/.*)/;
            var r = reg.exec(url) || reg.exec(url + "/");
            if (r) {
                if (r[1] != undefined) {
                    obj.origin = r[1];
                }
                if (r[2] != undefined) {
                    obj.protocol = r[2];
                }
                if (r[3] != undefined) {
                    obj.hostname = r[3];
                }
                if (r[4] != undefined) {
                    obj.port = r[4].slice(1);
                }
                if (r[5] != undefined) {
                    obj.path = r[5];
                }
            } else {
                obj.path = url;
            }
            
            obj.host = obj.hostname + (obj.port ? ':' + obj.port : '');

            var pos = obj.path.indexOf('?');
            if (pos != -1) {
                obj.pathname = obj.path.slice(0, pos);
                obj.query = obj.path.slice(pos + 1);
                obj.search = obj.path.slice(pos);
            } else {
                obj.pathname = obj.path;
            }
            
            return obj;
        },

        urljoin: function (base, url) {
            var urlO = this.urlparse(url);
            if (urlO.protocol) {
                return url;
            }

            var baseO = this.urlparse(base);
            var paths = [];

            if (!urlO.pathname[0] == "/") {
                /* like as ["a", "b", "c", "d", ""] */
                basePath = baseO.pathname.split("/");
                /* drop last element */
                basePath = basePath.slice(0, basePath.length - 1);
                paths.push(basePath);
            }
            paths.push(urlO.pathname.split("/"));

            var allPaths = [];
            for (var j = 0; j < paths.length; j++) {
                var pathE = paths[j];
                for (var i = 0; i < pathE.length; i++) {
                    var val = pathE[i];
                    if (!val || val == ".") {
                        continue;
                    } else if (val == "..") {
                        allPaths.pop();
                    } else {
                        allPaths.push(val);
                    }
                }
            }
            
            return baseO.origin + "/" + allPaths.join("/") + urlO.search;
        }

    }
};
