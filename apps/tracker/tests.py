from django.test import TestCase
from apps.tracker.models import JobApplication


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
