//var sheeturl = "https://script.google.com/macros/s/AKfycbzsj5VX09LxZHb_u9ExeGKVltVrKczSGAuwW0SimM4jlvxWO3LG/exec";
var sheeturl = "http://localhost:8000/learningaid";

function getCurrentTabId(callback) {

  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var id = tab.id;
    callback(id);
  });
}


function sendData(domContent) {
    console.log(domContent);

     $("#getdata").prop("disabled", true);

    request = $.ajax({
        url: sheeturl,
        type: "post",
        data: domContent,
        datatype: "json",
    });

    // Callback handler that will be called on success
    request.done(function (response, textStatus, jqXHR){
        // Log a message to the console
        console.log("Hooray, it worked!");
        console.log(response);
        console.log(textStatus);
        console.log(jqXHR);

        htmlcontent = "";
        for (var i = response.length; i >= 0; i--) {
            htmlcontent += "<img src='"+response[i]+"' /><br>";
        }
        $("#data").append(htmlcontent);
    });

    // Callback handler that will be called on failure
    request.fail(function (jqXHR, textStatus, errorThrown){
        // Log the error to the console
        console.error(
            "The following error occurred: "+
            textStatus, errorThrown
        );
    });

    // Callback handler that will be called regardless
    // if the request failed or succeeded
    request.always(function () {
        // Reenable the inputs
        $("#getdata").prop("disabled", false);
    });

}

$(document).ready(function() {

$("#getdata").click(function(){
    console.log("clicked");
    getCurrentTabId(function(tabID) {
    chrome.tabs.sendMessage(tabID, {text: 'report_back'}, sendData);
    });
});

});