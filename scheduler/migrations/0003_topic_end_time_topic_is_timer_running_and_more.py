# Generated by Django 4.2.13 on 2025-04-11 14:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scheduler", "0002_remove_topic_end_time_remove_topic_start_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="topic",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="topic",
            name="is_timer_running",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="topic",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
