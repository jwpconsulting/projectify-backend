"""Add WorkspaceUser m2m mapping."""
# Generated by Django 4.0 on 2021-12-15 02:53

import django.db.models.deletion
from django.conf import (
    settings,
)
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0005_user_is_active"),
        ("workspace", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkspaceUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="user.user",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="workspace",
            name="users",
            field=models.ManyToManyField(
                through="workspace.WorkspaceUser", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="workspaceuser",
            name="workspace",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="workspace.workspace",
            ),
        ),
    ]
