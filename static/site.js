$.when($.ready).then(function() {
    $(".img_btn").click(img_btn_click);
    $(".door_btn").click(door_btn_click);
    $("#btn-all-parts").click(all_parts_click);
    $("#btn-none-parts").click(none_parts_click);
});

function post(url, params) {
    return $.ajax({
        method: 'POST',
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: url,
        data: JSON.stringify(params)
    })
}

function none_parts_click(){
    $(".participant").each(function(i, img) {
        img.classList.remove('selected');
        img.classList.add('unselected');
    });
    calc_parts_root();
}

function all_parts_click(){
    $(".participant").each(function(i, img) {
        img.classList.remove('unselected');
        img.classList.add('selected');
    });
    calc_parts_root();
}

function calc_parts_root() {
    var parts = get_participants();
    post('/calc_root', {participants: parts}).then(function(resp) {
        $('.root_result')[0].textContent = resp.root;
    });
}

function img_btn_click(){
    if (this.classList.contains('participant')) {
        participant_click(this);
    }
    calc_parts_root();
}

function participant_click(img) {
    if (img.classList.contains('selected')) {
        img.classList.remove('selected');
        img.classList.add('unselected');

    } else {
        img.classList.remove('unselected');
        img.classList.add('selected');
    }

}

function door_btn_click(evt){
    var d = evt.currentTarget.textContent;
    var parts = get_participants();
    post('/list_parts', {participants: parts, door: d}).then(function(resp) {
        $('.div-list-parts').html(resp.html);
        $('.door_num')[0].textContent = resp.door;
    });
}

function get_participants() {
    var participants = [];
    $(".participant").each(function(i, img) {
        if (img.classList.contains('selected')) {
            participants.push(img.alt);
        }
    });
    return participants;
}