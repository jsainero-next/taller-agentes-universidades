# Taller de Agentes - Universidad

Repositorio de ejemplos prácticos con **LangChain** y **OpenAI** para aprender los fundamentos de los LLMs y los agentes de IA.

- **Python**: 3.11 o superior
- **Gestor de paquetes**: [uv](https://docs.astral.sh/uv/)
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
├── sesion_2/           # RAG, herramientas y agentes
│   ├── 1_busqueda_semantica.py
│   ├── 2_conexion_documentos.py
│   ├── 3_memoria_rag.py
│   ├── 4_uso_herramientas.py
│   ├── 5_loop_agente.py
│   └── ejercicios/
│       ├── ejercicio_1_enunciado.py
│       ├── ejercicio_2_enunciado.py
│       └── ejercicio_3_enunciado.py
├── datos/
│   └── documento.pdf   # PDF de ejemplo para RAG
└── scripts/
    └── generar_documento.py  # Genera el PDF de ejemplo
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

### Sesión 2: RAG y Agentes

| Ejemplo | Descripción | Comando |
|---------|-------------|---------|
| **1. Búsqueda semántica** | Embeddings de 3 frases; encontrar la más parecida a una pregunta (sin palabras exactas) | `uv run sesion_2/1_busqueda_semantica.py` |
| **2. Conexión a documentos** | Cargar PDF, trocear (chunking) y consultar con RAG básico | `uv run sesion_2/2_conexion_documentos.py` |
| **3. Memoria en RAG** | Comparativa RAG sin y con memoria: reformulación de preguntas de seguimiento con `history_aware_retriever` | `uv run sesion_2/3_memoria_rag.py` |
| **4. Uso de herramientas** | LLM usa búsqueda en Google para responder sobre noticias recientes | `uv run sesion_2/4_uso_herramientas.py` |
| **5. Loop del agente** | Agente que combina RAG + búsqueda web y muestra el razonamiento en consola | `uv run sesion_2/5_loop_agente.py` |

### Ejercicios Sesión 2

| Ejercicio | Descripción | Comando |
|-----------|-------------|---------|
| **1. Evaluador de relevancia** | Añadir un paso de evaluación JSON al RAG para decidir si el contexto recuperado es suficiente antes de responder | `uv run sesion_2/ejercicios/ejercicio_1_enunciado.py` |
| **2. Memoria por resumen** | Compactar el historial de mensajes cuando supera un umbral, resumiendo los turnos antiguos | `uv run sesion_2/ejercicios/ejercicio_2_enunciado.py` |
| **3. Chat con Streamlit** | Interfaz web de chat con historial persistente en `session_state` y control de temperatura desde la barra lateral | `streamlit run sesion_2/ejercicios/ejercicio_3_enunciado.py` |


### Notas

- **1_tokenizacion.py** no requiere API key (usa tiktoken localmente).
- El resto de ejemplos necesita `OPENAI_API_KEY` en `.env`.
- Para regenerar el PDF de ejemplo: `uv run scripts/generar_documento.py`

---

## Práctica Final: Chatbot Agéntico con RAG, Búsqueda Web y Guardarraíles

### Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                        INTERFAZ (Streamlit)                     │
│                  Chat UI con historial de mensajes              │
└──────────────────────────────┬──────────────────────────────────┘
                               │ mensaje del usuario
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       GUARDARRAÍLES                             │
│  ¿La pregunta es relevante para la temática del documento?      │
│                                                                 │
│       SÍ ──────────────────────────────────────────────┐        │
│       NO → respuesta de rechazo educada                │        │
└────────────────────────────────────────────────────────┼────────┘
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AGENTE ReAct                             │
│              (LangChain + ChatOpenAI, temperatura 0)            │
│                                                                 │
│  Razonamiento:                                                  │
│  1. ¿Tengo suficiente contexto? → usar buscar_en_documento      │
│  2. ¿Necesito info actual/no encontrada? → usar buscar_en_web   │
│  3. Formular respuesta final                                    │
└──────────┬──────────────────────────────┬───────────────────────┘
           │                              │
           ▼                              ▼
┌──────────────────────┐    ┌─────────────────────────────────────┐
│   TOOL: RAG          │    │   TOOL: Búsqueda Web                │
│                      │    │                                     │
│  Base de datos       │    │   DuckDuckGo / Tavily               │
│  vectorial (Chroma)  │    │   para información actual           │
│                      │    │   no presente en el documento       │
│  ← documentos PDF    │    │                                     │
└──────────────────────┘    └─────────────────────────────────────┘
           │                              │
           └──────────────┬───────────────┘
                          ▼
              respuesta final con fuentes
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     INTERFAZ (Streamlit)                        │
│            Respuesta mostrada en el chat + fuentes              │
└─────────────────────────────────────────────────────────────────┘
```

---

### Enunciado

#### Descripción general

Desarrolla un **chatbot agéntico con interfaz web** (Streamlit) especializado en la temática de los documentos que hayas indexado. El chatbot debe ser capaz de responder preguntas consultando primero su base de datos vectorial y, si no encuentra información suficiente, acudir a internet. Para mantener la coherencia del asistente, debe incorporar guardarraíles que rechacen preguntas ajenas al dominio del documento.

---

#### Requisitos funcionales

**1. Interfaz (Streamlit)**
- Pantalla de chat con historial de mensajes persistente durante la sesión.
- Campo de entrada de texto para el usuario.
- Las respuestas del agente deben mostrarse de forma clara, indicando si la información proviene del documento o de internet.
- Opcional: muestra el razonamiento interno del agente (cadena de pensamiento) en un expander o panel lateral.

**2. Guardarraíles (topic guard)**
- Antes de invocar al agente, evalúa si la pregunta es relevante para la temática del documento.
- Si la pregunta está fuera del dominio (por ejemplo, el documento es sobre inteligencia artificial y el usuario pregunta sobre recetas de cocina), el chatbot debe responder con un mensaje educado explicando en qué temáticas puede ayudar, **sin llamar al agente ni consumir herramientas**.
- Implementa el guardarraíl como una llamada al LLM con un system prompt clasificador que devuelva `"relevante"` o `"irrelevante"`.

**3. Herramienta RAG (`buscar_en_documento`)**
- Carga uno o varios PDFs y los indexa en una base de datos vectorial (Chroma u otra).
- Expón el retriever como una `@tool` de LangChain siguiendo el patrón visto en clase.
- El agente debe usarla como primera opción ante cualquier pregunta relevante.

**4. Herramienta de búsqueda web (`buscar_en_internet`)**
- Usa DuckDuckGoSearchRun (o Tavily si dispones de API key) como herramienta de respaldo.
- El agente solo debe llamarla cuando la búsqueda en el documento no haya proporcionado una respuesta satisfactoria, o cuando la pregunta requiera información actualizada que no puede estar en el documento.

**5. Agente**
- Crea un agente ReAct con `create_react_agent` que tenga acceso a ambas herramientas.
- El system prompt del agente debe reforzar su especialización: definir quién es, en qué es experto y el orden de preferencia de las herramientas.

---

#### Requisitos técnicos

| Componente | Tecnología |
|---|---|
| Interfaz | Streamlit |
| Agente | LangChain `create_react_agent` |
| LLM | OpenAI `gpt-5.4-nano` o superior |
| Embeddings | `text-embedding-3-small` |
| Base vectorial | Chroma (persistente o en memoria) |
| Búsqueda web | DuckDuckGoSearchRun |
| Variables de entorno | `python-dotenv` |

---

#### Pistas y referencias

- Revisa `sesion_2/5_loop_agente.py` para ver cómo se combinan RAG y búsqueda web en un agente ReAct.
- Revisa `sesion_2/3_memoria_rag.py` para entender el patrón `history_aware_retriever` que necesitarás para mantener el historial en el chatbot.
- Para arrancar la app: `uv run streamlit run practica_final/app.py`
- El historial de mensajes de Streamlit se gestiona con `st.session_state.messages`.
- Para que el guardarraíl sea robusto, usa `temperature=0` y pide al modelo que responda **únicamente** con la palabra `relevante` o `irrelevante`.
- Si el agente tarda en responder, considera usar `st.spinner()` mientras procesa.
