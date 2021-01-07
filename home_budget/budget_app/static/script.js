document.addEventListener("DOMContentLoaded", function() {
    let description = document.querySelector('#description');
    description.addEventListener('keyup', () =>{
        fetch(`/hint?text=${description.value}`)
            .then(response => response.json())
            .then(data => {
                let ul = document.querySelector('#hints');
                ul.innerHTML = '';
                data.forEach((hint) => {
                    let newLi = document.createElement('li');
                    newLi.innerText = hint;
                    ul.appendChild(newLi)
                    newLi.addEventListener('click', () =>{
                        description.innerText = hint;
                        ul.innerHTML = '';
                    });
                });
            });
    });
}