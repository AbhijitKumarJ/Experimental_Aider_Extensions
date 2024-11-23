// custom_aider/gui/templates/cmd_explain_tmpl/script.js
mermaid.initialize({startOnLoad: true, theme: 'neutral'});

function openTab(evt, tabName) {
    var tabcontents = document.getElementsByClassName("tab-content");
    for (var i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }
    
    var tabs = document.getElementsByClassName("tab");
    for (var i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }
    
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Open first tab by default
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.tab').click();
});