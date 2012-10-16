



$(document).ready(function(){

    $('#pinky').qtip({
        content: {
            text:'The semicolon “;” is mapped to “again”, too. Like this, \
it should work out with the programmer dvorak variant as well.',
        },
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });

});
