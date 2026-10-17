# Agente Inteligente de Adaptación de CV

MVP de un agente inteligente diseñado para analizar ofertas laborales, contrastarlas contra un CV base estático sin inventar experiencia, y generar sugerencias de mejora y respuestas a preguntas filtro.

## 🛠 Stack Tecnológico
- **Backend:** Python / Django
- **Base de Datos:** PostgreSQL (vía Supabase)
- **Frontend:** HTML5, Tailwind CSS, Vanilla JS
- **Motor de IA:** Google Gemini 1.5 Pro API
- **Infraestructura & CI/CD:** GitHub Actions + Render

## 📁 Arquitectura de Contexto
El sistema utiliza una arquitectura híbrida:
1. **Contexto Estático (`docs/`):** `cv_base.md` y `qa_base.md` actúan como la única fuente de verdad para evitar alucinaciones del modelo.
2. **Historial Dinámico (PostgreSQL):** Registro y trazabilidad de cada postulación realizada.

## 🚀 Entorno de Desarrollo Local
*(Se detallará paso a paso en el proceso de inicialización)*

## 🌿 Convenciones de Trabajo
- Git Flow simplificado: `main` (prod), `develop` (staging), `feature/*` (funcionalidades).
- Commits bajo estándar [Conventional Commits](https://www.conventionalcommits.org/).
- Cobertura de pruebas unitarias obligatoria antes de mergear a ramas principales.