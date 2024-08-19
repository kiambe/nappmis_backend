from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Project

def get_projects(request):
    projects = Project.objects.all()
    # Convert queryset to list of dictionaries
    projects_list = list(projects.values())
    return JsonResponse({'projects': projects_list}, status=200)

def create_project(request, project_details):  
    try:
        Project.objects.create(
            title=project_details.get('title'),
            start_date=project_details.get('start_date'),
            end_date=project_details.get('end_date'),
            extension_period=project_details.get('extension_period', ''),
            overview=project_details.get('overview'),
            program_objectives=project_details.get('program_objectives'),
            sources_of_funds=project_details.get('sources_of_funds'),
            gok_counterpart_contribution=project_details.get('gok_counterpart_contribution', 0.0),
            development_partner_contribution=project_details.get('development_partner_contribution', 0.0),
            estimated_total_value=project_details.get('estimated_total_value', 0.0),
            status=project_details.get('status'),
            county_coverage=project_details.get('county_coverage'),
            value_chains=project_details.get('value_chains'),
            target_and_beneficiaries=project_details.get('target_and_beneficiaries'),
            major_achievements=project_details.get('major_achievements'),
            project_pad=project_details.get('project_pad', None),  # Handle file upload separately if needed
            challenges=project_details.get('challenges'),
            recommended_actions=project_details.get('recommended_actions')
        )
        return JsonResponse({'status': 'success'}, status=201)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def update_project(request, project_id, project_details):
    # Retrieve the project to update
    project = get_object_or_404(Project, id=project_id)
    
    # Update fields
    for field, value in project_details.items():
        if hasattr(project, field):
            setattr(project, field, value)
    
    try:
        project.save()
        return JsonResponse({'status': 'success', 'project_id': project.id}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
def delete_project(request, id):
    # Retrieve the project to delete
    project = get_object_or_404(Project, id=id)

    try:
        project.delete()
        return JsonResponse({'status': 'success'}, status=204)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


