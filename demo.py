import pymail
import examples

if __name__ == '__main__':
    for unparsed_email in examples.emails:
        email = pymail.Email(**unparsed_email)
        print('The email was signed by {0.signer} and {0.country} is the most-referenced country.'.format(email))
