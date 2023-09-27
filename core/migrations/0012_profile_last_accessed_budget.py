# Generated by Django 4.2.5 on 2023-09-27 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_expense_frequency_expense_is_recurring_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="last_accessed_budget",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.budget",
            ),
        ),
    ]
