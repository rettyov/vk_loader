import yaml


def load_configs(auth_path='./configs/auth.yaml'):
    configs = {}
    with open(auth_path, "r") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)
            config = {}
    configs['auth'] = config
    return configs

def load_csv(csv_path='./configs/links.csv'):
    links = []
    with open(csv_path, "r") as f:
        for line in f.readlines():
            links.append(line[:-1])
    return links
