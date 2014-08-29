



$(document).ready(function(){
    $('.qtbase').qtip({
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	        solo: true
	    },
        hide: {
            delay: 500,
            fixed: true
        }
    });


    $('.andprofile').qtip({
        content: {
            text:"And the profile name, when there is more than one.",
        }
    });
    $('.orprofile').qtip({
        content: {
            text:"or profile",
        }
    });

});
