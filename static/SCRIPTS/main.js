const myButton = document.querySelectorAll(".btn-success");
    console.log("name")

myButton.forEach(function(button){
  button.addEventListener("click", function(){
    sendGameNameToFlask(this)
  });
})

function sendGameNameToFlask(clickedMovieButton){
    let name = clickedMovieButton.previousElementSibling.innerHTML;
    console.log(name)
    console.log(name)
    window.location.href = `/game/${name}`;
}