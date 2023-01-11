// function Register(){
//     document.getElementById("Panel_Login").style.display = "none";
//     document.getElementById("Panel_Register").style.display = "block";
// }
// function loginPage(){
//     document.getElementById("Panel_Register").style.display = "none";
//     document.getElementById("Panel_Login").style.display = "block";
// }
// function SignUP(){
//     var username = document.forms['registerForm']['userName_Register'].value;
//     var password = document.forms['registerForm']['passWord_Register'].value;
//     var password_repeat = document.forms['registerForm']['passWord_Repeat'].value;
//     var email = document.forms['registerForm']['Email'].value;
//     if(username == "" | username == null){
//         alert("用户名不得为空!");
//         return false;
//     }else if(password == "" | password == null){
//         alert("密码不得为空!");
//         return false;
//     }else if(password_repeat == "" | password_repeat == null){
//         alert("重复密码不得为空!");
//         return false;
//     }else if(email == "" | email == null){
//         alert("邮箱不得为空!");
//         return false;
//     }
// }

// function SignIn(){
//     var username = document.forms['loginForm']['username'].value;
//     var password = document.forms['loginForm']['password'].value;
//     if(username == "" | username == null){
//         alert("用户名不得为空!");
//         return false;
//     }else if(password == "" | password == null){
//         alert("密码不得为空！");
//         return false;
//     }else{
//         window.location.replace("/index");
//     }
// }
function hideElementById(elementID){
    let element = document.getElementById(elementID)
    element.style.display = "none"
}
function displayElementById(elementID){
    let element = document.getElementById(elementID)
    element.style.display = "flex"
}

function hideRegisterBox(){
    hideElementById("registerBox")
}
function displayRegisterBox(){
    let displayStatusOfLoginBox = document.getElementById("loginBox").style.display
    if (displayStatusOfLoginBox == "flex"){
        return
    }
    displayElementById("registerBox")
}
function hideLoginBox(){
    hideElementById("loginBox")
}
function displayLoginBox(){
    let displayStatusOfRegisterBox = document.getElementById("registerBox").style.display
    if (displayStatusOfRegisterBox == "flex"){
        return
    }
    displayElementById("loginBox")
}
function convertBoxToRegister(){
    hideLoginBox()
    displayRegisterBox()
}
function convertBoxToLogin(){
    hideRegisterBox()
    displayLoginBox()
}
function closePostCard(){
    hideElementById("cardUploadPicture")
}
function displayPostCard(){
    displayElementById("cardUploadPicture")
}
function openFullImage(numID){
    let classObject = document.getElementsByClassName("cardImages")[numID]
    let imageUUID = classObject.alt

    window.open("/remark" + "/imageDetailPage/" + imageUUID)
}
function openUserProfile(userName){
    window.open("/user/userProfile/" + userName)
}
function openOriginalSizeAvatar(userName){
    window.open("/static/avatars/originalSize/" + userName + ".png")
}
function sendLikedData(likedStatus, currentPOST, userNameForAuth){
    if(userNameForAuth == "" || userNameForAuth == undefined){
        alert("You are not logged in.")
        return
    }
    const xmlhttp = new XMLHttpRequest()

    let likeButtonDOM = document.getElementsByClassName("likeButton")
    let unLikeButtonDOM = document.getElementsByClassName("unLikeButton")
    let numberOfDotsDOM = document.getElementsByClassName("likedCount")
    let waitIconDOM = document.getElementsByClassName("waitIcon")
    let imageDOM = document.getElementsByClassName("cardImages")

    let imageUUID = imageDOM[currentPOST].alt


    if (likedStatus == "like"){
        xmlhttp.open("GET","/image/likedThisPOST?UUID=" + imageUUID + "&likedStatus=like")
        xmlhttp.send()
        likeButtonDOM[currentPOST].style.display= "none"
        waitIconDOM[currentPOST].style.display= "flex"
    }

    if (likedStatus == "unlike"){
        xmlhttp.open("GET", "/image/likedThisPOST?UUID=" + imageUUID + "&likedStatus=unlike")
        xmlhttp.send()
        unLikeButtonDOM[currentPOST].style.display= "none"
        waitIconDOM[currentPOST].style.display= "flex"
    }

    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
            jsonObj = JSON.parse(xmlhttp.response)
            if (jsonObj.status == "like"){
                waitIconDOM[currentPOST].style.display = "none"
                unLikeButtonDOM[currentPOST].style.display= "flex"
                numberOfDotsDOM[currentPOST].innerText = jsonObj.dots
            }
            if (jsonObj.status == "unlike"){
                waitIconDOM[currentPOST].style.display = "none"
                likeButtonDOM[currentPOST].style.display= "flex"
                numberOfDotsDOM[currentPOST].innerText = jsonObj.dots
            }
        if (xmlhttp.status==400){
            alert("You are not logged in")
        }
        }
    }
}
function inputStatusHandler(){
    let postCoverFormBox = document.getElementById("postCoverFormBox")
    
    if(postCoverFormBox.style.display == "none"){
        postCoverFormBox.style.display = "block"
    }else{
        postCoverFormBox.style.display = "none"
    }
}