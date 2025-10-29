import os
from html import escape

from resend import Emails


class MailerConfigError(RuntimeError):
    """Se lanza cuando la configuración de Resend es insuficiente."""


def _get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise MailerConfigError(f"{name} no está configurada.")
    return value


def send_contact_email(name: str, email: str, message: str | None = None) -> None:
    """Envía una notificación vía Resend con el contenido del formulario de contacto."""
    api_key = _get_env("RESEND_API_KEY")
    to_email = _get_env("CONTACT_NOTIFICATION_EMAIL")
    os.environ["RESEND_API_KEY"] = api_key  # requerido por la librería

    safe_name = escape(name or "")
    safe_email = escape(email or "")
    safe_message = escape(message or "") or "—"

    Emails.send(
        {
            "to": to_email,
            "from": "onboarding@resend.dev",
            "subject": "📬 Nuevo mensaje desde el formulario de contacto",
            "html": (
                "<h2>Nuevo contacto recibido</h2>"
                f"<p><strong>Nombre:</strong> {safe_name}</p>"
                f"<p><strong>Email:</strong> {safe_email}</p>"
                "<p><strong>Mensaje:</strong></p>"
                f"<pre>{safe_message}</pre>"
            ),
        }
    )
