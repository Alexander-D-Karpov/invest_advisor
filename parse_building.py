import pandas as pd
from django.db import transaction

from invest_advisor.chat.models import BuildingModel


# Функции для безопасной конвертации и обработки данных
def safe_float(value):
    try:
        return float(value) if pd.notna(value) else None
    except ValueError:
        return None


def safe_int(value):
    try:
        return int(value) if pd.notna(value) else None
    except ValueError:
        return None


def parse_array(value):
    if pd.isna(value) or value == "":
        return []
    return [str(item).strip() for item in value.split(";")]


def process_excel(file_path):
    df = pd.read_excel(file_path)
    with transaction.atomic():
        for _, row in df.iterrows():
            building = BuildingModel(
                name=row["Название площадки"]
                if pd.notna(row["Название площадки"])
                else None,
                pref_treatment=row["Преференциальный режим"]
                if pd.notna(row["Преференциальный режим"])
                else None,
                pref_object=row["Наименование объекта преференциального режима"]
                if pd.notna(row["Наименование объекта преференциального режима"])
                else None,
                pref_object_name=row[
                    "Наименование объекта преференциального режима_наименование"
                ]
                if pd.notna(
                    row["Наименование объекта преференциального режима_наименование"]
                )
                else None,
                support_infra_object=row["Объект инфраструктуры поддержки"]
                if pd.notna(row["Объект инфраструктуры поддержки"])
                else None,
                support_name=row["Наименование объекта инфраструктуры поддержки"]
                if pd.notna(row["Наименование объекта инфраструктуры поддержки"])
                else None,
                support_name_detail=row[
                    "Наименование объекта инфраструктуры поддержки_наименование"
                ]
                if pd.notna(
                    row["Наименование объекта инфраструктуры поддержки_наименование"]
                )
                else None,
                region=row["Регион"] if pd.notna(row["Регион"]) else None,
                municipal_entity=row["Муниципальное образование"]
                if pd.notna(row["Муниципальное образование"])
                else None,
                address=row["Адрес объекта"]
                if pd.notna(row["Адрес объекта"])
                else None,
                nearest_city=row["Ближайший город"]
                if pd.notna(row["Ближайший город"])
                else None,
                site_format=parse_array(row["Формат площадки"])
                if pd.notna(row["Формат площадки"])
                else [],
                site_type=parse_array(row["Тип площадки"])
                if pd.notna(row["Тип площадки"])
                else [],
                ownership_form=row["Форма собственности объекта"]
                if pd.notna(row["Форма собственности объекта"])
                else None,
                transaction_form=parse_array(row["Форма сделки"])
                if pd.notna(row["Форма сделки"])
                else [],
                cost_object=safe_float(
                    row["Стоимость объекта, руб. (покупки или месячной аренды)"]
                ),
                cost_per_year_ha=safe_float(row["Стоимость, руб./год за га"]),
                cost_per_year_sqm=safe_float(row["Стоимость, руб./год за кв.м."]),
                lease_term_min=safe_int(
                    row.get("min сроки аренды (если применимо), лет")
                ),
                lease_term_max=safe_int(
                    row.get("max сроки аренды (если применимо), лет")
                ),
                cost_determination_order=row["Порядок определения стоимости"]
                if pd.notna(row["Порядок определения стоимости"])
                else None,
                hazard_class=row["Класс опасности объекта"]
                if pd.notna(row["Класс опасности объекта"])
                else None,
                building_characteristics=row[
                    "Характеристики расположенных объектов капитального строительства"
                ]
                if pd.notna(
                    row[
                        "Характеристики расположенных объектов капитального строительства"
                    ]
                )
                else None,
                free_land_area=safe_float(row["Свободная площадь ЗУ, га"]),
                cadastral_number_land=row["Кадастровый номер ЗУ"]
                if pd.notna(row["Кадастровый номер ЗУ"])
                else None,
                permitted_use_options=row["Варианты разрешенного использования"]
                if pd.notna(row["Варианты разрешенного использования"])
                else None,
                land_surveying=row["Межевание ЗУ"] == "Да"
                if pd.notna(row["Межевание ЗУ"])
                else None,
                land_category=row["Категория земель"]
                if pd.notna(row["Категория земель"])
                else None,
                free_building_area=safe_float(
                    row["Свободная площадь здания, сооружения, помещения, кв. м"]
                ),
                cadastral_number_building=row[
                    "Кадастровый номер здания, сооружения, помещения"
                ]
                if pd.notna(row["Кадастровый номер здания, сооружения, помещения"])
                else None,
                building_technical_characteristics=row[
                    "Технические характеристики здания, сооружения, помещения"
                ]
                if pd.notna(
                    row["Технические характеристики здания, сооружения, помещения"]
                )
                else None,
                owner_name=row["Наименование собственника / администратора объекта"]
                if pd.notna(row["Наименование собственника / администратора объекта"])
                else None,
                owner_inn=row["ИНН собственника"]
                if pd.notna(row["ИНН собственника"])
                else None,
                website=row["Сайт"] if pd.notna(row["Сайт"]) else None,
                note=row["Примечание"] if pd.notna(row["Примечание"]) else None,
                water_supply_available=row["Водоснабжение Наличие (Да/Нет)"] == "Да"
                if pd.notna(row["Водоснабжение Наличие (Да/Нет)"])
                else None,
                water_supply_rate_consumption=safe_float(
                    row["Водоснабжение Тариф на потребление, руб./куб. м"]
                ),
                water_supply_rate_transport=safe_float(
                    row["Водоснабжение Тариф на транспортировку, руб./куб. м"]
                ),
                water_supply_objects_max_capacity=safe_float(
                    row[
                        "Объекты водоснабжения Максимально допустимая мощность, куб. м/ч"
                    ]
                ),
                water_supply_objects_free_capacity=safe_float(
                    row["Объекты водоснабжения Свободная мощность, куб.м/ч"]
                ),
                water_supply_other_characteristics=row[
                    "Объекты водоснабжения Иные характеристики"
                ]
                if pd.notna(row["Объекты водоснабжения Иные характеристики"])
                else None,
                water_network_capacity=safe_float(
                    row["Сети водоснабжения Пропускная способность, куб. м/ч"]
                ),
                sewage_available=row["Водоотведение Наличие (Да/Нет)"] == "Да"
                if pd.notna(row["Водоотведение Наличие (Да/Нет)"])
                else None,
                sewage_rate_consumption=safe_float(
                    row["Водоотведение Тариф на потребление, руб./куб. м"]
                ),
                sewage_rate_transport=safe_float(
                    row["Водоотведение Тариф на транспортировку, руб./куб. м"]
                ),
                sewage_objects_max_capacity=safe_float(
                    row[
                        "Объекты водоотведения Максимально допустимая мощность, куб. м/ч"
                    ]
                ),
                sewage_objects_free_capacity=safe_float(
                    row["Объекты водоотведения Свободная мощность, куб. м/ч"]
                ),
                sewage_other_characteristics=row[
                    "Объекты водоотведения Иные характеристики"
                ]
                if pd.notna(row["Объекты водоотведения Иные характеристики"])
                else None,
                sewage_network_capacity=safe_float(
                    row["Сети водоотведения Пропускная способность, куб. м/ч"]
                ),
                gas_supply_available=row["Газоснабжение Наличие (Да/Нет)"] == "Да"
                if pd.notna(row["Газоснабжение Наличие (Да/Нет)"])
                else None,
                gas_supply_rate_consumption=safe_float(
                    row["Газоснабжение Тариф на потребление, руб./куб. м"]
                ),
                gas_supply_rate_transport=safe_float(
                    row["Газоснабжение Тариф на транспортировку, руб./куб. м"]
                ),
                gas_supply_objects_max_capacity=safe_float(
                    row.get(
                        "Объекты газоснабжения Максимально допустимая мощность, куб. м./ч"
                    )
                ),
                gas_supply_objects_free_capacity=safe_float(
                    row["Объекты газоснабжения Свободная мощность, куб. м/ч"]
                ),
                gas_supply_other_characteristics=row[
                    "Объекты газоснабжения Иные характеристики"
                ]
                if pd.notna(row["Объекты газоснабжения Иные характеристики"])
                else None,
                gas_network_capacity=safe_float(
                    row["Сети газоснабжения Пропускная способность, куб. м/ч"]
                ),
                electricity_supply_available=row["Электроснабжение Наличие (Да/Нет)"]
                == "Да"
                if pd.notna(row["Электроснабжение Наличие (Да/Нет)"])
                else None,
                electricity_rate_consumption=safe_float(
                    row["Электроснабжение Тариф на потребление, руб./МВт*ч"]
                ),
                electricity_rate_transport=safe_float(
                    row["Электроснабжение Тариф на транспортировку, руб./МВт*ч"]
                ),
                electricity_objects_max_capacity=safe_float(
                    row[
                        "Объекты электроснабжения Максимально допустимая мощность, МВт/ч"
                    ]
                ),
                electricity_objects_free_capacity=safe_float(
                    row["Объекты электроснабжения Свободная мощность, МВт/ч"]
                ),
                electricity_other_characteristics=row[
                    "Объекты электроснабжения Иные характеристики"
                ]
                if pd.notna(row["Объекты электроснабжения Иные характеристики"])
                else None,
                electricity_network_capacity=safe_float(
                    row["Сети электроснабжения Пропускная способность, МВт/ч"]
                ),
                heating_available=row["Теплоснабжение Наличие (Да/Нет)"] == "Да"
                if pd.notna(row["Теплоснабжение Наличие (Да/Нет)"])
                else None,
                heating_rate_consumption=safe_float(
                    row["Теплоснабжение Тариф на потребление, руб./Гкал*ч"]
                ),
                heating_rate_transport=safe_float(
                    row["Теплоснабжение Тариф на транспортировку, руб./Гкал*ч"]
                ),
                heating_objects_max_capacity=safe_float(
                    row[
                        "Объекты теплоснабжения Максимально допустимая мощность, Гкал/ч"
                    ]
                ),
                heating_objects_free_capacity=safe_float(
                    row["Объекты теплоснабжения Свободная мощность, Гкал/ч"]
                ),
                heating_other_characteristics=row[
                    "Объекты теплоснабжения Иные характеристики"
                ]
                if pd.notna(row["Объекты теплоснабжения Иные характеристики"])
                else None,
                heating_network_capacity=safe_float(
                    row["Сети теплоснабжения Пропускная способность, Гкал/ч"]
                ),
                waste_disposal_available=row["Вывоз ТКО Наличие (Да/Нет)"] == "Да"
                if pd.notna(row["Вывоз ТКО Наличие (Да/Нет)"])
                else None,
                waste_disposal_rate_ton=safe_float(row["Вывоз ТКО Тариф, руб./тонна"]),
                waste_disposal_rate_cubic_meter=safe_float(
                    row["Вывоз ТКО Тариф, руб./куб. м"]
                ),
                access_roads_available=row["Наличие подъездных путей (Да/Нет)"] == "Да"
                if pd.notna(row["Наличие подъездных путей (Да/Нет)"])
                else None,
                railways_available=row["Наличие ж/д (Да/Нет)"] == "Да"
                if pd.notna(row["Наличие ж/д (Да/Нет)"])
                else None,
                truck_parking_available=row["Наличие парковки грузового транспорта"]
                == "Да"
                if pd.notna(row["Наличие парковки грузового транспорта"])
                else None,
                other_characteristics=row["Иные характеристики"]
                if pd.notna(row["Иные характеристики"])
                else None,
                application_procedure=row["Описание процедуры подачи заявки"]
                if pd.notna(row["Описание процедуры подачи заявки"])
                else None,
                required_documents=row[
                    "Перечень документов, необходимых для подачи заявки"
                ]
                if pd.notna(row["Перечень документов, необходимых для подачи заявки"])
                else None,
                application_form_link=row["Ссылка на форму подачи заявки"]
                if pd.notna(row["Ссылка на форму подачи заявки"])
                else None,
                possible_activities=row[
                    "Перечень видов экономической деятельности, возможных к реализации на площадке"
                ]
                if pd.notna(
                    row[
                        "Перечень видов экономической деятельности, возможных к реализации на площадке"
                    ]
                )
                else None,
                urban_planning_characteristics=row[
                    "Градостроительные характеристики и ограничения"
                ]
                if pd.notna(row["Градостроительные характеристики и ограничения"])
                else None,
                territorial_planning_documents=row[
                    "Документы территориального планирования"
                ]
                if pd.notna(row["Документы территориального планирования"])
                else None,
                other_information=row["Иные сведения"]
                if pd.notna(row["Иные сведения"])
                else None,
                maip_availability=row["Наличие МАИП"] == "Да"
                if pd.notna(row["Наличие МАИП"])
                else None,
                benefit_description=row["Описание льготы"]
                if pd.notna(row["Описание льготы"])
                else None,
                coordinates_lat=(
                    safe_float(row["Координаты (точка)"].split(",")[1].strip())
                    if pd.notna(row["Координаты (точка)"])
                    and "," in row["Координаты (точка)"]
                    else None
                ),
                coordinates_lon=(
                    safe_float(row["Координаты (точка)"].split(",")[0].strip())
                    if pd.notna(row["Координаты (точка)"])
                    and "," in row["Координаты (точка)"]
                    else None
                ),
            )
            building.save()
