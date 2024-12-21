# Gerenciador de Notas e Arquivos

Este projeto é um **gerenciador de notas e arquivos** criado com FastAPI, projetado para armazenar notas seguras e transferir arquivos entre sistemas operacionais. Ele suporta:

- Criação e armazenamento de notas com títulos e datas de expiração.
- Upload e download de arquivos. 
- Gerenciamento de metadados para arquivos.

## Funcionalidades

1. **Gerenciamento de Notas**:
   - Criação de notas com título, conteúdo e opção de expiração.
   - Recuperação de notas pelo ID.
   - Excluição de notas.

2. **Transferência de Arquivos**:
   - Upload de arquivos com opção de adicionar descrição.
   - Listagem de arquivos armazenados.
   - Download de arquivos por nome.

## Tecnologias Utilizadas

- **Python**
- **FastAPI**
- **Passlib** (para hash seguro de conteúdo de notas)
- **Uvicorn** (servidor ASGI)

## Como Executar o Projeto

### Requisitos
- Python 3.8+
- Pip para gerenciamento de pacotes
- Virtualenv (opcional, mas recomendado)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/gerenciador-de-notas.git
   cd gerenciador-de-notas
   ```

2. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate # No Windows, use: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```

O servidor estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Endpoints Principais

### **Notas**

- **Criar Nota**:
  - **POST** `/notes/`
  - Corpo da requisição (JSON):
    ```json
    {
      "title": "Minha Nota",
      "content": "Este é o conteúdo da minha nota",
      "expires_in": 60
    }
    ```
  - Resposta:
    ```json
    {
      "id": "<id>",
      "title": "Minha Nota",
      "created_at": "<data e hora>",
      "expires_at": "<data e hora>"
    }
    ```

- **Recuperar Nota**:
  - **GET** `/notes/{note_id}`
  - Resposta:
    ```json
    {
      "id": "<id>",
      "title": "Minha Nota",
      "created_at": "<data e hora>",
      "expires_at": "<data e hora>"
    }
    ```

- **Excluir Nota**:
  - **DELETE** `/notes/{note_id}`

### **Arquivos**

- **Upload de Arquivo**:
  - **POST** `/files/`
  - Parâmetro: Arquivo enviado no corpo da requisição.
  - Resposta:
    ```json
    {
      "filename": "meuarquivo.txt",
      "detail": "File uploaded successfully"
    }
    ```

- **Listar Arquivos**:
  - **GET** `/files/`
  - Resposta:
    ```json
    {
      "files": ["meuarquivo.txt", "outroarquivo.py"]
    }
    ```

- **Download de Arquivo**:
  - **GET** `/files/{file_name}`

## Melhorias Futuras

- Implementar autenticação e autorização (JWT).
- Suporte para organização de arquivos em pastas.
- Integração com banco de dados para armazenamento persistente.
- Interface gráfica para facilitar o uso.

## Contribuições

Contribuições são bem-vindas! Siga os passos:
1. Fork o repositório.
2. Crie uma branch para sua feature/bugfix: `git checkout -b minha-branch`.
3. Submeta um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes. Copyright (c) 2024 1mperador.


