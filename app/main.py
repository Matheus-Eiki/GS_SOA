
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.routers import usuarios
from app.routers import contatos
from app.routers import alertas
from app.routers import acompanhamentos


app = FastAPI(
    title="Moving Health",
    description="API de assistência e acompanhamento",
    version="1.0.0",
    docs_url=None
)


# REGISTRO DAS ROTAS
app.include_router(usuarios.router)
app.include_router(contatos.router)
app.include_router(alertas.router)
app.include_router(acompanhamentos.router)


# DOCUMENTAÇÃO SWAGGER COM TEMA ESCURO
@app.get("/docs", include_in_schema=False)
def documentacao():

    html = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Documentação"
    )

    conteudo = html.body.decode("utf-8")

    css = """
    <style>

        /* FUNDO GERAL */
        html,
        body,
        .swagger-ui {
            background: #000000 !important;
            color: #ffffff !important;
        }

        /* TEXTOS GERAIS */
        .swagger-ui h1,
        .swagger-ui h2,
        .swagger-ui h3,
        .swagger-ui h4,
        .swagger-ui p,
        .swagger-ui span,
        .swagger-ui label,
        .swagger-ui td,
        .swagger-ui th,
        .swagger-ui li,
        .swagger-ui div {
            color: #ffffff !important;
        }

        /* BARRA SUPERIOR */
        .swagger-ui .topbar {
            background: #111111 !important;
        }

        /* INFORMAÇÕES DA API */
        .swagger-ui .info,
        .swagger-ui .scheme-container {
            background: #000000 !important;
        }

        /* ENDPOINTS */
        .swagger-ui .opblock,
        .swagger-ui .opblock-summary,
        .swagger-ui .opblock-body,
        .swagger-ui .responses-wrapper,
        .swagger-ui .responses-inner,
        .swagger-ui .parameters-container,
        .swagger-ui .opblock-description-wrapper {
            background: #111111 !important;
            color: #ffffff !important;
        }

        /* SEÇÃO SCHEMAS */
        .swagger-ui section.models,
        .swagger-ui .models,
        .swagger-ui .models h4,
        .swagger-ui .model-container,
        .swagger-ui .model-box,
        .swagger-ui .model-box-control,
        .swagger-ui .model,
        .swagger-ui .model-title,
        .swagger-ui .model-example {
            background: #171717 !important;
            color: #ffffff !important;
            border-color: #444444 !important;
        }

        /* TODOS OS TEXTOS DENTRO DE SCHEMAS */
        .swagger-ui section.models *,
        .swagger-ui .models * {
            color: #ffffff !important;
        }

        /* BOTÕES DOS MODELOS */
        .swagger-ui section.models button,
        .swagger-ui .models button,
        .swagger-ui .model-box-control,
        .swagger-ui .models-control {
            background: #222222 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
            box-shadow: none !important;
            appearance: none !important;
        }

        /* NOMES DOS MODELOS */
        .swagger-ui .model-title,
        .swagger-ui .model-title span,
        .swagger-ui .model-box-control span {
            background: transparent !important;
            color: #ffffff !important;
        }

        /* PROPRIEDADES DOS MODELOS */
        .swagger-ui .prop-name,
        .swagger-ui .prop-type,
        .swagger-ui .prop-format,
        .swagger-ui .property,
        .swagger-ui .model .property {
            color: #ffffff !important;
        }

        /* ÍCONES DOS MODELOS */
        .swagger-ui section.models svg,
        .swagger-ui .models svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }

        /* CAMPOS DE ENTRADA */
        .swagger-ui input,
        .swagger-ui textarea,
        .swagger-ui select {
            background: #222222 !important;
            color: #ffffff !important;
            border: 1px solid #666666 !important;
        }

        /* RESPOSTAS E EXEMPLOS */
        .swagger-ui pre,
        .swagger-ui code,
        .swagger-ui .highlight-code,
        .swagger-ui .microlight,
        .swagger-ui .model-box {
            background: #171717 !important;
            color: #ffffff !important;
        }

        /* TABELAS */
        .swagger-ui table,
        .swagger-ui table tr,
        .swagger-ui table td,
        .swagger-ui table th {
            background: #111111 !important;
            color: #ffffff !important;
        }

        /* BOTÕES GERAIS */
        .swagger-ui .btn {
            background: #222222 !important;
            color: #ffffff !important;
            border-color: #666666 !important;
        }

        /* DESCRIÇÕES E RESPOSTAS */
        .swagger-ui .response-col_status,
        .swagger-ui .response-col_description,
        .swagger-ui .parameter__name,
        .swagger-ui .parameter__type {
            color: #ffffff !important;
        }

    </style>
    """

    # INSERE O CSS NO FINAL DO HTML
    conteudo = conteudo.replace(
        "</body>",
        css + "</body>"
    )

    return HTMLResponse(content=conteudo)


# PÁGINA INICIAL MOVING HEALTH
@app.get("/", response_class=HTMLResponse)
def inicio():

    return """
    <!DOCTYPE html>
    <html lang="pt-br">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>Moving Health</title>

        <style>

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #000000;
                color: white;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                text-align: center;
            }

            .container {
                padding: 40px;
                max-width: 600px;
            }

            h1 {
                font-size: 42px;
                margin-bottom: 15px;
                color: #ffffff;
            }

            p {
                color: #c4c0d4;
                margin-bottom: 30px;
                line-height: 1.6;
            }

            .botao {
                display: inline-block;
                padding: 15px 30px;
                background: #00FFFF;
                color: #000000;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: 0.3s;
            }

            .botao:hover {
                background: #00cccc;
                transform: scale(1.05);
            }

            .status {
                margin-top: 25px;
                color: #86efac;
                font-size: 14px;
            }

        </style>
    </head>

    <body>

        <div class="container">

            <h1>Moving Health</h1>

            <p>
                Plataforma de assistência, acompanhamento
                e segurança para pessoas que precisam de suporte.
            </p>

            <a href="/docs" class="botao">
                Acessar documentação da API
            </a>

            <div class="status">
                ● Sistema online
            </div>

        </div>

    </body>
    </html>
    """


# STATUS DA API
@app.get("/status")
def status():

    return {
        "status": "online"
    }
