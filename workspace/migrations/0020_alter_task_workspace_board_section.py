"""Allow cascading delete of workspace board section."""
# Generated by Django 4.0.2 on 2022-03-04 04:06

import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("workspace", "0019_alter_chatmessage_author_alter_subtask_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="workspace_board_section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="workspace.workspaceboardsection",
            ),
        ),
    ]
