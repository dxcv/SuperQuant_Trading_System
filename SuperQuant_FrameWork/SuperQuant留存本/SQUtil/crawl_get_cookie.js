
a1 = [4, 4, 4, 4, 1, 1, 1, 3, 2, 2, 2, 2, 2, 2, 2, 4, 2, 1];
var S = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
function aaa(a2) {
    for (var r = a1, n = [], t = -1, e = 0, a = r["length"]; a > e; e++)
        for (var u = a2[e], f = r[e], d = t += f; n[d] = u & parseInt("11111111", 2),
        --f != 0; )
            --d,
                u >>= parseInt("10", 8);
    return n
};

function T(r) {
    for (var n = ("imeNow",
        "429",
        0), t = 0, e = r["length"]; e > t; t++)
        n = (n << 5) - n + r[t];
    return n & parseInt("255", 10)
};

function P(r, n, t, e, a) {
    for (var f = r["length"]; f > n; )
        t[e++] = r[n++] ^ a & parseInt("255", 10),
            a = ~(a * parseInt("203", 8))
};

function N(r) {
    for (var _ = "3", E = 0, A = r["length"], b = []; A > E; ) {
        var B = r[E++] << parseInt("10000", 2) | r[E++] << 8 | r[E++];
        b.push(S.charAt(B >> parseInt("10010", 2)), S.charAt(B >> parseInt("14", 8) & parseInt("77", 8)), S.charAt(B >> 6 & parseInt(_ + "f",16)), S.charAt(B & parseInt("3f", 16)))
    }
    return b.join("")
};
function M(r) {
    var n = T(r)
        , t = [2, n];
    return P(r, +0, t, +2, n),
        N(t)
};



function fenshi(server_time){
a2 = {0: Math.random() * parseInt("4294967295", 10) >>> 0, 1: server_time, 2: (new Date()).getTime() / parseInt(8) >>> 0, 3: 1037329871,  4: 1, 5: 10, 6: 3, 7: 196, 8: 0, 9: 5, 10: 0, 11: 0, 12: 0, 13: 3756, 14: 0, 15: 0, 16: 3, 17: 3};
return M(aaa(a2));
};
function rixian(server_time){
a2 = {0: Math.random() * parseInt("4294967295", 10) >>> 0, 1: server_time, 2: (new Date()).getTime() / parseInt(8) >>> 0, 3: 1037329871, 4: 1, 5: 10, 6: 3, 7: 259, 8: 1, 9: 5, 10: 0, 11: 425, 12: 71, 13: 3756, 14: 0, 15: 0, 16: 5, 17: 3};
return M(aaa(a2));
};function zhouxian(server_time){
a2 = {0: Math.random() * parseInt("4294967295", 10) >>> 0, 1: server_time, 2: (new Date()).getTime() / parseInt(8) >>> 0, 3: 1037329871, 4: 1, 5: 10, 6: 3, 7: 314, 8: 3, 9: 5, 10: 0, 11: 186, 12: 204, 13: 3756, 14: 0, 15: 0, 16: 7, 17: 3};
return M(aaa(a2));
};function yuexian(server_time){
a2 = {0: Math.random() * parseInt("4294967295", 10) >>> 0, 1: server_time, 2: (new Date()).getTime() / parseInt(8) >>> 0, 3: 1037329871, 4: 1, 5: 10, 6: 3, 7: 363, 8: 4, 9: 5, 10: 0, 11: 571, 12: 69, 13: 3756, 14: 0, 15: 0, 16: 9, 17: 3};
return M(aaa(a2));
};

function get_hv(){
    var server_time = Math.floor((new Date()).getTime() / 1000 - 1);
    var fun_list = [fenshi, rixian, zhouxian, yuexian];
    var fun = fun_list[Math.floor(Math.random()*(3+1))];
    var hv = fun();
    return hv
}