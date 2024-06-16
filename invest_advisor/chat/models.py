import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Technopark(models.Model):
    type = models.CharField(
        max_length=500, verbose_name=_("Категория объекта"), null=True
    )
    oez = models.CharField(
        max_length=500, verbose_name=_("Объект особого назначения"), null=True
    )
    name = models.CharField(
        max_length=500,
        verbose_name=_("Наименование объекта"),
        null=True,
    )
    region = models.CharField(max_length=500, verbose_name=_("Регион"), null=True)
    region_object = models.CharField(
        max_length=500, verbose_name=_("Муниципальное образование"), null=True
    )
    nearest_region = models.CharField(
        max_length=500, verbose_name=_("Ближайший регион"), null=True
    )
    num_residents = models.IntegerField(
        verbose_name=_("Количество резидентов"), null=True
    )
    object_photos = models.TextField(verbose_name=_("Фотографии объекта"), null=True)
    documents = models.TextField(verbose_name=_("Документы"), null=True)
    year_of_object_forming = models.IntegerField(
        verbose_name=_("Год формирования объекта"), null=True
    )
    year_of_object_destroy = models.IntegerField(
        verbose_name=_("Срок действия объекта, лет"), null=True
    )
    total_square = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Общая площадь, кв. м"),
        null=True,
    )
    minimal_cost_of_buy = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальная стоимость аренды, руб./кв.м/год"),
        null=True,
    )
    ability_to_buy = models.BooleanField(
        verbose_name=_("Возможность выкупа помещения / участка (да / нет)"), null=True
    )
    list_of_activities = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Перечень видов деятельности"),
        null=True,
    )
    restrictions = models.TextField(
        verbose_name=_("Ограничения по видам деятельности"), null=True
    )
    infrastructure = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Инфраструктура и сервисы"),
        null=True,
    )
    additional_infra = models.TextField(
        verbose_name=_("Дополнительные услуги управляющей компании"), null=True
    )
    name_of_administration_object = models.CharField(
        max_length=500, verbose_name=_("Название администратора объекта"), null=True
    )
    address_administration_object = models.CharField(
        max_length=500, verbose_name=_("Адрес администратора объекта"), null=True
    )
    link = models.URLField(verbose_name=_("Ссылка на сайт"), null=True)
    work_time = models.CharField(
        max_length=100, verbose_name=_("Время работы"), null=True
    )
    tax_income = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Налог на прибыль"), null=True
    )
    tax_estate = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Налог на имущество"), null=True
    )
    tax_ground = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Земельный налог"), null=True
    )
    tax_transport = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Транспортный налог"), null=True
    )
    insurance_premiums = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name=_("Страховые взносы"), null=True
    )
    another_benefits = models.TextField(verbose_name=_("Прочие льготы"), null=True)
    free_custom_zone = models.BooleanField(
        verbose_name=_("Наличие режима свободной таможенной зоны (да/нет), условия"),
        null=True,
    )
    how_to_become_resident = models.TextField(verbose_name=_("Как стать резидентом"))
    minimal_investment_volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальный объём инвестиций, млн руб"),
        null=True,
    )
    coords_lat = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Координаты: широта"), null=True
    )
    coords_lon = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Координаты: долгота"), null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Технопарк")
        verbose_name_plural = _("Технопарки")


class TechnoparkSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="technopark_submissions",
        null=True,
    )
    name = models.CharField(
        max_length=500, verbose_name=_("Имя чата"), default="Новый чат"
    )
    state = models.IntegerField(default=0)

    region = models.CharField(
        max_length=500, verbose_name=_("Регион"), null=True, blank=True
    )

    # num_residents
    min_num_residents = models.IntegerField(
        verbose_name=_("Минимальное количество резидентов"), null=True, blank=True
    )
    max_num_residents = models.IntegerField(
        verbose_name=_("Максимальное количество резидентов"), null=True, blank=True
    )

    # year_of_object_forming
    min_year_of_object_forming = models.IntegerField(
        verbose_name=_("Минимальный год формирования объекта"), null=True, blank=True
    )
    max_year_of_object_forming = models.IntegerField(
        verbose_name=_("Максимальный год формирования объекта"), null=True, blank=True
    )

    # total_square
    min_total_square = models.IntegerField(
        verbose_name=_("Минимальная общая площадь, кв. м"), null=True, blank=True
    )
    max_total_square = models.IntegerField(
        verbose_name=_("Максимальная общая площадь, кв. м"), null=True, blank=True
    )

    # minimal_cost_of_buy
    min_minimal_cost_of_buy = models.IntegerField(
        verbose_name=_("Минимальная стоимость аренды, руб./кв.м/год"),
        null=True,
        blank=True,
    )
    max_minimal_cost_of_buy = models.IntegerField(
        verbose_name=_("Максимальная стоимость аренды, руб./кв.м/год"),
        null=True,
        blank=True,
    )

    list_of_activities = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Перечень видов деятельности"),
        null=True,
    )

    infrastructure = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Инфраструктура и сервисы"),
        null=True,
    )

    # tax_income
    min_tax_income = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Минимальный налог на прибыль"),
        null=True,
        blank=True,
    )
    max_tax_income = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Максимальный налог на прибыль"),
        null=True,
        blank=True,
    )

    # tax_estate
    min_tax_estate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Минимальный налог на имущество"),
        null=True,
        blank=True,
    )
    max_tax_estate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Максимальный налог на имущество"),
        null=True,
        blank=True,
    )

    # tax_ground
    min_tax_ground = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Минимальный земельный налог"),
        null=True,
        blank=True,
    )
    max_tax_ground = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Максимальный земельный налог"),
        null=True,
        blank=True,
    )

    # tax_transport
    min_tax_transport = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Минимальный транспортный налог"),
        null=True,
        blank=True,
    )
    max_tax_transport = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Максимальный транспортный налог"),
        null=True,
        blank=True,
    )

    # insurance_premiums
    min_insurance_premiums = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Минимальные страховые взносы"),
        null=True,
        blank=True,
    )
    max_insurance_premiums = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Максимальные страховые взносы"),
        null=True,
        blank=True,
    )

    free_custom_zone = models.BooleanField(
        verbose_name=_("Наличие режима свободной таможенной зоны"),
        null=True,
        blank=True,
    )

    # minimal_investment_volume
    min_minimal_investment_volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальный объем инвестиций, млн руб"),
        null=True,
        blank=True,
    )
    max_minimal_investment_volume = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Максимальный объем инвестиций, млн руб"),
        null=True,
        blank=True,
    )

    additional_preferences = models.TextField(
        verbose_name=_("Дополнительные предпочтения"), null=True, blank=True
    )

    ml_data = models.JSONField(verbose_name=_("Данные от ML"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Заявка на технопарк")
        verbose_name_plural = _("Заявки на технопарк")


class BuildingModel(models.Model):
    name = models.CharField(
        max_length=500, verbose_name=_("Название площадки"), null=True
    )
    pref_treatment = models.CharField(
        max_length=500, verbose_name=_("Преференциальный режим"), null=True
    )
    pref_object = models.CharField(
        max_length=500,
        verbose_name=_("Наименование объекта преференциального режима"),
        null=True,
    )
    pref_object_name = models.CharField(
        max_length=500,
        verbose_name=_("Наименование объекта преференциального режима_наименование"),
        null=True,
    )
    support_infra_object = models.CharField(
        max_length=500, verbose_name=_("Объект инфраструктуры поддержки"), null=True
    )
    support_name = models.CharField(
        max_length=500,
        verbose_name=_("Наименование объекта инфраструктуры поддержки"),
        null=True,
    )
    support_name_detail = models.CharField(
        max_length=500,
        verbose_name=_("Наименование объекта инфраструктуры поддержки_наименование"),
        null=True,
    )
    region = models.CharField(max_length=500, verbose_name=_("Регион"), null=True)
    municipal_entity = models.CharField(
        max_length=500, verbose_name=_("Муниципальное образование"), null=True
    )
    address = models.CharField(
        max_length=500, verbose_name=_("Адрес объекта"), null=True
    )
    nearest_city = models.CharField(
        max_length=500, verbose_name=_("Ближайший город"), null=True
    )
    site_format = ArrayField(
        models.CharField(max_length=500), verbose_name=_("Формат площадки"), null=True
    )
    site_type = ArrayField(
        models.CharField(max_length=500), verbose_name=_("Тип площадки"), null=True
    )
    ownership_form = models.CharField(
        max_length=500, verbose_name=_("Форма собственности объекта"), null=True
    )
    transaction_form = ArrayField(
        models.CharField(max_length=500), verbose_name=_("Форма сделки"), null=True
    )
    cost_object = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Стоимость объекта, руб. (покупки или месячной аренды)"),
        null=True,
    )
    cost_per_year_ha = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Стоимость, руб./год за га"),
        null=True,
    )
    cost_per_year_sqm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Стоимость, руб./год за кв.м."),
        null=True,
    )
    lease_term_min = models.IntegerField(
        verbose_name=_("min сроки аренды (если применимо), лет"), null=True, blank=True
    )
    lease_term_max = models.IntegerField(
        verbose_name=_("max сроки аренды (если применимо), лет"), null=True, blank=True
    )
    cost_determination_order = models.CharField(
        max_length=500, verbose_name=_("Порядок определения стоимости"), null=True
    )
    hazard_class = models.CharField(
        max_length=500, verbose_name=_("Класс опасности объекта"), null=True
    )
    building_characteristics = models.TextField(
        verbose_name=_(
            "Характеристики расположенных объектов капитального строительства"
        ),
        null=True,
    )
    free_land_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Свободная площадь ЗУ, га"),
        null=True,
    )
    cadastral_number_land = models.CharField(
        max_length=500, verbose_name=_("Кадастровый номер ЗУ"), null=True
    )
    permitted_use_options = models.TextField(
        verbose_name=_("Варианты разрешенного использования"), null=True
    )
    land_surveying = models.BooleanField(verbose_name=_("Межевание ЗУ"), null=True)
    land_category = models.CharField(
        max_length=500, verbose_name=_("Категория земель"), null=True
    )
    free_building_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Свободная площадь здания, сооружения, помещения, кв. м"),
        null=True,
    )
    cadastral_number_building = models.CharField(
        max_length=500,
        verbose_name=_("Кадастровый номер здания, сооружения, помещения"),
        null=True,
    )
    building_technical_characteristics = models.TextField(
        verbose_name=_("Технические характеристики здания, сооружения, помещения"),
        null=True,
    )
    owner_name = models.CharField(
        max_length=500,
        verbose_name=_("Наименование собственника / администратора объекта"),
        null=True,
    )
    owner_inn = models.CharField(
        max_length=20, verbose_name=_("ИНН собственника"), null=True
    )
    website = models.URLField(verbose_name=_("Сайт"), null=True, max_length=500)
    note = models.TextField(verbose_name=_("Примечание"), null=True)
    water_supply_available = models.BooleanField(
        verbose_name=_("Водоснабжение Наличие (Да/Нет)"), null=True
    )
    water_supply_rate_consumption_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоснабжение Тариф на потребление, минимальный, руб./куб. м"),
        null=True,
    )
    water_supply_rate_consumption_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоснабжение Тариф на потребление, максимальный, руб./куб. м"),
        null=True,
    )
    water_supply_rate_transport_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Водоснабжение Тариф на транспортировку, минимальный, руб./куб. м"
        ),
        null=True,
    )
    water_supply_rate_transport_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Водоснабжение Тариф на транспортировку, максимальный, руб./куб. м"
        ),
        null=True,
    )
    water_supply_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Объекты водоснабжения Максимально допустимая мощность, куб. м/ч"
        ),
        null=True,
    )
    water_supply_objects_free_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Объекты водоснабжения Свободная мощность, куб.м/ч"),
        null=True,
    )
    water_supply_other_characteristics = models.TextField(
        verbose_name=_("Объекты водоснабжения Иные характеристики"), null=True
    )
    water_network_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сети водоснабжения Пропускная способность, куб. м/ч"),
        null=True,
    )
    sewage_available = models.BooleanField(
        verbose_name=_("Водоотведение Наличие (Да/Нет)"), null=True
    )
    sewage_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоотведение Тариф на потребление, руб./куб. м"),
        null=True,
    )
    sewage_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоотведение Тариф на транспортировку, руб./куб. м"),
        null=True,
    )
    sewage_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Объекты водоотведения Максимально допустимая мощность, куб. м/ч"
        ),
        null=True,
    )
    sewage_objects_free_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Объекты водоотведения Свободная мощность, куб. м/ч"),
        null=True,
    )
    sewage_other_characteristics = models.TextField(
        verbose_name=_("Объекты водоотведения Иные характеристики"), null=True
    )
    sewage_network_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сети водоотведения Пропускная способность, куб. м/ч"),
        null=True,
    )
    gas_supply_available = models.BooleanField(
        verbose_name=_("Газоснабжение Наличие (Да/Нет)"), null=True
    )
    gas_supply_rate_consumption_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на потребление, минимальный, руб./куб. м"),
        null=True,
    )
    gas_supply_rate_consumption_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на потребление, максимальный, руб./куб. м"),
        null=True,
    )
    gas_supply_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на транспортировку, руб./куб. м"),
        null=True,
    )
    gas_supply_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Объекты газоснабжения Максимально допустимая мощность, куб. м/ч"
        ),
        null=True,
    )
    gas_supply_objects_free_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Объекты газоснабжения Свободная мощность, куб. м/ч"),
        null=True,
    )
    gas_supply_other_characteristics = models.TextField(
        verbose_name=_("Объекты газоснабжения Иные характеристики"), null=True
    )
    gas_network_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сети газоснабжения Пропускная способность, куб. м/ч"),
        null=True,
    )
    electricity_supply_available = models.BooleanField(
        verbose_name=_("Электроснабжение Наличие (Да/Нет)"), null=True
    )
    electricity_rate_consumption_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Электроснабжение Тариф на потребление, минимальный, руб./КВт*ч"
        ),
        null=True,
    )
    electricity_rate_consumption_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Электроснабжение Тариф на потребление, максимальный, руб./КВт*ч"
        ),
        null=True,
    )
    electricity_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Электроснабжение Тариф на транспортировку, руб./МВтч"),
        null=True,
    )
    electricity_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Объекты электроснабжения Максимально допустимая мощность, МВт/ч"
        ),
        null=True,
    )
    electricity_objects_free_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Объекты электроснабжения Свободная мощность, МВт/ч"),
        null=True,
    )
    electricity_other_characteristics = models.TextField(
        verbose_name=_("Объекты электроснабжения Иные характеристики"), null=True
    )
    electricity_network_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сети электроснабжения Пропускная способность, МВт/ч"),
        null=True,
    )
    heating_available = models.BooleanField(
        verbose_name=_("Теплоснабжение Наличие (Да/Нет)"), null=True
    )
    heating_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Теплоснабжение Тариф на потребление, руб./Гкалч"),
        null=True,
    )
    heating_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Теплоснабжение Тариф на транспортировку, руб./Гкал*ч"),
        null=True,
    )
    heating_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Объекты теплоснабжения Максимально допустимая мощность, Гкал/ч"
        ),
        null=True,
    )

    heating_objects_free_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Объекты теплоснабжения Свободная мощность, Гкал/ч"),
        null=True,
    )
    heating_other_characteristics = models.TextField(
        verbose_name=_("Объекты теплоснабжения Иные характеристики"), null=True
    )
    heating_network_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Сети теплоснабжения Пропускная способность, Гкал/ч"),
        null=True,
    )
    waste_disposal_available = models.BooleanField(
        verbose_name=_("Вывоз ТКО Наличие (Да/Нет)"), null=True
    )
    waste_disposal_rate_ton = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Вывоз ТКО Тариф, руб./тонна"),
        null=True,
    )
    waste_disposal_rate_cubic_meter = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Вывоз ТКО Тариф, руб./куб. м"),
        null=True,
    )
    access_roads_available = models.BooleanField(
        verbose_name=_("Наличие подъездных путей (Да/Нет)"), null=True
    )
    railways_available = models.BooleanField(
        verbose_name=_("Наличие ж/д (Да/Нет)"), null=True
    )
    truck_parking_available = models.BooleanField(
        verbose_name=_("Наличие парковки грузового транспорта"), null=True
    )
    other_characteristics = models.TextField(
        verbose_name=_("Иные характеристики"), null=True
    )
    application_procedure = models.TextField(
        verbose_name=_("Описание процедуры подачи заявки"), null=True
    )
    required_documents = models.TextField(
        verbose_name=_("Перечень документов, необходимых для подачи заявки"), null=True
    )
    application_form_link = models.URLField(
        verbose_name=_("Ссылка на форму подачи заявки"), null=True
    )
    possible_activities = models.TextField(
        verbose_name=_(
            "Перечень видов экономической деятельности, возможных к реализации на площадке"
        ),
        null=True,
    )
    urban_planning_characteristics = models.TextField(
        verbose_name=_("Градостроительные характеристики и ограничения"), null=True
    )
    territorial_planning_documents = models.TextField(
        verbose_name=_("Документы территориального планирования"), null=True
    )
    other_information = models.TextField(verbose_name=_("Иные сведения"), null=True)
    maip_availability = models.BooleanField(verbose_name=_("Наличие МАИП"), null=True)
    benefit_description = models.TextField(verbose_name=_("Описание льготы"), null=True)
    coordinates_lat = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Координаты: широта"), null=True
    )
    coordinates_lon = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name=_("Координаты: долгота"), null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Объект недвижимости")
        verbose_name_plural = _("Объекты недвижимости")


class BuildingSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="building_submissions",
        null=True,
    )
    name = models.CharField(
        max_length=500, verbose_name=_("Имя чата"), default="Новый чат"
    )
    state = models.IntegerField(default=0)

    pref_treatment = models.CharField(
        verbose_name=_("Преференциальный режим"), null=True, blank=True
    )

    region = models.CharField(
        max_length=500, verbose_name=_("Регион"), null=True, blank=True
    )

    site_format = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Формат площадки"),
        null=True,
    )

    site_type = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Тип площадки"),
        null=True,
    )

    transaction_form = ArrayField(
        models.CharField(max_length=500),
        verbose_name=_("Форма сделки"),
        null=True,
    )

    min_cost_object = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальная стоимость объекта, руб."),
        null=True,
        blank=True,
    )
    max_cost_object = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Максимальная стоимость объекта, руб."),
        null=True,
        blank=True,
    )

    water_supply_available = models.BooleanField(
        verbose_name=_("Водоснабжение Наличие"), null=True, blank=True
    )
    min_water_supply_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоснабжение Тариф на потребление, минимальный, руб./куб. м"),
        null=True,
    )
    max_water_supply_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Водоснабжение Тариф на потребление, максимальный, руб./куб. м"),
        null=True,
    )

    min_water_supply_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Минимальный тариф на транспортировку водоснабжения, руб./куб. м"
        ),
        null=True,
        blank=True,
    )
    max_water_supply_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Максимальный тариф на транспортировку водоснабжения, руб./куб. м"
        ),
        null=True,
        blank=True,
    )
    min_water_supply_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Минимальная максимально допустимая мощность объектов водоснабжения, куб. м/ч"
        ),
        null=True,
        blank=True,
    )
    max_water_supply_objects_max_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Максимальная максимально допустимая мощность объектов водоснабжения, куб. м/ч"
        ),
        null=True,
        blank=True,
    )

    gas_supply_available = models.BooleanField(
        verbose_name=_("Газоснабжение Наличие"), null=True, blank=True
    )
    gas_supply_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на потребление, руб./куб. м"),
        null=True,
    )
    gas_supply_rate_consumption_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на потребление, минимальный, руб./куб. м"),
        null=True,
    )
    gas_supply_rate_consumption_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Газоснабжение Тариф на потребление, максимальный, руб./куб. м"),
        null=True,
    )
    min_gas_supply_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Минимальный тариф на транспортировку газоснабжения, руб./куб. м"
        ),
        null=True,
        blank=True,
    )
    max_gas_supply_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Максимальный тариф на транспортировку газоснабжения, руб./куб. м"
        ),
        null=True,
        blank=True,
    )

    electricity_supply_available = models.BooleanField(
        verbose_name=_("Электроснабжение Наличие"), null=True, blank=True
    )
    min_electricity_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальный тариф на потребление электроснабжения, руб./МВтч"),
        null=True,
        blank=True,
    )
    max_electricity_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Максимальный тариф на потребление электроснабжения, руб./МВтч"),
        null=True,
        blank=True,
    )
    min_electricity_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Минимальный тариф на транспортировку электроснабжения, руб./МВтч"
        ),
        null=True,
        blank=True,
    )
    max_electricity_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Максимальный тариф на транспортировку электроснабжения, руб./МВтч"
        ),
        null=True,
        blank=True,
    )

    heating_available = models.BooleanField(
        verbose_name=_("Теплоснабжение Наличие"), null=True, blank=True
    )
    min_heating_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальный тариф на потребление теплоснабжения, руб./Гкалч"),
        null=True,
        blank=True,
    )
    max_heating_rate_consumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Максимальный тариф на потребление теплоснабжения, руб./Гкалч"),
        null=True,
        blank=True,
    )
    min_heating_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Минимальный тариф на транспортировку теплоснабжения, руб./Гкалч"
        ),
        null=True,
        blank=True,
    )
    max_heating_rate_transport = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_(
            "Максимальный тариф на транспортировку теплоснабжения, руб./Гкалч"
        ),
        null=True,
        blank=True,
    )

    waste_disposal_available = models.BooleanField(
        verbose_name=_("Вывоз ТКО Наличие"), null=True, blank=True
    )
    min_waste_disposal_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Минимальный тариф на вывоз ТКО"),
        null=True,
        blank=True,
    )
    max_waste_disposal_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Максимальный тариф на вывоз ТКО"),
        null=True,
        blank=True,
    )

    access_roads_available = models.BooleanField(
        verbose_name=_("Наличие подъездных путей"), null=True, blank=True
    )
    railways_available = models.BooleanField(
        verbose_name=_("Наличие ж/д"), null=True, blank=True
    )
    truck_parking_available = models.BooleanField(
        verbose_name=_("Наличие парковки грузового транспорта"), null=True, blank=True
    )

    additional_comments = models.TextField(
        verbose_name=_("Дополнительные комментарии"), null=True, blank=True
    )

    ml_data = models.JSONField(verbose_name=_("Данные от ML"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Заявка на подбор здания")
        verbose_name_plural = _("Заявки на подбор здания")


class Chat(models.Model):
    type = models.CharField(
        choices=[
            ("technopark", _("Технопарк")),
            ("building", _("Объект недвижимости")),
        ],
        max_length=20,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=500, verbose_name=_("Имя чата"), default="Новый чат"
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name=_("Пользователь"),
        related_name="chats",
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        "Chat",
        on_delete=models.CASCADE,
        verbose_name=_("Чат"),
        related_name="messages",
        null=True,
    )
    from_user = models.BooleanField(verbose_name=_("Отправитель - пользователь"))
    file = models.FileField(
        upload_to="chat_files", verbose_name=_("Файл"), null=True, blank=True
    )
    data = models.JSONField(verbose_name=_("Данные"), null=True, blank=True)
    text = models.TextField(verbose_name=_("Текст сообщения"))
    created = models.DateTimeField(auto_now_add=True)
