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

$(function() {
    // setTimeout() function will be fired after page is loaded
    // it will wait for 5 sec. and then will fire
    // $("#successMessage").hide() function
    
    setTimeout(function(){ $('#successMessage').hide(); }, 5000);
});