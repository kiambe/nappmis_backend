from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project

def get_projects(request, project_details):
    pass

def create_project(request, project_details):
    #check permissions
    
    title = project_details.get('title')
    start_date = project_details.get('start_date')
    end_date = project_details.get('end_date')
    extension_period = project_details.get('extension_period', '')
    overview = project_details.get('overview')
    program_objectives = project_details.get('program_objectives')
    sources_of_funds = project_details.get('sources_of_funds')
    gok_counterpart_contribution = project_details.get('gok_counterpart_contribution', 0.0)
    development_partner_contribution = project_details.get('development_partner_contribution', 0.0)
    estimated_total_value = project_details.get('estimated_total_value', 0.0)
    status = project_details.get('status')
    county_coverage = project_details.get('county_coverage')
    value_chains = project_details.get('value_chains')
    target_and_beneficiaries = project_details.get('target_and_beneficiaries')
    major_achievements = project_details.get('major_achievements')
    project_pad = project_details.get('project_pad', None)  # Handle file uploads separately
    challenges = project_details.get('challenges')
    recommended_actions = project_details.get('recommended_actions')
    
    try:
        project = Project.objects.create(
            title=title,
            start_date=start_date,
            end_date=end_date,
            extension_period=extension_period,
            overview=overview,
            program_objectives=program_objectives,
            sources_of_funds=sources_of_funds,
            gok_counterpart_contribution=gok_counterpart_contribution,
            development_partner_contribution=development_partner_contribution,
            estimated_total_value=estimated_total_value,
            status=status,
            county_coverage=county_coverage,
            value_chains=value_chains,
            target_and_beneficiaries=target_and_beneficiaries,
            major_achievements=major_achievements,
            project_pad=project_pad,  # Handle file upload separately if needed
            challenges=challenges,
            recommended_actions=recommended_actions
        )
        return JsonResponse({'status': 'success', 'project_id': project.id}, status=201)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def update_project(request, project_details):
    pass

def delete_project(request, project_details):
    pass


