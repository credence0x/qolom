import re
def get_asterisked_mail(email_address):
    mail_split = re.split('@',email_address)
    name = mail_split[0]
    extension = mail_split[1]
    store = ""
    for i in range(len(name)):
        if len(store)<=2:
            store+=name[i]
        else:
            store+="*"

    asterisked_mail = f"{store}@{extension}"
    return asterisked_mail