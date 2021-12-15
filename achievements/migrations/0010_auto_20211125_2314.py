# Generated by Django 3.1.12 on 2021-11-25 17:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bodies', '0023_body_canonical_name'),
        ('achievements', '0009_auto_20190819_2310'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='isSkill',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('body', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='bodies.body')),
            ],
        ),
    ]