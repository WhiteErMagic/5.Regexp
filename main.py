from pprint import pprint
import re
import csv


def get_data_from_file():
    """Читаем адресную книгу в формате CSV в список contacts_list"""
    contacts_list = []
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    # pprint(contacts_list)
    return contacts_list


def regex_list(contacts_list):
    """Обрабатываем список с помощью регулярных выражений"""
    for temp_list in contacts_list[1:]:
        # print(temp_list[-2])
        pattern = "(\+7|8)?\s*\(?(\d{3})\s*?\-*?\)?\s*?(\d{3})\s*?\-*?\s*?(\d{2})\s*?\-*?\s*?(\d{2})(\s?)\(?(\w+\.)?\s?(\d{2,})?\)?"
        temp_list[-2] = re.sub(pattern, r"+7(\2)\3-\4-\5\6\7\8", temp_list[-2])
        # print(temp_list[-2])
        # print(" ".join(temp_list[0:3]))
        # pattern = "([а-яёА-ЯЁ]+)(\s*)\,?([а-яёА-ЯЁ]+)(\s*)\,?([а-яёА-ЯЁ]+)?"
        pattern = "^(\w+)(\s*)\,?(\w+)(\s*)\,?(\w+)?"

        temp_fio = re.sub(pattern, r"\1 \3 \5", " ".join(temp_list[0:3]).strip())
        list_temp_fio = temp_fio.split(" ")
        temp_list[0] = list_temp_fio[0]
        temp_list[1] = list_temp_fio[1]
        temp_list[2] = list_temp_fio[2]
        #print(temp_list)
        # print(type(list_temp_fio[0]))
        # print(list_temp_fio[0] in contacts_list)

    return contacts_list


def delete_duplicates(contacts_list_in):
    """Удаляем дубликаты"""
    contacts_list_out = contacts_list_in[0:1]
    for temp_contacts_list in contacts_list_in[1:]:
        temp_list = []

        for temp_list_out in contacts_list_out:
            # Проверка, есть ли уже в итоговом списке
            # по полному фио
            if temp_contacts_list[2] != '':
                if temp_contacts_list[0] == temp_list_out[0] \
                        and temp_contacts_list[1] == temp_list_out[1] \
                        and temp_contacts_list[2] == temp_list_out[2]:
                            temp_list = temp_contacts_list
                            # Заполним не пустые поля
                            for ind in range(2, len(temp_contacts_list)):
                                 if temp_contacts_list[ind] != '':
                                     temp_list_out[ind] = temp_contacts_list[ind]

            # Проверка, есть ли уже в итоговом списке
            # по фамилии и имени, если не заполнено отчество
            if temp_contacts_list[2] == '':
                if temp_contacts_list[0] == temp_list_out[0] \
                        and temp_contacts_list[1] == temp_list_out[1]:
                            temp_list = temp_contacts_list
                            # Заполним не пустые поля
                            for ind in range(2, len(temp_contacts_list)):
                                if temp_contacts_list[ind] != '':
                                    temp_list_out[ind] = temp_contacts_list[ind]

        # Добавим в итоговый список, если еще нет такого фио
        if len(temp_list) == 0:
            contacts_list_out.append(temp_contacts_list)

    return contacts_list_out


def write_result_list(contacts_list):
    """Код для записи файла в формате CSV"""
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    contacts_list = get_data_from_file()
    contacts_list = regex_list(contacts_list)
    contacts_list = delete_duplicates(contacts_list)
    pprint(contacts_list)
    write_result_list(contacts_list)
