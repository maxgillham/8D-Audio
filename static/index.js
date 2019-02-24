$("#convert").click(function(){
    $("#error").html("");
    const link = $(".input").val();
    if(!link){
        $("#error").html("field can't be empty");
        $(".input").select();
        return;
    }
    var regex = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
    var match = link.match(regex);
    if(match == null){
        $("#error").html("enter a valid youtube link");
        return;
    }
    // start converting here, convert(link)
    $.post( "/convert", {
    url: link
    }).done(function(){
      $("#after_convert").css("display","block");
      $("#before_convert").removeClass("animated fadeIn");
      $("#after_convert").addClass("animated fadeIn");
      $("#before_convert").css("display","none");
    });
    $(".input").css("display","none");
    $(".input").val("");
    $("#convert").css("display","none");
    $("#spinner").css("display","inherit");
});

$("#again").click(function(){
    document.getElementById("playa").load()
    $(".input").css("display","block");
    $("#convert").css("display","block");
    $("#before_convert").css("display","block");
    $("#before_convert").addClass("animated fadeIn");
    $("#after_convert").css("display","none");
    $("#after_convert").removeClass("animated fadeIn");
    $("#spinner").css("display","none");
});

// use this when its done converting not setTimeout :)
function done() {
    $("#after_convert").css("display","block");
    $("#before_convert").removeClass("animated fadeIn");
    $("#after_convert").addClass("animated fadeIn");
    $("#before_convert").css("display","none");
}

$("#fork").click(function(){
    window.location.href = "https://github.com/maxgillham/8D-Audio";
})

setTimeout(function(){
    $("#loading").addClass("animated fadeOut");
    setTimeout(function(){
        $("#loading").removeClass("animated fadeOut");
        $("#loading").css("display","none");
    },800);
},3000);
