/*********************************************************
 * Taidu Technology Inc. © 2021
 * created at 12/13/2021
 * author: Yuwei Le
 * description: Taidu Tech's common js library
 *********************************************************/

/*
    BASIC CONFIGURATION SETTINGS
 */
const const_api_url = "120.27.131.20:12345/getAbbr";
const const_api_version = "";
const const_api_list = {
    // abbr
    getAbbr: "/getAbbr",
};
const const_success_code_list = ["200", "success", "ok", "1"];

/*
    WARNING TEXT SETTINGS
 */
const warn_dep_abnormal = "您的依赖环境未安装或未正确加载，请检查网络状态并刷新重试，或请网站管理员检查";

/*
    BOOLEAN FLAGS
 */
var bools_env_prepared = {};  // X:true/false indicates whether dependency X has been initialized

/*
    USER VARIABLES
 */
var user_tokens = "";


/**
 * prepare dependencies in the head
 * @param url str js-file url to be added
 * @param callback pointer function that handles after-loading events
 */
function envPrepare(url, callback) {
    if (!bools_env_prepared.hasOwnProperty(url))
        bools_env_prepared[url] = document.getElementById(url) !== null;  // avoid duplicate dependencies
    if (!bools_env_prepared[url]) {
        var script = document.createElement("script");
        script.type = "text/javascript";
        script.id = url;
        if (typeof(callback) != "undefined")
            if (script.readyState)
                script.onreadystatechange = function() {
                    if (script.readyState === "loaded" || script.readyState === "complete") {
                        script.onreadystatechange = null;
                        bools_env_prepared[url] = true;
                        callback();
                    }
                };
            else {
                script.onload = function () {
                    bools_env_prepared[url] = true;
                    callback();
                };
            }
        script.src = url;
        document.head.appendChild(script);
    } else {
        bools_env_prepared[url] = true;
        callback();
    }
}


/**
 * get api url based on the const_api settings
 * @param api str api from const_api_list
 * @returns {string} full absolute api url
 */
function getApiUrl(api) {
    return const_api_url + const_api_version + api;
}


/**
 * request based on jquery
 * @param method str post or get
 * @param params a dictionary-like array, {key1:value1, key2:value2}
 * @param url str url to be requested
 * @param callback_p pointer callback function must accept status code and data string as inputs
 */
function request(method, url, callback_p) {

    // make request
    $.ajax({
        url: url ,
        responseType: 'application/json; charset=utf-8',
        dataType: 'json',
        crossDomain: true,
        contentType: 'application/json; charset=utf-8',
        // data: form_data,
        type: method,
        beforeSend: function(xhr) {
            xhr.setRequestHeader('Access-Control-Allow-Origin', '*'); // 允许所有来源访问
            xhr.setRequestHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS'); // 允许的请求方法
            xhr.setRequestHeader('Access-Control-Allow-Headers', 'Content-Type'); // 允许的请求头
        },
        success: function (output, status, xhr) {
            console.log("success");
            callback_p(status, output);
        },
        error: function (xhr, ajaxOptions, thrownError){
            console.log("error");
            callback_p(xhr.status, thrownError);
        }
    });
}


/**
 * make API request
 * @param params two-dimensional array, e.g., [[key1, value1], [key2, value2]], or a dictionary-like array
 * @param api str API chosen from const_api_list
 * @param callback_p pointer callback function must accept status code and data string as inputs
 */
function apiRequest(params, api, callback_p) {
    // identify method: post or get
    var method;
    for (var i in const_api_list) {
        if (const_api_list[i] === api) {
            method = i.startsWith("get")?"get":"post";
            break;
        }
    }

    // add user tokens to header
    if (user_tokens !== "" && api !== const_api_list.postLogin && api !== const_api_list.postAccount) {
        params['token'] = user_tokens;
    }

    // make a request
    request(method, params, getApiUrl(api), function (code, data) {
        // save user tokens if the api is login
        if (api === const_api_list.postLogin) {
            user_tokens = unescape(data);
            setToken();
        }
        // return to original callback function
        callback_p(code, data);
    });
}


/**
 * clear all cookies on the current page
 */
function clearToken() {
    var keys = document.cookie.match(/[^ =;]+(?==)/g);
    if (keys) {
        for (var i = keys.length; i--;) {
            console.log(keys[i]);
            document.cookie = keys[i] + '=0;path=/;expires=' + new Date(0).toUTCString();
            document.cookie = keys[i] + '=0;path=/;domain=' + document.domain + ';expires=' + new Date(0).toUTCString();
        }
    }
}


/**
 * save user tokens in the cookie on the current page
 */
function setToken() {
    var expires = 24 * 60 * 60 * 1000;
    var exp = new Date();
    exp.setTime(exp.getTime() + expires);
    document.cookie = "user_token=" + user_tokens + ";path=/;domain=" + document.domain + ";expires=" + exp.toUTCString();
}


/**
 * get and set user tokens automatically from cookies
 */
function getToken() {
    var reg = new RegExp("(^| )" + "user_token" + "=([^;]*)(;|$)");
    var arr = document.cookie.match(reg);
    if (arr)
        user_tokens = arr[2];
}
// run once after the script is loaded
getToken();


/**
 * check if a value is in an array
 * @param arr array
 * @param value value
 */
function isInArray(arr, value) {
    if(arr.indexOf && typeof(arr.indexOf)=='function'){
        var index = arr.indexOf(value);
        if(index >= 0){
            return true;
        }
    }
    return false;
}


/**
 * check whether the return code indicates a success request
 * @param code HTTP return code
 * @returns {boolean} whether the code indicates a success
 */
function isSuccess(code) {
    return isInArray(const_success_code_list, code.toString());
}


/**
 * extend the String prototype to support C-like format function
 * credit to https://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format/610415
 */
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}