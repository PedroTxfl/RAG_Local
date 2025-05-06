# 🧠 RAG Local - Question Answer sobre ICP-Brasil

Este projeto implementa um sistema de **Perguntas e Respostas (Q\&A)** com base em documentos da **ICP-Brasil**, utilizando um modelo local de linguagem (LLM) e embeddings vetoriais persistentes com **ChromaDB**. Ele é ideal para consultas jurídicas sobre certificação digital baseadas **somente no conteúdo fornecido**.

> ✅ Tudo roda localmente. Nenhum dado é enviado para servidores externos.

---

## 📂 Estrutura do Projeto

```
.
├── data/                # Coloque aqui seus arquivos PDF
├── chroma_db/           # Banco de vetores persistente (gerado automaticamente)
├── main.py              # Código principal do projeto
├── requirements.txt     # Dependências do projeto
└── README.md
```

---

## 🚀 Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/PedroTxfl/RAG_local_Question-Answer.git
cd RAG_local_Question-Answer
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> 📌 **Importante:** Certifique-se de ter o **Python 3.10+** instalado.

### 4. Instale e configure o Ollama

Este projeto utiliza o [Ollama](https://ollama.com/) para rodar o modelo LLM localmente.

* Baixe e instale o Ollama de acordo com seu sistema operacional.
* Após instalado, certifique-se de iniciar o servidor Ollama:

```bash
ollama run gemma3:12b
```

### 5. Adicione os documentos

Coloque seus arquivos **.PDF** no diretório `/data/`.

> ⚠️ **Atenção:** O sistema só indexará arquivos com extensão `.pdf`. Outros formatos serão ignorados.

---

## 🛠️ Personalização

### Modificar o Prompt do Assistente

Caso deseje personalizar o comportamento do modelo (por exemplo, mudar o foco jurídico, tom da resposta, idioma etc.), edite a variável `template` em `main.py` com o seu próprio texto orientativo.

---

## 💬 Executando o Assistente

Depois de tudo configurado, execute o script principal:

```bash
python main.py
```

Você verá a seguinte mensagem:

```
Assistente Jurídico ICP-Brasil (Persistente) - Pergunte algo ou digite 'sair' para encerrar.
```

Agora você pode começar a interagir com o sistema de perguntas e respostas.

---

## 📌 Requisitos

* Python 3.10+
* [Ollama](https://ollama.com/) instalado e em execução
* Ambiente virtual (`venv`) ativo
* Modelos baixados:

  * `gemma3:12b` (via Ollama)
  * `intfloat/multilingual-e5-large` (via Hugging Face)

---

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).

---

