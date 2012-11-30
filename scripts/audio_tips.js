



$(document).ready(function(){
    $('.qtbase').qtip({
        style: {
            classes: 'ui-tooltip-rounded ui-tooltip-shadow',
        },
        show: {
	    solo: true
	}
    });



    $('.ignorecase').qtip({
        content: {
            text:'The case of the field name is ignored, so “expression”' +
'“FRONT” “bACk” &c. will all work.',
        }
    });


    $('#fourth').qtip({
        content: {
            text:'A fourth way is to change the default_audio_language code ' +
                'in the file "downloadaudio/language.py" in the addons folder.',
        },
    });

    $('.profload').qtip({
        content: {
            text:'This happens when the profile is loaded, and once per user.',
        }
    });

    $('.nolangcode').qtip({
        content: {
            text:'This will apear until the language code is set for the default deck.'
        }
    });

    $('.hanzipinyin').qtip({
        content: {
            text:'At the moment the Chinese support add-on stores everything including the pinyin in a single field called Hanzi.'
        }
    });


    $('.morefields').qtip({
        content: {
            text:'The model actually has even more fields, i skip a few that are not relevant here.'
        }
    });


    $('.orfirst').qtip({
        content: {
            text:'This method can be used for the first field, too.'
        }
    });

    $('.sendicons').qtip({
        content: {
            text:'I am not perfectly happy with some of the icons i use. If you have better ones, please let me know.'
        }
    });

    $('.tu').qtip({
        content: {
            text:'Technische Universität, university of technology.'
        }
    });

    $('.sonya').qtip({
        content: {
            text:'It get<em>s on ya</em> nerves. Apologies to all people named Sonya.'
        }
    });

});
