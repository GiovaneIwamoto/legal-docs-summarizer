document.getElementById("attach-file").onchange = function (event) {
  const fileName = event.target.files[0].name.split(".")[0];
  const file = event.target.files[0];

  const pdfIcon = document.createElement("img");
  pdfIcon.src = "assets/img/pdf-icon.svg";
  pdfIcon.alt = "Imagem de um arquivo PDF";

  var image = document.getElementById("icon-file-attach");
  console.log(image);
  image.setAttribute("src", "assets/img/pdf-icon.svg");
  document.getElementById("label-file-attach").innerHTML = fileName;

  lerArquivo(file)
    .then((base64Data) => {
      // Aqui você pode usar a variável base64Data como desejar
      base64 = base64Data;
      console.log("dentro do async:", base64Data);
      // Por exemplo, você pode enviar isso para um endpoint ou armazenar em uma variável externa
      // Faz alguma ação com base64Data
    })
    .catch((error) => {
      console.error("Erro:", error);
    });
};

let base64 = null;

document.getElementById("extract").onclick = function (event) {
  const selectElement = document.getElementById("select").value;

  let isSuccess = selectElement !== "0" ? true : false;

  const numeroProcesso = document.getElementById("numero-processo").value;

  if (base64 !== null && isSuccess) {
    document.getElementById("chat-loader").style.display = "flex";
    window.scrollTo(0, 500);

    fazerRequisicao_doc(base64, selectElement)
      .then((uuid) => {
        console.log(uuid);
        localStorage.setItem("UUID", uuid);
        verificarEndpoint(uuid)
          .then((body) => {
            console.log("Body da requisição bem-sucedida:", body);
            const resultadoElement = document.getElementById("message-txt");
            document.getElementById("chat-loader").style.display = "none";
            document.getElementById("chat-wrapper").style.display = "block";
            document.getElementById("ask-assistent-form").style.display =
              "block";
            window.scrollTo(0, 1000);
            document.getElementsByTagName("footer")[0].style.position =
              "relative";
            resultadoElement.innerHTML = body.replace(/\n/g, "<br>");
          })
          .catch((error) => {
            console.error("Erro ao verificar a requisição:", error);
            // Trate os erros aqui, se necessário
          });
      })
      .catch((error) => {
        console.error("Erro na obtenção do UUID:", error);
        // Trate os erros aqui, se necessário
      });
  }

  let terminaComPDF = numeroProcesso.endsWith(".pdf") ? true : false;

  if (selectElement && !terminaComPDF) {
    isSuccess = true;
  }

  if (numeroProcesso.trim() !== "" && isSuccess) {
    document.getElementById("chat-loader").style.display = "flex";
    window.scrollTo(0, 500);

    fazerRequisicao_texto(numeroProcesso, selectElement)
      .then((uuid) => {
        console.log(uuid);
        localStorage.setItem("UUID", uuid);
        if (uuid !== null) {
          verificarEndpoint(uuid)
            .then((body) => {
              console.log("Body da requisição bem-sucedida:", body);
              const resultadoElement = document.getElementById("message-txt");
              /*resultadoElement.innerHTML = addBreakBeforePhrase(
                formatTextWithHTML(body)
              );*/
              resultadoElement.innerHTML = body.replace(/\n/g, "<br>");

              document.getElementById("chat-loader").style.display = "none";
              document.getElementById("chat-wrapper").style.display = "block";
              document.getElementById("ask-assistent-form").style.display =
                "block";
              window.scrollTo(0, 1000);
              document.getElementsByTagName("footer")[0].style.position =
                "relative";
            })
            .catch((error) => {
              console.error("Erro ao verificar a requisição:", error);
              // Trate os erros aqui, se necessário
            });
        } else {
          document.getElementById("chat-loader").style.display = "none";
          document.getElementById("chat-wrapper").style.display = "block";
          const resultadoElement = document.getElementById("message-txt");
          resultadoElement.innerHTML = addBreakBeforePhrase(
            "Documento não encontrado"
          );
        }
      })
      .catch((error) => {
        console.error("Erro na obtenção do UUID:", error);
        // Trate os erros aqui, se necessário
      });
  }
  // Faça a resquest aqui
  // Troque o setTimeout para o retorno da request

  /* setTimeout(() => {
    document.getElementById('chat-loader').style.display = 'none'
    document.getElementById('chat-wrapper').style.display = 'block'
    document.getElementById('ask-assistent-form').style.display = 'block'
    window.scrollTo(0, 1000);
    document.getElementsByTagName('footer')[0].style.position = 'relative';
  }, 1000);*/
};

document.getElementById("ask-assistent-submit").onclick = function (event) {
  const input = document.getElementById("ask-assistent-input");
  const ask = input.value;

  if (input.value.length === 0) {
  } else {
    newMessage({
      messageText: input,
      isAssistent: false,
    });
    const uuidSalvo = localStorage.getItem("UUID");

    fazerRequisicao_rag(ask, uuidSalvo)
      .then((body) => {
        console.log("requisição");
        console.log(uuidSalvo);
        console.log(body);
        verificarEndpoint(body)
          .then((body) => {
            console.log("Body da requisição bem-sucedida:", body);
            newMessage({
              messageText: body,
            });
          })
          .catch((error) => {
            console.error("Erro ao verificar a requisição:", error);
            // Trate os erros aqui, se necessário
          });
      })
      .catch((error) => {
        console.error("Erro na obtenção do body:", error);
        // Trate os erros aqui, se necessário
      });
  }
};

function newMessage({ messageText, isAssistent = true }) {
  var newMessageBox = document.createElement("div");
  newMessageBox.classList.add("message-box");
  var messageSenderWrapper = document.createElement("div");

  messageSenderWrapper.id = "sender";

  var sender = document.createElement("span");
  sender.id = "identifier";
  sender.innerText = isAssistent ? "Assistente STF" : "Você";
  messageSenderWrapper.appendChild(sender);

  if (isAssistent) {
    var copyUtil = document.createElement("span");
    copyUtil.innerText = "Copiar";
    var idNumber = Math.random();
    copyUtil.id = "copy" + idNumber;
    copyUtil.style = "cursor: pointer;";
    copyUtil.onclick = () => {
      var idToCopy = document.getElementById(copyUtil.id).parentElement
        .nextSibling.id;
      console.log(idToCopy);
      CopyToClipboard(idToCopy);
      copyUtil.innerHTML = "<i>Copiado</i>";
      setTimeout(() => {
        copyUtil.innerText = "Copiar";
      }, 1000);
    };
    messageSenderWrapper.appendChild(copyUtil);
  }

  var message = document.createElement("div");
  message.classList.add("message");
  isAssistent ? (message.id = "message" + idNumber) : "";
  message.innerText = isAssistent ? messageText : messageText.value;

  newMessageBox.appendChild(messageSenderWrapper);
  newMessageBox.appendChild(message);

  document.getElementById("chat").appendChild(newMessageBox);

  !isAssistent ? (messageText.value = "") : () => {};
}

function CopyToClipboard(containerid) {
  var range = document.createRange();
  range.selectNode(document.getElementById(containerid));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
}

//minhas funcs

function fazerRequisicao_rag(ask, uuid) {
  const url =
    "COLOQUE AQUI O LINK ";

  const payload = {
    prompt: ask,
    uuid: uuid,
  };

  const headers = {
    Authorization: "",
    "Content-Type": "application/json",
  };

  const requestOptions = {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload),
  };

  return fetch(url, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data.body; // Retornar o UUID obtido da resposta
      // Faça o que quiser com a resposta aqui
    })
    .catch((error) => {
      console.error("Erro:", error);
      // Trate os erros aqui
    });
}

function separarPerguntas(textoBruto) {
  // Separação do texto por cada pergunta
  let perguntas = textoBruto.match(/[A-Z]\).*?(?=[A-Z]\)|$)/gs);

  // Formatando as perguntas uma abaixo da outra
  let perguntasFormatadas = perguntas.map((pergunta) => {
    return `<p>${pergunta}</p>\n`;
  });

  return perguntasFormatadas.join("");
}

function fazerRequisicao_doc(base64, id) {
  const url =
    "";

  const payload = {
    base64: base64,
    id: id,
  };

  const headers = {
    Authorization: "",
    "Content-Type": "application/json",
  };

  const requestOptions = {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload),
  };

  return fetch(url, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data.body.uuid; // Retornar o UUID obtido da resposta
      // Faça o que quiser com a resposta aqui
    })
    .catch((error) => {
      console.error("Erro:", error);
      // Trate os erros aqui
    });
}

function fazerRequisicao_texto(numeroProcesso, id) {
  const url =
    "";

  const payload = {
    doc: numeroProcesso,
    id: id,
  };

  const headers = {
    Authorization: "",
    "Content-Type": "application/json",
  };

  const requestOptions = {
    method: "POST",
    headers: headers,
    body: JSON.stringify(payload),
  };

  return fetch(url, requestOptions)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      return data.body.uuid; // Retornar o UUID obtido da resposta
      // Faça o que quiser com a resposta aqui
    })
    .catch((error) => {
      console.error("Erro:", error);
      // Trate os erros aqui
    });
}

async function verificarEndpoint(uuid) {
  return new Promise((resolve, reject) => {
    const url =
      "";

    const payload = {
      uuid: uuid,
    };

    const headers = {
      Authorization: "",
      "Content-Type": "application/json",
    };

    const requestOptions = {
      method: "POST",
      headers: headers,
      body: JSON.stringify(payload),
    };

    const verificar = async () => {
      try {
        const response = await fetch(url, requestOptions);
        const data = await response.json();
        const status = data.statusCode;

        if (status === 200) {
          console.log("Requisição bem-sucedida. Status:", status);
          console.log(data);
          resolve(data.body); // Resolvendo a Promessa com data.body
        } else {
          console.log("Requisição ainda não foi bem-sucedida. Status:", status);
          console.log(data);
          // Se necessário, aguarde e faça uma nova chamada
          setTimeout(verificar, 3000); // Chama a função novamente após 3 segundos (ou outro intervalo desejado)
        }
      } catch (error) {
        console.error("Erro na requisição:", error);
        reject(error); // Rejeita a Promessa em caso de erro
      }
    };

    verificar(); // Inicia a verificação
  });
}

function lerArquivo(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = function (event) {
      const base64Data = event.target.result.split(",")[1];
      resolve(base64Data); // Resolvendo a Promise com base64Data
    };

    reader.onerror = function (error) {
      reject(error); // Rejeitando a Promise em caso de erro
    };

    reader.readAsDataURL(file);
  });
}

document
  .getElementById("ask-assistent-form")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      console.log("teste");
      e.preventDefault();
    }
  });

document
  .getElementById("numero-processo")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      console.log("teste");
      e.preventDefault();
    }
  });

function formatTextWithHTML(text) {
  const questionsArray = text.split(/(?=[A-Z]\))/).filter(Boolean);
  const formattedQuestions = questionsArray.map((question) => {
    const trimmedQuestion = question.trim();
    return `<p>${trimmedQuestion}</p>`;
  });
  console.log(formattedQuestions.join("\n"));
  return formattedQuestions.join("\n");
}

function addBreakBeforePhrase(text) {
  const phrase =
    "As perguntas abaixo não cabem a este documento, portanto não são informadas:";
  const index = text.indexOf(phrase);

  if (index !== -1) {
    const beforePhrase = text.substring(0, index);
    const afterPhrase = text.substring(index);
    return `${beforePhrase}<br/>${afterPhrase}`;
  }

  return text;
}
