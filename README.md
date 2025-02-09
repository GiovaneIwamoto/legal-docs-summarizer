# LEGAL DOCS SUMMARIZER

### **OVERVIEW**

This project utilizes AWS Bedrock and OCR technology to extract text from PDFs, enabling the creation of detailed summaries of legal documents. The summarization leverages prompt engineering, with specific parameters tailored to enhance response accuracy and relevance. The Bedrock API uses the Anthropic Claude-v2 model, configured with a deterministic approach and prioritizing the most probable tokens. The setup focuses on precise output generation, ensuring summaries are coherent and well-structured, guided by advanced AI capabilities from the Claude-v2 model.

## [![My Skills](https://skillicons.dev/icons?i=aws,py,fastapi,js,html,css&theme=dark)](https://skillicons.dev)

![Page](img/image.png)

---

### **LEGAL SUMMARIZATION**

Legal summarization is a critical task that requires precision, consistency, and the ability to handle complex legal language. This project leverages the **Anthropic Claude-v2 model** through **AWS Bedrock** to generate accurate and coherent summaries of legal documents. Below, we delve into the key aspects of how this process is optimized for legal use cases:

#### **Consistency in Legal Summarization**

One of the primary challenges in legal summarization is maintaining consistency across documents, especially when dealing with lengthy or complex texts. The Claude-v2 model is specifically designed to handle this challenge by:

- **Prioritizing deterministic outputs**: The model is configured to focus on the most probable tokens, ensuring that the summaries are consistent and reliable.

- **Structured prompts**: By using carefully engineered prompts, the model is guided to produce summaries that adhere to legal standards and maintain coherence.

#### **Prompt Engineering for Legal Use Cases**
Prompt engineering plays a crucial role in tailoring the summarization process to legal documents. The prompts are designed to:

- **Focus on key legal elements**: The model is guided to prioritize information such as case law, statutes, legal arguments, and judicial reasoning.

- **Ensure relevance and accuracy**: By specifying parameters such as tone, structure, and focus areas, the prompts help the model generate summaries that are both relevant and accurate.

> [!IMPORTANT]
> When summarizing a legal contract, the Claude-v2 model can extract key clauses, obligations, and conditions, presenting them in a concise and structured format. This capability is invaluable for legal professionals who need to quickly understand the essence of lengthy documents.

---

### **RESOURCES**

- [AWS Bedrock Prompt for Summarization](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-templates-and-examples.html#summarization)

- [Anthropic Legal Summarization](https://docs.anthropic.com/en/docs/about-claude/use-case-guides/legal-summarization)

- [Anthropic Summarization Prompt Engineering Guide](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb)

By combining advanced AI capabilities with robust infrastructure, this project delivers a powerful solution for legal summarization, ensuring that summaries are accurate, consistent, and tailored to the needs of legal professionals.

---

### **BACKEND ENDPOINT**

| Method | Endpoint                                | Description       |
| ------ | --------------------------------------- | ----------------- |
| POST   | https://localhost:8000/generate_summary | Generate Summmary |

---

### **AUTHOR**

- Giovane Hashinokuti Iwamoto - Computer Science - Brazil

I am always open to receiving constructive criticism and suggestions for improvement in my developed code. I believe that feedback is an essential part of the learning and growth process, and I am eager to learn from others and make my code the best it can be. Whether it's a minor tweak or a major overhaul, I am willing to consider all suggestions and implement the changes that will benefit my code and its users.
