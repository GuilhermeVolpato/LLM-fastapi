# Guia de Configuração e Execução do Projeto

Este guia irá guiá-lo na configuração e execução do projeto FastAPI utilizando Poetry.

## Sobre o projeto

Este projeto é um microsserviço desenvolvido em Python utilizando FastAPI, com integração à API do OpenAI. O objetivo é auxiliar usuários de Ema ERP na análise e compreensão de relatórios empresariais. A API é projetada para receber fotos e/ou arquivos PDF contendo relatórios gerados pelo ERP e fornecer uma análise detalhada e abrangente. Com isso, o sistema ajuda os usuários a interpretar melhor as informações, identificar pontos fortes e fracos da empresa, e realizar uma avaliação mais precisa e informada dos relatórios apresentados.

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

Se ainda não tiver o projeto, clone-o do repositório. Substitua `<url-do-repositorio>` pela URL do repositório:

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
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

## Rodar API

```bash
poetry run uvicorn app.main:app --reload
```

Seguindo esses passos, você terá configurado e executado o projeto FastAPI utilizando Poetry com sucesso

## Documentação

O fastapi cria documentação swagger automaticamente, para acessa-la , incie o projeto e, em seu navegador, vá para o seguinte endereço:

```bash
http://127.0.0.1:8000/docs
```
