document.getElementById("attach-file").onchange = function (event) {
  const fileName = event.target.files[0].name;

  if (!fileName.endsWith(".zip")) {
    alert("O arquivo deve ser no formato ZIP.");
    return;
  }
  document.getElementById("label-file-attach").innerHTML = fileName;
};

let base64 = null;

// Ação de extração do arquivo
document.getElementById("extract").onclick = function (event) {
  const fileInput = document.getElementById("attach-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("Nenhum arquivo selecionado!");
    return;
  }

  // Limpa o resumo anterior
  const resultadoElement = document.getElementById("message-txt");
  resultadoElement.innerHTML = "";

  const formData = new FormData();
  formData.append("file", file);

  document.getElementById("chat-loader").style.display = "flex";
  window.scrollTo(0, 500);

  // Fetch no backend para processar o arquivo
  fetch("http://127.0.0.1:8000/generate_summary/", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro ao processar o arquivo");
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("chat-loader").style.display = "none";
      document.getElementById("chat-wrapper").style.display = "block";
      document.getElementById("ask-assistent-form").style.display = "block";
      window.scrollTo(0, 1000);

      if (data.final_summary) {
        const resultadoElement = document.getElementById("message-txt");
        resultadoElement.innerHTML = data.final_summary.replace(/\n/g, "<br>");
      } else {
        alert("Erro ao processar o arquivo.");
      }
    })
    .catch((error) => {
      document.getElementById("chat-loader").style.display = "none";
      console.error("Erro ao enviar o arquivo:", error);
    });
};
