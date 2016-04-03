from cli_bdd.lettuce.steps.mixins import LettuceStepMixin
from cli_bdd.core.steps.command import base_steps
from cli_bdd.core.steps.base import build_steps


steps = build_steps(
    mixin_class=LettuceStepMixin,
    base_steps=base_steps
)
locals().update(steps)
__all__ = steps.keys()
