from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi_mail.schemas import NameEmail

from core.configs import application_config
from services.interfaces import EmailServiceInterface

class EmailService(EmailServiceInterface):
    def __init__(self, connection_config: ConnectionConfig):
        self._fm = FastMail(connection_config)

    async def send_verification_email(self, user_email: str, code: str) -> None:
        message = MessageSchema(
            subject="Your verification code",
            recipients=[NameEmail(name="", email=user_email)],
            body=self._get_verification_template(code),
            subtype=MessageType.html
        )
        await self._fm.send_message(message)

    async def send_forgot_password_email(self, user_email: str, reset_token: str) -> None:
        frontend_url = f"{application_config.FRONTEND_URL}/reset-password"
        reset_link = f"{frontend_url}?token={reset_token}"

        message = MessageSchema(
            subject="Your Password Reset Code",
            recipients=[NameEmail(name="", email=user_email)],
            body=self._get_forgot_password_template(reset_link),
            subtype=MessageType.html
        )
        await self._fm.send_message(message)

    def _get_forgot_password_template(self, reset_link: str):
        return f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f7; color: #51545e;">
                <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color: #f4f4f7; padding: 20px;">
                    <tr>
                        <td align="center">
                            <table width="100%" style="max-width: 570px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); overflow: hidden;" cellpadding="0" cellspacing="0" role="presentation">
                                <tr>
                                    <td style="padding: 25px; text-align: center; background-color: #4CAF50;">
                                        <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">Password Reset</h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 35px; text-align: center;">
                                        <p style="font-size: 16px; line-height: 1.5; color: #51545e;">Hello! We received a request to reset your password.</p>
                                        <p style="font-size: 16px; line-height: 1.5; color: #51545e; margin-bottom: 25px;">Click the button below to set a new password:</p>
                                        
                                        <a href="{reset_link}" style="display: inline-block; padding: 14px 28px; background-color: #4CAF50; color: #ffffff; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 16px;">
                                            Reset Password
                                        </a>
                                        
                                        <p style="font-size: 14px; line-height: 1.5; color: #9da3ae; margin-top: 35px;">
                                            Or copy and paste this link into your browser:<br>
                                            <a href="{reset_link}" style="color: #4CAF50; word-break: break-all;">{reset_link}</a>
                                        </p>

                                        <p style="font-size: 14px; line-height: 1.5; color: #9da3ae; margin-top: 25px;">
                                            This link is valid for 15 minutes.<br>
                                            If you did not request a password reset, please simply ignore or delete this email.
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 15px; text-align: center; background-color: #f9fafb;">
                                        <p style="font-size: 12px; color: #b0adc5; margin: 0;">Automated message • {self.__class__.__name__}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """

    def _get_verification_template(self, code: str) -> str:
        return f"""
        <html>
            <body style="margin: 0; padding: 0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #f4f4f7; color: #51545e;">
                <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color: #f4f4f7; padding: 20px;">
                    <tr>
                        <td align="center">
                            <table width="100%" style="max-width: 570px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); overflow: hidden;" cellpadding="0" cellspacing="0" role="presentation">
                                <tr>
                                    <td style="padding: 25px; text-align: center; background-color: #4CAF50;">
                                        <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: bold;">Account Verification</h1>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 35px; text-align: center;">
                                        <p style="font-size: 16px; line-height: 1.5; color: #51545e;">Welcome! You received this email to confirm your registration.</p>
                                        <p style="font-size: 16px; line-height: 1.5; color: #51545e; margin-bottom: 25px;">Your code:</p>
                                        
                                        <div style="background-color: #f4f4f7; border-radius: 4px; padding: 20px; margin: 0 auto; display: inline-block; letter-spacing: 5px;">
                                            <span style="font-size: 32px; font-weight: bold; color: #333333; font-family: monospace;">{code}</span>
                                        </div>
                                        
                                        <p style="font-size: 14px; line-height: 1.5; color: #9da3ae; margin-top: 25px;">
                                            This code is valid for 15 minutes.<br>
                                            If you did not request this code, please simply delete this email.
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 15px; text-align: center; background-color: #f9fafb;">
                                        <p style="font-size: 12px; color: #b0adc5; margin: 0;">Automated message • {self.__class__.__name__}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """