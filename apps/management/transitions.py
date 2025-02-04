from django_fsm import can_proceed, transition

from apps.management.conditions import ManagementConditions
from apps.management.workflows import UpdateLevelWorkflow
from apps.profiles.services import ProfileService


class LevelUpdateTransitions:
    workflow = UpdateLevelWorkflow()

    @transition(
        field="state",
        source=[workflow.DRAFT],
        target=workflow.DONE,
        conditions=[
            ManagementConditions.is_admin,
        ],
        custom=dict(verbose="Cerrar"),
    )
    def close(self, **kwargs):
        for line in self.lines.filter(state=self.workflow.DRAFT):
            if can_proceed(line.close):
                line.close()
                line.save()

    @transition(
        field="state",
        source=[workflow.DRAFT],
        target=workflow.DONE,
        conditions=[
            ManagementConditions.is_admin,
        ],
        custom=dict(verbose="Completar"),
    )
    def complete(self, **kwargs):
        update_lines = kwargs.get("update_lines", True)

        if update_lines:
            for line in self.lines.filter(state=self.workflow.DRAFT):
                try:
                    if can_proceed(line.update):
                        line.update()
                        line.save()
                except Exception:
                    pass


class LevelUpdateLineTransitions:
    workflow = UpdateLevelWorkflow()

    @transition(
        field="state",
        source=[
            workflow.DRAFT,
        ],
        target=workflow.DONE,
        conditions=[
            ManagementConditions.is_admin,
            ManagementConditions.not_done,
        ],
        custom=dict(verbose="Cerrar", hide=True),
    )
    def close(self, **kwargs):
        pass

    @transition(
        field="state",
        source=[
            workflow.DRAFT,
        ],
        target=workflow.DONE,
        conditions=[
            ManagementConditions.is_admin,
            ManagementConditions.not_done,
        ],
        custom=dict(verbose="Actualizar"),
    )
    def update(self, **kwargs):
        ProfileService.update_level_and_social_rank(
            self.profile, self.calculated_level, self.calculated_social_rank
        )
