/* -*- mode: Javascript ; coding: utf-8 -*- */

// A shared object containing all the values you want shared between
// your tooltips
var shared = {
    show: 'mouseover',
    hide: 'mouseout',
    style: {
        classes: 'ui-tooltip-red'
    }
}

function kanji_object(k, size) {

    var kanji = '<object width="' + size + ' " height="' + size +
        '" type="image/svg+xml" data="file://' + k + '">' +
        k + '</object>';
    return '<figure class="kanjivg standard">\n' + kanji + '\n</figure>';
}

function kanji_variant_object(k, size) {

    return '<object width="' + size + ' " height="' + size +
        '" type="image/svg+xml" data="file://' + k + '">' +
        k + '</object>';
}
