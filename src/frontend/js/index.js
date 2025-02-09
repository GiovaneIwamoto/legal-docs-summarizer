document.getElementById("attach-file").onchange = function (event) {
  const fileName = event.target.files[0].name;

  if (!fileName.endsWith(".zip")) {
    alert("The file must be in ZIP format.");
    return;
  }
  document.getElementById("label-file-attach").innerHTML = fileName;
};

let base64 = null;

// File extraction action
document.getElementById("extract").onclick = function (event) {
  const fileInput = document.getElementById("attach-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("No file selected!");
    return;
  }

  // Clear previous summary
  const resultElement = document.getElementById("message-txt");
  resultElement.innerHTML = "";

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("chat-loader").style.display = "flex";
  window.scrollTo(0, 500);

  // Fetch backend to process the file
  fetch("http://127.0.0.1:8000/generate_summary/", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Error processing the file");
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("chat-loader").style.display = "none";
      document.getElementById("chat-wrapper").style.display = "block";
      document.getElementById("ask-assistent-form").style.display = "block";
      window.scrollTo(0, 1000);

      if (data.final_summary) {
        const resultElement = document.getElementById("message-txt");
        resultElement.innerHTML = data.final_summary.replace(/\n/g, "<br>");
      } else {
        alert("Error processing the file.");
      }
    })
    .catch((error) => {
      document.getElementById("chat-loader").style.display = "none";
      console.error("Error sending the file:", error);
    });
};
