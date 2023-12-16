const myButton = document.querySelectorAll(".moviePageButton");
    console.log("name")

myButton.forEach(function(button){
  button.addEventListener("click", function(){
    sendMovieNameToFlask(this)
  });
})

function sendMovieNameToFlask(clickedMovieButton){
    let name = clickedMovieButton.previousElementSibling.innerHTML;
    console.log(name)
    window.location.href = `/games/${name}`;
}