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

    treated_output = [{item.split('*')[0]: item.split('*')[1]
                       for item in entry.split('#') if len(item.split('*')) > 1} 
                      for entry in brenda_response.split('!')]

    return treated_output
    # treated_output_by_substrate = treated_output
    # new_entry = {}
    # for entry in treated_output[ID]:
    #     for data_point, description in entry.iteritems():
    #         if data_point == 'substrate':
    #             if description in new_entry:
    #                 new_entry[description].append(entry)
    #             else:
    #                 new_entry[description] = []
    # treated_output[ID] = new_entry




# def treatBrendaOutput(output):
#     '''
#     Removes unnecessary parameters from entries and
#     checks to see if enzymes characterized were
#     wild-type or mutant.
#     '''
#     treated_output = {}
#     treated_output = {ID: [{item.split('*')[0]: item.split('*')[1] 
#         for item in entry.split('#') 
#         if len(item.split('*')) > 1} 
#         for entry in output[ID].split('!')] for ID in output.keys()}

#     treated_output_by_substrate = treated_output
#     for ID in treated_output:
#         new_entry = {}
#         for entry in treated_output[ID]:
#             for data_point, description in entry.iteritems():
#                 if data_point == 'substrate':
#                     if description in new_entry:
#                         new_entry[description].append(entry)
#                     else:
#                         new_entry[description] = []
#         treated_output[ID] = new_entry

#     no_data = []

#     for ID in treated_output: 
#         if output[ID] == '':
#             no_turnover_data.append(ID)
#         else:
#             empty = bool
#             for substrate in treated_output[ID]:        
#                 commentary_treated = False
#                 wild_type = False
#                 for entry in treated_output[ID][substrate]:
#                     if entry == [] :
#                         continue
#                     else:
#                         for key,value in entry.iteritems():
#                             if (key == 'commentary') and 'wild' in value:
#                                 wild_type = True
#                                 commentary_treated = True
#                             elif (key == 'commentary') and 'mutant' in value:
#                                 wild_type = False
#                                 commentary_treated = True
#                         print(ID)
#                         entry.pop('literature')
#                         entry.pop('substrate')
#                         entry.pop('ligandStructureId')
#                         entry.pop('turnoverNumberMaximum')
#                         entry.pop('commentary', 'No comment')
#                         if wild_type:
#                             entry['wild-type'] = True
#                         elif not wild_type and commentary_treated:
#                             entry['wild-type'] = False
