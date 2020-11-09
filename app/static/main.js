document.addEventListener("DOMContentLoaded", function(){

    let entryForm = document.getElementById("create-edit-form");
    
    if(entryForm) {
        entryForm.addEventListener("click", function (e) {
        // remove phone elem
            // if (e.target.classList.contains("rem-phone")){
            if (e.target.closest(".rem-phone")){

                let rem = e.target.closest(".rem-phone").parentNode;
                this.removeChild(rem);
                return;
    
        // add phone elem            
            // } else if (e.target.id == "add-phone") {
            } else if (e.target.closest('#add-phone')) {
                    
                let items = this.getElementsByClassName("phone-item");
                let n = items.length;
                
                if(n >= 5){
                    alert("can\'t add more than 5 phones");
                    return;
                }
                /// name to process in form
                let name = "phones-" + (n) + "-num";
                // create node
                let div = document.createElement("div");
                div.setAttribute("class", "phone-item");
                
                div.innerHTML = `<label for=`+ name +`>phone:</label>
                <a class="rem-phone" href="#">
                    <i class="far fa-trash-alt"></i>
                </a>
                <input class="phone-num" id=` + name + ` name=` + name + ` type="text" value="" required>`;
    
                this.insertBefore(div, this.lastElementChild.previousSibling);
                return;
            }
        });
    }
});
