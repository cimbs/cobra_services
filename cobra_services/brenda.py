from SOAPpy import SOAPProxy ## for usage without WSDL file
import hashlib
import os


def brenda_query(EC_number, brenda_email="", brenda_pass=""):
    """
    Returns raw output string from BRENDA for an EC number.
    """
    
    # in some intranets an issue: how to use a web proxy for WS. Here
    # we assume a set environment variable 'http_proxy'.·
    # This is common in unix environments. SOAPpy does not like
    # a leading 'http://'
    if 'http_proxy' in os.environ.keys():
        my_http_proxy=os.environ["http_proxy"].replace("http://","")
    else:
        my_http_proxy=None

    endpointURL = "http://www.brenda-enzymes.org/soap/brenda_server.php"
    proxy = SOAPProxy(endpointURL, http_proxy=my_http_proxy)
    password = hashlib.sha256(brenda_pass).hexdigest()
    parameters = brenda_email + ',' + password + ',ecNumber*' + EC_number

    new_EC = proxy.getEcNumber(parameters)
    
    if('transferred to' in new_EC):
        new_EC = new_EC.rsplit(' ', 1)[1]
        new_EC = new_EC[:-1]
        parameters = brenda_email + ',' + password + ',ecNumber*' + new_EC
    
    brenda_response = proxy.getTurnoverNumber(parameters)

    return parse_brenda_raw_output(brenda_response)


def parse_brenda_raw_output(raw):
    """
    Parses raw BRENDA string output into a dict.
    """
    # BRENDA returns a string, where entries are separated by '!'.
    # Each entry consists of several key value pairs, separated by '#'.
    # The key is separated from the value by '*'.
    treated_output = [{item.split('*')[0]: item.split('*')[1]
                        for item in entry.split('#') if len(item.split('*')) > 1} 
                        for entry in raw.split('!')]
    
    if 'turnoverNumber' in treated_output:
        treated_output['turnoverNumber'] = float(treated_output['turnoverNumber'])

    return treated_output


def brenda_entry_is_wild_type(entry):
    "True if this entry (from BRENDA) represents a wild-type measurement"
    return entry.haskey('commentary') and 'wild' in entry['commentary']
