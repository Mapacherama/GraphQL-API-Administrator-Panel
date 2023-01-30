import phonenumbers

def convert_to_phonenumber(phone_nr):
    try:
        # parse the phone number and store it as a phonenumber object
        parsed_number = phonenumbers.parse(phone_string, None)
        # check if the number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
        # format the number as E.164 format
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberFormatException:
        raise ValueError("Invalid phone number")