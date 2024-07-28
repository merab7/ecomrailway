# email_utils.py
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
from django.utils.translation import gettext as _
from django.utils import translation

def send_order_confirmation(email, content, EMAIL, sum_order, language):
    current_year = datetime.now().year

   

    # Activate the selected language
    translation.activate(language)

     # Construct the message content for order items
    if language == 'en':
        message_content = '\n\n'.join(
            [f"Item: {x['em_name']}\nPrice: ₾ {x['em_price']}\nSize: {x['em_size']}\nQuantity: {x['em_quantity']}"
            for x in sum_order]
        )
    if language == 'ka' :    
        message_content = '\n\n'.join(
            [f"პროდუქტი: {x['em_name']}\nფასი: ₾ {x['em_price']}\nზომა: {x['em_size']}\nრაოდენობა: {x['em_quantity']}"
            for x in sum_order])


    msg = MIMEMultipart()
    msg['From'] = formataddr((_('Hariha'), EMAIL))
    msg['To'] = email
    msg['Subject'] = _('Your order confirmation')

    body = f"""
    <html>
        <head>
            <style>
                .email-container {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                }}
                .email-header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #ddd;
                }}
                .email-body {{
                    padding: 20px;
                }}
                .email-footer {{
                    text-align: center;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 12px;
                    color: #999;
                }}
                .order-details {{
                    margin: 20px 0;
                }}
                .order-details th, .order-details td {{
                    text-align: left;
                    padding: 5px 0;
                }}
                .order-details th {{
                    font-weight: bold;
                }}
                .order-items {{
                    margin-top: 20px;
                    white-space: pre-wrap;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">
                    <h1>{_('Thank you for your purchase!')}</h1>
                </div>
                <div class="email-body">
                    <p>{_('Dear Customer,')}</p>
                    <p>{_('We are pleased to confirm your order. Below are the details:')}</p>
                    <table class="order-details">
                        <tr>
                            <th>{_('Order Number:')}</th>
                            <td>{content['order_num']}</td>
                        </tr>
                        <tr>
                            <th>{_('Total Paid:')}</th>
                            <td>{content['sum']}</td>
                        </tr>
                        <tr>
                            <th>{_('Shipping Address:')}</th>
                            <td>{content['shipping_address']}</td>
                        </tr>
                    </table>
                    <div class="order-items">
                        <h2>{_('Here is your order:')}</h2>
                        <pre>{message_content}</pre>
                    </div>
             
                    <p>{_('Thank you for shopping with us!')}</p>
                </div>
                <div class="email-footer">
                    <p>&copy; {current_year} {_('Hariha. All rights reserved.')}</p>
                </div>
            </div>
        </body>
    </html>
    """
    msg.attach(MIMEText(body, 'html', 'utf-8'))

    # Deactivate the language after use
    translation.deactivate()

    return msg
