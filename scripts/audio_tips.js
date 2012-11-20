



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


    $('#fourth').qtip({
        content: {
            text:'A fourth way is to change the default_audio_language code ' +
                'in the file "downloadaudio/language.py" in the addons folder.',
        },
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });

    $('.profload').qtip({
        content: {
            text:'Actually this happens when the profile is loaded, and once per user.',
        },
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });

});
