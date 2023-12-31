# Generated by Django 4.2.5 on 2023-09-16 08:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="profile",
            name="facebook",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[
                    ("M", "Male"),
                    ("F", "Female"),
                    ("O", "Other"),
                    ("N", "Prefer Not to Say"),
                ],
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="instagram",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="is_public",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="join_date",
            field=models.DateField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="linkedin",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="location",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profile",
            name="occupation",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="profile",
            name="skills",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="theme_preference",
            field=models.CharField(
                choices=[("light", "Light Mode"), ("dark", "Dark Mode")],
                default="light",
                max_length=5,
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="twitter",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="website_url",
            field=models.URLField(blank=True),
        ),
    ]
