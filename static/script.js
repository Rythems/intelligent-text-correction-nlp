function setExample(text){

document.getElementById("inputText").value = text;

}

async function correctText(){

let text = document.getElementById("inputText").value;

try{

let response = await fetch("/correct",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
text:text
})

});

let data = await response.json();

document.getElementById("outputText").value = data.corrected_text;

}catch{

alert("Failed to process the text.");

}

}