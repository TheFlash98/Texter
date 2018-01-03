chrome.runtime.onMessage.addListener(function (msg, sender,sendResponse) {
    console.log("content js loaded");
    if (msg.text === 'report_back') {
        var phone;
        $('.ci-phone > ul > li').each(function() { 
            phone = $(this).find(".pv-contact-info__contact-item").text();
        });

        var textcontent = $('.postArticle-content > section > .section-content > div')[0].innerText;
        console.log(textcontent);

        /*var postData = {
            "name" : $('.pv-top-card-section__name').text(),
            "designation" : $('.pv-top-card-section__headline').text(),
            "company" : $('.pv-top-card-section__company').text(),
            "email": $('.ci-email > div').find(".pv-contact-info__contact-item").text(),
            "phone" : phone,
            "linkedin" : $('.ci-vanity-url > div').find(".pv-contact-info__contact-item").text(),
            "address" : $('.ci-address > div').text()
        };*/
        var postData = {
            "textcontent" : textcontent, 
        };

        console.log($('.pv-top-card-section__name').text());
        console.log($('.ci-vanity-url > div').find(".pv-contact-info__contact-item").text());
        console.log($('.ci-email > div').find(".pv-contact-info__contact-item").text());
		console.log(phone);

        serializedData = $.param(postData);
        sendResponse(serializedData);
    }
});