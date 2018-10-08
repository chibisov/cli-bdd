from cli_bdd.behave.steps.mixins import BehaveStepMixin
from cli_bdd.core.steps.base import build_steps
from cli_bdd.core.steps.command import base_steps

steps = build_steps(
    mixin_class=BehaveStepMixin,
    base_steps=base_steps
)
locals().update(steps)
__all__ = list(steps.keys())
