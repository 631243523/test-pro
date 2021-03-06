# Generated by Django 2.1.2 on 2018-11-12 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('aid', models.AutoField(primary_key=True, serialize=False)),
                ('aname', models.CharField(max_length=32)),
                ('age', models.IntegerField()),
                ('phone', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Author_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addr', models.CharField(max_length=32)),
                ('tel', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('bid', models.AutoField(primary_key=True, serialize=False)),
                ('bname', models.CharField(max_length=32)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pub_date', models.DateTimeField()),
                ('authors', models.ManyToManyField(to='app01.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('pname', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='publish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Publish'),
        ),
        migrations.AddField(
            model_name='author',
            name='a_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Author_info'),
        ),
    ]
