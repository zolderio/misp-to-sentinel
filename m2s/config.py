graph_auth = {
    'tenant': '',
    'client_id': '',
    'client_secret': '',
}
targetProduct = 'Azure Sentinel'

misp_event_filters = {
  "type_attribute": 'ip-src',
  "type_attribute": 'ip-dst',
  "type_attribute": 'email-subject'
}

action = 'alert'
passiveOnly = False
days_to_expire = 5
misp_key = ''
misp_domain = ''
misp_verifycert = False