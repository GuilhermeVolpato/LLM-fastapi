# Guia de Configuração e Execução do Projeto

Este guia irá guiá-lo na configuração e execução do projeto FastAPI utilizando Poetry.

## Sobre o projeto

Este projeto é um microsserviço desenvolvido em Python utilizando FastAPI e Langchain, com integração à API do OpenAI. A API foi projetada para receber imagens e arquivos PDF contendo relatórios e fornecer uma análise detalhada e abrangente. Isso auxilia os usuários a interpretarem melhor as informações, identificarem pontos fortes e fracos nos relatórios e realizarem uma avaliação mais precisa e informada. Com essa solução, espera-se que os usuários possam tomar decisões mais embasadas e estratégicas, otimizando a compreensão e o uso dos dados apresentados.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o `Python`, `pipx` e o `Poetry` instalados em sua máquina.

### Instalar Python

1. **Baixe e instale o Python**: Você pode baixar a versão mais recente do Python [aqui](https://www.python.org/downloads/).
2. **Verifique a instalação**: Após a instalação, abra um terminal e execute:
   ```bash
   python --version
   ```
   Isso deve mostrar a versão do Python instalada.

### Instalar pipx

1. **Instale o pipx**: Abra um terminal e execute:
   ```bash
   python -m pip install --user pipx
   ```
   ```bash
    python -m pipx ensurepath
   ```
2. **Verifique a instalação**: Após a instalação, feche e reabra o terminal, e verifique se o `pipx` está instalado corretamente executando:
   ```bash
   pipx --version
   ```

### Instalar Poetry

1. **Instale o Poetry usando pipx**: Abra um terminal e execute:
   ```bash
   pipx install poetry
   ```
2. **Verifique a instalação**: Após a instalação, verifique se o Poetry está instalado corretamente executando:
   ```bash
   poetry --version
   ```

## Configurar o Projeto

### Clonar o Repositório

Se ainda não tiver o projeto, clone-o do repositório.

```bash
git clone https://github.com/GuilhermeVolpato/LLM-fastapi.git
```

## Configuração do Ambiente

Este projeto usa variáveis de ambiente para gerenciar configurações sensíveis. Siga os passos abaixo para configurar o ambiente:

1. Copie o arquivo `.env.example` para `.env`:

   ```sh
   cp .env.example .env
   ```

2. Abra o arquivo `.env` e preencha os valores necessários:
   ```dotenv
   OPENAI_API_KEY=your_real_openai_api_key_here
   ```

## Rodar Projeto

### Iniciar Poetry (venv)

Poetry cria um ambiente virtual para o projeto, gerenciando dependências isoladas das outras instalações de Python no sistema.

```bash
poetry shell
```

### Instalar Dependências do Projeto

```bash
poetry install
```

## Iniciar API

```bash
poetry run uvicorn app.main:app --reload
```

Seguindo esses passos, você terá configurado e executado o projeto FastAPI utilizando Poetry com sucesso

## Rodar Testes

```bash
poetry run pytest
```

## Documentação

O fastapi cria documentação swagger automaticamente, para acessa-la , incie o projeto e, em seu navegador, vá para o seguinte endereço:

```bash
http://127.0.0.1:8000/docs
```
