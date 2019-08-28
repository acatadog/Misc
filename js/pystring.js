/*!
 * 一些类似于思路来自于python的工具函数
 * write by penghuawei
 */

if (typeof String.prototype.format != 'format') {
    String.prototype.format = function(args) {
        var result = this;
        if (arguments.length > 0) {
            if (arguments.length == 1 && typeof (args) == "object") {
                for (var key in args) {
                    if(args[key]!=undefined){
                        var reg = new RegExp("({" + key + "})", "g");
                        result = result.replace(reg, args[key]);
                    }
                }
            }
            else {
                for (var i = 0; i < arguments.length; i++) {
                    if (arguments[i] != undefined) {
                        var reg= new RegExp("({)" + i + "(})", "g");
                        result = result.replace(reg, arguments[i]);
                    }
                }
            }
        }
        return result;
    };
}

if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (prefix){
        return this.slice(0, prefix.length) === prefix;
    };
}

if (typeof String.prototype.endsWith != 'function') {
    String.prototype.endsWith = function(suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    };
}

if (typeof String.prototype.lstrip != 'lstrip') {
    String.prototype.lstrip = function( str2 ) {
        var str1 = this;
        var spl = str2; 
        var typeName = typeof str2;
        if (typeName === 'undefined' || typeName === 'null')
            spl = "^[\r\n\t ]*";
        else
            spl = "^[" + str2 + "]*";
        
        return str1.replace(new RegExp(spl), "");
    };
}

if (typeof String.prototype.rstrip != 'rstrip') {
    String.prototype.rstrip = function( str2 ) {
        var str1 = this;
        var spl = str2; 
        var typeName = typeof str2;
        if (typeName === 'undefined' || typeName === 'null')
            spl = "[\r\n\t ]*$";
        else
            spl = "[" + str2 + "]*$";
        
        return str1.replace(new RegExp(spl), "");
    };
}

if (typeof String.prototype.rstrip != 'rstrip') {
    strip : function( str2 ) {
        var str1 = this;
        var spl = str2; 
        var typeName = typeof str2;
        if (typeName === 'undefined' || typeName === 'null')
            spl = "^[\r\n\t ]*|[\r\n\t ]*$";
        else
            spl = "^[" + str2 + "]*" + "[" + str2 + "]*$";
        
        return str1.replace(new RegExp(spl, "g"), "");
    };
}
