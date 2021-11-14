import re

creditcard_number = input("Credit card number: ")

# regular expression for American Express which must contain exact sequence of digits
AMEX = re.search("^3[47][0-9]{13}$", creditcard_number)

# regular expression for MsterCard. A bit longer but that is just because it can start from 51,52,53,54,55
MASTERCARD = re.search("^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$", creditcard_number)

# regular expression for VISA which must contain exact sequence of following digits
VISA = re.search("^4[0-9]{12}(?:[0-9]{3})?$", creditcard_number)


if AMEX:
    print("AMEX")
elif MASTERCARD:
    print("MASTERCARD")
elif VISA:
    print("VISA")
else:
    print("INVALID")