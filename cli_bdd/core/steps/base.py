

class StepBase(object):
    type_ = None  # given, when, then
    sentence = None
    func_name = None

    def build_step_func(self):
        raise NotImplementedError()

    def get_table(self):
        raise NotImplementedError()

    def get_text(self):
        raise NotImplementedError()

    def get_scenario_context(self):
        raise NotImplementedError()


def build_steps(mixin_class, base_steps):
    result = {}
    for base_step in base_steps:
        result_class = type(
            'ResultClass',
            (mixin_class, base_step['class']),
            {}
        )
        instance = result_class()
        result[base_step['func_name']] = instance.build_step_func()
    return result
