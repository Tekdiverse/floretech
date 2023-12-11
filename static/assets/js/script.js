const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add('visible');
        }
    });
});

const hiddenElements = document.querySelectorAll("[show]");
hiddenElements.forEach((el) => observer.observe(el));







const input = document.querySelector("input"), 
      showHide = document.querySelector(".show_hide"),
      indicator = document.querySelector(".indicator"),
      iconText = document.querySelector(".icon-text"),
      text = document.querySelector(".text");

showHide.addEventListener("click", ()=>{
    if(input.type == "password"){
       input.type == "text";       showHide.classList.replace("fa-eye-slash","fa-eye");
    }else{
       input.type == "password"; showHide.classList.replace("fa-eye","fa-eye-slash");
    }
    
});   



// js code to show password strength
let alphabet = /[a-zA-Z]/,
    numbers = /[0-9]/,
    scharacters = /[!,@,#,$,%,^,&,*,?,_,(,),-,+,=,~]/;
    

input.addEventListener("keyup",()=>{
    indicator.classList.add("active");
    
    let val = input.value;
    if(val.match(alphabet) || val.match(numbers) || val.match(scharacters)){
        text.textContent = "Password is weak";
        iconText.style.color = "#FF6333"
    }
    if(val == ""){
        indicator.classList.remove("active");
    }
});
