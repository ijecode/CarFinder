import yaml
class params:
    searchCriteria = {}
    sites = {}
    notifications = {}

    def __init__(self) -> None:
        try:
            stream = open('parameters.yaml', 'r')
            yamlFile = yaml.load(stream, yaml.CLoader)
        except Exception as e:
            print(e)
            print('Issues loading parameters.yaml, exiting...')
            exit()

        params.searchCriteria = yamlFile['searchCriteria']
        params.sites = yamlFile['sites']
        params.notifications = yamlFile['notifications']

        self.qualityCheckAndCleanUp()
        self.scanForMissingParameters()

    def scanForMissingParameters(self):
        requiredSearchCriteriaParameters = ['postcode']
        try:
            for requiredSearchCriteria in requiredSearchCriteriaParameters:
                if requiredSearchCriteria not in params.searchCriteria:
                    raise Exception('Required Search Criteria %s is not present', requiredSearchCriteria)
            if True not in params.sites.values():
                raise Exception('At least one site must be enabled for searching')
            if params.notifications['pushover']['enabled'] == True:
                if 'userKey' or 'apiKey' not in params.notifications['pushover'].values():
                    raise Exception('Missing required userKey/apiKey for Pushover notifications')
                if params.notifications['pushover']['userKey'] or params.notifications['pushover']['apiKey'] == 'your_key_here':
                    raise Exception('To enable Pushover notifications, set your user key and api key')
        except Exception as e:
            print(e)
            print('Issues with YAML parameter file detected, exiting...')
            exit()

    def qualityCheckAndCleanUp(self):    
        for key, value in params.searchCriteria.items():
            try:
                # General checks
                if value is None:
                    raise Exception('Parameter %s is empty', value)
                # Check values
                if key == 'postcode':
                    print('found postcode')
                    if len(value) < 6:
                        raise Exception('Postcode %s is less than 6 characters', value)
                    if len(value) > 8:
                        raise Exception('Postcode %s is greater than 8 characters', value)
                    # Strip any whitespace
                    params.searchCriteria[key] = value.replace(' ', '')
                elif key == 'distance':
                    if value != 'max' and type(value) is not int:
                        raise Exception('Distance %s is not an integer or \"max\"', value)
            except Exception as e:
                print(e)
                print('Issues with YAML parameter file detected, exiting...')
                exit()
