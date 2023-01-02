#!/usr/bin/env python
"""
    A brute force location importer from an Australian postcodes json dump

    Original source data gratefully obtained from https://github.com/joahua/AusPostcode.git

    Author: David L. Nugent <davidn@uniquode.io>, Sep 9 2015
"""

import os
import json
import re
# awesome argparse frontend
import begin

import django
os.environ.setdefault("PYTHONPATH", ".")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventmgr.settings")
django.setup()

from contacts.models import Country, State, Locality


def state_for_postcode(country, postcode, locality):
    """
    Uses a simple range check to determine the state
    """
    if country == 'AU':
        """ Australian states """
        if 800 <= postcode < 900:
            return None # 'NT'
        if (2600 <= postcode < 2618) or (2900 <= postcode < 2915):
            return None # 'ACT'     # arggh
        if 2000 <= postcode < 3000:
            return None # 'NSW'
        if 3000 <= postcode < 4000:
            return 'VIC'
        if 4000 <= postcode < 5000:
            return None # 'QLD'
        if 5000 <= postcode < 6000:
            return None # 'SA'
        if 6000 <= postcode < 7000:
            return None # 'WA'
        if 7000 <= postcode < 8000:
            return None # 'TAS'
        if 9000 <= postcode < 10000:
            return None  # special cases, not important for us
    else:
        ValueError("Unknown country '%s'" % (country,))
    raise ValueError("Unknown state for postcode '%i', locality '%s'" % (postcode, locality))


@begin.start
def run(country='AU', init=False, *srcfiles):
    """ json states/postcode importer """

    if init:
        countries = {
            'AU': 'Australia',
            'USA': 'United States',
            'GB': 'Great Britain',
            'FR': 'France',
            'DE': 'Germany',
        }
        states = {
            'AU': {
                'ACT': 'Australian Capital Territory',
                'NSW': 'New South Wales',
                'NT': 'Northern Territory',
                'QLD': 'Queensland',
                'SA': 'South Australia',
                'TAS': 'Tasmania',
                'VIC': 'Victoria',
                'WA': 'Western Australia',
            }
        }
        for cc in countries.keys():
            c = Country(abbrev=cc, name=countries[cc])
            c.save()
            if cc in states:
                for st in states[cc].keys():
                    State(country=c, abbrev=st, name=states[cc][st]).save()
    else:
        """
            here we rely on the countries/states having been previously set up
        """
        country_object = Country.objects.filter(abbrev=country)
        if country_object is None:
            raise ValueError("Unknown country code '%s'" % (country,))

        """
            parse and process each of the given source files in turn
        """
        for srcfile in srcfiles:
            try:
                with open(srcfile, 'r') as src:
                    """
                        parse the json input to a list of dicts
                        expected format:
                        [{
                            'Suburb': '<suburb name>',
                            'Postcode': '<numeric postcode>'
                         },
                         ...
                        ]
                    """
                    data = json.load(src)
                    print('JSON source data successfully loaded')

                    """
                        process each suburb, find a matching state
                        save to db unless it already exists there
                    """
                    namecheck = re.compile(r'(.*)\s+\(.*\)')
                    dupe_count, create_count, update_count = 0, 0, 0
                    for r in data:
                        state = state_for_postcode(country, int(r['Postcode']), r['Suburb'])
                        """ do a bit of cleaning """
                        postcode = r['Postcode']
                        suburb = r['Suburb']
                        result = namecheck.match(suburb)
                        if result is not None:
                            suburb = result.group(1)
                        if state is not None:
                            try:
                                state_object = State.objects.get(country=country_object, abbrev=state)
                            except State.DoesNotExist:
                                raise State.DoesNotExist("State '%s' for country '%s' not in database" % (state, country))
                            # There may be more than one locality with the same postcode
                            locality_objects = Locality.objects.filter(state=state_object, postcode=postcode)
                            # So make sure we are not duplicating
                            for locality_object in locality_objects:
                                if locality_object.name == suburb:
                                    dupe_count += 1
                                    break
                            else:
                                locality_object = Locality(state=state_object, name=suburb, postcode=postcode)
                                locality_object.save()
                                create_count += 1

                    print("%d created, %d updated, %d duplicates skipped" % (create_count, update_count, dupe_count))

            except (State.DoesNotExist, Locality.DoesNotExist) as exc:
                print(exc)
                exit(1)
            except EnvironmentError as exc:
                print(exc)
                exit(1)
