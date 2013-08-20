



$(document).ready(function(){

    $('.or_replay_button').qtip({
        content: {
            text:"Or the play button from <a href=\"Play%20button.html\">the add-on</a>.",
        },
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

});
