import os
from html import escape
import resend


class MailerConfigError(RuntimeError):
    """Se lanza cuando la configuración de Resend es insuficiente."""


def _get_env(name: str) -> str:
    """Obtiene una variable de entorno o lanza error si falta."""
    value = os.getenv(name, "").strip()
    if not value:
        raise MailerConfigError(f"{name} no está configurada.")
    return value


def send_contact_email(name: str, email: str, message: str | None = None) -> None:
    """
    Envía una notificación vía Resend con el contenido del formulario de contacto.
    - Usa el dominio opunnence.com verificado.
    - Permite configuración completa vía variables de entorno.
    """

    # Configuración
    api_key = _get_env("RESEND_API_KEY")
    from_email = os.getenv("RESEND_FROM_EMAIL", "formulario@opunnence.com").strip()
    to_email = _get_env("CONTACT_NOTIFICATION_EMAIL")

    resend.api_key = api_key

    # Sanitización de campos
    safe_name = escape(name or "")
    safe_email = escape(email or "")
    safe_message = escape(message or "") or "—"

    # Construcción del contenido
    html_content = (
        "<h2>📬 Nuevo contacto recibido desde Opunnence</h2>"
        f"<p><strong>Nombre:</strong> {safe_name}</p>"
        f"<p><strong>Email:</strong> {safe_email}</p>"
        "<p><strong>Mensaje:</strong></p>"
        f"<pre>{safe_message}</pre>"
        "<hr>"
        "<p style='font-size:12px;color:#999;'>Este mensaje fue enviado automáticamente desde el backend de Opunnence.</p>"
    )

    # Envío
    try:
        resend.Emails.send(
            {
                "from": f"Formulario Opunnence <{from_email}>",
                "to": [to_email],
                "subject": "📬 Nuevo mensaje desde el formulario de contacto",
                "html": html_content,
            }
        )
    except Exception as exc:
        raise RuntimeError(f"Error al enviar el correo con Resend: {exc}") from exc
