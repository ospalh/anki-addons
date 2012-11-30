



$(document).ready(function(){

    $('.pinky').qtip({
        content: {
            text:"The apostrophe “'” and semicolon “;” are both mapped to the little finger. For programmer dvorak these keys are swapped, so this is of no consequence.",
        },
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });

});
