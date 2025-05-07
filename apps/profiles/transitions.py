from django_fsm import transition

from apps.profiles.workflows import ProfileWorkflow
from apps.workflows.exceptions import WorkflowException


class ProfileTransitions:
    workflow = ProfileWorkflow()

    @transition(
        field="state",
        source=[workflow.CREATED],
        target=workflow.CREATED,
        permission="profiles.can_sync",
        custom=dict(verbose="Actualizar datos", icon="fas fa-check-double"),
    )
    def confirm(self, **kwargs):
        from apps.profiles.services import ProfileService
        from apps.utils.services import UserAPIService

        forum_profile, errors = UserAPIService.get_updated_profile_data(
            self.forum_user_id
        )

        if errors:
            raise WorkflowException(errors)

        ProfileService.update_profile(self, forum_profile)
