from django.db import models


class JobApplication(models.Model):
    """
    Representa una postulación y el análisis inteligente generado
    por el agente para una oferta laboral específica.
    """
    company_name = models.CharField(
        max_length=200,
        verbose_name="Nombre de la Empresa"
    )
    role_title = models.CharField(
        max_length=200,
        verbose_name="Cargo / Puesto"
    )
    job_description = models.TextField(
        verbose_name="Descripción de la Oferta"
    )

    # Resultados del Análisis de IA (Estructurados en JSON)
    gap_analysis = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Análisis de Brecha (Gap Analysis)"
    )
    cv_suggestions = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Sugerencias de Adaptación del CV"
    )
    qa_answers = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Respuestas a Preguntas Filtro"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Postulación de Empleo"
        verbose_name_plural = "Postulaciones de Empleo"

    def __str__(self):
        return f"{self.role_title} en {self.company_name}"
