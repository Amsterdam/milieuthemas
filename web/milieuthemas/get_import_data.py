"""
We use the objectstore to get the latest and greatest

Should be able to run standalone
"""

import os
import logging
from swiftclient.client import Connection

# from dateutil import parser

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


assert os.getenv('OS_PASSWORD_BAG')
assert os.getenv('OS_PASSWORD_BOM')


MILIEUTHEMA = dict(
    VERSION='2.0',
    AUTHURL='https://identity.stack.cloudvps.com/v2.0',
    TENANT_NAME='BGE000081 BAG',
    TENANT_ID='4f2f4b6342444c84b3580584587cfd18',
    USER='bag_brk',
    PASSWORD=os.getenv('OS_PASSWORD_BAG', 'insecure'),
    REGION_NAME='NL',
)

BOMMENKAART = dict(
    VERSION='2.0',
    AUTHURL='https://identity.stack.cloudvps.com/v2.0',
    TENANT_NAME='BGE000081_Bommenkaart',
    # TENANT_ID='0efc828b88584759893253f563b35f9b',
    TENANT_ID='e063b706cffc4002883c28d531f0234f',
    USER='bommenkaart',
    PASSWORD=os.getenv('OS_PASSWORD_BOM', 'insecure'),
    REGION_NAME='NL',
)


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("swiftclient").setLevel(logging.WARNING)

print(MILIEUTHEMA)
print(BOMMENKAART)

m_store = MILIEUTHEMA

bag_connection = Connection(
    authurl=m_store['AUTHURL'],
    user=m_store['USER'],
    key=m_store['PASSWORD'],
    tenant_name=m_store['TENANT_NAME'],
    auth_version=m_store['VERSION'],
    os_options={'tenant_id': m_store['TENANT_ID'],
                'region_name': m_store['REGION_NAME']})

b_store = BOMMENKAART

bom_connection = Connection(
    authurl=b_store['AUTHURL'],
    user=b_store['USER'],
    key=b_store['PASSWORD'],
    tenant_name=b_store['TENANT_NAME'],
    auth_version=b_store['VERSION'],
    os_options={'tenant_id': b_store['TENANT_ID'],
                'region_name': b_store['REGION_NAME']})


def get_store_object(connection, folder, object_meta_data):
    return connection.get_object(folder, object_meta_data['name'])[1]


def get_full_container_list(conn, container, **kwargs):
    limit = 10000
    kwargs['limit'] = limit
    page = []

    seed = []

    _, page = conn.get_container(container, **kwargs)
    seed.extend(page)

    while len(page) == limit:
        # keep getting pages..
        kwargs['marker'] = seed[-1]['name']
        _, page = conn.get_container(container, **kwargs)
        seed.extend(page)

    return seed


def get_data(connection, folder):
    """
    Download data in folder from connection
    """

    file_list = []

    meta_data = get_full_container_list(
        connection, folder)

    for o_info in meta_data:
        # if o_info['content_type'] == 'application/zip':
        file_list.append(o_info)

    # Download the latest data
    for meta_file in file_list:
        full_name = meta_file['name']
        dir_path = "/".join(full_name.split('/')[:-1])

        if meta_file['content_type'] == 'application/directory':
            continue

        if not meta_file['content_type'].endswith('csv'):
            continue

        log.warning('Downloading: %s', full_name)

        new_file = get_store_object(connection, folder, meta_file)

        file_dir = 'data/{}/{}/'.format(folder, dir_path)
        file_path = 'data/{}/{}'.format(folder, full_name)

        # save output to file!
        try:
            os.makedirs(os.path.dirname(file_dir))
        except FileExistsError:
            pass

        with open(file_path, 'wb') as output_file:
            output_file.write(new_file)


def get_all_files():
    """
    Get csv, shpe, dumps etc.. just all data!
    """

    all_sources = [
        (bom_connection, 'bommenkaart'),
        (bag_connection, 'Milieuthemas')
    ]

    for connection, folder in all_sources:
        get_data(connection, folder)


if __name__ == '__main__':
    get_all_files()
