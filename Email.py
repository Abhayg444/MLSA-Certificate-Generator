#Run the code after you have successfully created the certificates

import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to send email with attachment
def send_email(from_email, password, to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment_path, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + os.path.basename(attachment_path))
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

# Read the CSV file
csv_file = 'Data Template\Event Participate Template.csv'  # Update with your CSV file path
data = pd.read_csv(csv_file)

# Directory paths
pdf_folder = 'output/pdf/'

# Email template
subject_template = "Congratulations on Completing the Azure Fundamentals Cloud Skills Challenge!"
body_template = """
Dear {name},

I'm thrilled to extend my heartfelt congratulations on successfully completing the Azure Fundamentals Cloud Skills Challenge! 🌟 Your commitment to advancing your Azure knowledge is truly inspiring. 🚀

Your achievement not only showcases your proficiency in Azure fundamentals but also demonstrates your readiness to innovate with cloud technologies. 🌈

As you continue your journey with Azure, remember that your dedication and passion will continue to drive your success. 💪

Once again, congratulations on this remarkable milestone! 🎉 We're proud to have you as part of our community of skilled professionals. 🙌

Warm regards,

Your Name 
Beta Microsoft Student Learn Ambassadors

"""

# Iterate through each participant
for index, row in data.iterrows():
    name = row['Name Surname']
    email = row['Email']

    # Assuming PDF file name format is participant_name.pdf
    pdf_filename = f"{name}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_filename)

    # Send email with PDF attachment
    if os.path.exists(pdf_path):
        subject = subject_template
        body = body_template.format(name=name)
        send_email('your email', 'password(create a app password on your google account if you want)', email, subject, body, pdf_path)
        print(f"Email sent to {email} with PDF attachment: {pdf_filename}")
    else:
        print(f"PDF file not found for {name} ({email})")
