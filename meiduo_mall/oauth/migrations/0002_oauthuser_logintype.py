# Generated by Django 2.1.3 on 2019-06-18 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthuser',
            name='loginType',
            field=models.CharField(choices=[('1', 'qq'), ('2', 'weibo'), ('3', 'github')], default=2, max_length=1),
            preserve_default=False,
        ),
    ]