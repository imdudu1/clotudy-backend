// Utility functions.
function querySelectorAllArray(selector){
    return Array.prototype.slice.call(
        document.querySelectorAll(selector), 0
    );
}

function contains(a, b){
    return a.contains ?
        a !== b && a.contains(b) :
        !!(a.compareDocumentPosition(b) & 16);
}

let qna_messages;
let lecture_id;
let user_name;

// Dragula JS
let last_over_el_id;
let current_drop_el_id;
let drake = dragula(querySelectorAllArray('.dragula-container'),{
                accepts: function (el, target, source, sibling) {
                    return !contains(el, target);
                }
            }).on('drag', function (el) {
                el.className = el.className.replace('ex-moved', '');
            }).on('drop', function (el) {
                el.className += ' ex-moved';
                current_drop_el_id = el.id;
                sendMoveIdeaPacket(current_drop_el_id, last_over_el_id);
            }).on('over', function (el, container) {
                container.className += ' ex-over';
                last_over_el_id = container.id;
            }).on('out', function (el, container) {
                container.className = container.className.replace('ex-over', '');
            });


// WebSocket
let increase_box_id = 0;
let current_ppt_page = 1;
let ppt_sync_flag = true;
let is_exist_new_qna = true;

function remoteSyncPPTPage(request) {
    if (!ppt_sync_flag) {
        return;
    }

    let page = request['data']['page'];
    let numPages = document.getElementById("ppt-frame").contentWindow.PDFViewerApplication.pagesCount;
    if((page > numPages) || (page < 1)){
        return;
    }
    document.getElementById("ppt-frame").contentWindow.PDFViewerApplication.page = page;
}

function liveQnAMessage(request) {
    let qna = request['data']['qna'];

    if (qna === '') {
        return
    }

    let qna_body = qna['body'];
    let qna_like_count = request['data']['likeCount'];
    let qna_message_id = request['data']['messageId'];
    let qna_userID = request['data']['userID'];
    qna_messages.push({'body': qna_body, 'likeCount': qna_like_count, 'messageId': qna_message_id, 'userID': qna_userID});
    is_exist_new_qna = true;

    let live_qna_chat_box = $('#live-qna-chat-box');
    live_qna_chat_box.append(
        $("<div>").addClass("card").append(
            $("<div>").addClass("card-body").append(
                $("<div>").addClass("d-flex justify-content-start align-items-center mb-1").append(
                    $("<div>").addClass("avatar mr-1").append(
                        $("<img>").attr("src", "{% static 'app-assets/images/profile/user-uploads/user-01.jpg' %}")
                                    .attr("alt", "avatar img holder")
                                    .attr("height", "45")
                                    .attr("width", "45")
                    ),
                    $("<div>").addClass("user-page-info").append(
                        $("<p>").addClass("mb-0").text(user_name),
                        $("<span>").addClass("font-small-2").text("Date 9999-99-99")
                    )
                ),
                $("<p>").text(qna_body),
                $("<div>").addClass("d-flex justify-content-start align-items-center mb-1").append(
                    $("<p>").addClass("ml-auto d-flex align-items-center").append(
                        $("<i>").addClass("feather icon-message-square font-medium-2 mr-50")
                    ).append(qna_like_count)
                )
            )
        )
    );
    live_qna_chat_box.scrollTop(live_qna_chat_box[0].scrollHeight);
}

function redrawSortingQnAChat() {
    if (!is_exist_new_qna) {
        return;
    } else {
        is_exist_new_qna = false;
    }

    $('#live-qna-chat-box').empty();
    qna_messages.sort((lhs, rhs) => {
        return rhs['likeCount'] - lhs['likeCount'];
    });

    qna_messages.forEach((message) => {
        $('#live-qna-chat-box').append(
            $("<div>").addClass("card").append(
                $("<div>").addClass("card-body").append(
                    $("<div>").addClass("d-flex justify-content-start align-items-center mb-1").append(
                        $("<div>").addClass("avatar mr-1").append(
                            $("<img>").attr("src", "{% static 'app-assets/images/profile/user-uploads/user-01.jpg' %}")
                                        .attr("alt", "avatar img holder")
                                        .attr("height", "45")
                                        .attr("width", "45")
                        ),
                        $("<div>").addClass("user-page-info").append(
                            $("<p>").addClass("mb-0").text(user_name),
                            $("<span>").addClass("font-small-2").text("Date 9999-99-99")
                        )
                    ),
                    $("<p>").text(message['body']),
                    $("<div>").addClass("d-flex justify-content-start align-items-center mb-1").append(
                        $("<p>").addClass("ml-auto d-flex align-items-center").append(
                            $("<i>").addClass("feather icon-message-square font-medium-2 mr-50")
                        ).append(message['likeCount'])
                    )
                )
            )
        );
    });
}
setInterval(redrawSortingQnAChat, 5000);

function updateLikeCount(data) {
    let message_id = data['data']['messageId'];
    for (let i = 0; i < qna_messages.length; i++) {
        if (qna_messages[i]['messageId'] === message_id) {
            qna_messages[i]['likeCount'] += 1;
            break;
        }
    }
}

function addIdeaMessage(request) {
    let body = request['data']['body'];
    const sender_id = request['data']['sender-id'];
    const box_id = sender_id + '-box-' + increase_box_id;
    $('#idea-dashboard').append(
        $("<p>").attr("style", "line-height: 14px; margin: 0;display: table-cell;vertical-align: middle;padding: 10px; border-radius: 5px;background: #f6f7f8;border: 2px solid #5a5d60;")
                .attr("id", box_id)
                .addClass("el")
                .text(body)
    );
    increase_box_id += 1;
}

function addGroupMessage(request) {
    const title = request['data']['group-title'];
    const sender_id = request['data']['sender-id'];
    const group_id = sender_id + '-group-' + increase_box_id;
    const container_id = sender_id + '-container-' + increase_box_id;;
    $('#idea-dashboard').append(
        $("<div>").attr("id", group_id).attr("style", "border: 2px solid #5a5d60;border-radius: 5px;padding: 3px;background: #f5cf8e;margin: 3px;").addClass("row").append(
            $("<div>").attr("style", "color: #565758;font-size: 14px;margin: 3px; font-weight: bold;").text(title),
            $("<div>").attr("id", container_id).attr("style", "min-height: 20px;border: 2px solid #5a5d60;border-radius: 5px;background: #b2d6ff;").addClass("dragula-container")
        )
    );
    drake.containers.push(document.getElementById(container_id));
    increase_box_id += 1;
}

function moveIdeaMessage(request) {
    if (unique_id === request['data']['sender-id']) {
        return;
    }
    let d = request['data'];
    let src = '#' + d['src'];
    let des = '#' + d['des'];
    $(src).appendTo(des);
}

function lockIdeaMessage(request) {

}

function removeIdeaMessage(request) {

}

let groupSocket;
function group_socket_connect() {
    groupSocket = new WebSocket('ws://' + window.location.host + '/ws/cloredis/samplegroupid/');

    groupSocket.onmessage = (message) => {
        let message_data = JSON.parse(message.data);
        switch (message_data.action) {
            case 'add-idea-message':
                addIdeaMessage(message_data);
                break;
            case 'move-idea-message':
                moveIdeaMessage(message_data);
                break;
            case 'lock-idea-message':
                lockIdeaMessage(message_data);
                break;
            case 'remove-idea-message':
                removeIdeaMessage(message_data);
                break;
            case 'add-group-message':
                addGroupMessage(message_data);
                break;
            default:
                break;
        }
    };

    groupSocket.onclose = (err) => {
        setTimeout(() => {
            group_socket_connect();
        }, 1000);
    };

    groupSocket.onerror = (err) => {
        groupSocket.close();
    };
}
group_socket_connect();

let chatSocket;
function chat_socket_connect() {
    chatSocket = new WebSocket('ws://' + window.location.host + '/ws/cloredis/sampleroomid/');

    chatSocket.onmessage = (message) => {
        let message_data = JSON.parse(message.data);
        switch (message_data.action) {
            case 'sync-ppt-page':
                remoteSyncPPTPage(message_data);
                break;
            case 'live-qna-chat':
                liveQnAMessage(message_data);
                break;
            case 'add-like-count':
                updateLikeCount(message_data);
                break;
            default:
                break;
        }
    };

    chatSocket.onclose = (e) => {
        setTimeout(() => {
            chat_socket_connect();
        }, 1000);
    };

    chatSocket.onerror = (err) => {
        chatSocket.close();
    };
}
chat_socket_connect();

function showAddQnAModal() {$("#addQnAModalCenter").modal("show");}
document.querySelector('#addqnatextarea').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#addQnAButton').click();
    }
};

// Packet senders.
document.querySelector('#addQnAButton').onclick = (error) => {
    let messageInputDom = document.querySelector('#addqnatextarea');
    let message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'action': 'live-qna-chat',
        'data': {
            'qna': {
                'body': message,
            },
            'lecture': lecture_id,
        }
    }));

    messageInputDom.value = '';
};

function sendLikeCountPacket(id) {
    chatSocket.send(JSON.stringify({
        'action': 'add-like-count',
        'data': {
            'messageId': id,
            'lecture': lecture_id,
        }
    }));
}

function showAddIdeaModal() {$("#addIdeaModalCenter").modal("show");}
function sendAddIdeaPacket() {
    let body = $("#addideatextarea").val();
    groupSocket.send(JSON.stringify({
        'action': 'add-idea-message',
        'data': {
            'body': body,
            'sender-id': unique_id,
        }
    }));
}

function showAddGroupModal() {$("#addGroupModalCenter").modal("show");}
function sendAddGroupPacket() {
    let title = $("#addgrouptextarea").val();
    groupSocket.send(JSON.stringify({
        'action': 'add-group-message',
        'data': {
            'group-title': title,
            'sender-id': unique_id,
        }
    }));
}

function sendMoveIdeaPacket(src, des) {
    groupSocket.send(JSON.stringify({
        'action': 'move-idea-message',
        'data': {
            'src': src,
            'des': des,
            'sender-id': unique_id,
        }
    }));
}

function lecture_init(id, messages, username) {
    lecture_id = id;
    qna_messages = messages;
    user_name = username;
}
