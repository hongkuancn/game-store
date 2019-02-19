$(function(){
//generate a random number
var playerItems = new Array(1);
var n = playerItems.length;
for (var i = 0; i < n; i++){
    playerItems[i]=new Array(3);
}
var isClick = false;
var count = 1;
var score;
var load = false;
var num;
var hints;
var clickNum = 1;

var restart = document.getElementById("restart");
var start = document.getElementById("start");

// start game
start.addEventListener("click", Start);
function Start(){
    if(load){
        count = playerItems[0][0]+1;
        num = playerItems[0][2];
        submit.disabled = false;
        isClick = true;
    }
    else{
        num = Math.floor(Math.random()*21);
        isClick = true;
        submit.disabled = false;
        count = 1;
    }
       
}

// restart game
restart.addEventListener("click", Restart)
function Restart(){
    if(submit.disabled==false){
        var con = confirm("You can still play, are you sure you want to restart the game?");
        if(con==true){
            num = Math.floor(Math.random()*21);
            count=1;
            document.getElementById("input").value = "";
            document.getElementById('hints').innerHTML = "";
        }
    }
    else{
        num = Math.floor(Math.random()*21);
        submit.disabled == false;
        count = 1;
    }
}

// main game: use can only click the submit button ten times, each click 
// will receive corresponding responses
var submit = document.getElementById("submit");
submit.addEventListener("click", myFunction);
function myFunction(){
    var inNum = document.getElementById("input").value;
    var restCount = 10 - count;
    if(count<=10){
        if (clickNum==1&&isClick==false){
            alert("Please press Start Game first. Thank you!");
            clickNum++;
            submit.disabled=true;
        }
        else{
            if(inNum > num){
                hints = inNum+" is bigger, You have "+restCount+" times left.";		  
                document.getElementById('hints').innerHTML = hints;
                playerItems[0][0] = count;
                playerItems[0][1] = hints;
                playerItems[0][2] = num;
                count++;
            }
            if(inNum<num){  
                hints = inNum+" is smaller, You have "+restCount+" times left.";
                document.getElementById('hints').innerHTML = hints;
                playerItems[0][0] = count;
                playerItems[0][1] = hints;
                playerItems[0][2] = num;
                count++; 
            }
            if(inNum==num){   
                score = (restCount+1)*10;
                hints = "Great! You are right! You got "+score+" scores!";
                document.getElementById('hints').innerHTML = hints;
                submit.disabled = true;
                playerItems[0][0]= count;
                playerItems[0][1]= hints;
                playerItems[0][2] = num;
                var msg = {
                    "messageType": "SCORE",
                    "score": score
                };
                window.parent.postMessage(msg, "*"); 
            }
        }
    }
    if(count > 10){
        document.getElementById('hints').innerHTML = "Sorry, you run out of times"; 
        score =  0;
        playerItems[0][0]= count;
        playerItems[0][1]= hints;
        playerItems[0][2] = num;
        submit.disabled=true;
    }                   
}

// click save button for saving gamestate and score
$("#save").click(function(){
    var msg = {
        "messageType": "SAVE",
        "gameState": {
          "playerItems": playerItems,
          "score": score
        }
    };
    window.parent.postMessage(msg, "*");
});

// click load button for loading gamestate and score 
$("#load").click( function () {
    var msg = {
        "messageType": "LOAD_REQUEST",
    };
    window.parent.postMessage(msg, "*");
});

// listen messages from service
window.addEventListener("message", function(evt) {
    if(evt.data.messageType === "LOAD") {
        playerItems = evt.data.gameState.playerItems;
        score = evt.data.gameState.score;
        update();
        load = true;
    } else if (evt.data.messageType === "ERROR") {
        alert(evt.data.info);
    }
});

// update gamestate and other data
function update(){
    document.getElementById('hints').innerHTML = playerItems[0][1];
    count = playerItems[0][0];
    num = playerItems[0][2];
}

// send setting message to the parent window
var message =  {
    messageType: "SETTING",
    options: {
        "width": 800, //Integer
        "height": 1000 //Integer
    }
};
window.parent.postMessage(message, "*");

});