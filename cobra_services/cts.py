import requests
import json


def cts_brenda_to_kegg(brenda_name, max_requests=3):
    """
    Returns the KEGG id of a compound, from the name
    on BRENDA.
    """

    cts_response = requests.get('http://cts.fiehnlab.ucdavis.edu/'
                                'service/convert/Chemical%20Name/'
                                'KEGG/' + brenda_name)
    request_counter = 0
    while request_counter <= max_requests:
        try:
            kegg_ids = json.loads(cts_response.text)[0]['result']
            break
        except (KeyError, IndexError):
            request_counter = request_counter + 1
    else:
        assert False

    if kegg_ids:
        return kegg_ids[0]
    else:
        return None
