const CryptoJS = require('crypto-js');

function getAesString(n, f, c) {
    f = f.replace(/(^\s+)|(\s+$)/g, "");
    f = CryptoJS.enc.Utf8.parse(f);
    c = CryptoJS.enc.Utf8.parse(c);
    return CryptoJS.AES.encrypt(n, f, {
        iv: c,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    }).toString()
}
function encryptAES(n, f) {
    return f ? getAesString(randomString(64) + n, f, randomString(16)) : n
}

var $aes_chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
  , aes_chars_len = $aes_chars.length;
function randomString(n) {
    var f = "";
    for (i = 0; i < n; i++)
        f += $aes_chars.charAt(Math.floor(Math.random() * aes_chars_len));
    return f
}
// let data = 'github@cv-cat'
// let _p1 = '5wXdftSiqe1PbzYe'
// let res = encryptAES(data, _p1)
// console.log(res)