from utils import load_configs, load_csv
from loader import Vk, get_data


if __name__ == '__main__':
    configs = load_configs()
    links = load_csv()
    vk = Vk(configs).log_in()
    data = get_data(vk, links)
    print(data)

    # ToDo: add async!

