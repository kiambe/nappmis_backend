from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class ProjectCoordinationUnit(models.Model):
    LEVEL_CHOICES = [
        ('National', 'National'),
        ('County', 'County'),
    ]

    SUB_SECTOR_CHOICES = [
        ('Crops', 'Crops'),
        ('Livestock', 'Livestock'),
    ]

    unit_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    coordinator = models.CharField(max_length=255)
    monitoring_eval_officer = models.ForeignKey()
    office_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    sub_sector = models.CharField(max_length=20, choices=SUB_SECTOR_CHOICES)

    def __str__(self):
        return self.name


class CountyGovernment(models.Model):
    county_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    county_map_shapefile = models.URLField(max_length=2000, blank=True, null=True)
    centroid_gps = models.CharField(max_length=50)  # Latitude and longitude in 'lat, long' format
    county_population = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    number_of_projects = models.PositiveIntegerField(default=0)
    office_address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website_urls = models.JSONField(default=list, blank=True)  # List of URLs
    key_responsibilities = models.TextField()

    def __str__(self):
        return self.name
    

class Project(models.Model):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    extension_period = models.CharField(max_length=255, blank=True, null=True)
    project_overview = models.TextField()
    project_components = models.TextField()
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

    # Relationships
    units = models.ForeignKey(ProjectCoordinationUnit, related_name='project coordination unit')
    counties = models.ForeignKey(CountyGovernment, related_name='projects')

    def __str__(self):
        return self.title

class DevelopmentPartner(models.Model):
    SCOPES = [
        ('International', 'International'),
        ('Local', 'Local'),
        ('National', 'National'),
    ]

    ORGANIZATION_TYPES = [
        ('Funding', 'Funding'),
        ('Technical Assistance', 'Technical Assistance'),
    ]

    THEME_FOCUSES = [
        ('Resilience', 'Resilience'),
        ('Food Security', 'Food Security'),
        ('Climate Change', 'Climate Change'),
    ]

    SECTORS = [
        ('Crops', 'Crops'),
        ('Livestock', 'Livestock'),
        ('Aquaculture', 'Aquaculture'),
        ('Apiculture', 'Apiculture'),
    ]
    CONTRIBUTION_TYPE = [('Loan', 'Loan'), ('Grant', 'Grant'), ('Other', 'Other')]
    name = models.CharField(max_length=255)
    website_url = models.URLField()
    headquarter_locations = models.CharField(max_length=255)
    scope = models.CharField(max_length=20, choices=SCOPES)
    organization_type = models.CharField(max_length=30, choices=ORGANIZATION_TYPES) # Funding, Technical Assistance.
    theme_focus =  ArrayField(
        ArrayField(
            models.CharField(max_length=10, blank=True),
            size=8,
        ),
        size=8,
    ) # Resilience, Food Security, Climate Change.
    sector = models.CharField(max_length=20, choices=SECTORS) # Crops, Livestock, Aquaculture, Apiculture.
    logo = models.ImageField()
    projects_funded = models.ForeignKey(Project)
    reporting_requirements = models.TextField()
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2)
    contribution_type = models.CharField(max_length=10, choices=CONTRIBUTION_TYPE) # Loan, Grant, or Other (e.g., In-kind support).
    support_start = models.DateField()
    support_end = models.DateField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Funds(models.Model):
    FUNDING_SOURCE_CHOICES = [
        ('Government', 'Government'),
        ('Donor', 'Donor'),
        # Add more funding sources as needed
    ]

    FUNDING_TYPE_CHOICES = [
        ('Grant', 'Grant'),
        ('Loan', 'Loan'),
    ]

    funding_source = models.CharField(max_length=100, choices=FUNDING_SOURCE_CHOICES)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    availability_date = models.DateField()
    allocations = models.TextField()  # You might want to use a more structured format, e.g., JSON
    utilization_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    funding_type = models.CharField(max_length=10, choices=FUNDING_TYPE_CHOICES)
    project = models.ForeignKey(Project, related_name='funds', on_delete=models.CASCADE)
    provided_by = models.ForeignKey(DevelopmentPartner, related_name='funds', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.funding_source} - {self.amount} - {self.project.title}"
    
class SubProject(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Ongoing', 'Ongoing'),
        ('Not Started', 'Not Started'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    ]

    TARGET_SECTOR_CHOICES = [
        ('Crops', 'Crops'),
        ('Livestock', 'Livestock'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    AGE_CHOICES = [
        ('<18', 'Under 18'),
        ('18-35', '18-35'),
        ('36-50', '36-50'),
        ('51+', '51 and over'),
    ]
    name = models.CharField()
    description = models.TextField()
    status = models.CharField() # Current status (e.g., Active, Ongoing, Not Started).
    start_date = models.DateField()
    expected_end_date = models.DateField()
    expected_budget = models.DecimalField()
    disbursed_amounts = models.DecimalField()
    utilized_amount = models.DecimalField()
    objectives = models.TextField()
    outcomes = models.TextField()
    milestones = models.TextField()
    project_type = models.CharField(max_length=100)
    achievements = models.TextField()
    funding_sources = models.TextField()  # List or description of funding sources
    project_location = models.ManyToManyField(CountyGovernment, related_name='sub_projects')  # A sub-project can be in multiple counties
    project_partners = models.TextField()  # List or description of partners
    beneficiaries_count = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    beneficiary_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    beneficiary_age = models.CharField(max_length=10, choices=AGE_CHOICES)
    actual_beneficiaries = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    reporting_requirements = models.TextField()
    performance_indicators = models.TextField()
    target_sector = models.CharField(max_length=20, choices=TARGET_SECTOR_CHOICES)
    Challenges = models.TextField()
    project = models.ForeignKey(Project, related_name="parent project")
    location = models.ForeignKey(CountyGovernment, related_name="located within which county")


