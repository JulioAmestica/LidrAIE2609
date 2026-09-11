# LLM Estimator

API en FastAPI que recibe la transcripcion de una reunion y devuelve una estimacion de esfuerzo generada con un modelo LLM.

## Requisitos

- Python 3.12+
- `uv` o `pip`
- Una API key de OpenAI

## Configuracion

Crea o actualiza el archivo `.env` en la raiz del proyecto:

```env
OPENAI_API_KEY=tu_api_key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
APP_ENV=development
LOG_LEVEL=INFO
```

## Instalacion

Con `uv`:

```powershell
uv sync
```

O con `pip`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic-settings openai python-dotenv
```

## Ejecutar la API

```powershell
uvicorn app.main:app --reload
```

La documentacion interactiva queda disponible en:

```text
http://localhost:8000/docs
```

## Endpoints

### Health check

```http
GET /health
```

Respuesta esperada:

```json
{
  "status": "ok"
}
```

### Estimar esfuerzo

```http
POST /api/v1/estimate
```

Body:

```json
{
  "transcription": "Texto de la reunion a estimar"
}
```

Ejemplo en PowerShell:

```powershell
$uri = 'http' + '://localhost:8000/api/v1/estimate'

$body = @{
  transcription = 'En la reunion con el equipo de marketing, el cliente explico que necesita una landing page con formulario de contacto, integracion con HubSpot y una seccion de blog con editor WYSIWYG. El plazo ideal seria tenerlo listo en 4 semanas. El diseno ya existe en Figma.'
} | ConvertTo-Json

$utf8Body = [System.Text.Encoding]::UTF8.GetBytes($body)

Invoke-RestMethod -Uri $uri -Method Post -ContentType 'application/json; charset=utf-8' -Body $utf8Body
```

Respuesta esperada:

```json
{
  "estimation": "...",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "tokens_used": null,
  "cost_estimated": null,
  "timestamp": "2026-09-11T00:00:00+00:00"
}
```

## Estructura

```text
app/
  main.py                         # Entrada FastAPI
  config.py                       # Configuracion desde .env
  routers/
    estimations.py                # Endpoint de estimacion
    estimationRequest.py          # Modelo de request
    estimationResponse.py         # Modelo de response
  services/
    llm_service.py                # Integracion con OpenAI
```

## Notas

- En PowerShell, `curl` suele ser alias de `Invoke-WebRequest`; para probar la API es mas simple usar `Invoke-RestMethod`.
- Si usas texto con acentos o caracteres especiales, envia el body como UTF-8 para evitar errores de parsing.
- El endpoint `/api/v1/estimate` requiere `OPENAI_API_KEY`; `/health` no.
