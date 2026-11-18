# Moving Health

API REST desenvolvida com **Python, FastAPI e Oracle Database** para apoiar o cadastro de usuários e o gerenciamento de contatos de emergência, alertas e acompanhamentos.

O projeto tem como objetivo oferecer uma estrutura de assistência, acompanhamento e segurança para pessoas que precisam de suporte, incluindo pessoas que moram sozinhas ou possuem necessidades de acessibilidade.

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de usuários.
- Cadastro e gerenciamento de contatos de emergência vinculados a usuários.
- Cadastro e gerenciamento de alertas vinculados a usuários e, opcionalmente, a contatos de emergência.
- Cadastro e gerenciamento de acompanhamentos vinculados a usuários.
- Armazenamento dos dados em um banco Oracle.
- Documentação interativa dos endpoints por meio do Swagger UI.
- Armazenamento da senha do usuário como hash, em vez de texto puro.

## Tecnologias utilizadas

- **Python 3.11**
- **FastAPI** — criação da API REST.
- **Uvicorn** — servidor ASGI para executar a aplicação.
- **Oracle Database** — banco de dados relacional.
- **python-oracledb** — conexão entre Python e Oracle.
- **python-dotenv** — leitura das configurações armazenadas no arquivo `.env`.
- **Pydantic** — validação e estruturação dos dados de entrada e saída.

## Estrutura do projeto

```text
GS_SOA/
├── app/
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── acompanhamento.py
│   │   ├── alerta.py
│   │   ├── base.py
│   │   ├── contato.py
│   │   └── usuario.py
│   ├── routers/
│   │   ├── acompanhamentos.py
│   │   ├── alertas.py
│   │   ├── contatos.py
│   │   └── usuarios.py
│   ├── schemas/
│   │   ├── acompanhamento.py
│   │   ├── alerta.py
│   │   ├── contato.py
│   │   └── usuario.py
│   ├── services/
│   │   ├── acompanhamento_service.py
│   │   ├── alerta_service.py
│   │   ├── contato_service.py
│   │   ├── db_helper.py
│   │   └── usuario_service.py
│   └── main.py
├── migrations/
│   └── tabelas.sql
├── test_connection.py
├── requirements.txt
├── .env
└── .gitignore
```

### Organização das pastas

| Pasta/arquivo | Responsabilidade |
|---|---|
| `database/` | Configuração e abertura da conexão com o Oracle. |
| `models/` | Definição das estruturas que representam os dados do projeto. |
| `schemas/` | Validação dos dados recebidos e enviados pela API. |
| `routers/` | Definição das rotas e dos métodos HTTP disponíveis. |
| `services/` | Regras de negócio e operações realizadas no banco de dados. |
| `migrations/tabelas.sql` | Script SQL para criação das tabelas e índices. |
| `main.py` | Inicialização da aplicação e registro dos routers. |
| `test_connection.py` | Script para testar a conexão com o Oracle. |

## Banco de dados

O projeto utiliza Oracle Database. O script `migrations/tabelas.sql` contém a criação das seguintes tabelas:

- **USUARIOS:** armazena os dados dos usuários, como nome, e-mail, telefone, endereço e informações de acessibilidade.
- **CONTATOS_EMERGENCIA:** armazena os contatos de emergência associados aos usuários.
- **ACOMPANHAMENTOS:** registra os acompanhamentos realizados para cada usuário.
- **ALERTAS:** armazena alertas associados aos usuários e, quando informado, a um contato de emergência.

Também são criadas chaves estrangeiras para relacionar os registros e índices para auxiliar consultas por usuário.

### Relacionamentos

- Um usuário pode possuir vários contatos de emergência.
- Um usuário pode possuir vários acompanhamentos.
- Um usuário pode possuir vários alertas.
- Um alerta pode estar associado a um contato de emergência.

## Configuração do ambiente

### 1. Pré-requisitos

Antes de iniciar, tenha instalado:

- Python 3.11 ou compatível.
- Oracle Database acessível.
- Oracle SQL Developer (ou outra ferramenta para executar o script SQL).
- Git, caso deseje clonar o repositório.

### 2. Clone o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd GS_SOA
```

Se você já possui os arquivos do projeto, abra o terminal na pasta `GS_SOA`.

### 3. Crie e ative o ambiente virtual (caso não venha junto com o repositório)

No Windows usando Git Bash:

```bash
python -m venv venv
source venv/Scripts/activate
```

### 4. Instale as dependências

```bash
python -m pip install --upgrade pip
pip install fastapi uvicorn oracledb python-dotenv
```

> O `requirements.txt` deve conter as dependências do projeto. Caso esteja vazio no repositório, os comandos acima instalam os pacotes necessários identificados no código.

### 5. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto, no mesmo nível de `app/`, com os dados da sua conexão Oracle:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=seu_service_name
```

Substitua os valores de exemplo pelos dados do seu ambiente Oracle. Não compartilhe seu `.env` e não envie senhas para o repositório.

### 6. Crie as tabelas no Oracle

Abra o Oracle SQL Developer, conecte-se ao banco e execute o conteúdo do arquivo:

```text
migrations/tabelas.sql
```

O script cria as tabelas, os relacionamentos e os índices utilizados pela aplicação.

### 7. Teste a conexão com o banco

Com o ambiente virtual ativado e na raiz do projeto, execute:

```bash
python test_connection.py
```

Quando a conexão estiver correta, o script deverá informar que a conexão com Oracle foi realizada com sucesso e exibir a quantidade de usuários cadastrados.

## Executando a aplicação

Na raiz do projeto, com o ambiente virtual ativado, execute:

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível localmente em:

- Página inicial: http://127.0.0.1:8000/
- Documentação Swagger: http://127.0.0.1:8000/docs
- Status da API: http://127.0.0.1:8000/status

A documentação Swagger permite visualizar e testar os endpoints, enviando dados e consultando as respostas da API.

## Endpoints disponíveis

Os endpoints estão organizados por recurso:

### Usuários — `/usuarios`

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/usuarios/` | Cadastra um usuário. |
| `GET` | `/usuarios/` | Lista os usuários ativos. |
| `GET` | `/usuarios/{usuario_id}` | Busca um usuário pelo ID. |
| `PUT` | `/usuarios/{usuario_id}` | Atualiza os dados de um usuário. |
| `DELETE` | `/usuarios/{usuario_id}` | Exclui um usuário e seus registros relacionados. |

### Contatos de emergência — `/contatos`

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/contatos/` | Cadastra um contato de emergência. |
| `GET` | `/contatos/` | Lista os contatos. |
| `GET` | `/contatos/usuario/{usuario_id}` | Lista os contatos de um usuário. |
| `GET` | `/contatos/{contato_id}` | Busca um contato pelo ID. |
| `PUT` | `/contatos/{contato_id}` | Atualiza um contato. |
| `DELETE` | `/contatos/{contato_id}` | Exclui um contato. |

### Alertas — `/alertas`

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/alertas/` | Cadastra um alerta. |
| `GET` | `/alertas/` | Lista os alertas. |
| `GET` | `/alertas/usuario/{usuario_id}` | Lista os alertas de um usuário. |
| `GET` | `/alertas/{alerta_id}` | Busca um alerta pelo ID. |
| `PUT` | `/alertas/{alerta_id}` | Atualiza um alerta. |
| `DELETE` | `/alertas/{alerta_id}` | Exclui um alerta. |

### Acompanhamentos — `/acompanhamentos`

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/acompanhamentos/` | Cadastra um acompanhamento. |
| `GET` | `/acompanhamentos/` | Lista os acompanhamentos. |
| `GET` | `/acompanhamentos/usuario/{usuario_id}` | Lista os acompanhamentos de um usuário. |
| `GET` | `/acompanhamentos/{acompanhamento_id}` | Busca um acompanhamento pelo ID. |
| `PUT` | `/acompanhamentos/{acompanhamento_id}` | Atualiza um acompanhamento. |
| `DELETE` | `/acompanhamentos/{acompanhamento_id}` | Exclui um acompanhamento. |

## Fluxo básico de utilização

1. Inicie a aplicação e abra a documentação em `/docs`.
2. Cadastre um usuário pelo endpoint `POST /usuarios/`.
3. Utilize o ID retornado no cadastro para associar contatos, alertas e acompanhamentos ao usuário.
4. Consulte, atualize ou exclua os registros utilizando os endpoints correspondentes.

## Observações

- Os dados de conexão com o Oracle são carregados pelo arquivo `.env`.
- O arquivo `.env` não deve ser versionado nem compartilhado, pois contém credenciais.
- A API utiliza schemas para validar os dados recebidos.
- As operações de banco de dados são executadas pelos serviços da aplicação.
- A exclusão de um usuário também remove os registros relacionados, conforme a implementação do serviço de usuários.
- A documentação interativa é disponibilizada pelo Swagger UI em `/docs`.

## Status do projeto

Projeto acadêmico em desenvolvimento, com API REST integrada ao Oracle Database e operações de gerenciamento para usuários, contatos de emergência, alertas e acompanhamentos.
