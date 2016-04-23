from cli_bdd.core.steps.base import build_steps
from cli_bdd.core.steps.environment import base_steps
from cli_bdd.lettuce.steps.mixins import LettuceStepMixin

steps = build_steps(
    mixin_class=LettuceStepMixin,
    base_steps=base_steps
)
locals().update(steps)
__all__ = steps.keys()
