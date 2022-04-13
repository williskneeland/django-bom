from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.conf import settings
from bom.models import (
    PartClassWorkflowCompletedTransition,
)

def change_workflow_state_and_redirect(request, part, workflow_instance, change_state_form):
    if not change_state_form.is_valid():
        messages.error(request, f"An error occured: {change_state_form.errors['transition']}")

    if change_state_form.cleaned_data['transition'] is None and not workflow_instance.current_state.is_final_state:
        messages.error(request, "Error, please select a transition")
        return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id})+'#workflow')

    selected_transition = change_state_form.cleaned_data['transition']
    comments = change_state_form.cleaned_data['comments']

    if selected_transition is None and not workflow_instance.current_state.is_final_state:
        messages.error(request, "Error, please select a transition")
        return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part_id})+'#workflow')

    if change_state_form.cleaned_data['notifying_next_users'] and not selected_transition.source_state.is_final_state:
        for assigned_user in selected_transition.source_state.assigned_users.all():
            message_context = {
                'assigned_user': assigned_user,
                'part': part,
                'previous_assigned_user': request.user.get_full_name(),
                'comments': comments,
                'transition_name': selected_transition.target_state.name,
                'part_info_url': f'http://{request.get_host()}/bom/part/{part.id}/#workflow'
            }


            html_message = render_to_string('bom/workflow_email_template.html', message_context)
            plain_message = strip_tags(html_message)

            send_mail(
                subject=f"[IndaBOM] New Task For Part {part}!",
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[assigned_user.email],
                html_message=html_message,
                fail_silently=True,
            )

    completed_transition = PartClassWorkflowCompletedTransition(
        transition=selected_transition,
        completed_by=request.user,
        comments=comments,
        part=part
    )
    completed_transition.save()

    if workflow_instance.current_state.is_final_state and 'submit-workflow-state' in request.POST:
        workflow_instance.delete()
        messages.success(request, f"Workflow for {part} completed!")
        return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part.id}))
    else:
        workflow_instance.current_state = selected_transition.target_state
        workflow_instance.save()
        return HttpResponseRedirect(reverse('bom:part-info', kwargs={'part_id': part.id})+'#workflow')
