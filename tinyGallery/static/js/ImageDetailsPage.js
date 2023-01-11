function getUUIDForvirtualInput(){
    let inputValue = document.getElementById("virtualInputForUUID")
    let UUID = document.getElementById("cover")
    inputValue.value = UUID.alt
}
getUUIDForvirtualInput()

function openOriginalSizeCover(uuid, fileType){
    window.open("/static/posts/orginalSizeImages/" + uuid + "/" + uuid + "." + fileType)
}
function openOriginalSizeImage(path){
    window.open(path)
}
function sendLikedDataForDetailPage(uuid,likedStatus,userNameForAuth){
    if(userNameForAuth == "" || userNameForAuth == undefined){
        alert("You are not logged in.")
        return
    }
    const xmlhttp = new XMLHttpRequest()

    let likeButtonDOM = document.getElementById("likeButton")
    let unLikeButtonDOM = document.getElementById("unLikeButton")
    let placeHolderButtonDOM = document.getElementById("placeHolderButton")

    if (likedStatus == "like"){
        xmlhttp.open("GET","/image/likedThisPOST?UUID=" + uuid + "&likedStatus=like")
        xmlhttp.send()
        likeButtonDOM.style.display = "none"
        placeHolderButtonDOM.style.display = "block"
    }

    if (likedStatus == "unlike"){
        xmlhttp.open("GET", "/image/likedThisPOST?UUID=" + uuid + "&likedStatus=unlike")
        xmlhttp.send()
        unLikeButtonDOM.style.display = "none"
        placeHolderButtonDOM.style.display = "block"
    }

    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4 && xmlhttp.status==200){
            jsonObj = JSON.parse(xmlhttp.response)
            if (jsonObj.status == "like"){
                placeHolderButtonDOM.style.display = "none"
                unLikeButtonDOM.style.display = "block"
                document.getElementById("likedNum").innerText = jsonObj.dots + " Likes"
            }
            if (jsonObj.status == "unlike"){
                placeHolderButtonDOM.style.display = "none"
                likeButtonDOM.style.display = "block"
                document.getElementById("likedNum").innerText = jsonObj.dots + " Likes"
            }
        if (xmlhttp.status==400){
            alert("You are not logged in")
        }
        }
    }
}
function getShareUrl(){
    let shareUrl = window.location.href
    
    navigator.clipboard.writeText(shareUrl)
    alert("Share link copied the to clipboard")
}