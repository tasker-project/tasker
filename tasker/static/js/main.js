# 2020-09-19 18:16:30 -0700 - Emily Martens - add JS functionality, add change view front end controls and styles - lines:,6,7,8,9,10,11,12,13,14,15
# 2020-09-19 16:30:14 -0700 - Emily Martens - add task blueprint with routes to task detail - lines:,4,5,17,18
# 2020-09-19 20:04:43 -0700 - Emily Martens - add mobile navigation and home link - lines:,16
$(document).ready(function(){

  console.log("Working");

  var toggleSection = function(triggerId, contentBlockId){
    $(triggerId).click(function(){
      $(contentBlockId).slideToggle("slow");
      console.log("Triggered");
    });
  }

  toggleSection('#changeViewTrigger', '#changeView');
  toggleSection('#mobileNavTrigger', '#mobileNavContent');

});
