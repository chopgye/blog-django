$(document).ready(function () {
    $('.vote').click(function (e) {
        var id = $(this).data("id"); //get data-id
        var vote_type = $(this).data("vote"); //get data-vote
        var voteURL = $(this).attr("data-url");
        var content_type = $(this).data("content_type")
        var csrf = $("[name='csrfmiddlewaretoken']").val();

        console.log("post id:" + id)
        console.log("vote_type: " + vote_type)
        console.log("vote url: " + voteURL)
        console.log("content type: " + content_type)

        e.preventDefault();
        
        $.ajax({
            url: voteURL,           
            type: 'POST',
            data: {
                'id': id,
                'vote_type':vote_type,
                'content_type':content_type,
                'csrfmiddlewaretoken': csrf
            },
            success: function(data){

            console.log(data)
            console.log("post upvotes: " + data['post_upvotes'])
            console.log("post downvotes: " + data['post_downvotes'])
            console.log("total vote count: " + data['vote_count'])
            console.log("post favorites: " + data['post_favorites'])


                $(".vote_count"+ id).html(data.vote_count + " Votes"); 
                $(".up"+ id).html(data['post_upvotes'])    
                $(".down"+  id).html(data['post_downvotes'])    
                $(".favorite"+ id).html(data['post_favorites'])    
                
                console.log("post id after :" + id)
                
            }
        });
    });
});