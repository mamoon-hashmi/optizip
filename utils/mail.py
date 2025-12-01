# utils/mail.py → FINAL SIMPLE VERSION
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

def send_otp_email(to_email, otp):
    sender_email = os.getenv("EMAIL_USER")        # ← yeh use hoga
    host = os.getenv("EMAIL_HOST")
    port = os.getenv("EMAIL_PORT")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = "Your OptiZip Verification Code"

    body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
            
            <!-- Main Card -->
            <div style="background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.15);">
                
                <!-- Header with Gradient -->
                <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); padding: 40px 30px; text-align: center; position: relative;">
                    <div style="display: inline-flex; align-items: center; gap: 12px;">
                        <div style="background: rgba(255,255,255,0.3); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; backdrop-filter: blur(10px);">
                            <span style="font-size: 24px;">⚡</span>
                        </div>
                        <h1 style="color: black; margin: 0; font-size: 32px; font-weight: 900; letter-spacing: -1px;">OptiZip</h1>
                    </div>
                </div>
                
                <!-- Content -->
                <div style="padding: 50px 30px;">
                    <div style="text-align: center;">
                        <h2 style="color: #1f2937; font-size: 24px; margin: 0 0 15px; font-weight: 700;">Verify Your Account</h2>
                        <p style="color: #6b7280; font-size: 16px; line-height: 1.6; margin: 0 0 35px;">Enter this verification code to complete your registration</p>
                        
                        <!-- OTP Code Box -->
                        <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); padding: 3px; border-radius: 16px; display: inline-block; margin: 0 0 30px;">
                            <div style="background: white; padding: 25px 50px; border-radius: 14px;">
                                <div style="font-size: 48px; font-weight: 900; letter-spacing: 12px; color: #1f2937; font-family: 'Courier New', monospace;">
                                    {otp}
                                </div>
                            </div>
                        </div>
                        
                        <!-- Info Pills -->
                        <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 30px;">
                            <div style="background: #fef3c7; padding: 10px 20px; border-radius: 50px; display: inline-flex; align-items: center; gap: 8px;">
                                <span style="font-size: 16px;">⏱️</span>
                                <span style="color: #92400e; font-size: 13px; font-weight: 600;">Valid for 10 minutes</span>
                            </div>
                            <div style="background: #fee2e2; padding: 10px 20px; border-radius: 50px; display: inline-flex; align-items: center; gap: 8px;">
                                <span style="font-size: 16px;">🔒</span>
                                <span style="color: #991b1b; font-size: 13px; font-weight: 600;">Do not share</span>
                            </div>
                        </div>
                        
                        <!-- Security Note -->
                        <div style="background: #f3f4f6; padding: 20px; border-radius: 12px; border-left: 4px solid #fbbf24;">
                            <p style="color: #4b5563; font-size: 14px; line-height: 1.6; margin: 0;">
                                <strong style="color: #1f2937;">Security Tip:</strong> OptiZip will never ask for this code via phone or email. If you didn't request this code, please ignore this email.
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Footer -->
                <div style="background: #f9fafb; padding: 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <div style="display: inline-flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                            <span style="font-size: 20px;">⚡</span>
                        </div>
                        <h3 style="color: #1f2937; margin: 0; font-size: 20px; font-weight: 900;">OptiZip</h3>
                    </div>
                    <p style="color: #9ca3af; font-size: 13px; margin: 0 0 15px; line-height: 1.6;">
                        This email was sent to verify your OptiZip account.<br>
                        If you have any questions, contact our support team.
                    </p>
                    <div style="margin-top: 20px;">
                        <a href="#" style="color: #fbbf24; text-decoration: none; font-weight: 600; font-size: 13px; margin: 0 10px;">Help Center</a>
                        <span style="color: #d1d5db;">•</span>
                        <a href="#" style="color: #fbbf24; text-decoration: none; font-weight: 600; font-size: 13px; margin: 0 10px;">Privacy Policy</a>
                        <span style="color: #d1d5db;">•</span>
                        <a href="#" style="color: #fbbf24; text-decoration: none; font-weight: 600; font-size: 13px; margin: 0 10px;">Terms</a>
                    </div>
                    <p style="color: #d1d5db; font-size: 12px; margin: 20px 0 0;">© 2024 OptiZip. All rights reserved.</p>
                </div>
                
            </div>
            
            <!-- Bottom Text -->
            <p style="text-align: center; color: #92400e; font-size: 12px; margin-top: 30px; line-height: 1.6;">
                Having trouble? Copy and paste this code manually:<br>
                <strong style="letter-spacing: 3px; font-family: 'Courier New', monospace;">{otp}</strong>
            </p>
            
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print("SMTP Error:", e)
        return False