from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_blockedstudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockedstudent',
            name='course',
            field=models.ForeignKey(
                related_name='blocked_students',
                null=True,
                blank=True,
                on_delete=models.CASCADE,
                to='courses.course',
            ),
        ),
    ]
