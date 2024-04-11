import forms.form_filler as ff

from forms.form_filler import FLD_NM  # for tests


# New fields for sign-up form
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
DATE_OF_BIRTH = 'date_of_birth'
EMAIL = 'email'
PASSWORD = 'password'

# Additional password instructions
PASSWORD_INSTRUCTIONS = "Password must be at least 8 characters long and contain at least one digit."

SIGNUP_FORM_FLDS = [
    {
        FLD_NM: 'Instructions',
        ff.QSTN: 'Enter your details to sign up.',
        ff.INSTRUCTIONS: True,
    },
    {
        FLD_NM: FIRST_NAME,
        ff.QSTN: 'First Name:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: LAST_NAME,
        ff.QSTN: 'Last Name:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: DATE_OF_BIRTH,
        ff.QSTN: 'Date of Birth (YYYY-MM-DD):',
        ff.PARAM_TYPE: ff.DATE,
        ff.OPT: False,
    },
    {
        FLD_NM: EMAIL,
        ff.QSTN: 'Email:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: PASSWORD,
        ff.QSTN: 'Password:',
        ff.PARAM_TYPE: ff.PASSWORD,
        ff.OPT: False,
    },
    {
        FLD_NM: 'Password Instructions',
        ff.QSTN: PASSWORD_INSTRUCTIONS,
        ff.INSTRUCTIONS: True,
    },
]


def get_form() -> list:
    return SIGNUP_FORM_FLDS


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(SIGNUP_FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(SIGNUP_FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()