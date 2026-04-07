# Taller de Agentes - Universidad

Repositorio de ejemplos prácticos con **LangChain** y **OpenAI** para aprender los fundamentos de los LLMs.

- **Python**: 3.11 o superior
- **Framework**: LangChain
- **Proveedor de LLMs**: OpenAI

## Requisitos previos

- Python 3.11+
- Clave de API de OpenAI (Solicitar a la persona que está impartiendo el taller)

## Instalación

### Con uv (recomendado)

```bash
# Clonar o entrar en el directorio del proyecto
cd "Taller Agentes Universidad"

# Instalar dependencias
uv sync

# Configurar la clave de API
cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

### Con pip

```bash
cd "Taller Agentes Universidad"

pip install -r requirements.txt

cp .env.example .env
# Editar .env y añadir tu OPENAI_API_KEY
```

## Estructura del proyecto

```
├── sesion_1/           # Fundamentos de LLMs
│   ├── 1_tokenizacion.py
│   ├── 2_control_creatividad.py
│   ├── 3_roles_system_prompt.py
│   ├── 4_extraccion_json.py
│   └── 5_function_calling.py
```

## Ejemplos

### Sesión 1: Fundamentos

| Ejemplo | Descripción | Con uv | Con python |
|---------|-------------|--------|------------|
| **1. Tokenización** | Cómo una frase se convierte en IDs de tokens y su impacto en coste/límite | `uv run sesion_1/1_tokenizacion.py` | `python sesion_1/1_tokenizacion.py` |
| **2. Control de creatividad** | Mismo prompt con temperatura 0 vs 1.5 para ver la degradación del lenguaje | `uv run sesion_1/2_control_creatividad.py` | `python sesion_1/2_control_creatividad.py` |
| **3. Roles y System Prompt** | El mismo mensaje con tres system prompts distintos (profesor, niños, escéptico) para ver cómo moldean el comportamiento del modelo | `uv run sesion_1/3_roles_system_prompt.py` | `python sesion_1/3_roles_system_prompt.py` |
| **4. Extracción JSON** | Obligar al modelo a responder con JSON válido para que un programa pueda leerlo | `uv run sesion_1/4_extraccion_json.py` | `python sesion_1/4_extraccion_json.py` |
| **5. Function Calling** | El modelo indica "necesito llamar a enviar_correo()" en lugar de responder con texto | `uv run sesion_1/5_function_calling.py` | `python sesion_1/5_function_calling.py` |

### Notas

- **1_tokenizacion.py** no requiere API key (usa tiktoken localmente).
- El resto de ejemplos necesita `OPENAI_API_KEY` en `.env`.
