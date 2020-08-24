import yaml

__config = None

def config(): 
    #here get the value of the yaml file to a dictionary 
    global __config
    if not __config: 
        with open('config.yaml', mode='r') as f: 
            __config = yaml.load(f)
    return __config