class ClotudyWS {
    constructor(ws_room_id) {
        // 전역 정보 설정
        this.ROOT_URL = window.location.host;
        this.WEBSOCKET_PATH = 'ws/cloredis';

        this.temp_id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

        // 전역 정보 변수
        this.ws_room_id = ws_room_id;
    
        // Websocket 설정
        this.ws_global_onmessage_callback_array = [];
        this.ws_global_onclose_callback_array = [];
        this.ws_global_onerror_callback_array = [];
        this.websocket_setup();
    }

    websocket_setup() {
        this.ws = new WebSocket(`ws://${this.ROOT_URL}/${this.WEBSOCKET_PATH}/${this.ws_room_id}/`);
        this.ws.onmessage = (packet) => {
            let {action, data} = JSON.parse(packet.data);
            for (let i = 0; i < this.ws_global_onmessage_callback_array.length; i++) {
                this.ws_global_onmessage_callback_array[i](this, action, data);
            }
        }
        this.ws.onclose = (err) => {
            for (let i = 0; i < this.ws_global_onclose_callback_array.length; i++) {
                this.ws_global_onclose_callback_array[i](this, err);
            }
        }
        this.ws.onerror = (err) => {
            for (let i = 0; i < this.ws_global_onerror_callback_array.length; i++) {
                this.ws_global_onerror_callback_array[i](this, err);
            }
        }
    }

    // 콜백 등록 함수
    push_onmessage_callback(fn) {
        this.ws_global_onmessage_callback_array.push(fn);
    }

    push_onclose_callback(fn) {
        this.ws_global_onclose_callback_array.push(fn);
    }

    push_onerror_callback(fn) {
        this.ws_global_onerror_callback_array.push(fn);
    }

    // Sender
    send_qna_message(content) {
        this.ws.send(JSON.stringify({
            action: 'live-qna-message',
            data: {
                content,
                lecture: this.lecture_id
            }
        }));
    }

    send_like_count(message_id) {
        this.ws.send(JSON.stringify({
            action: 'add-like-count',
            data: {
                message_id,
                lecture: this.lecture_id
            }
        }));
    }

    send_quiz_complete_signal(quiz_id) {
        this.ws.send(JSON.stringify({
            action: 'quiz-complete-signal',
            data: {
                quiz_id
            }
        }));
    }

    send_new_idea(content) {
        this.ws.send(JSON.stringify({
            'action': 'add-idea-message',
            'data': {
                content,
                id: self.temp_id,
            }
        }));
    }

    send_new_group(content) {
        this.ws.send(JSON.stringify({
            'action': 'add-group-message',
            'data': {
                content,
                id: self.temp_id,
            }
        }));
    }

    send_move_node(src, des) {
        this.ws.send(JSON.stringify({
            'action': 'move-idea-message',
            'data': {
                src,
                des,
                id: self.temp_id,
            }
        }));
    }
};

class Clotudy extends ClotudyWS {
    constructor(ws_room_id, class_id, lecture_id, ppt_dom, qna_box_dom) {
        super(ws_room_id);
        this.push_onmessage_callback(this.default_onmessage_callback);

        // PPT 설정 관련 변수
        this.current_ppt_page_num = 1;
        this.ppt_sync_lock = true;
        this.ppt_dom = ppt_dom;

        // 질문 메세지 관련 변수
        this.exist_new_qna_message = false;
        this.qna_box_dom = qna_box_dom;
        this.question_message_store = [];

        // 수업 관련 변수
        this.class_id = class_id;
        this.lecture_id = lecture_id

        this.sync_ppt_page_callback = [this.sync_ppt_page];
        this.live_question_message_callback = [this.add_qna_message];
        this.add_like_count_callback = [this.add_like_count];
    }

    push_sync_ppt_page_callback(fn) {
        this.sync_ppt_page_callback.push(fn);
    }

    push_live_question_message_callback(fn) {
        this.live_question_message_callback.push(fn);
    }

    push_add_like_count_callback(fn) {
        this.add_like_count_callback.push(fn);
    }

    add_qna_message(self, data) {
        let {content, message_id, username, like_count} = data;
        if (data === '') {
            return;
        }
        self.question_message_store.push(
            {
                content,
                message_id,
                username,
                like_count
            }
        );
        self.exist_new_qna_message = true;
    }

    sync_ppt_page(self, data) {
        if ( !self.ppt_sync_lock ) {
            return;
        }
        self.ppt_sync_lock = false; // LOCK
        let {page} = data;
        let ppt_max_page = self.ppt_dom.contentWindow.PDFViewerApplication.pagesCount;
        if ( 0 < page || page < ppt_max_page ) {
            self.ppt_dom.contentWindow.PDFViewerApplication.page = page
        }
        self.ppt_sync_lock = true; // UNLOCK
    }

    add_like_count(self, data) {
        let {message_id} = data;
        for (let i = 0; i < self.question_message_store.length; i++) {
            if (self.question_message_store[i].message_id === message_id) {
                self.question_message_store[i].like_count += 1;
                break;
            }
        }
    }

    set_question_message(messages) {
        this.question_message_store = messages;
    }

    get_question_message() {
        return this.question_message_store;
    }

    // 수업에서 활용되는 공통 액션에 대한 핸들러와 함수
    default_onmessage_callback(self, action, data) {
        switch (action) {
            case 'sync-ppt-page':
                for (let i = 0; i < self.sync_ppt_page_callback.length; i++) {
                    self.sync_ppt_page_callback[i](self, data);
                }
                break;
            case 'live-qna-message':
                for (let i = 0; i < self.live_question_message_callback.length; i++) {
                    self.live_question_message_callback[i](self, data);
                }
                break;
            case 'add-like-count':
                for (let i = 0; i < self.add_like_count_callback.length; i++) {
                    self.add_like_count_callback[i](self, data);
                }
                break;
            case 'show-quiz-modal':
                let {qid} = data;
                showQuizModal(self, self.class_id, qid);
                break;
            default:
        }
    }
};

let cur_quiz_link_id = 0;
function showQuizModal(self, cid, qid) {
    cur_quiz_link_id = qid;
    axios.get(`/api/quiz/${cid}/${qid}`)
        .then(res => {
            setModalQuizHTML((res.data)[0]);
            $("#exampleModalCenter").modal("show");
        })
        .catch(err => {
            console.log(err);
        });
    self.send_quiz_complete_signal(qid);
}
