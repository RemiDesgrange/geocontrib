# Generated by Django 2.2 on 2019-07-12 14:21

import collab.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_administrator', models.BooleanField(default=False, verbose_name='Est gestionnaire-métier')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name="Date de l'évènement")),
                ('feature_id', models.UUIDField(blank=True, editable=False, null=True, verbose_name='Identifiant du signalement')),
                ('comment_id', models.UUIDField(blank=True, editable=False, null=True, verbose_name='Identifiant du commentaire')),
                ('attachment_id', models.UUIDField(blank=True, editable=False, null=True, verbose_name='Identifiant de la pièce jointe')),
                ('object_type', models.CharField(choices=[('comment', 'Commentaire'), ('feature', 'Signalement'), ('feature', 'Pièce jointe'), ('Projet', 'Projet')], max_length=100, verbose_name="Type de l'objet lié")),
                ('event_type', models.CharField(choices=[('create', 'Création'), ('update_attachment', "Modification d'une pièce jointe"), ('update_loc', 'Modification de la localisation'), ('update_attrs', 'Modification d’un attribut'), ('update_status', 'Changement de statut'), ('delete', 'Suppression')], max_length=100, verbose_name="Type de l'évènement")),
                ('project_slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Slug Projet')),
                ('feature_type_slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Slug Feature')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Évènement',
                'verbose_name_plural': 'Évènements',
            },
        ),
        migrations.CreateModel(
            name='FeatureLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.CharField(choices=[('doublon', 'Doublon'), ('remplace', 'Remplace'), ('est_remplace_par', 'Est remplacé par'), ('depend_de', 'Dépend de')], default='doublon', max_length=50, verbose_name='Type de liaison')),
                ('feature_from', models.UUIDField(blank=True, null=True, verbose_name='Identifiant du signalement source')),
                ('feature_to', models.UUIDField(blank=True, null=True, verbose_name='Identifiant du signalement lié')),
            ],
            options={
                'verbose_name': 'Type de liaison',
                'verbose_name_plural': 'Types de liaison',
            },
        ),
        migrations.CreateModel(
            name='UserLevelPermission',
            fields=[
                ('user_type_id', models.CharField(choices=[('anonymous', 'Utilisateur anonyme'), ('logged_user', 'Utilisateur connecté'), ('contributor', 'Contributeur'), ('moderator', 'Modérateur'), ('admin', 'Admin')], max_length=100, primary_key=True, serialize=False, verbose_name='Identifiant')),
                ('rank', models.PositiveSmallIntegerField(unique=True, verbose_name='Rang')),
            ],
            options={
                'verbose_name': 'Niveau de permission',
                'verbose_name_plural': 'Niveaux de permisions',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_id', models.UUIDField(editable=False, verbose_name='Identifiant du signalement')),
                ('project_slug', models.SlugField(max_length=128, verbose_name='Slug')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name="Date de création de l'Abonnement")),
                ('users', models.ManyToManyField(help_text='Utilisateurs abonnés', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateurs')),
            ],
            options={
                'verbose_name': 'Abonnement',
                'verbose_name_plural': 'Abonnements',
            },
        ),
        migrations.CreateModel(
            name='StackedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sending_frequency', models.CharField(blank=True, choices=[('instantly', 'Instantanément'), ('daily', 'Quotidienne'), ('weekly', 'Hebdomadaire')], default='daily', max_length=20, null=True, verbose_name='Fréquence de notification')),
                ('state', models.CharField(choices=[('pending', "Tâche en attente d'exécution"), ('failed', 'Echec de la tâche'), ('succesful', 'Tâche terminée avec succés')], default='pending', max_length=20, verbose_name='État')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création du lot')),
                ('updated_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de derniére modification du lot')),
                ('schedualed_delivery_on', models.DateTimeField(blank=True, null=True, verbose_name="Timestamp d'envoi prévu")),
                ('events', models.ManyToManyField(to='collab.Event')),
            ],
            options={
                'verbose_name': 'Lot de notification',
                'verbose_name_plural': 'Lots de notifications des abonnées',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True, verbose_name='Titre')),
                ('slug', models.SlugField(blank=True, max_length=256, null=True, verbose_name='Slug')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('moderation', models.BooleanField(default=False, verbose_name='Modération')),
                ('thumbnail', models.ImageField(default='default.png', upload_to=collab.models.Project.thumbnail_dir, verbose_name='Illustration')),
                ('archive_feature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Délai avant archivage (nb jours)')),
                ('delete_feature', models.PositiveIntegerField(blank=True, null=True, verbose_name='Délai avant suppression (nb jours)')),
                ('features_info', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Info sur les types de signalements disponibles')),
                ('access_level_arch_feature', models.ForeignKey(limit_choices_to=collab.models.Project.limit_arch, on_delete=django.db.models.deletion.PROTECT, related_name='access_archived', to='collab.UserLevelPermission', verbose_name='Visibilité des signalements archivés')),
                ('access_level_pub_feature', models.ForeignKey(limit_choices_to=collab.models.Project.limit_pub, on_delete=django.db.models.deletion.PROTECT, related_name='access_published', to='collab.UserLevelPermission', verbose_name='Visibilité des signalements publiés')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Projet',
                'verbose_name_plural': 'Projets',
            },
        ),
        migrations.CreateModel(
            name='FeatureType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Titre')),
                ('slug', models.SlugField(max_length=256, unique=True, verbose_name='Slug')),
                ('geom_type', models.CharField(choices=[('linestring', 'Ligne brisée'), ('point', 'Point'), ('polygon', 'Polygone')], default='boolean', max_length=50, verbose_name='Type de champs géometrique')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
            ],
            options={
                'verbose_name': 'Type de signalement',
                'verbose_name_plural': 'Types de Signalements',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('feature_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Identifiant')),
                ('title', models.CharField(blank=True, max_length=128, null=True, verbose_name='Titre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('status', models.CharField(blank=True, choices=[('draft', 'Brouillon'), ('pending', 'En attente de publication'), ('published', 'Publié'), ('archived', 'Archivé')], default='draft', max_length=50, null=True, verbose_name='Statut des signalements')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création')),
                ('updated_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de maj')),
                ('archived_on', models.DateField(blank=True, null=True, verbose_name="Date d'archivage automatique")),
                ('deletion_on', models.DateField(blank=True, null=True, verbose_name='Date de suppression automatique')),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326, verbose_name='Champs geometrique')),
                ('feature_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('feature_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.FeatureType')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
                ('user', models.ForeignKey(help_text='Utilisateur abonné', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Signalement',
                'verbose_name_plural': 'Signalements',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Identifiant')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création')),
                ('feature_id', models.UUIDField(blank=True, null=True, verbose_name='Identifiant du signalement')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Commentaire')),
                ('feature_type_slug', models.SlugField(max_length=128, verbose_name='Slug du type de signalement')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
            ],
            options={
                'verbose_name': 'Commentaire',
                'verbose_name_plural': 'Commentaires',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Identifiant')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création')),
                ('feature_id', models.UUIDField(blank=True, null=True, verbose_name='Identifiant du signalement')),
                ('title', models.CharField(max_length=128, verbose_name='Titre')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Info')),
                ('type_objet', models.CharField(choices=[('comment', 'Commentaire'), ('feature', 'Signalement')], max_length=50, verbose_name="Type d'objet concerné")),
                ('attachment_file', models.FileField(upload_to=collab.models.Attachment.attachement_dir, verbose_name='Pièce jointe')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Auteur')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='collab.Comment')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
            ],
            options={
                'verbose_name': 'Pièce Jointe',
                'verbose_name_plural': 'Pièces Jointes',
            },
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Nom')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='Titre')),
                ('style', models.CharField(blank=True, max_length=256, null=True, verbose_name='Style')),
                ('service', models.URLField(verbose_name='Service')),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name="Numéro d'ordre")),
                ('schema_type', models.CharField(choices=[('wms', 'WMS'), ('tms', 'TMS')], default='wms', max_length=50, verbose_name='Type de couche')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
            ],
            options={
                'verbose_name': 'Couche',
                'verbose_name_plural': 'Couches',
                'unique_together': {('project', 'order')},
            },
        ),
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=128, null=True, verbose_name='Label')),
                ('name', models.CharField(blank=True, max_length=128, null=True, verbose_name='Nom')),
                ('position', models.PositiveSmallIntegerField(default=0, verbose_name='Position')),
                ('field_type', models.CharField(blank=True, choices=[('boolean', 'Booléen'), ('char', 'Chaîne de caractères'), ('date', 'Date'), ('integer', 'Entier'), ('decimal', 'Décimale'), ('text', 'Champs texte')], default='boolean', max_length=50, null=True, verbose_name='Type de champs')),
                ('feature_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.FeatureType')),
            ],
            options={
                'verbose_name': 'Champs personnalisés',
                'verbose_name_plural': 'Champs personnalisés',
                'unique_together': {('name', 'feature_type')},
            },
        ),
        migrations.CreateModel(
            name='Authorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de création')),
                ('updated_on', models.DateTimeField(blank=True, null=True, verbose_name='Date de modification')),
                ('level', models.ForeignKey(limit_choices_to=collab.models.Authorization.upper_ranks, on_delete=django.db.models.deletion.CASCADE, to='collab.UserLevelPermission')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collab.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'project')},
            },
        ),
    ]
