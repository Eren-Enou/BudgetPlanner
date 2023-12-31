# Generated by Django 4.2.5 on 2023-09-16 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_profile_bio_profile_facebook_profile_gender_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="images/default_profile_pic.jpg",
                null=True,
                upload_to="profile_pics/",
            ),
        ),
    ]
