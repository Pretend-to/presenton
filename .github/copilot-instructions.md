# Presenton AI Coding Instructions

## Project Overview

Presenton is an **open-source AI presentation generator** with a dual-server architecture:
- **FastAPI backend** (`servers/fastapi/`) - Handles AI generation, document processing, and PPTX creation
- **Next.js frontend** (`servers/nextjs/`) - React/TypeScript UI with Tailwind CSS
- **MCP Server** (`servers/fastapi/mcp_server.py`) - Model Context Protocol interface (port 8001)
- **Nginx** - Routes frontend (:3000), backend API (:8000), and MCP (:8001) through port 80/5000

## Architecture & Data Flow

### Presentation Generation Pipeline
1. **User Input** → Frontend collects content/config → POST `/api/v1/ppt/presentation/generate`
2. **Outline Generation** → `generate_ppt_outline()` uses LLM to create slide outlines from content
3. **Structure Selection** → `generate_presentation_structure()` maps outlines to template layouts
4. **Content Population** → `get_slide_content_from_type_and_outline()` generates Zod schema data for each slide
5. **PPTX Creation** → `PptxPresentationCreator` converts `PptxPresentationModel` to python-pptx format
6. **Export** → Returns presentation ID, file path, and edit URL

### Key Services & Singletons
```python
# Global service instances (servers/fastapi/services/)
TEMP_FILE_SERVICE = TempFileService()      # Manages temp directories per request
CONCURRENT_SERVICE = ConcurrentService()    # Limits concurrent LLM/image calls
LLMClient()                                 # Multi-provider LLM abstraction (OpenAI/Gemini/Anthropic/Ollama)
ImageGenerationService()                    # Image generation (DALL-E/Gemini/Pexels/Pixabay)
```

### Template System (Critical Pattern)
Templates are **React components** (`servers/nextjs/presentation-templates/`) that export:
1. **Zod Schema** - Defines slide data structure with metadata
2. **React Component** - Renders slide as HTML (converted to PPTX via html2canvas + python-pptx)

```tsx
// Example: servers/nextjs/presentation-templates/general/TitleSlide.tsx
export const Schema = z.object({
  title: z.string().meta({ description: "Main title" }),
  subtitle: z.string().optional(),
  backgroundImage: ImageSchema.default({
    __image_url__: "...",
    __image_prompt__: "background image description"
  })
});

export default function TitleSlide({ data }: { data: z.infer<typeof Schema> }) {
  return <div className="aspect-video w-[1280px] h-[720px]">...</div>;
}
```

**AI generates data matching this schema**, then the component renders it.

## Development Workflow

### Local Development Setup
```bash
# Install dependencies (automatically handled by start.js)
cd servers/nextjs && npm install
cd servers/fastapi && pip install -r requirements.txt

# Start all services (dev mode with hot reload)
node start.js --dev

# Ports:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - MCP Server: http://localhost:8001
# - Nginx Proxy: http://localhost:5000 (production)
```

### Docker Development
```bash
# Build and run with docker-compose
docker-compose up production        # Standard mode
docker-compose up production-gpu    # With GPU support for Ollama

# Environment variables (see docker-compose.yml)
LLM=openai|google|anthropic|ollama|custom
OPENAI_API_KEY=...
CAN_CHANGE_KEYS=true|false  # Controls if UI allows key modification
```

### Testing
```bash
# Backend tests (pytest)
cd servers/fastapi
pytest tests/

# Key test files:
# - tests/test_presentation_generation_api.py - E2E presentation generation
# - tests/test_pptx_creator.py - PPTX model rendering
# - tests/test_mcp_server.py - MCP tool validation
```

## Code Conventions & Patterns

### Backend (FastAPI)
- **Models** (`models/`) - Pydantic models for request/response + SQL (SQLModel)
  - `pptx_models.py` - Core PPTX structure (PptxSlideModel, PptxShapeModel, etc.)
  - `generate_presentation_request.py` - API request schema
  - `sql/*.py` - SQLModel database entities (PresentationModel, SlideModel)
- **Services** (`services/`) - Stateful business logic (initialized once)
- **Utils** (`utils/`) - Stateless helper functions
  - `llm_calls/*.py` - Structured LLM prompts for each generation phase
- **Enums** (`enums/`) - Typed constants (LLMProvider, Tone, Verbosity, ImageProvider)

### Frontend (Next.js)
- **App Router** (`app/`) - Next.js 13+ file-based routing
- **Components** (`components/`) - Shared React components
- **Store** (`store/`) - Redux Toolkit state management
- **API Calls** - Direct fetch to `/api/v1/*` (proxied by nginx in production)

### LLM Integration Pattern
```python
# ALL LLM calls go through LLMClient (services/llm_client.py)
client = LLMClient()  # Auto-detects provider from env

# Structured output (JSON mode or tool calls)
result = await client.generate_with_response_model(
    messages=[LLMSystemMessage(...), LLMUserMessage(...)],
    response_model=YourPydanticModel,
    tools=[SearchWebTool()] if web_search else None
)

# Streaming responses
async for chunk in client.generate_stream(...):
    yield chunk
```

**Never call OpenAI/Gemini/Anthropic directly** - always use LLMClient abstraction.

### Database Pattern
```python
# Async SQLModel sessions via dependency injection
from services.database import get_async_session

@router.post("/...")
async def endpoint(sql_session: AsyncSession = Depends(get_async_session)):
    # Query
    result = await sql_session.execute(select(PresentationModel).where(...))
    presentation = result.scalar_one_or_none()
    
    # Insert
    new_slide = SlideModel(presentation=presentation_id, index=0, ...)
    sql_session.add(new_slide)
    await sql_session.commit()
```

### Asset Management
- **Images** - `app_data/images/{presentation_id}/` 
- **Exports** - `app_data/exports/{presentation_id}/`
- **Temp files** - Use `TEMP_FILE_SERVICE.get_temp_dir()` (auto-cleanup)
- **Network images** - Downloaded via `download_files()` before PPTX creation

## Critical Files & Entry Points

### Backend Entry Points
- `servers/fastapi/server.py` - Uvicorn startup
- `servers/fastapi/api/main.py` - FastAPI app configuration
- `servers/fastapi/api/v1/ppt/endpoints/presentation.py` - Core presentation endpoints
  - `/generate` - Main generation endpoint (line 804)
  - `/create` - Create outline only
  - `/prepare` - Generate structure from outline
  - `/export` - Convert to PPTX/PDF

### Frontend Entry Points
- `servers/nextjs/app/page.tsx` - Home page
- `servers/nextjs/components/Home.tsx` - Main UI component
- `servers/nextjs/app/(presentation-generator)/` - Presentation workflow pages

### Configuration
- `start.js` - Orchestrates server startup, reads env vars, creates userConfig.json
- `app_data/userConfig.json` - Runtime config (API keys, model selection)
- `nginx.conf` - Production routing (proxies Next.js, FastAPI, MCP)

## Common Pitfalls

1. **Image Paths** - Always use absolute paths or proper `/app_data/` relative paths
2. **LLM Schema Validation** - Ensure Pydantic models have `strict=True` for OpenAI compatibility
3. **Template Dimensions** - Slides MUST be 1280x720px (`aspect-video` + `w-[1280px] h-[720px]`)
4. **Async Context** - All DB/LLM operations are async, use `await` consistently
5. **Environment Variables** - Backend reads from `userConfig.json` (synced by middleware), not directly from env

## Debugging Tips

- **LLM Failures** - Check `services/llm_client.py` for provider-specific error handling
- **PPTX Issues** - Inspect `PptxPresentationModel` JSON structure before passing to `PptxPresentationCreator`
- **Template Errors** - Validate Zod schema matches generated data structure
- **API Routing** - In production, remember nginx proxies `/api/v1/` to port 8000

## External Documentation
- Official Docs: https://docs.presenton.ai
- API Reference: https://docs.presenton.ai/using-presenton-api
- Discord Community: https://discord.gg/9ZsKKxudNE
