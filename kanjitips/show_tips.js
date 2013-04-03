/* -*- mode: Javascript ; coding: utf-8 -*- */


function kanji_object(k, size, v) {

    var kanji = '<object width="' + size + ' " height="' + size +
        '" type="image/svg+xml" data="' + k + '.svg">' +
        k + '</object>';
    if (v == undefined || v == 'Standard') {
        return '<figure>\n' + kanji + '\n</figure>';
    } else {
        return '<figure>\n' + kanji +
            '\n<figcaption>' + v + '</ficaption>\n' +
            '</figure>';
    }
}
