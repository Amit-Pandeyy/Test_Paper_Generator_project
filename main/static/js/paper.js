$('.remove_paper').click(function () {

    var id = $(this).attr("qid").toString();
    var eml = this

    $.ajax({
        type: "GET",
        url: "/paper/remove_paper",
        data: {
            que_id: id
        },
        success: function (data) {
            // document.getElementById('total_questions').innerText = data.totalitem
            // document.getElementById('total_marks').innerText = data.total_marks
            // document.getElementById('points').innerText = data.points
            eml.parentNode.parentNode.parentNode.parentNode.parentNode.remove()
            // x = document.getElementById('cart_items_count').innerText
            // document.getElementById('cart_items_count').innerText = parseInt(x)-1
            alert("Question Removed Successfully!");
        }
    })
})

$('.plus-paper').click(function(){    
    var id = $(this).attr("qid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/paper/increase_marks",
        data:{
            que_id : id
        },
        success: function(data){
            if(data.is_valid){
                eml.innerText = data.marks
                marks = parseInt(document.getElementById('total_marks').innerText)
                document.getElementById('total_marks').innerText=marks+1
            }
            
        }
    })
})

$('.minus-paper').click(function(){
    var id = $(this).attr("qid").toString();
    var eml = this.parentNode.children[2];

    $.ajax({
        type: "GET",
        url: "/paper/decrease_marks",
        data:{
            que_id : id
        },
        success: function(data){
            if(data.is_valid){
                eml.innerText = data.marks
                marks = parseInt(document.getElementById('total_marks').innerText)
                document.getElementById('total_marks').innerText=marks-1
            }
            
        }
    })
})
