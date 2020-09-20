$(document).ready(function(){

  console.log("Working");

  var toggleSection = function(triggerId, contentBlockId){
    $(triggerId).click(function(){
      $(contentBlockId).slideToggle("slow");
      console.log("Triggered");
    });
  }

  toggleSection('#changeViewTrigger', '#changeView');

});
