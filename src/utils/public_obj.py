from ..config.settings import ALL_CONFIG
from ..utils.filter_sdk import BWBandPassFilter, BWBandStopFilter

BP_FILTER = ALL_CONFIG["FILTER"]["bp"]
BS_FILTER = ALL_CONFIG["FILTER"]["bs"]


BP_FILTER_OBJ = BWBandPassFilter(order=BP_FILTER["order"],
                                 sample_rate=BP_FILTER["sample_rate"],
                                 fl=BP_FILTER["low"],
                                 fu=BP_FILTER["high"])


BS_FILTER_OBJ = BWBandStopFilter(order=BS_FILTER["order"],
                                 sample_rate=BS_FILTER["sample_rate"],
                                 fl=BS_FILTER["low"],
                                 fu=BS_FILTER["high"])

