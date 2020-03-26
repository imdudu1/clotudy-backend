const unique_id = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

function setModalQuizHTML(data) {
    $("#modal-body").empty();
    $("#exampleModalCenterTitle").empty();

    $("#modal-nav-wrap").empty();
    $("#modal-content-header").empty();
    $("#modal-nav-content-wrap").empty();

    $("#modal-content-header").append(
        $("<h5>").addClass("modal-title").attr("id", "exampleModalCenterTitle").text(data.category_title),
        $("<button>").attr("type", "button").addClass("close").attr("data-dismiss", "modal").attr("aria-label", "Close").append(
            $("<span>").attr("aria-hidden", "true").text("X")
        )
    );

    let prob_count = 1;
    for (let quiz_obj of data.quiz_content) {
        $("#modal-nav-wrap").append(
            $("<li>").addClass("nav-item").append(
                $("<a>").addClass("nav-link " + ((prob_count === 1) ? "active" : ""))
                        .attr("id", "baseVerticalLeft-tab" + prob_count)
                        .attr("data-toggle", "tab")
                        .attr("aria-controls", "tabVerticalLeft" + prob_count)
                        .attr("href", "#tabVerticalLeft" + prob_count)
                        .attr("role", "tab")
                        .attr("aria-selected", (prob_count === 1) ? "true" : "false")
                        .text("문제" + prob_count)
            )
        );

        $("#modal-nav-content-wrap").append(
            $("<div>").addClass("tab-pane " + ((prob_count === 1) ? "active" : ""))
                        .attr("id", "tabVerticalLeft" + prob_count)
                        .attr("role", "tabpanel")
                        .attr("aria-labelledby", "baseVerticalLeft-tab" + prob_count)
                        .append(
                            $("<p>").text(quiz_obj.problem),
                            $("<hr />"),
                            $("<ul>").addClass("list-unstyled mb-0").append(
                                $("<fieldset>").append(
                                    () => {
                                        let ret = [];
                                        for (let answer_obj of quiz_obj.answer) {
                                            ret.push(
                                                $("<li>").addClass("mr-2").append(
                                                    $("<div>").addClass("vs-radio-con vs-radio-success").append(
                                                        $("<input>").attr("type", "radio").attr("name", quiz_obj.id).attr("value", answer_obj.id),
                                                        $("<span>").addClass("vs-radio").append(
                                                            $("<span>").addClass("vs-radio--border"),
                                                            $("<span>").addClass("vs-radio--circle")
                                                        ),
                                                        $("<span>").text(answer_obj.content)
                                                    )
                                                )
                                            )
                                        }
                                        return ret;
                                    }
                                )
                            )
                        )
        );
        prob_count += 1;
    }
} 

function showQuizModal(data) {
    axios.get(`/api/quiz/${data.data.classID}/${data.data.quizBoxId}`)
        .then(res => {
            setModalQuizHTML((res.data)[0]);
            $("#exampleModalCenter").modal("show");
        })
        .catch(err => {
            console.log(err);
        });
}
