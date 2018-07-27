$(".deleteButton").on("click", function(e){
  $.ajax({
    type: "POST",
    url: "/delete",
    data: {data: e.target.name},
    success: function() {
      console.log("SUCCESS");
      $("#"+e.target.name).remove();
    },
  });
});
