# Generated by Django 3.1.7 on 2021-03-28 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210327_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='banco',
            name='pessoa',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='core.pessoa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registro',
            name='banco',
            field=models.ForeignKey(default=10, on_delete=django.db.models.deletion.CASCADE, to='core.banco'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registro',
            name='pessoa',
            field=models.ForeignKey(default='10', on_delete=django.db.models.deletion.CASCADE, to='core.pessoa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
    ]
