# Generated by Django 5.1.3 on 2024-11-09 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0005_alter_userprofile_user_feedbackprocess_review"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedbackprocess",
            name="reviewer",
        ),
        migrations.AddField(
            model_name="review",
            name="reviewer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews_given",
                to="feedback.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackprocess",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managed_feedback_processes",
                to="feedback.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="feedbackprocess",
            name="reviewee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reviews_received",
                to="feedback.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="feedback_process",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review",
                to="feedback.feedbackprocess",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employees",
                to="feedback.userprofile",
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("reviewer", "feedback_process"),
                name="unique_reviewer_feedback_process",
            ),
        ),
    ]
