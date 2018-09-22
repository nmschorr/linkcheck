
function doesFileExist(urlToFile) {
    var xhr = new XMLHttpRequest();
    xhr.open('HEAD', urlToFile, false);
    xhr.send();

    if (xhr.status == "404") {
        return false;
    } else {
        return true;
        console.log("perfect");
        location.reload(true);
    }
}

//function refreshData() {
//    x = 5;  // 5 Seconds
//    console.log("howdy");
//    setTimeout(refreshData, x*1000);
//}

function keepchecking() {
    x = 7;  // 5 Seconds
    console.log("in keepchecking");
    setTimeout(checkRefrsh, x*1000);
}


//function checkAndRefresh(){
//        var done_file = 'http://127.0.0.1:8080/static/res20180919150343.htmldone';
//        var result = doesFileExist(tfile);
//
//        if (result == true) {
//                console.log("yay, file exists!");
//                location.reload(true);
//
//            // yay, file exists!
//        } else {
//                 console.log("file does not exist!");
//           // file does not exist!
//        }
//}
