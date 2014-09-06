var DL = DL || {},
    tabName,
    thisTab;

DL.buttonClick = function() {
    thisTab = $(this).attr('id').slice(0, -4);
    // slicing off '-btn'

    for (var i=0; i<DL.tabs.length; i++) {
        if (thisTab === DL.tabs[i]) {
            DL[thisTab + 'Btn'].attr('class', 'btn btn-success');
            DL[thisTab].show();
        } else {
            DL[DL.tabs[i] + 'Btn'].attr('class', 'btn btn-primary');
            DL[DL.tabs[i]].hide();
        }
    }
    if (thisTab === 'scrapbook' && typeof DL.iframe.attr("src") === 'undefined') {
        DL.iframe.attr("src", "//storify.com/vprnet/dorothy-s-list-scrapbook/embed?border=false");
        $('#iframe_script').attr('src', "//storify.com/vprnet/dorothy-s-list-scrapbook.js?border=false");
    }
};

DL.iframe = $('iframe#storify');
DL.tabs = ['books', 'about', 'scrapbook'];
for (var i=0; i<DL.tabs.length; i++) {
    tabName = DL.tabs[i];
    DL[tabName] = $('#' + tabName);
    DL[tabName + 'Btn'] = $('#' + tabName + '-btn');
    DL[tabName + 'Btn'].on("click", DL.buttonClick);
}
