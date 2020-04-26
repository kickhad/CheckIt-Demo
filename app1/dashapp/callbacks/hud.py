from app1.dicts import PCTR_ID__PCTR_TEXT


def get_hud_title(cache, pctr_id=None, eanupc=None):
    if pctr_id:
        return cache.get(PCTR_ID__PCTR_TEXT)[pctr_id]
        # if eanupc:


"""""""""""""""""


better filter for label from id




"""""""""""""""""
