import random
import string
import gspread
import httplib2
import apiclient
import xml.etree.ElementTree as ET

from google.oauth2.gdch_credentials import ServiceAccountCredentials


class GoogleSheetInteraction:
    def __init__(self, key_for_file, spreadsheetId):
        self.CREDENTIALS_FILE = key_for_file  # Имя файла с закрытым ключом,Вы должны подставить свое, стоит 'test-project-fym-1-282f87f76ddb.json'
        self.spreadsheetId = spreadsheetId  # id таблицы '1di-oF9LcZ8rLH-MdUl3tacgFAqbqNduGYESAQ3oZzJQ'
        # Читаем ключи из файла
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.CREDENTIALS_FILE,
                                                                            ['https://www.googleapis.com/auth'
                                                                             '/spreadsheets',
                                                                             'https://www.googleapis.com/auth/drive'])

        self.httpAuth = self.credentials.authorize(httplib2.Http())  # Авторизуемся в системе
        self.service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

    def create_google_sheets(self, table_name, first_sheet_name, row_count: int, column_count: int):
        """
        create_google_sheets - функция служт для создания google таблицы и возвраает ее id - spreadsheetId
        spreadsheetId - является основным элементом, для взаимодействия с таблицей.
        P.S.придумать, как и где его хранить
        """
        spreadsheet = self.service.spreadsheets().create(body={
            'properties': {'title': f'{table_name}', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                       'sheetId': 0,
                                       'title': f'{first_sheet_name}',
                                       'gridProperties': {'rowCount': row_count, 'columnCount': column_count}}}]
        }).execute()

        self.spreadsheetId = spreadsheet['spreadsheetId']  # сохраняем идентификатор файла
        return self.spreadsheetId

    def setting_and_permissions(self):
        Service = apiclient.discovery.build('drive', 'v3',
                                            http=self.httpAuth)  # Выбираем работу с Google Drive и 3 версию API v3
        access = Service.permissions().create(
            fileId=self.spreadsheetId,
            body={'type': 'user', 'role': 'writer', 'emailAddress': 'megooogurec@gmail.com'},
            # Открываем доступ на редактирование меняем  на свой gmail
            fields='id'
        ).execute()

    def get_sheet_id(self, sheet_name):
        spreadsheet = test_dev.service.spreadsheets().get(spreadsheetId=test_dev.spreadsheetId).execute()
        sheet_id = None
        for _sheet in spreadsheet['sheets']:
            if _sheet['properties']['title'] == sheet_name:  #
                sheet_id = _sheet['properties']['sheetId']
        print(f"{sheet_name}={sheet_id}")
        return sheet_id

    def adding_a_sheet(self, title_sheet: str, row_count, column_count):
        """
        adding_a_sheet - фунция служит для добавления нового листа.
        spreadsheetId - идентификатор файла, меняется взависимости от таблицы.
        title_sheet - название нового листа, оно должно быть уникально.
        row_count - количество строк на новом листе.
        column_count - количество столбцов на новом листе.
        """
        results = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId,
            body=
            {
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": title_sheet,
                                "gridProperties": {
                                    "rowCount": row_count,
                                    "columnCount": column_count
                                }
                            }
                        }
                    }
                ]
            }).execute()

    def fill_or_add_or_change_table(self, title_list: str, start_row_range, end_row_range, list_with_data: list):
        """
        fill_or_add_or_change_table - функция служит для заполнения, изменения или добавления данных в таблицу.
        title_list - название заполняемого листа.
        start_row_range - начало заполняемой строки.
        end_row_range - конец заполняемой строки (не включительно).
        fill_first_line - данные для заполнения верхней строки.
        """
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": f"{title_list}!{start_row_range}:{end_row_range}",
                 "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                 "values": [list_with_data]
                 }
            ]
        }).execute()

    def fill_table(self, title_list: str, start_row_range, end_row_range, list_with_data: list):
        """
        fill_table - функция служит для заполнения, изменения или добавления данных в таблицу.
        title_list - название заполняемого листа.
        start_row_range - начало заполняемой строки.
        end_row_range - конец заполняемой строки (не включительно).
        fill_first_line - данные для заполнения верхней строки.
        """
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheetId, body={
            "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range": f"{title_list}!{start_row_range}:{end_row_range}",
                 "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
                 "values": [data for data in list_with_data]
                 }
            ]
        }).execute()

    def check_len_title_list(self, list_with_title, list_with_value):
        if len(list_with_title) < len(list_with_value):
            while len(list_with_title) != len(list_with_value):
                list_with_title.append('')
            return list_with_title
        else:
            return list_with_title

    def zip_list_with_data(self, sheet_values):
        title_list = []
        value_list = []
        for index in range(len(sheet_values)):
            if index % 2 == 0:
                title_list.append(sheet_values[index])
            else:
                value_list.append(sheet_values[index])

        zipped_list = zip(title_list, value_list)
        return zipped_list

    def zip_title_and_value(self, list_with_data):
        zip_list = []
        for title, value in list_with_data:
            zip_list.append(list(zip(self.check_len_title_list(title, value), value)))
        return zip_list

    def read_from_sheets(self, title_sheet: str, start_row_range: str, end_row_range: str, dev):
        ranges = [f"{title_sheet}!{start_row_range}:{end_row_range}"]  # "Лист номер один!A1:H11"

        results = dev.service.spreadsheets().values().batchGet(spreadsheetId=dev.spreadsheetId,
                                                                ranges=ranges,
                                                                valueRenderOption='FORMATTED_VALUE',
                                                                dateTimeRenderOption='FORMATTED_STRING').execute()
        sheet_values = results['valueRanges'][0]['values']

        # list_with_data = self.zip_list_with_data(sheet_values)
        return sheet_values  # self.zip_title_and_value(list_with_data)

    def formatted_sheet(self, end_row_index: int, text_format: str):
        DATA = {'requests': [
            {'repeatCell': {
                'range': {'endRowIndex': end_row_index},  # 1
                'cell': {'userEnteredFormat': {'textFormat': {text_format: True}}},  # "bold"
                'fields': f'userEnteredFormat.textFormat.{text_format}'
            }}
        ]}

        self.service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=DATA).execute()

    def get_len_sheets(self, title_list):
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId,
            range=f"{title_list}!A1:A").execute()
        return len(response["values"])

    def filling_header(self, title_sheet: str):
        test_dev = GoogleSheetInteraction('test-project-fym-1-282f87f76ddb.json',
                                          # это аватар разработчика, он нужен для кнекта с макетными таблицами
                                          '1gBDCYRIyIH2FvpjE8r6Ew2xBQ_vs73SrWPbQmPXLQxM')
        header = test_dev.read_from_sheets(title_sheet, "A1", "BY1")[0]
        self.fill_or_add_or_change_table(title_sheet, 'A1', 'BY1', header)

    def filling_settings(self):
        test_dev = GoogleSheetInteraction('test-project-fym-1-282f87f76ddb.json',
                                          '1gBDCYRIyIH2FvpjE8r6Ew2xBQ_vs73SrWPbQmPXLQxM')
        settings = test_dev.read_from_sheets("Настройки Авито", "A1", "EO1362")#"EO1362")
        # print(len(settings))
        self.fill_table("Авито настройки", 'A1', "EO1362", settings)


    def creation_and_filling_with_json_xml(self, dict_with_data: dict, xml_name: str):
        root = ET.Element("Ads", target="Avito.ru", formatVersion="3")

        for key, item in dict_with_data.items():
            for val in item:
                ad = ET.SubElement(root, key)

                for title, value in val.items():
                    if type(value) == list:
                        image = ET.SubElement(ad, f"{title}")
                        for list_elem in value:
                            ET.SubElement(image, f"{title}", url=f"{list_elem}")
                    else:
                        ET.SubElement(ad, title).text = value

        tree = ET.ElementTree(root)
        tree.write(f"{xml_name}.xml", encoding="utf-8")

    def filter_and_collecting_users_data(self, list_with_data: list):
        """
        Функция получает данные пользователя из таблицы, фильтрирует и распределяет данные
        для словаря, которым будет заполняться XML файл.
        Этот вариант создания xml будет работать при неизменной позици столбцов,
        другими словами - статичном положении их в таблице.
        Parameters
        ----------
        list_with_data - список со списками/списком данных от пользователя

        -------
        Returns - словарь с данными для XML

        """

        important_point = [14, 15, 57, 58, 59, 61, 63, 65, 68, 69, 73, 74]
        returned_dict = {}

        for data_queue in list_with_data:
            random_id = "{}".format(random.choice(string.ascii_letters) + str(random.randint(100000, 999999)))
            dict_with_users_data = {'Id': random_id,
                                    'Category': None,
                                    'Condition': None,
                                    'GoodsType': None,
                                    'AdType': None,
                                    'Address': None,
                                    'Title': None,
                                    'Description': None,
                                    'Price': 0,
                                    'ManagerName': None,
                                    'AllowEmail': "test@avito.ru",
                                    'Images': [],
                                    'VideoURL': None
                                    }
            for elem in range(len(data_queue)):
                if elem in important_point:
                    if elem == 14:
                        dict_with_users_data["Category"] = data_queue[elem]
                    elif elem == 15:
                        dict_with_users_data["GoodsType"] = data_queue[elem]
                    elif elem == 57:
                        dict_with_users_data["AdType"] = data_queue[elem]
                    elif elem == 58:
                        dict_with_users_data["Condition"] = data_queue[elem]
                    elif elem == 69:
                        dict_with_users_data["Address"] = data_queue[elem]
                    elif elem == 59:
                        dict_with_users_data["Title"] = data_queue[elem]
                    elif elem == 61:
                        dict_with_users_data["Description"] = data_queue[elem]
                    elif elem == 63:
                        dict_with_users_data["Price"] = data_queue[elem]
                    elif elem == 73:
                        dict_with_users_data["ManagerName"] = data_queue[elem]
                    elif elem == 65:
                        dict_with_users_data["Images"].append(data_queue[elem])
                    elif elem == 68:
                        dict_with_users_data["VideoURL"] = data_queue[elem]
            returned_dict[random_id] = dict_with_users_data

        return returned_dict  # dict_with_users_data

    def create_user_sheet(self, table_name: str, first_sheet_name: str, row_count: int, column_count: int):
        # TODO эту функцию дописывай и оптимизируй с наличием новых переменных по разработке
        """
        Функция для создания пользователем его таблицы для заполнения, а так же вспомогательных листов,
        таких как "Авито настройки"
        """
        self.create_google_sheets(table_name, first_sheet_name, row_count, column_count)
        self.setting_and_permissions()
        self.filling_header("Avito")
        self.adding_a_sheet('Авито настройки', 1600, 600)  # TODO Название и количество строк/столбов уточнить
        self.filling_settings()
        print(f"https://docs.google.com/spreadsheets/d/{self.spreadsheetId}/edit#gid=0")




# gc = gspread.service_account(filename='test-project-fym-1-282f87f76ddb.json')
# sh = gc.open("Avito") # сюда вписывается имя таблицы с которой работаем
#
# fmt = CellFormat(
#     backgroundColor=Color(0, 0, 0),
#     textFormat=textFormat(bold=True, foregroundColor=Color(1, 1, 1)),
#     horizontalAlignment='CENTER')
#
# format_cell_range(sh.worksheet('Avito'), 'A1:H1', fmt) # сюда вписывается имя листа с которой работаем
# #
# set_row_height(sh.worksheet('Avito'), '1:100', 40)
# set_column_width(sh.worksheet('Avito'), 'A2:E', 50)
# print(sh.worksheet('Авито').get_all_values())


# range = ['Авито!A1:D1'] # This is a sample. #Тут получают гиперссылку
# result = test_dev.service.spreadsheets().get(
#     spreadsheetId=test_dev.spreadsheetId,
#     ranges=range,
#     fields="sheets/data/rowData/values/hyperlink"
# ).execute()


test_dev = GoogleSheetInteraction('test-project-fym-1-282f87f76ddb.json',
                                  '1gBDCYRIyIH2FvpjE8r6Ew2xBQ_vs73SrWPbQmPXLQxM') #1 -  инициализация таблицы разработчика

test_client = GoogleSheetInteraction('test-project-fym-1-282f87f76ddb.json', None) #2 -  инициализация пользователя
#

#
# test_client.create_user_sheet("TestUserTable", 'Avito', 100, 350) #3 -  создаём таблицу для пользователя
#
# test_client.creating_drop_down_list_in_cell(values_list, sheet_name, user, start_row_index, end_row_index, start_column_indexnt,
#                                         end_column_index) #4 - создаем выпадающие списки

