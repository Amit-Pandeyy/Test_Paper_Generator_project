$('.plus-credit').click(function () {
    var username = $(this).attr("tid").toString();
    var eml_teacher = this.parentNode.parentNode.parentNode.children[2];
    var increase_value = document.getElementById('increase_value_' + username).value
    console.log("jgjhgjhgjhghj")

    $.ajax({
        type: "GET",
        url: "/school_dashboard/increase_credits",
        data: {
            username: username,
            increase_value: increase_value,
        },
        success: function (data) {
            if (data.is_valid) {
                eml_teacher.innerText = data.teacher_credits
                document.getElementById('school_credits').innerText = data.school_credits
                alert("Credits Added Successfully!");
            }
            else {
                alert("Something went wrong");
            }

        }
    })
})