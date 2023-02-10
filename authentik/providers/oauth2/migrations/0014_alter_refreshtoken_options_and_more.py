# Generated by Django 4.1.6 on 2023-02-09 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import authentik.core.models
import authentik.lib.generators
import authentik.lib.utils.time


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("authentik_providers_oauth2", "0013_devicetoken"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="refreshtoken",
            options={
                "verbose_name": "OAuth2 Refresh Token",
                "verbose_name_plural": "OAuth2 Refresh Tokens",
            },
        ),
        migrations.RenameField(
            model_name="oauth2provider",
            old_name="token_validity",
            new_name="refresh_token_validity",
        ),
        migrations.RemoveField(
            model_name="authorizationcode",
            name="is_open_id",
        ),
        migrations.RemoveField(
            model_name="refreshtoken",
            name="access_token",
        ),
        migrations.RemoveField(
            model_name="refreshtoken",
            name="refresh_token",
        ),
        migrations.AddField(
            model_name="oauth2provider",
            name="access_token_validity",
            field=models.TextField(
                default="hours=1",
                help_text="Tokens not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).",
                validators=[authentik.lib.utils.time.timedelta_string_validator],
            ),
        ),
        migrations.AddField(
            model_name="refreshtoken",
            name="token",
            field=models.TextField(default=authentik.lib.generators.generate_key),
        ),
        migrations.AlterField(
            model_name="oauth2provider",
            name="sub_mode",
            field=models.TextField(
                choices=[
                    ("hashed_user_id", "Based on the Hashed User ID"),
                    ("user_id", "Based on user ID"),
                    ("user_username", "Based on the username"),
                    (
                        "user_email",
                        "Based on the User's Email. This is recommended over the UPN method.",
                    ),
                    (
                        "user_upn",
                        "Based on the User's UPN, only works if user has a 'upn' attribute set. Use this method only if you have different UPN and Mail domains.",
                    ),
                ],
                default="hashed_user_id",
                help_text="Configure what data should be used as unique User Identifier. For most cases, the default should be fine.",
            ),
        ),
        migrations.CreateModel(
            name="AccessToken",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "expires",
                    models.DateTimeField(default=authentik.core.models.default_token_duration),
                ),
                ("expiring", models.BooleanField(default=True)),
                ("revoked", models.BooleanField(default=False)),
                ("_scope", models.TextField(default="", verbose_name="Scopes")),
                ("token", models.TextField()),
                ("_id_token", models.TextField()),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentik_providers_oauth2.oauth2provider",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "OAuth2 Access Token",
                "verbose_name_plural": "OAuth2 Access Tokens",
            },
        ),
    ]