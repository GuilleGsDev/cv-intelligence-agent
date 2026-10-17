import json
from unittest.mock import MagicMock, patch
from django.test import TestCase
from apps.tracker.models import JobApplication
from apps.tracker.services.gemini_service import GeminiAnalyzerService


class JobApplicationModelTest(TestCase):
    def setUp(self):
        self.application = JobApplication.objects.create(
            company_name="Empresa Minera SpA",
            role_title="Backend Python Developer",
            job_description="Buscamos dev con Django y APIs REST.",
            gap_analysis={"missing_skills": ["Docker"], "matching_skills": ["Python", "SQL"]},
            cv_suggestions=["Destacar experiencia en Teck Resources"],
            qa_answers={"disponibilidad": "Inmediata"}
        )

    def test_job_application_creation(self):
        """Verifica que el modelo se guarde correctamente en la base de datos."""
        self.assertEqual(self.application.company_name, "Empresa Minera SpA")
        self.assertEqual(self.application.role_title, "Backend Python Developer")
        self.assertIn("Docker", self.application.gap_analysis["missing_skills"])

    def test_str_representation(self):
        """Verifica que la representación en string sea amigable."""
        expected_str = "Backend Python Developer en Empresa Minera SpA"
        self.assertEqual(str(self.application), expected_str)


class GeminiAnalyzerServiceTest(TestCase):
    @patch.dict("os.environ", {"GEMINI_API_KEY": "fake-test-key"})
    @patch("apps.tracker.services.gemini_service.genai.Client")
    def test_analyze_job_offer_success(self, mock_client_class):
        """
        Verifica que el servicio cargue el contexto, invoque a Gemini
        y parsee correctamente la respuesta JSON simulada.
        """
        mock_response_data = {
            "gap_analysis": {
                "matching_skills": ["Python", "SQL"],
                "missing_skills": ["Kubernetes"],
                "match_percentage": 80,
                "summary": "Buen match general con experiencia sólida en Teck Resources."
            },
            "cv_suggestions": [
                "Enfatizar diseño de arquitectura RAG en el resumen inicial"
            ],
            "qa_answers": {
                "disponibilidad": "Inmediata",
                "pretension_renta": "$1.000.000 CLP"
            }
        }

        # Simulamos la respuesta de Gemini para el nuevo SDK (client.models.generate_content)
        mock_client_instance = MagicMock()
        mock_response = json.dumps(mock_response_data)
        mock_client_instance.models.generate_content.return_value.text = mock_response
        mock_client_class.return_value = mock_client_instance

        service = GeminiAnalyzerService()
        result = service.analyze_job_offer("Se busca desarrollador Python con Kubernetes")

        # Verificamos que se llamó a la API simulada y que los datos se procesaron bien
        mock_client_instance.models.generate_content.assert_called_once()
        self.assertEqual(result["gap_analysis"]["match_percentage"], 80)
        self.assertIn("Kubernetes", result["gap_analysis"]["missing_skills"])
        self.assertEqual(result["qa_answers"]["disponibilidad"], "Inmediata")
