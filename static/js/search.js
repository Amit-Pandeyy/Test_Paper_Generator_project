    // Get the modal
    var modal = document.getElementById("myModal");

    // Get the button that opens the modal
    var btn = document.getElementById("search_questions_base");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks on the button, open the modal 
    btn.onclick = function () {
        modal.style.display = "block";
        var input = document.getElementById('search_questions');
        input.focus();
        input.select();
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
        document.getElementById('question_container').innerHTML="";
        var topicObject = JSON.parse(localStorage.getItem('topicObject'));
        localStorage.clear();
        for (const key in topicObject) {
            document.getElementById('topic-' + key).checked = true
            get_questions(key, topicObject[key]);
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }



    $(document).ready(function () {
        jQuery('#search_questions').on('input propertychange paste', function () {

            query = document.getElementById('search_questions').value

           if(query.length>0){

            $.ajax({
                type: "GET",
                url: `/search_questions/${chapter_id}`,
                data: {
                    query: query
                },
                success: function (data) {

                    questions = JSON.parse(data.questions)
                    
                    if (questions.length > 0) {

                        var ques_str = ""
                        questions.forEach(item => {
                            var que = item.fields
                            ques_str +=
                                `
            <div class="col-xl-3 col-lg-4 col-md-6 question">
                                <div class="fcrse_1 mt-30" >
                                    <div class="tutor_content_dt">
                                        <div class="tutor150">
                                            <a href="instructor_profile_view.html" class="tutor_name">${que.title}</a>
                                            <div class="mef78" title="Verify">
                                                <i class="uil uil-check-circle"></i>
                                            </div>
                                        </div>
                                        <div class="tutor_cate">${que.hardness}</div>
                                        <a>
                                        ${data.paper.includes(item.pk) ?
                                    `<button style="background-color: blue;"  class="btn1542 remove_from_cart" pid="${item.pk}">Click to Remove</button>` : `<button class="btn1542 add_to_cart" pid="${item.pk}">Add to Paper</button>`}
                                  
                                  </a>
                                  <div class="tut1250 modal-question" style="height:240px !important; overflow:hidden; cursor:pointer;" pid="${item.pk}" style="overflow: hidden; cursor:pointer" class="btn btn-primary" data-toggle="modal" data-target="#exampleModalCenter">
                                            <span class="vdt15" style="margin-top:30px;>${que.text}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <br><br>
                            
            `
                        })
                        document.getElementById('question_container_modal').innerHTML = `
                    <div class='row'>
                        ${ques_str}
                    </div>
            `
                    }
                    else {
                        document.getElementById('question_container_modal').innerHTML = `
                    <h2 style="margin-top: 30px;">No results matching your query!</h2>
                `
                    }


                }
            })




           }
           else{
            document.getElementById('question_container_modal').innerHTML = `
                    <h2 style="margin-top: 30px;">Type to start searching</h2>
                `

           }
        });
    });