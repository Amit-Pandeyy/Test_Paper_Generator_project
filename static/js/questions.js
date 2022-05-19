function filter_by_difficulty(difficulty) {

    var is_checked = document.getElementById(difficulty).checked;
    var cards = document.getElementsByClassName("card-" + difficulty);
    if (is_checked) {
        for (item of cards) {
            item.style.display = 'block';
        }

    }
    else {
        for (item of cards) {
            item.style.display = 'none';
        }
    }

}

function get_questions(topic_id, topic_name) {
    var is_checked = document.getElementById('topic-' + topic_id).checked;
    if (is_checked) {
        if (localStorage['topicObject']) {
            var topicObject = JSON.parse(localStorage.getItem('topicObject'))
        }
        else {
            var topicObject = {}
        }
        topicObject[topic_id] = topic_name;
        localStorage.setItem('topicObject', JSON.stringify(topicObject));

        $.ajax({
            type: 'GET',
            url: "/question_topic_selector",
            data: {
                topic_id: topic_id,
            },
            success: function (data) {
                var ques_str = ""
                JSON.parse(data.questions).forEach(item => {
                    var que = item.fields
                    ques_str +=
                        `
                        <li class="col-span-1 flex flex-col text-center bg-white rounded-lg shadow divide-y divide-gray-200">
                        <div class="flex-1 flex flex-col p-8">
                            <p class="font-medium">${que.title}</p>
                          <dl class="mt-1 flex-grow flex flex-col justify-between">
                            <dd class="mt-3">
                              <span class="px-2 py-1 text-green-800 text-xs font-medium bg-green-100 rounded-full">${que.hardness}</span>
                            </dd>
                          </dl>
                          <p class="h-72 text-clip overflow-hidden mt-4">
                            ${que.text}
                          </p>
                        </div>
                        <div>
                          <div class="-mt-px flex divide-x divide-gray-200">
                            <div class="w-0 flex-1 flex">
                              <a href="mailto:janecooper@example.com" class="relative -mr-px w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-bl-lg hover:text-gray-500">
                                <span class="ml-3">See More</span>
                              </a>
                            </div>
                            <div class="-ml-px w-0 flex-1 flex">
                              <a href="tel:+1-202-555-0170" class="relative w-0 flex-1 inline-flex items-center justify-center py-4 text-sm text-gray-700 font-medium border border-transparent rounded-br-lg hover:text-gray-500">
                                <span class="ml-3">Add to Paper</span>
                              </a>
                            </div>
                          </div>
                        </div>
                      </li>
                                
                `
                })
                var previous = document.getElementById('question_container').innerHTML
                document.getElementById('question_container').innerHTML = `
                <h2>${topic_name}</h2>
                <ul role="list" id = 'topicDiv-${topic_id}' class="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4" style=display:${document.getElementById(que.hardness).checked ? 'block' : 'none'}>
                            ${ques_str}
                        </ul>
                ${previous}
                `
            }
        })
    }
    else {
        var myobj = document.getElementById(`topicDiv-${topic_id}`);
        myobj.remove();
        var topicObject = JSON.parse(localStorage.getItem('topicObject'))
        delete topicObject[topic_id]
        localStorage.setItem('topicObject', JSON.stringify(topicObject));
    }
}


$(document).on("click", '.remove_from_cart', function (event) {
    var id = $(this).attr("pid").toString();
    eml = this.parentNode
    $.ajax({
        type: "GET",
        url: "/paper/remove_paper/",
        data: {
            que_id: id
        },
        success: function (data) {
            if (data.is_valid) {
                eml.innerHTML = `<button class="btn1542 add_to_cart" pid="${id}">Add to Paper</button>`
                x = document.getElementById('cart_items_count').innerText
                document.getElementById('cart_items_count').innerText = parseInt(x) - 1
                alert("Question Removed Successfully!");
            }
            else {
                alert("Something went wrong");
            }

        }
    })
})


$(document).on("click", '.add_to_cart', function (event) {
    var id = $(this).attr("pid").toString();
    eml = this.parentNode
    $.ajax({
        type: "GET",
        url: "/paper/add_to_paper/",
        data: {
            que_id: id
        },
        success: function (data) {
            if (data.is_valid) {
                eml.innerHTML = `<button style="background-color: blue;"  class="btn1542 remove_from_cart" pid="${id}">Click to Remove</button>`
                x = document.getElementById('cart_items_count').innerText
                document.getElementById('cart_items_count').innerText = parseInt(x) + 1
                alert("Question Added Successfully!");
            }
            else {
                alert("Something went wrong");
            }

        }
    })
})

window.onload = function displayQuestions() {

    var topicObject = JSON.parse(localStorage.getItem('topicObject'));
    localStorage.clear();
    for (const key in topicObject) {
        document.getElementById('topic-' + key).checked = true
        get_questions(key, topicObject[key]);
    }
}

$(document).on("click", '.modal-question', function (event) {
    var id = $(this).attr("pid").toString();
    eml = this.parentNode
    $.ajax({
        type: "GET",
        url: "/paper/get_question/",
        data: {
            que_id: id
        },
        success: function (data) {
            question = JSON.parse(data.question)
            question = question[0].fields.text;

            options = JSON.parse(data.options)
            solution = JSON.parse(data.solution)

            if (options.length > 0) {
                question += "<h2>Options</h2>"
                options.forEach(item => {
                    question += item.fields.option
                })
            }
            if (solution) {
                question += "<h2>Solution</h2>"
                question += solution[0].fields.text
            }
            document.getElementById('question-modal-body').innerHTML = question
        }
    })
})