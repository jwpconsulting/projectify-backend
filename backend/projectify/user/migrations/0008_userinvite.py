# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2022 JWP Consulting GK
"""Create user invite model."""
# Generated by Django 4.0.2 on 2022-03-09 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import projectify.lib.models


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        ("user", "0007_user_full_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserInvite",
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
                    "created",
                    projectify.lib.models.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    projectify.lib.models.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="Email"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        help_text="Matched user",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "get_latest_by": "modified",
                "abstract": False,
            },
        ),
    ]
