# src/model_registry_lr
MODEL_NAME = "sim_applications_lr"
MODEL_VERSION = "v1"

FEATURES_BASIC = [
    "prev_1",
    "prev_2",
    "prev_3",
    "ma3",
]

FEATURES_PLUS = FEATURES_BASIC + [
    "ma3",
    "trend",
    "month_sin",
    "month_cos",
]