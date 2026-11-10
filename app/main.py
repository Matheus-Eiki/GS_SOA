
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import usuarios
from app.routers import contatos
from app.routers import alertas
from app.routers import acompanhamentos


app = FastAPI(
    title="CitizenTech",
    description="API de assistência e acompanhamento",
    version="1.0.0"
)


app.include_router(usuarios.router)
app.include_router(contatos.router)
app.include_router(alertas.router)
app.include_router(acompanhamentos.router)


@app.get("/", response_class=HTMLResponse)
def inicio():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>CitizenTech</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                background: #171426;
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
                color: #a78bfa;
            }

            p {
                color: #c4c0d4;
                margin-bottom: 30px;
                line-height: 1.6;
            }

            .botao {
                display: inline-block;
                padding: 15px 30px;
                background: #7c3aed;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
                transition: 0.3s;
            }

            .botao:hover {
                background: #6d28d9;
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

            <h1>CitizenTech</h1>

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


@app.get("/status")
def status():
    return {
        "status": "online"
    }
