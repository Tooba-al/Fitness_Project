# Generated by Django 4.1.4 on 2023-01-14 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdMR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isLiked', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='education',
            name='description',
        ),
        migrations.AddField(
            model_name='club',
            name='enrollers',
            field=models.ManyToManyField(blank=True, related_name='enrollers', to='core.userprofile'),
        ),
        migrations.AddField(
            model_name='education',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='education',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='trainer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='core.trainer'),
        ),
        migrations.DeleteModel(
            name='ETR',
        ),
        migrations.AddField(
            model_name='edmr',
            name='education',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EdMR_education', to='core.education'),
        ),
        migrations.AddField(
            model_name='edmr',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EdMR_member', to='core.member'),
        ),
    ]
