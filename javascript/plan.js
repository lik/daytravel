//function shows and hides more options under the plan page
function showOptions(topic) {
    var x = document.getElementById(topic);
    if (x.style.display === 'none') {
        x.style.display = 'block';
    } else {
        x.style.display = 'none';
    }
}
