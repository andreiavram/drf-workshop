from operator import lt, le, gt, ge, eq, ne


class MessageDirection(object):

    DEVICE_READ = 1
    DEVICE_WRITE = 0

    DEVICE_DIRECTIONS = (
        (DEVICE_READ, 'data provider'),
        (DEVICE_WRITE, 'data consumer')
    )


class Operation(object):

    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    EQ = '='
    NE = '!='

    OPERATIONS = (
        (LT, 'less than'),
        (LE, 'less than or equal'),
        (GT, 'greater than'),
        (GE, 'greater than or equal'),
        (EQ, 'equal'),
        (NE, 'not equal')
    )

    @staticmethod
    def eval_for_op(op, a, b):
        mapping = {'<': lt, '<=': le, '>': gt, '>=': ge, '=': eq, '!=': ne}

        return mapping[op](a, b)
