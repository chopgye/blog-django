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

            console.log(data);
            console.log(data.is_upvoted);
            console.log(data.is_downvoted);
            console.log("post upvotes: " + data['post_upvotes'])
            console.log("post downvotes: " + data['post_downvotes'])
            console.log("total vote count: " + data['vote_count'])
            console.log("post favorites: " + data['post_favorites'])
            console.log("is Upvoted: " + data['is_upvoted'])
            console.log("is Downvoted: " + data['is_downvoted'])
            console.log("is_favorited: " + data['is_favorited'])



                $(".vote_count"+ id).html(data.vote_count + " Votes"); 
                $(".up"+ id).html(data['post_upvotes'])    
                $(".down"+  id).html(data['post_downvotes'])    
                $(".favorite"+ id).html(data['post_favorites']) 
                
        

                    if (data['is_upvoted'] == true) { 
                        $(".upcolor" + id).css('fill', 'orange');
                    } else {
                        $(".upcolor" + id).css('fill', 'gray');
                    }

                    if (data['is_downvoted'] == true) { 
                        $(".downcolor"+ id).css('fill', 'blue');
                    } else {
                        $(".downcolor"+ id).css('fill', 'gray');
                    }

                    if (data['is_favorited'] == true) { 
                        $(".favcolor"+ id).css('fill', 'gold');
                    } else {
                        $(".favcolor"+ id).css('fill', 'gray');
                    }
                    
        

                
                console.log("post id after :" + id);
                
            }
        });
    });
});