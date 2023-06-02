function fetchNotes(elem,url){
    setInterval(async function() {
        const response = await fetch(url);
        const text = await response.text();
        elem.innerHTML = text;
    }, 3000);     
}

function showNoteModal(url){
    fetch(url).then((data) => {
        return data.text()
    }).then((data) =>  {modal_content.innerHTML = data})
}

function submitSignUpForm(){
    verify.setCustomValidity(
        verify.value != password.value ? "Passwords do not match." : ""
    )
    verify.reportValidity()
    let formData=new FormData(sign_up_form);
    fetch("signup/user",
        {
            body: formData,
            method: "post"
        }).then((data) => {return data.json()})
    .then((data) =>  {
        console.log(data)
        if (data["status"] !== "ok"){
            let field = document.getElementById(data["field"])
            field.setCustomValidity(data["message"])
            field.reportValidity()
        }
        else{
            window.location = "/"
        }
    })
}

function submitLoginForm(){
    let formData=new FormData(login_form);
    fetch("login",
        {
            body: formData,
            method: "post"
        }).then((data) => {return data.json()})
    .then((data) =>  {
        if (data["status"] === "Fail"){
            document.getElementById("log_now")
            .innerHTML = "Incorrect login or password Try again";
        }
        else{
            console.log("success")
            window.location = "/dashboard"
        }
        
    })
}
