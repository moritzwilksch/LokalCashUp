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
from app.models import AppConfig, CashUpForm
from app.parsing import format_euro


def apply_calculation_pipeline(form: CashUpForm, config: AppConfig) -> CashUpForm:
    updated = form.model_copy(deep=True)

    calculate_stueckelung(updated, config.denominations)

    barentnahmen_summe = calculate_barentnahmen_summe(updated.barentnahmen_liste)
    updated.outputs.barentnahmen_summe = "= " + format_euro(barentnahmen_summe)

    ausgezaehlte_bareinnahmen = calculate_ausgezaehlte_bareinnahmen(
        geld_in_kasse=updated.outputs.geld_in_kasse,
        barentnahmen_summe=barentnahmen_summe,
        wechselgeld_tagesanfang=config.wechselgeld_tagesanfang,
    )
    updated.outputs.ausgezaehlte_bareinnahmen = format_euro(ausgezaehlte_bareinnahmen)

    total = calculate_total(
        tagesumsatz_zbon=updated.zbon.tagesumsatz_zbon,
        mit_gutschein_bezahlt=updated.zbon.mit_gutschein_bezahlt,
    )
    updated.outputs.total = format_euro(total)

    trinkgeld_gesamt = calculate_trinkgeld_gesamt(
        ausgezaehlte_bareinnahmen=ausgezaehlte_bareinnahmen,
        bargeld_zbon=updated.zbon.bargeld_zbon,
        ec_trinkgeld_zbon=updated.zbon.ec_trinkgeld_zbon,
    )
    updated.outputs.trinkgeld_gesamt = format_euro(trinkgeld_gesamt)

    geld_in_umschlag = calculate_geld_in_umschlag(
        bargeld_zbon=updated.zbon.bargeld_zbon,
        ec_trinkgeld_zbon=updated.zbon.ec_trinkgeld_zbon,
        barentnahmen_summe=barentnahmen_summe,
    )
    updated.outputs.geld_in_umschlag = format_euro(geld_in_umschlag)

    tip_distribution = calculate_tip_distribution(updated, trinkgeld_gesamt)
    for tip, tip_amount in zip(updated.tips, tip_distribution.values, strict=True):
        tip.tip_formatted = tip_amount

    return updated
