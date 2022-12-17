// function Hi(){
//     alert("Under Development.");
// }
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
    let classObject = document.getElementsByClassName("cardImages")[numID-1]
    let imageUUID = classObject.alt

    window.open("/remark" + "/imageDetailPage/" + imageUUID)
}
function getUUIDForvirtualInput(){
    let inputValue = document.getElementById("virtualInputForUUID")
    let UUID = document.getElementById("bigSizeImage")
    inputValue.value = UUID.alt
}
getUUIDForvirtualInput()
function openUserProfile(userName){
    window.open("/user/userProfile/" + userName)
}
function openOriginalSizeAvatar(userName){
    window.open("/static/avatars/originalSize/" + userName + ".png")
}
function openOriginalImage(uuid,fileType){
    window.open("/static/images/originalSize/" + uuid + "." + fileType)
}