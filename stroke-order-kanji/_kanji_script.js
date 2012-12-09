//<![CDATA[
/*
  This is part of kanji-colorize, which shows KanjiVG data as colored
  stroke order diagrams.

  This file adds filters to the SVG files that show the groups with
  colored shadows. (This works only when the kanji_colorizer was run
  with "--mode css".)

  This file copyright © 2012 Roland Sieker <ospalh@gmail.com>
  License: GNU AGPL, version 3 or later;
  http://www.gnu.org/licenses/agpl.html

*/
var svgns = "http://www.w3.org/2000/svg";
var svg;
var defs;
var shad_of_x = "3";
var shad_of_y = "3";
var shad_opacity = "0.75";
var blur_dev = "2.5";
var group_colors = ["#bf0909", "#bf6409", "#09bf09", "#09bfbf", "#0909bf", "black"];

function init(evt) {
    svg = document.getElementById("kanjisvg");
    defs = document.createElementNS(svgns, "defs");
    for (i=0; i < group_colors.length; i++) {
        createFilter(i);
        // Now do the filtering for the groups. There should be only
        // one element with each class, but iterated over that anyway.
        var filter_url = 'url(#filter' + i.toString() + ')';
        var stroke_groups = document.getElementsByClassName(
            "group_num" + i.toString());
        if (stroke_groups) {
            for (j=0; j < stroke_groups.length; j++) {
                stroke_groups[j].setAttribute("filter", filter_url);
            }
        }
    }
    svg.appendChild(defs);
}

function createFilter(i) {
    var filter = document.createElementNS(svgns, "filter");
    filter.setAttribute("id", 'filter' + i.toString());
//width="200%" height="200%">
    filter.setAttribute("width", "200%");
    filter.setAttribute("height", "200%");
    var shift = document.createElementNS(svgns, "feOffset");
    shift.setAttribute("dx", shad_of_x);
    shift.setAttribute("dy", shad_of_y);
    filter.appendChild(shift);
    var blur = document.createElementNS(svgns, "feGaussianBlur");
    blur.setAttribute("stdDeviation", blur_dev);
    blur.setAttribute("result", "offset-blur");
    filter.appendChild(blur);
    var flood = document.createElementNS(svgns, "feFlood");
    // This color it the point we do different filters. There may be
    // an easier way, but i didn't find it.
    flood.setAttribute("flood-color", group_colors[i]);
    flood.setAttribute("flood-opacity", shad_opacity);
    flood.setAttribute("result", "color");
    filter.appendChild(flood);
    var flood_shadow = document.createElementNS(svgns, "feComposite");
    flood_shadow.setAttribute("operator", "in");
    flood_shadow.setAttribute("in", "color");
    flood_shadow.setAttribute("in2", "offset-blur");
    flood_shadow.setAttribute("result", "shadow");
    filter.appendChild(flood_shadow);
    var orig_shadow = document.createElementNS(svgns, "feComposite");
    orig_shadow.setAttribute("operator", "over");
    orig_shadow.setAttribute("in", "SourceGraphic");
    orig_shadow.setAttribute("in2", "shadow");
    filter.appendChild(orig_shadow);
    defs.appendChild(filter);
}

//]]>
