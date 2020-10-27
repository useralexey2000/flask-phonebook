document.addEventListener("DOMContentLoaded", function(){

    let entryForm = document.getElementById("create-edit-form");
    
    if(entryForm) {
        entryForm.addEventListener("click", function (e) {
        // remove phone elem
            if (e.target.classList.contains("rem-phone")){
                let rem = e.target.parentNode;
                this.removeChild(rem);
    
        // add phone elem            
            } else if (e.target.id == "add-phone") {
                    
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
                <input class="phone-num" id=` + name + ` name=` + name + ` type="text" value="" required>
                <a class="rem-phone" href="#">remove</a>`;
    
                this.insertBefore(div, this.lastElementChild.previousSibling);
            }
        });
    }
});
