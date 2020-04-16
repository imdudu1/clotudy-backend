class Clotudy {
    constructor(ws_room_id, class_id, lecture_id, ppt_dom, qna_box_dom) {
        // 전역 정보 설정
        this.ROOT_URL = window.location.host;
        this.WEBSOCKET_PATH = 'ws/cloredis';

        // 전역 정보 변수
        this.ws_room_id = ws_room_id;
        this.class_id = class_id;
        this.lecture_id = lecture_id;

        // Websocket 설정
        this.ws_global_onmessage_callback_array = [];
        this.ws_global_onclose_callback_array = [];
        this.ws_global_onerror_callback_array = [];
        this.websocket_setup();

        // PPT 설정 관련 변수
        this.current_ppt_page_num = 1;
        this.ppt_sync_lock = true;
        this.ppt_dom = ppt_dom;

        // 질문 메세지 관련 변수
        this.exist_new_qna_message = false;
        this.qna_box_dom = qna_box_dom;
    }

    websocket_setup() {
        this.ws = new WebSocket(`ws://${this.ROOT_URL}/${this.WEBSOCKET_PATH}/${this.ws_room_id}/`);
        this.ws.onmessage = (packet) => {
            let {data} = JSON.stringify(packet);
            if ( !(this.default_ws_handler(data)) ) {
                for (let i = 0; i < this.ws_global_onmessage_callback_array.length; i++) {
                    this.ws_global_onmessage_callback_array[i](data);
                }
            }
        }
        this.ws.onclose = (err) => {
            for (let i = 0; i < this.ws_global_onclose_callback_array.length; i++) {
                this.ws_global_onclose_callback_array[i](err);
            }
        }
        this.ws.onerror = (err) => {
            for (let i = 0; i < this.ws_global_onerror_callback_array.length; i++) {
                this.ws_global_onerror_callback_array[i](err);
            }
        }
    }

    // 콜백 등록 함수
    add_onmessage_callback(fn) {
        this.ws_global_onmessage_callback_array.push(fn);
    }

    add_onclose_callback(fn) {
        this.ws_global_onclose_callback_array.push(fn);
    }

    add_onerror_callback(fn) {
        this.ws_global_onerror_callback_array.push(fn);
    }

    // 수업에서 활용되는 공통 액션에 대한 핸들러와 함수
    default_ws_handler(data) {
        let {action} = data;
        switch (action) {
            case 'sync-ppt-page':
                let {page} = data;
                this.sync_ppt_page(page);
                break;
            case 'live-qna-chat':
                let {content, lecture} = data;
                this.add_qna_message(content, lecture);
                break;
            case 'add-like-count':
                let {msgid, lecture} = data;
                this.
                break;
            case 'show-quiz-modal':
                break;
            default:
                return false;
        }
        return true;
    }

    sync_ppt_page(page) {
        if ( !this.ppt_sync_lock ) {
            return;
        }
        this.ppt_sync_lock = false; // LOCK
        let ppt_max_page = this.ppt_dom.contentWindow.PDFViewerApplication.pagesCount;
        if ( 0 < page || page < ppt_max_page ) {
            this.ppt_dom.contentWindow.PDFViewerApplication.page = page
        }
        this.ppt_sync_lock = true; // UNLOCK
    }

    add_qna_message(content, lecture) {
        if (content === '') {
            return;
        }
        this.exist_new_qna_message = true;
    }
}
