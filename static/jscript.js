

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

function checkAndRefresh(){
        var tfile = 'http://127.0.0.1:8080/static/res20180919150343.htmldone';
        var result = doesFileExist(tfile);

        if (result == true) {
                console.log("yay, file exists!");
                location.reload(true);

            // yay, file exists!
        } else {
                 console.log("file does not exist!");
           // file does not exist!
        }
}

function refreshData() {
    x = 5;  // 5 Seconds
    console.log("howdy");
    setTimeout(refreshData, x*1000);
}
//   refreshData(); // execute function

function keepchecking() {
    x = 7;  // 5 Seconds
    console.log("in keepchecking");
    setTimeout(checkAndRefresh, x*1000);
}


