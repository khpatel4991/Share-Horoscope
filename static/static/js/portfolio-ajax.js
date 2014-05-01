$(function(){

    $('#search').keyup(function() {
    
        $.ajax({
            type: "POST",
            url: "/suggestion/",
            data: { 
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
        
    });

});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search-results').html(data);
}

$("#option").change(function (){
              if(this.value == 3){
                   $("#strategy").removeAttr("disabled");
              }else{
           $("#strategy").attr("disabled", "true");
           }
           });

/*
$(function(){

    $('#list').click(function() {
    
        $.ajax({
            type: "POST",
            url: "/add-to-portfolio/",
            data: { 
                'user_id' : $('#list').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
        
    });

});

function searchSuccess(data, textStatus, jqXHR)
{
	$('#search-results').html(data);
}*/