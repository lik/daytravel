//function shows and hides more options under the plan page
function showOptions(topic) {
    var x = document.getElementById(topic);
    if (x.style.display === 'block') {
        x.style.display = 'none';
    } else {
        x.style.display = 'block';
    }
}
