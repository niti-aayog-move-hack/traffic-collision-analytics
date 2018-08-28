function changed(){
  if(document.getElementById("input-1").value){
    document.getElementById("go-button").href = "demo/result";
    }
  else{
    document.getElementById("go-button").removeAttribute("href");
  }
}
