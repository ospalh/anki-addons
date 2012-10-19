



$(document).ready(function(){

    $('.ignorecase').qtip({
        content: {
            text:'The case of the field name is ignored, so “expression”' +
'“FRONT” “bACk” &c. will all work.',
        },
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });

});
