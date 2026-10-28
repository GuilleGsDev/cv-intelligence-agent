import json
import os
from google import genai
from django.conf import settings


class GeminiAnalyzerService:
    """
    Servicio encargado de conectar con Google Gemini mediante el nuevo SDK (google-genai)
    para analizar ofertas laborales contra el contexto estático del candidato.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en las variables de entorno.")

        # Cliente del nuevo SDK oficial de Google
        self.client = genai.Client(api_key=api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

    def _load_static_context(self) -> tuple[str, str]:
        """Carga el contenido de cv_base.md y qa_base.md desde la carpeta docs/."""
        docs_dir = settings.BASE_DIR / "docs"
        cv_path = docs_dir / "cv_base.md"
        qa_path = docs_dir / "qa_base.md"

        if not cv_path.exists() or not qa_path.exists():
            raise FileNotFoundError("Los archivos de contexto en docs/ no fueron encontrados.")

        cv_content = cv_path.read_text(encoding="utf-8")
        qa_content = qa_path.read_text(encoding="utf-8")
        return cv_content, qa_content

    def _build_prompt(self, job_description: str, cv_content: str, qa_content: str) -> str:
        """Construye el prompt con instrucciones estrictas de no alucinación."""
        rules = (
            "1. Tu ÚNICA fuente de verdad sobre el candidato es el 'CV BASE' y el 'QA BASE'.\n"
            "2. Queda ESTRICTAMENTE PROHIBIDO inventar, asumir o inferir experiencia técnica "
            "o herramientas que no estén detalladas en el CV Base.\n"
            "3. Si la oferta exige una tecnología que el candidato NO tiene, regístrala "
            "en 'missing_skills'. NO justifiques que la sabe ni suavices la carencia técnica.\n"
            "4. Las sugerencias de adaptación deben indicar qué resaltar del CV Base REAL, "
            "sin alterar datos verídicos.\n"
            "5. Redacta las respuestas a preguntas filtro con el tono del QA BASE "
            "(primera persona)."
        )

        return f"""
        Eres un Tech Lead evaluando la compatibilidad real de un candidato para una vacante.

        REGLAS ESTRICTAS DE SEGURIDAD (ANTI-ALUCINACIÓN):
        {rules}

        ---
        CONTEXTO DEL CANDIDATO (CV BASE):
        {cv_content}

        ---
        GUÍA DE ESTILO Y RESPUESTAS (QA BASE):
        {qa_content}

        ---
        DESCRIPCIÓN DE LA OFERTA LABORAL:
        {job_description}

        ---
        FORMATO DE SALIDA REQUERIDO (JSON PURO):
        {{
            "gap_analysis": {{
                "matching_skills": ["habilidad 1", "habilidad 2"],
                "missing_skills": ["requisito no cumplido 1"],
                "match_percentage": 85,
                "summary": "Resumen técnico objetivo."
            }},
            "cv_suggestions": [
                "Sugerencia 1 en viñeta",
                "Sugerencia 2 en viñeta"
            ],
            "qa_answers": {{
                "disponibilidad": "Respuesta basada en qa_base",
                "pretension_renta": "Respuesta basada en qa_base",
                "motivacion_rol": "Por qué su experiencia en Teck encaja aquí"
            }}
        }}
        """

    def analyze_job_offer(self, job_description: str) -> dict:
        """
        Ejecuta el análisis de la oferta laboral y devuelve un diccionario estructurado.
        """
        cv_content, qa_content = self._load_static_context()
        prompt = self._build_prompt(job_description, cv_content, qa_content)

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        try:
            return json.loads(response.text)
        except json.JSONDecodeError as err:
            raise ValueError(f"Gemini no devolvió un JSON válido: {response.text}") from err
