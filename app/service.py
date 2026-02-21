from __future__ import annotations

from app.calculations import (
    calculate_ausgezaehlte_bareinnahmen,
    calculate_barentnahmen_summe,
    calculate_geld_in_umschlag,
    calculate_stueckelung,
    calculate_tip_distribution,
    calculate_total,
    calculate_trinkgeld_gesamt,
)
from app.models import AppConfig, CashFields
from app.parsing import format_euro


def _apply_alias_updates(fields: CashFields, updates: dict[str, str]) -> CashFields:
    data = fields.model_dump(by_alias=True)
    data.update(updates)
    return CashFields.model_validate(data)


def apply_calculation_pipeline(fields: CashFields, config: AppConfig) -> CashFields:
    updated_fields = fields.model_copy(deep=True)

    stueckelung_updates, _ = calculate_stueckelung(updated_fields, config.denominations)
    updated_fields = _apply_alias_updates(updated_fields, stueckelung_updates)

    barentnahmen_summe = calculate_barentnahmen_summe(updated_fields.barentnahmen_list)
    updated_fields = _apply_alias_updates(
        updated_fields, {"barentnahmenSumme": "= " + format_euro(barentnahmen_summe)}
    )

    ausgezaehlte = calculate_ausgezaehlte_bareinnahmen(
        geld_in_kasse=updated_fields.geld_in_kasse,
        barentnahmen_summe=barentnahmen_summe,
        wechselgeld_tagesanfang=config.wechselgeld_tagesanfang,
    )
    updated_fields = _apply_alias_updates(
        updated_fields, {"ausgezaehlteBareinnahmen": format_euro(ausgezaehlte)}
    )

    total = calculate_total(
        tagesumsatz_zb=updated_fields.tagesumsatz_zb,
        gutschein_bezahlt=updated_fields.gutschein_bezahlt,
    )
    updated_fields = _apply_alias_updates(updated_fields, {"total": format_euro(total)})

    trinkgeld_gesamt = calculate_trinkgeld_gesamt(
        ausgezaehlte_bareinnahmen=ausgezaehlte,
        barein_zb=updated_fields.barein_zb,
        ectrink_zb=updated_fields.ectrink_zb,
    )
    updated_fields = _apply_alias_updates(
        updated_fields, {"trinkgeldGesamt": format_euro(trinkgeld_gesamt)}
    )

    geld_umschlag = calculate_geld_in_umschlag(
        barein_zb=updated_fields.barein_zb,
        ectrink_zb=updated_fields.ectrink_zb,
        barentnahmen_summe=barentnahmen_summe,
    )
    updated_fields = _apply_alias_updates(
        updated_fields, {"geldInUmschlag": format_euro(geld_umschlag)}
    )

    tips = calculate_tip_distribution(updated_fields, trinkgeld_gesamt)
    updated_fields = _apply_alias_updates(updated_fields, tips.model_dump())

    return updated_fields
