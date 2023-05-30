import pycountry


def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country is not None:
            return country.alpha_2
        else:
            return None
    except LookupError:
        return None
