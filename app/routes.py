from dotenv import load_dotenv
from flask import Flask, request, render_template
from app import app, _update_db, mail
from flask_mail import Message
from app.models import User
from pprint import pprint
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from .geocoder import get_location

load_dotenv()
GoogleMaps(app, key="KEY") #Google API KEY

account_sid = 'KEY' 
auth_token = 'KEY' #Twilio ACCOUNT DATA
client = Client(account_sid, auth_token)

values = []

links = {
    'ссылка в лк': "https://www.netflix.com/ua/",
    'связь с менеджером': "https://www.amazon.com/",
    'contact the manager': "https://www.youtube.com/",
    'faq': "https://www.google.com/"
}

professions_types = ['self specialist ', 'company']
business_types = ['beauty salon', 'manicure master',
                  'self cleaner', 'cleaning company', 'massage ']
genders_types = ['men', 'women', 'all']
ages_types = ['18-24', '25-30', '30-45', '45-60', 'all']
price_categories_types = ['economy', 'standard', 'premium']
actions_types = ['ordered call', 'call',
                 'ordering on the site', 'viewing the menu', 'viewing contacts']

location_data = []


def _send_message(output_lines):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)


@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    remote_number = request.values.get("From", "")

    output_lines = []

    if remote_number.startswith("whatsapp:"):
        remote_number = remote_number.split(":")[1]

    if not remote_number:
        remote_number = "123"

    user = User.query.get(remote_number)

    name_file = 'app/data.doc'

    def writeInFile(value):
        with open(name_file, "a") as file_object:
            file_object.write(value)

    message_latitude = request.values.get('Latitude')
    message_longitude = request.values.get('Longitude')

    if(incoming_msg == "/start"):
        values.clear()
        location_data.clear()
        open(name_file, 'w').close()
        writeInFile("Phone number: " + str(remote_number))
        output_lines.append(
            "☀️ Hello!\n\n🤖 I'm a MarkIT BOT\n\nI will help you set up an advertising campaign to achieve the maximum result!\n\nPlease answer a few questions.\n")
        output_lines.append("🔥 Write 'ok' to get started.")
        return _send_message(output_lines)

    if incoming_msg == "/help":
        output_lines.append("❓ Help:\n")
        output_lines.append("For answering on a question type a number of a option or type a full name of the option.")
        output_lines.append("For example:\n")
        output_lines.append("You are:\n")
        output_lines.append("1️⃣ Self specialist\n")
        output_lines.append("2️⃣ Company\n")
        output_lines.append("Your answer:\n")
        output_lines.append("Self specialist\n\n")
        output_lines.append("⛳ Type '/start' to start over.\n")
        return _send_message(output_lines)

    if not user:
        if incoming_msg == "/ok" or incoming_msg == "ok":
            output_lines.append("🧸 You are:\n")
            output_lines.append("1️⃣ Self specialist\n")
            output_lines.append("2️⃣ Company\n")
            output_lines.append(
                "0️⃣ Type 'miss' or '0' for missing the answer.")
            values.append(incoming_msg)
            return _send_message(output_lines)

        if(len(values) == 1):
            if (incoming_msg == "self specialist" or incoming_msg == "company" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == '1' or incoming_msg == '2'):
                if(incoming_msg == '1'):
                    incoming_msg = 'self specialist'
                if(incoming_msg == '2'):
                    incoming_msg = 'company'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.profession = 'missed'
                    values.append('1')
                else:
                    User.profession = incoming_msg
                    values.append(incoming_msg)
                writeInFile("\nProfession: " + str(User.profession))
                output_lines.append(
                    "🍔 What are we advertising?\n")
                output_lines.append("1️⃣ Beauty salon\n")
                output_lines.append("2️⃣ Manicure master\n")
                output_lines.append("3️⃣ Self cleaner\n")
                output_lines.append("4️⃣ Cleaning company\n")
                output_lines.append("5️⃣ Massage\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

        if(len(values) == 2):
            if (incoming_msg == "beauty salon" or incoming_msg == "manicure master" or incoming_msg == "self cleaner" or incoming_msg == "cleaning company" or incoming_msg == "massage" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = 'beauty salon'
                if(incoming_msg == '2'):
                    incoming_msg = 'manicure master'
                if(incoming_msg == '3'):
                    incoming_msg = 'self cleaner'
                if(incoming_msg == '4'):
                    incoming_msg = 'cleaning company'
                if(incoming_msg == '5'):
                    incoming_msg = 'Massage'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.business_type = 'missed'
                    values.append('2')
                else:
                    User.business_type = incoming_msg
                    values.append(incoming_msg)
                writeInFile("\nBusiness type: " + str(User.business_type))
                output_lines.append("🗻 Your located (select a point on the map):\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

        if(len(values) == 3):
            if(incoming_msg == '0' or incoming_msg == 'miss'):
                location_data.append('city')
                location_data.append('country')
                User.location = 'missed'
                writeInFile("\nCity: missed")
                writeInFile("\nCountry: missed")
                output_lines.append("🏔️ Your location is: missed\n")
                output_lines.append(
                "💈 How many target orders per month do you need?\n")
                output_lines.append("Manual input:\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                values.append(str(location_data[0]))
                values.append(str(location_data[1]))
                return _send_message(output_lines)

            if(message_latitude is not None and message_longitude is not None):
                location = get_location(message_latitude, message_longitude)
                location_data.append(location[0])
                location_data.append(location[1])
                User.location = str(location_data[0]) + str(location_data[1])
                writeInFile("\nCity: " + str(location[0]))
                writeInFile("\nCountry: " + str(location[1]))
                output_lines.append(
                    "🏔️ Your location is: " + str(location_data[0]) + ", " + str(location_data[1]))
                output_lines.append("\nIf it is not yours choose another.\n")
                output_lines.append(
                "💈 How many target orders per month do you need?\n")
                output_lines.append("Manual input:\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                values.append(str(location_data[0]))
                values.append(str(location_data[1]))
                return _send_message(output_lines)

            if(incoming_msg.isdigit() and len(incoming_msg) < 4):
                output_lines.append("Sorry, I don`t understand this, type '/help' for help. 🤔")
                return _send_message(output_lines)

        if(len(values) == 5):
            if(incoming_msg.isdigit() or incoming_msg == 'miss'):
                if(int(incoming_msg) >= 1 or incoming_msg == '0' or incoming_msg == 'miss'):
                    if(values[-1] == location_data[1] or values[-1] == 'country'):
                        if(incoming_msg == 'miss'):
                            incoming_msg = '0'
                        if(incoming_msg == '0' or incoming_msg == 'miss'):
                            User.orders = '0'
                            values.append('5')
                        else:
                            User.orders = int(incoming_msg)
                            values.append(incoming_msg)
                        writeInFile(
                            "\nМaximum target orders in month: " + str(User.orders))
                        output_lines.append(
                            "😍 Let`s talk about your audience\n")
                        output_lines.append("Who is your target audience?\n")
                        output_lines.append("👨 Men \n")
                        output_lines.append("👩 Women \n")
                        output_lines.append("👨‍👩‍👧‍👦 All\n")
                        output_lines.append(
                            "0️⃣ Type 'miss' or '0' for missing the answer.")
                        return _send_message(output_lines)

        if(len(values) == 6):
            if(incoming_msg == "men" or incoming_msg == "women" or incoming_msg == "all" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3"):
                if(incoming_msg == '1'):
                    incoming_msg = 'men'
                if(incoming_msg == '2'):
                    incoming_msg = 'women'
                if(incoming_msg == '3'):
                    incoming_msg = 'all'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.gender = 'missed'
                    values.append('6')
                else:
                    User.gender = incoming_msg
                    values.append(incoming_msg)
                writeInFile("\nAudience: " + str(User.gender))
                output_lines.append(
                    "🕒 Age of your target audience.\n\nChoose all correct options:\n")
                output_lines.append("1️⃣ 18-24\n")
                output_lines.append("2️⃣ 25-30\n")
                output_lines.append("3️⃣ 30-45\n")
                output_lines.append("4️⃣ 45-60\n")
                output_lines.append("5️⃣ All\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

        if(len(values) == 7):
            if(incoming_msg == "18-24" or incoming_msg == "25-30" or incoming_msg == "30-45" or incoming_msg == "45-60" or incoming_msg == "all" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = '18-24'
                if(incoming_msg == '2'):
                    incoming_msg = '25-30'
                if(incoming_msg == '3'):
                    incoming_msg = '30-45'
                if(incoming_msg == '4'):
                    incoming_msg = '45-60'
                if(incoming_msg == '5'):
                    incoming_msg = 'all'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.age = 'missed'
                    values.append('7')
                    values.append('8')
                    output_lines.append("💰 Price category of your product.\n")
                    output_lines.append("1️⃣ Economy\n")
                    output_lines.append("2️⃣ Standard\n")
                    output_lines.append("3️⃣ Premium\n")
                    output_lines.append(
                        "0️⃣ Type 'miss' or '0' for missing the answer.")
                    return _send_message(output_lines)
                else:
                    User.age = incoming_msg
                    values.append(incoming_msg)
                    output_lines.append("😅 Do you want more? (yes or no)")
                    return _send_message(output_lines)
                writeInFile("\nAge: " + str(User.age))

        if(len(values) == 8):
            if(incoming_msg == 'yes'):
                output_lines.append(
                    "🕒 Age of your target audience.\n\nChoose all correct options:\n")
                output_lines.append("1️⃣ 18-24\n")
                output_lines.append("2️⃣ 25-30\n")
                output_lines.append("3️⃣ 30-45\n")
                output_lines.append("4️⃣ 45-60\n")
                output_lines.append("5️⃣ All\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

            if(incoming_msg == 'no'):
                values.append('8')
                output_lines.append("💰 Price category of your product.\n")
                output_lines.append("1️⃣ Economy\n")
                output_lines.append("2️⃣ Standard\n")
                output_lines.append("3️⃣ Premium\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

            if(incoming_msg == "18-24" or incoming_msg == "25-30" or incoming_msg == "30-45" or incoming_msg == "45-60" or incoming_msg == "all" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = '18-24'
                if(incoming_msg == '2'):
                    incoming_msg = '25-30'
                if(incoming_msg == '3'):
                    incoming_msg = '30-45'
                if(incoming_msg == '4'):
                    incoming_msg = '45-60'
                if(incoming_msg == '5'):
                    incoming_msg = 'all'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                else:
                    User.age = str(User.age) + ", " + str(incoming_msg)
                    del values[0]
                values.append(incoming_msg)
                writeInFile(", " + str(incoming_msg))
                output_lines.append("😅 Do you want more? (yes or no)")
                return _send_message(output_lines)

        if(len(values) == 9):
            if(incoming_msg == "economy" or incoming_msg == "standard" or incoming_msg == "premium" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == '1' or incoming_msg == '2' or incoming_msg == '3'):
                if(incoming_msg == '1'):
                    incoming_msg = 'economy'
                if(incoming_msg == '2'):
                    incoming_msg = 'standard'
                if(incoming_msg == '3'):
                    incoming_msg = 'premium'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.price_category = 'missed'
                    values.append('9')
                else:
                    User.price_category = incoming_msg
                    values.append(incoming_msg)
                writeInFile("\nPrice category: " + str(User.price_category))
                output_lines.append("🕹️ Select the type of target orders:\n")
                output_lines.append("1️⃣ Ordered call\n")
                output_lines.append("2️⃣ Call\n")
                output_lines.append("3️⃣ Ordering on the site\n")
                output_lines.append("4️⃣ Viewing the menu\n")
                output_lines.append("5️⃣ Viewing contacts\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

        if(len(values) == 10):
            if(incoming_msg == "ordered call" or incoming_msg == "call" or incoming_msg == "ordering on the site" or incoming_msg == "viewing the menu" or incoming_msg == "viewing contacts" or incoming_msg == '0' or incoming_msg == 'miss' or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = 'ordered call'
                if(incoming_msg == '2'):
                    incoming_msg = 'call'
                if(incoming_msg == '3'):
                    incoming_msg = 'ordering on the site'
                if(incoming_msg == '4'):
                    incoming_msg = 'viewing the menu'
                if(incoming_msg == '5'):
                    incoming_msg = 'viewing contacts'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.action = 'missed'
                    values.append('10')
                    values.append('11')
                    output_lines.append(
                    "💸 Target cost per action.\n\nInput the sum (euro):\n")
                    output_lines.append(
                        "0️⃣ Type 'miss' or '0' for missing the answer.")
                    return _send_message(output_lines)
                else:
                    User.action = incoming_msg
                    values.append(incoming_msg)
                    output_lines.append("😅 Do you want more? (yes or no)")
                    return _send_message(output_lines)
                writeInFile("\nUser action: " + str(User.action))
        
        if(len(values) == 11):
            if(incoming_msg == 'yes'):
                output_lines.append("🕹️ Select the type of target orders:\n")
                output_lines.append("1️⃣ Ordered call\n")
                output_lines.append("2️⃣ Call\n")
                output_lines.append("3️⃣ Ordering on the site\n")
                output_lines.append("4️⃣ Viewing the menu\n")
                output_lines.append("5️⃣ Viewing contacts\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

            if(incoming_msg == 'no'):
                values.append('11')
                output_lines.append(
                "💸 Target cost per action.\n\nType the sum (euro):\n")
                output_lines.append(
                    "0️⃣ Type 'miss' or '0' for missing the answer.")
                return _send_message(output_lines)

            if(incoming_msg == "ordered call" or incoming_msg == "call" or incoming_msg == "ordering on the site" or incoming_msg == "viewing the menu" or incoming_msg == "viewing contacts" or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "3" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = 'ordered call'
                if(incoming_msg == '2'):
                    incoming_msg = 'call'
                if(incoming_msg == '3'):
                    incoming_msg = 'ordering on the site'
                if(incoming_msg == '4'):
                    incoming_msg = 'viewing the menu'
                if(incoming_msg == '5'):
                    incoming_msg = 'viewing contacts'
                if(incoming_msg in values):
                    del values[values.index(incoming_msg)]
                else:
                    User.action = str(User.action) + ", " + str(incoming_msg)
                    del values[0]
                values.append(incoming_msg)
                writeInFile(", " + str(incoming_msg))
                output_lines.append("😅 Do you want more? (yes or no)")
                return _send_message(output_lines)
                
        if(len(values) == 12):
            if(isinstance(float(incoming_msg), float) or incoming_msg.isdigit() or incoming_msg == '0' or incoming_msg == 'miss'):
                if(User.price_category in values or values[-1] == '11'):
                    if(incoming_msg == 'miss' or incoming_msg == 'no'):
                        incoming_msg = '0'
                    if(incoming_msg == '0' or incoming_msg == 'miss'):
                        User.action_price = '0'
                        values.append('12')
                    else:
                        User.action_price = incoming_msg
                    writeInFile(
                        "\nAction price: " + str(User.action_price) + " euro")
                    output_lines.append(
                        "💵 Budget per month.\n\nType the sum (euro):\n")
                    output_lines.append(
                        "0️⃣ Type 'miss' or '0' for missing the answer.")
                    values.append(incoming_msg)
                    return _send_message(output_lines)

        if(len(values) == 13):
            if(isinstance(float(incoming_msg), float) or incoming_msg.isdigit() or incoming_msg == '0' or incoming_msg == 'miss'):
                if(User.price_category in values or values[-1] == '12'):
                    if(incoming_msg == 'miss'):
                        incoming_msg = '0'
                    if(incoming_msg == '0' or incoming_msg == 'miss'):
                        User.budget = '0'
                        values.append('13')
                    else:
                        User.budget = incoming_msg
                    writeInFile("\nBudget: " + str(User.budget) + " euro")
                    output_lines.append("📰 Do you have a website? (yes or no)\n")
                    output_lines.append(
                        "0️⃣ Type 'miss' or '0' for missing the answer.")
                    values.append(incoming_msg)
                    return _send_message(output_lines)

        if(len(values) == 14):
            if(incoming_msg == "yes"):
                User.site = incoming_msg
                writeInFile("\nSite: " + str(User.site))
                output_lines.append(
                    "😄 Great!\n\nWrite website address:")
                values.append(incoming_msg)
                return _send_message(output_lines)

            if(incoming_msg == "no" or incoming_msg == '0' or incoming_msg == 'miss'):
                if(incoming_msg == '0' or incoming_msg == 'miss'):
                    User.site = 'missed'
                    User.site_url = 'no'
                    values.append('14')
                    values.append('15')
                else:
                    User.site = incoming_msg
                    User.site_url = 'no'
                    values.append(incoming_msg)
                    values.append('15')
                writeInFile("\nSite: " + str(User.site))
                writeInFile("\nSite (url): " + str(User.site_url))
                output_lines.append(
                    "🤗 Thank you for your answers.\n\nLet`s check:")
                output_lines.append("Business type: " + str(User.business_type) + "\nPrice category: " + str(User.price_category) + "\nTarget audience: " + str(User.gender) + ", " + str(User.age) + " age\nLocation: " + str(location_data[0]) + ", " + str(location_data[1]) + "\nTarget action: " + str(User.action) +
                                    "\nTarget action price: " + str(User.action_price) + " euro\nMontly budget of the company: " + str(User.budget) + " euro\nMaximum target actions per month: " + str(User.budget) + "\nSite: " + str(User.site_url) + "\n\nCorrectly? (yes or no)")
                return _send_message(output_lines)

        if(len(values) >= 15):
            if('http' in incoming_msg or 'https' in incoming_msg or '//' in incoming_msg or '.com' in incoming_msg or '.' in incoming_msg or 'www' in incoming_msg):
                User.site_url = incoming_msg
                writeInFile("\nSite (url): " + str(User.site_url))
                values.append(str(User.site_url))
                output_lines.append(
                    "🤗 Thank you for your answers.\n\nLet`s check:")
                output_lines.append("Business type: " + str(User.business_type) + "\nPrice category: " + str(User.price_category) + "\nTarget audience: " + str(User.gender) + ", " + str(User.age) + " age\nLocation: " + str(location_data[0]) + ", " + str(location_data[1]) + "\nTarget action: " + str(User.action) +
                                    "\nTarget action price: " + str(User.action_price) + " euro\nMontly budget of the company: " + str(User.budget) + " euro\nMaximum target actions per month: " + str(User.budget) + "\nSite: " + str(User.site_url) + "\n\nCorrectly? (yes or no)")
                return _send_message(output_lines)

        if(len(values) == 16 or len(values) == 17):
            if(incoming_msg == "yes"):
                with app.app_context():
                    gmail_message = Message(subject="Report " + str(remote_number) + ":", sender=app.config.get(
                        "MAIL_USERNAME"), recipients=["email"]) #Email for message with report
                with app.open_resource("data.doc", 'r') as fp:
                    gmail_message.attach(
                        "data.doc", 'application/msword', fp.read().encode("utf-8"))
                mail.send(gmail_message)
                output_lines.append(
                    "😁 Great!\nYour advertising campaigns are ready.\n\nYour username and password to your personal account:\n\nLOGIN_USER1 / 123456ewq\n")
                output_lines.append("1️⃣ Top up my account\n")
                output_lines.append("2️⃣ Link to your personal account\n")
                output_lines.append("3️⃣ Thank You! (end chat)\n")
                output_lines.append("4️⃣ Contact the Manager\n")
                output_lines.append("5️⃣ FAQ\n")
                return _send_message(output_lines)
            if(incoming_msg == 'no'):
                values.clear()
                location_data.clear()
                output_lines.append("⛳ Type '/start' to start over.\n")
                return _send_message(output_lines)

        if(len(values) >= 15):
            if(incoming_msg == "top up my account" or incoming_msg == "link to your personal account" or incoming_msg == "contact the manager" or incoming_msg == "faq" or incoming_msg == "1" or incoming_msg == "2" or incoming_msg == "1" or incoming_msg == "4" or incoming_msg == "5"):
                if(incoming_msg == '1'):
                    incoming_msg = 'top up my account'
                if(incoming_msg == '2'):
                    incoming_msg = 'link to your personal account'
                if(incoming_msg == '4'):
                    incoming_msg = 'contact the manager'
                if(incoming_msg == '5'):
                    incoming_msg = 'faq'
                for key in links:
                    if(incoming_msg == key):
                        output_lines.append(
                            "📎 It`s your link:\n\n" + str(links[key]))
                        return _send_message(output_lines)
        
        if(len(values) >= 15):
            if(incoming_msg == '3'):
                output_lines.append("👋 Goodbye!")
                return _send_message(output_lines)

    #     #     new_user = User(remote_number)
    #     #     _update_db(new_user)

    output_lines.append(
        "Sorry, I don`t understand, type '/help' for help. 🤔")
    return _send_message(output_lines)
