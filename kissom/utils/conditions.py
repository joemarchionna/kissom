COMPARER = "comparer"
FIELDNAME = "fieldName"
FIELDVALUE = "fieldValue"

OPERATOR = "operator"
CONDITIONS = "conditions"


def getConditions(fieldName: str, fieldValue, comparer: str = "="):
    c = {FIELDNAME: fieldName, FIELDVALUE: fieldValue}
    if comparer != "=":
        c[COMPARER] = comparer
    return c


def getConditionGroup(conditions: list, operator: str = "AND"):
    c = {OPERATOR: operator, CONDITIONS: conditions}
    return c
