from django.db import migrations


class AttributeMigration(migrations.Migration):
    """
    This migration subclass allows a migration in application X to change
    a model defined in application Y.
    This is useful to extend models in application Y with custom fields.
    """

    # Application in which we are extending the models.
    extends_app_label = None

    def __init__(self, name, app_label):
        super().__init__(name, app_label)
        self.real_app_label = app_label

    def __eq__(self, other):
        return (
            isinstance(other, AttributeMigration)
            and migrations.Migration.__eq__(self, other)
            and self.extends_app_label == other.extends_app_label
        )

    def __hash__(self):
        return hash("%s.%s.%s" % (self.app_label, self.name, self.extends_app_label))

    def mutate_state(self, project_state, preserve=True):
        self.app_label = self.extends_app_label
        state = super().mutate_state(project_state, preserve)
        self.app_label = self.real_app_label
        return state

    def apply(self, project_state, schema_editor, collect_sql=False):
        if not self.extends_app_label:
            raise Exception("Missing extends_app_label in attribute migration")
        self.app_label = self.extends_app_label
        state = super().apply(project_state, schema_editor, collect_sql)
        self.app_label = self.real_app_label
        return state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        if not self.extends_app_label:
            raise Exception("Missing extends_app_label in attribute migration")
        self.app_label = self.extends_app_label
        state = super().unapply(project_state, schema_editor, collect_sql)
        self.app_label = self.real_app_label
        return state
