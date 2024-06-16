import tempfile
from ast import literal_eval

import markdown
import pdfkit
from django.core.files import File
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from invest_advisor.chat.models import BuildingModel, Technopark


def filter_technoparks(submission):
    technoparks = Technopark.objects.all()

    if submission.region:
        technoparks = technoparks.filter(region=submission.region)

    if submission.min_num_residents is not None:
        technoparks = technoparks.filter(
            num_residents__gte=submission.min_num_residents
        )
    if submission.max_num_residents is not None:
        technoparks = technoparks.filter(
            num_residents__lte=submission.max_num_residents
        )

    if submission.min_year_of_object_forming is not None:
        technoparks = technoparks.filter(
            year_of_object_forming__gte=submission.min_year_of_object_forming
        )
    if submission.max_year_of_object_forming is not None:
        technoparks = technoparks.filter(
            year_of_object_forming__lte=submission.max_year_of_object_forming
        )

    if submission.min_total_square is not None:
        technoparks = technoparks.filter(total_square__gte=submission.min_total_square)
    if submission.max_total_square is not None:
        technoparks = technoparks.filter(total_square__lte=submission.max_total_square)

    if submission.min_minimal_cost_of_buy is not None:
        technoparks = technoparks.filter(
            minimal_cost_of_buy__gte=submission.min_minimal_cost_of_buy
        )
    if submission.max_minimal_cost_of_buy is not None:
        technoparks = technoparks.filter(
            minimal_cost_of_buy__lte=submission.max_minimal_cost_of_buy
        )

    if submission.list_of_activities:
        technoparks = technoparks.filter(
            list_of_activities__overlap=submission.list_of_activities
        )

    if submission.infrastructure:
        technoparks = technoparks.filter(
            infrastructure__overlap=submission.infrastructure
        )

    if submission.min_tax_income is not None:
        technoparks = technoparks.filter(tax_income__gte=submission.min_tax_income)
    if submission.max_tax_income is not None:
        technoparks = technoparks.filter(tax_income__lte=submission.max_tax_income)

    if submission.min_tax_estate is not None:
        technoparks = technoparks.filter(tax_estate__gte=submission.min_tax_estate)
    if submission.max_tax_estate is not None:
        technoparks = technoparks.filter(tax_estate__lte=submission.max_tax_estate)

    if submission.min_tax_ground is not None:
        technoparks = technoparks.filter(tax_ground__gte=submission.min_tax_ground)
    if submission.max_tax_ground is not None:
        technoparks = technoparks.filter(tax_ground__lte=submission.max_tax_ground)

    if submission.min_tax_transport is not None:
        technoparks = technoparks.filter(
            tax_transport__gte=submission.min_tax_transport
        )
    if submission.max_tax_transport is not None:
        technoparks = technoparks.filter(
            tax_transport__lte=submission.max_tax_transport
        )

    if submission.min_insurance_premiums is not None:
        technoparks = technoparks.filter(
            insurance_premiums__gte=submission.min_insurance_premiums
        )
    if submission.max_insurance_premiums is not None:
        technoparks = technoparks.filter(
            insurance_premiums__lte=submission.max_insurance_premiums
        )

    if submission.free_custom_zone is not None:
        technoparks = technoparks.filter(free_custom_zone=submission.free_custom_zone)

    if submission.min_minimal_investment_volume is not None:
        technoparks = technoparks.filter(
            minimal_investment_volume__gte=submission.min_minimal_investment_volume
        )
    if submission.max_minimal_investment_volume is not None:
        technoparks = technoparks.filter(
            minimal_investment_volume__lte=submission.max_minimal_investment_volume
        )

    return technoparks


def get_options_for_technopark_question(question_number, technoparks):
    question_field_mapping = {
        1: {"field": "region", "type": "string"},
        2: {"field": ["num_residents"], "type": "range"},
        3: {"field": ["year_of_object_forming"], "type": "range"},
        4: {"field": ["total_square"], "type": "range"},
        5: {"field": ["minimal_cost_of_buy"], "type": "range"},
        6: {"field": "list_of_activities", "type": "array"},
        7: {"field": "infrastructure", "type": "array"},
        8: {"field": ["tax_income"], "type": "range"},
        9: {"field": ["tax_estate"], "type": "range"},
        10: {"field": ["tax_ground"], "type": "range"},
        11: {"field": ["tax_transport"], "type": "range"},
        12: {"field": ["insurance_premiums"], "type": "range"},
        13: {"field": "free_custom_zone", "type": "boolean"},
        14: {"field": ["minimal_investment_volume"], "type": "range"},
    }
    if question_number > 14:
        return None, None
    field_info = question_field_mapping[question_number]
    fields = field_info["field"]
    field_type = field_info["type"]
    next_question = question_number + 1 if technoparks.count() != 0 else None

    if field_type == "range":
        min_field, max_field = fields[0], fields[0]
        min_value = technoparks.exclude(**{f"{min_field}__isnull": True}).aggregate(
            models.Min(min_field)
        )[f"{min_field}__min"]
        max_value = technoparks.exclude(**{f"{max_field}__isnull": True}).aggregate(
            models.Max(max_field)
        )[f"{max_field}__max"]
        return (min_value, max_value), next_question

    if field_type == "array":
        options = (
            technoparks.values_list(fields, flat=True)
            .distinct()
            .exclude(**{f"{fields}__isnull": True})
        )
        unique_options = set()
        for option in options:
            unique_options.update(option)
        return list(unique_options), next_question

    if field_type == "boolean":
        return (
            technoparks.values_list(fields, flat=True)
            .distinct()
            .exclude(**{f"{fields}__isnull": True}),
            next_question,
        )

    return (
        technoparks.values_list(fields, flat=True)
        .distinct()
        .exclude(**{f"{fields}__isnull": True}),
        next_question,
    )


def filter_buildings(submission):
    buildings = BuildingModel.objects.all()

    if submission.pref_treatment is not None:
        buildings = buildings.filter(pref_treatment=submission.pref_treatment)

    if submission.region:
        buildings = buildings.filter(region=submission.region)

    if submission.site_format:
        buildings = buildings.filter(site_format__overlap=submission.site_format)

    if submission.site_type:
        buildings = buildings.filter(site_type__overlap=submission.site_type)

    if submission.transaction_form:
        buildings = buildings.filter(
            transaction_form__overlap=submission.transaction_form
        )

    if submission.min_cost_object is not None:
        buildings = buildings.filter(cost_object__gte=submission.min_cost_object)
    if submission.max_cost_object is not None:
        buildings = buildings.filter(cost_object__lte=submission.max_cost_object)

    if submission.water_supply_available is not None:
        buildings = buildings.filter(
            water_supply_available=submission.water_supply_available
        )
    if submission.water_supply_available:
        if (
            submission.min_water_supply_rate_consumption is not None
            and submission.max_water_supply_rate_consumption is not None
        ):
            buildings = buildings.filter(
                Q(
                    water_supply_rate_consumption_min__gte=submission.min_water_supply_rate_consumption
                )
                & Q(
                    water_supply_rate_consumption_max__lte=submission.max_water_supply_rate_consumption
                )
            )
        if (
            submission.min_water_supply_objects_max_capacity is not None
            and submission.max_water_supply_objects_max_capacity is not None
        ):
            buildings = buildings.filter(
                Q(
                    water_supply_objects_max_capacity__gte=submission.min_water_supply_objects_max_capacity
                )
                & Q(
                    water_supply_objects_max_capacity__lte=submission.max_water_supply_objects_max_capacity
                )
            )

    if submission.gas_supply_available is not None:
        buildings = buildings.filter(
            gas_supply_available=submission.gas_supply_available
        )
    if submission.gas_supply_available:
        if submission.gas_supply_rate_consumption is not None:
            buildings = buildings.filter(
                Q(
                    gas_supply_rate_consumption_min__lte=submission.gas_supply_rate_consumption
                )
                & Q(
                    gas_supply_rate_consumption_max__gte=submission.gas_supply_rate_consumption
                )
            )
        if (
            submission.min_gas_supply_rate_transport is not None
            and submission.max_gas_supply_rate_transport is not None
        ):
            buildings = buildings.filter(
                Q(
                    gas_supply_rate_transport__gte=submission.min_gas_supply_rate_transport
                )
                & Q(
                    gas_supply_rate_transport__lte=submission.max_gas_supply_rate_transport
                )
            )

    if submission.electricity_supply_available is not None:
        buildings = buildings.filter(
            electricity_supply_available=submission.electricity_supply_available
        )
    if submission.electricity_supply_available:
        if (
            submission.min_electricity_rate_consumption is not None
            and submission.max_electricity_rate_consumption is not None
        ):
            buildings = buildings.filter(
                Q(
                    electricity_rate_consumption_min__gte=submission.min_electricity_rate_consumption
                )
                & Q(
                    electricity_rate_consumption_max__lte=submission.max_electricity_rate_consumption
                )
            )
        if (
            submission.min_electricity_rate_transport is not None
            and submission.max_electricity_rate_transport is not None
        ):
            buildings = buildings.filter(
                Q(
                    electricity_rate_transport__gte=submission.min_electricity_rate_transport
                )
                & Q(
                    electricity_rate_transport__lte=submission.max_electricity_rate_transport
                )
            )

    if submission.heating_available is not None:
        buildings = buildings.filter(heating_available=submission.heating_available)
    if submission.heating_available:
        if (
            submission.min_heating_rate_consumption is not None
            and submission.max_heating_rate_consumption is not None
        ):
            buildings = buildings.filter(
                Q(heating_rate_consumption__gte=submission.min_heating_rate_consumption)
                & Q(
                    heating_rate_consumption__lte=submission.max_heating_rate_consumption
                )
            )
        if (
            submission.min_heating_rate_transport is not None
            and submission.max_heating_rate_transport is not None
        ):
            buildings = buildings.filter(
                Q(heating_rate_transport__gte=submission.min_heating_rate_transport)
                & Q(heating_rate_transport__lte=submission.max_heating_rate_transport)
            )

    if submission.waste_disposal_available is not None:
        buildings = buildings.filter(
            waste_disposal_available=submission.waste_disposal_available
        )

    if submission.access_roads_available is not None:
        buildings = buildings.filter(
            access_roads_available=submission.access_roads_available
        )
    if submission.railways_available is not None:
        buildings = buildings.filter(railways_available=submission.railways_available)
    if submission.truck_parking_available is not None:
        buildings = buildings.filter(
            truck_parking_available=submission.truck_parking_available
        )

    return buildings


def get_options_for_building_question(question_number, buildings, submission):
    question_field_mapping = {
        1: {"field": "pref_treatment", "type": "boolean", "next": 2},
        2: {"field": "region", "type": "string", "next": 3},
        3: {"field": "site_format", "type": "array", "next": 4},
        4: {"field": "site_type", "type": "array", "next": 5},
        5: {"field": "transaction_form", "type": "array", "next": 6},
        6: {"field": "cost_object", "type": "range", "next": 7},
        7: {
            "field": "water_supply_available",
            "type": "boolean",
            "next": 8 if getattr(submission, "water_supply_available", None) else 10,
        },
        8: {
            "field": [
                "water_supply_rate_consumption_min",
                "water_supply_rate_consumption_max",
            ],
            "type": "range",
            "next": 9,
        },
        9: {
            "field": "water_supply_objects_max_capacity",
            "type": "range",
            "next": 10,
        },
        10: {
            "field": "gas_supply_available",
            "type": "boolean",
            "next": 11 if getattr(submission, "gas_supply_available", None) else 13,
        },
        11: {
            "field": [
                "gas_supply_rate_consumption_min",
                "gas_supply_rate_consumption_max",
            ],
            "type": "range",
            "next": 12,
        },
        12: {
            "field": "gas_supply_rate_transport",
            "type": "range",
            "next": 13,
        },
        13: {
            "field": "electricity_supply_available",
            "type": "boolean",
            "next": (
                14 if getattr(submission, "electricity_supply_available", None) else 16
            ),
        },
        14: {
            "field": [
                "electricity_rate_consumption_min",
                "electricity_rate_consumption_max",
            ],
            "type": "range",
            "next": 15,
        },
        15: {
            "field": "electricity_rate_transport",
            "type": "range",
            "next": 16,
        },
        16: {
            "field": "heating_available",
            "type": "boolean",
            "next": 17 if getattr(submission, "heating_available", None) else 19,
        },
        17: {
            "field": "heating_rate_consumption",
            "type": "range",
            "next": 18,
        },
        18: {
            "field": "heating_rate_transport",
            "type": "range",
            "next": 19,
        },
        19: {
            "field": "waste_disposal_available",
            "type": "boolean",
            "next": 20,
        },
        20: {"field": "access_roads_available", "type": "boolean", "next": 21},
        21: {"field": "railways_available", "type": "boolean", "next": 22},
        22: {"field": "truck_parking_available", "type": "boolean", "next": 23},
    }
    if question_number not in question_field_mapping:
        return None, None
    buildings_count = buildings.count()
    field_info = question_field_mapping[question_number]
    fields = field_info["field"]
    field_type = field_info["type"]
    next_question = field_info["next"]
    if buildings_count == 1:
        return None, None

    if field_type == "range":
        if isinstance(fields, list):
            min_field, max_field = fields
            min_value = buildings.exclude(**{f"{min_field}__isnull": True}).aggregate(
                models.Min(min_field)
            )[f"{min_field}__min"]
            max_value = buildings.exclude(**{f"{max_field}__isnull": True}).aggregate(
                models.Max(max_field)
            )[f"{max_field}__max"]
        else:
            min_value = buildings.exclude(**{f"{fields}__isnull": True}).aggregate(
                models.Min(fields)
            )[f"{fields}__min"]
            max_value = buildings.exclude(**{f"{fields}__isnull": True}).aggregate(
                models.Max(fields)
            )[f"{fields}__max"]
        return (min_value, max_value), next_question

    if field_type == "array":
        options = (
            buildings.values_list(fields, flat=True)
            .distinct()
            .exclude(**{f"{fields}__isnull": True})
        )
        unique_options = set()
        for option in options:
            unique_options.update(option)
        return list(unique_options), next_question

    if field_type == "boolean":
        return (
            buildings.values_list(fields, flat=True)
            .distinct()
            .exclude(**{f"{fields}__isnull": True}),
            next_question,
        )

    return (
        buildings.values_list(fields, flat=True)
        .distinct()
        .exclude(**{f"{fields}__isnull": True}),
        next_question,
    )


def clean_and_process_text(text):
    return literal_eval(text)


def generate_report_file(chat_message, support_text, advice_text):
    support_text = clean_and_process_text(support_text)
    advice_text = clean_and_process_text(advice_text)

    support_html = markdown.markdown(support_text, output_format="html")
    advice_html = markdown.markdown(advice_text, output_format="html")

    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h2>Меры поддержки</h2>
        {support_html}
        <h2>Советы по найму</h2>
        {advice_html}
    </body>
    </html>
    """

    options = {
        "page-size": "A4",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [],
        "no-outline": None,
    }

    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as output:
        pdfkit.from_string(html_content, output.name, options=options)
        with open(output.name, "rb") as f:
            chat_message.file.save(f"{chat_message.chat.id}_report.pdf", File(f))
        chat_message.save()
    return chat_message.file.path
