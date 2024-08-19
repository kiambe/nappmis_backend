from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    extension_period = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField()
    program_objectives = models.TextField()
    sources_of_funds = models.TextField()
    gok_counterpart_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    development_partner_contribution = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_total_value = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.IntegerField()
    county_coverage = models.CharField(max_length=255)
    value_chains = models.CharField(max_length=255)
    target_and_beneficiaries = models.TextField()
    major_achievements = models.TextField()
    project_pad = models.FileField(upload_to='project_pads/', blank=True, null=True)
    challenges = models.TextField()
    recommended_actions = models.TextField()

    def __str__(self):
        return self.title

