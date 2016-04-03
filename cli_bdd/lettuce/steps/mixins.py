from lettuce import step, world


class LettuceStepMixin(object):
    def build_step_func(self):
        @step(self.sentence)
        def lettuce_step(step, *args, **kwargs):
            self.step_context = step
            return self.step(*args, **kwargs)

        return lettuce_step

    def get_table(self):
        return self.step_context.hashes

    def get_text(self):
        return self.step_context.multiline

    def get_scenario_context(self):
        return world
