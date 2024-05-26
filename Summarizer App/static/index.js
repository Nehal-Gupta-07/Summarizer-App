
function sendEmail(){
    Email.send({
        Host : "smtp.elasticemail.com",
        Username : "nehalgupta2002@gmail.com",
        Password : "5237C93F1A3DFE7D7B437D35B9649287F870",
        To : 'nehalgupta2002@gmail.com',
        From : document.getElementById("email").value,
        Subject : "Query",
        Body : document.getElementById("query").value
    }).then(
      message => alert("Query has been sent successfully")
    );
}

window.onload = function() {
  var element = document.getElementById("answer");
  var shouldScroll = element.getAttribute("show");
  console.log(shouldScroll)
  if (shouldScroll) {
      element.scrollIntoView();
  }
};