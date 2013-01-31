



$(document).ready(function(){
    $('.qtbase').qtip({
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });



    $('.nakaguro').qtip({
        content: {
            text:'Also called middle dot, raised dot, 中黒 or, i presume, nakaguro.',
        }
    });

});
