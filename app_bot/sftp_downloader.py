import logging
import csv
import io
import os
import paramiko
from core.database import init, models
from settings import settings


logger = logging.getLogger(__name__)


def __download_file_to_memory(sftp: paramiko.SFTPClient, remote_file_path):
    file_in_memory = io.BytesIO()
    sftp.getfo(remote_file_path, file_in_memory)
    file_in_memory.seek(0)
    return file_in_memory

def save_files_from_ftp():
    transport = paramiko.Transport((settings.ftp_host, settings.ftp_port))
    transport.connect(username=settings.ftp_user, password=settings.ftp_pass.get_secret_value())
    
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    files = sftp.listdir(settings.remote_directory)
    for file in files:
        file_in_memory = __download_file_to_memory(sftp, settings.remote_directory + f'/{file}')

        save_dir = os.path.join(settings.base_files_dir, '')
        if not os.path.exists(save_dir):
            logger.info(f'new rep {save_dir}') 
            os.makedirs(save_dir)
        
        file_path = os.path.join(save_dir, f'ftp_{file}')

        with open(file_path, 'wb') as local_file:
            local_file.write(file_in_memory.read())
            logger.info(f'file {file_path} is saved')

    sftp.close()
    transport.close()



def save_stop_list_as_json(csv_file, json_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)

        restaurant_data = {}

        # dict {restaurant: data}
        for row in csv_reader:
            restaurant = row[0]
            if restaurant != 'End':
                if restaurant == 'Start':
                    continue
                if restaurant in restaurant_data:
                    restaurant_data[restaurant].append(row[1:])
                else:
                    restaurant_data[restaurant] = [row[1:]]
            else:
                break

    # save N .txt files for each restaurant
    for restaurant, items in restaurant_data.items():
        filename = os.path.join(settings.base_files_dir, f'{restaurant}.txt')
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('Ресторан,Ресторан_SIFR,Ресторан_CODE,Артикул,MENUITEMS_SIFR,Наименованиеn')
            for item in items:
                file.write(','.join(item) + '\n')
            logger.info(f'File {filename} is saved!')
    logger.info(f'Total saved files: {len(restaurant_data.keys())}')

    return restaurant_data

async def sftp_worker():
    csv_file = os.path.join(settings.base_files_dir, 'ftp_Stop.csv')

    save_files_from_ftp()
    restaurants = save_stop_list_as_json(csv_file=csv_file, json_file=settings.stop_list_json_file)

    # add report and sub_reports for StopList
    report = await models.Report.get_or_none(name='Отчет по стоп-листу')
    if not report:
        report = await models.Report.create(name='Отчет по стоп-листу')

    for restaurant in restaurants.keys():
        await models.SubReport.update_or_create(file_name=f'{restaurant}.txt', parent_report_id=report.id)
