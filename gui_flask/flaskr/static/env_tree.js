
window.onload = function() {
    var anchor_code;
    var anchor_id;
    var object;
    var scroll_top;
    var rect_viewport;
    var top;

    anchor_code = window.location.hash;

    if (anchor_code == "") {
        return;
    }

    anchor_id = anchor_code.substring(1);
    object = document.getElementById(anchor_id);
    scroll_top = window.pageYOffset || document.documentElement.scrollTop;
    rect_viewport = object.getBoundingClientRect();
    top = rect_viewport.top + scroll_top - (window.innerHeight / 2);

    window.scrollTo({
        top: top,
        behavior: 'smooth'
    });

    object.classList.add("req_poped_up");

    console.log("style added to poped up requirement");
};
