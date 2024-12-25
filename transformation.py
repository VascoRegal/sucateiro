
class Transformations:

    @staticmethod
    def split_transformation(field, conf):
        by = conf["by"]
        index = conf["index"]
        max_split = conf.get("max_split")

        if not max_split:
            return field.split(by)[index].strip()

        else:
            return field.split(by, max_split)[index].strip()

    @staticmethod
    def splice_transformation(field, conf):
        splice = conf["splice_index"]
        reverse = conf.get("reverse")

        if reverse:
            return field[:splice]
        else:
            return field[splice:]

    @staticmethod
    def replace_transformation(field, conf):
        old = conf["old"]
        new = conf["new"]

        return field.replace(old, new)