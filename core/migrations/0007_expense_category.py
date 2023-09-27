# Generated by Django 4.2.5 on 2023-09-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_rename_website_url_profile_website"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("GR", "Groceries"),
                    ("TR", "Transport"),
                    ("EN", "Entertainment"),
                    ("UT", "Utilities"),
                    ("RE", "Rent"),
                    ("HE", "Health"),
                    ("OT", "Other"),
                    ("TV", "Travel"),
                    ("ED", "Education"),
                    ("SV", "Savings"),
                    ("SB", "Subscriptions"),
                ],
                default="OT",
                max_length=2,
            ),
        ),
    ]