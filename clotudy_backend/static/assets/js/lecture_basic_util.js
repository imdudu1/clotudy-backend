let qna_messages;
let lecture_id;
let user_name;

function quiz_form_submit() {
    document.getElementById("quiz_form").submit();
}

// WebSocket
let current_ppt_page = 1;
let ppt_sync_flag = true;
let is_exist_new_qna = true;

function remoteSyncPPTPage(data) {
    if (!ppt_sync_flag) {
        return;
    }

    ppt_sync_flag = false;
    let page = data['data']['page'];
    let numPages = document.getElementById("ppt-frame").contentWindow.PDFViewerApplication.pagesCount;
    if((page > numPages) || (page < 1)){
        return;
    }
    document.getElementById("ppt-frame").contentWindow.PDFViewerApplication.page = page;
    ppt_sync_flag = true;
}

function liveQnAMessage(request) {
    let qna = request['data']['qna'];

    if (qna === '') {
        return
    }

    let qna_body = qna['body'];
    let qna_like_count = request['data']['likeCount'];
    let qna_message_id = request['data']['messageId'];
    let qna_username = request['data']['userID'];
    qna_messages.push({'body': qna_body, 'likeCount': qna_like_count, 'messageId': qna_message_id, 'userID': qna_username});
    is_exist_new_qna = true;

    let live_qna_chat_box = $('#live-qna-chat-content');
    live_qna_chat_box.append(questionMsgHtmlGenerator(qna_body, qna_like_count));
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
        $('#live-qna-chat-box').append(questionMsgHtmlGenerator(message['body'], message['likeCount']));
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

function showQuizModal(data) {
    axios.get(`/api/quiz/${data.data.classID}/${data.data.quizBoxId}`)
        .then(res => {
            setModalQuizHTML(res.data[0]);
            $("#exampleModalCenter").modal("show");
        })
        .catch(err => {
            console.log(err);
        });
}

let chatSocket;
function ws_connect() {
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
            case 'show-quiz-modal':
                showQuizModal(message_data);
                break;
            default:
                break;
        }
    };

    chatSocket.onclose = (e) => {
        setTimeout(() => {
            ws_connect();
        }, 1000);
    };

    chatSocket.onerror = (err) => {
        chatSocket.close();
    }
}
ws_connect();

function questionMsgHtmlGenerator(msg, like_count) {
    return 
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
                $("<p>").text(msg),
                $("<div>").addClass("d-flex justify-content-start align-items-center mb-1").append(
                    $("<p>").addClass("ml-auto d-flex align-items-center").append(
                        $("<i>").addClass("feather icon-message-square font-medium-2 mr-50")
                    ).append(like_count)
                )
            )
        ); 
}

function sendQuestionMessagePacket(message) {
    chatSocket.send(JSON.stringify({
        'action': 'live-qna-chat',
        'data': {
            'qna': {
                'body': message,
            },
            'lecture': lecture_id,
        }
    }));
}

function addLikeCount(id) {
    chatSocket.send(JSON.stringify({
        'action': 'add-like-count',
        'data': {
            'messageId': id, // QnAMessage.pk
            'lecture': lecture_id,
        }
    }));
}

function lecture_init(id, messages, username) {
    lecture_id = id;
    qna_messages = messages;
    user_name = username;
}
