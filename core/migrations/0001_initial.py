# Generated by Django 4.1.4 on 2022-12-28 07:20

import core.helpers
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('address', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DMR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(default=165)),
                ('weight', models.IntegerField(default=60)),
                ('sex', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0)),
                ('wallet', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TargetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, null=True, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trainer', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TCR_club', to='core.club')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TCR_trainers', to='core.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_days', models.IntegerField(blank=True, default=0, null=True)),
                ('target_height', models.IntegerField(blank=True, default=165, null=True)),
                ('target_weight', models.IntegerField(blank=True, default=60, null=True)),
                ('category', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='core.targetcategory')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='core.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(default=0)),
                ('capacity', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=None)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_club', to='core.club')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_trainer', to='core.trainer')),
            ],
        ),
        migrations.AddField(
            model_name='owner',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='core.userprofile'),
        ),
        migrations.CreateModel(
            name='MPR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MPR_member', to='core.member')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MPR_program', to='core.program')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member', to='core.userprofile'),
        ),
        migrations.CreateModel(
            name='MCR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MCR_club', to='core.club')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MCR_member', to='core.member')),
            ],
        ),
        migrations.CreateModel(
            name='ForgetPasswordLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(default=core.helpers.generate_16char_link, max_length=16)),
                ('used', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forget_password_link', to='core.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=300)),
                ('date', models.DateField(blank=True, null=True)),
                ('hour', models.IntegerField(blank=True, null=True)),
                ('minute', models.IntegerField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('capacity', models.IntegerField(default=0)),
                ('attachment', models.ImageField(blank=True, null=True, upload_to=None)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_event_owner', to='core.member')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_event_owner', to='core.owner')),
            ],
        ),
        migrations.CreateModel(
            name='EMR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isRegistered', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EMR_event', to='core.event')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='EMR_member', to='core.member')),
            ],
        ),
        migrations.CreateModel(
            name='Diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=50, null=True)),
                ('price', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to=None)),
                ('day', models.ImageField(blank=True, null=True, upload_to=None)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_club', to='core.club')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diet_trainer', to='core.trainer')),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='club', to='core.owner'),
        ),
    ]
