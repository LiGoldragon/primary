#!/usr/bin/env python3
"""The schema walk for anatomy/index.datom.

Each position's meaning comes from the type, written once here, in the order
modelFlowAnatomy.ethos declares it. Nothing about the shape is repeated in the
datom text.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple

import datom_read as dr

HARNESS = ('Claude', 'Codex', 'OpenSource')
TEMPERAMENT = ('Wise', 'Martian', 'Doer', 'Unnamed')
WINDOW = ('Standard', 'Million')
LAYER = ('Primary', 'Secondary', 'Tertiary', 'Quaternary')
SUBFLOW_KIND = ('Checkup', 'Audit', 'Witness', 'Proof', 'Send', 'Illustrate',
                'LowPowerThinking', 'Distillation')
# Extension of the f55ec8 anatomy proposal, by flow b49251 on 2026-09-16:
# Role gains a third kind, Psyche.Effort, for the three psyche-flow effort
# levels the living named (vision/psycheFlows.md, "Three levels of psyche
# flows, low, medium and high effort"). Additive: every existing Main and Sub
# role name and composition is unchanged.
EFFORT = ('Low', 'Medium', 'High')
INSTALL_EFFECT = ('Replace', 'Append')
STRATUM = ('Top', 'Middle', 'Bottom')


def _snake(camel: str) -> str:
    out = []
    for i, ch in enumerate(camel):
        if ch.isupper() and i:
            out.append('-')
        out.append(ch.lower())
    return ''.join(out)


@dataclass(frozen=True)
class Role:
    kind: str      # 'Main' | 'Sub' | 'Psyche'
    value: str     # a Layer, a SubflowKind or an Effort

    @property
    def name(self) -> str:
        if self.kind == 'Main':
            return _snake(self.value) + '-main'
        if self.kind == 'Psyche':
            return 'psyche-' + _snake(self.value)
        return 'subflow-' + _snake(self.value)

    def datom(self) -> str:
        return f'{self.kind}.{self.value}'


def role_by_name(name: str) -> Optional[Role]:
    for layer in LAYER:
        if Role('Main', layer).name == name:
            return Role('Main', layer)
    for kind in SUBFLOW_KIND:
        if Role('Sub', kind).name == name:
            return Role('Sub', kind)
    for effort in EFFORT:
        if Role('Psyche', effort).name == name:
            return Role('Psyche', effort)
    return None


def harness_by_name(name: str) -> Optional[str]:
    for harness in HARNESS:
        if _snake(harness) == name:
            return harness
    return None


@dataclass
class Provenance:
    vision_path: str
    heading: str


@dataclass
class Model:
    model_id: str
    model_name: str
    harness: str
    temperament: str
    window: str
    provenance: Provenance


@dataclass
class Impersonation:
    role: Role
    model_id: str
    note: str
    provenance: Provenance


@dataclass
class Module:
    module_name: str
    module_path: str
    sha256: str
    wrap: str                           # 'Bare' | 'Source' | 'Skill'
    emitted_path: str = ''
    skill: Tuple[str, str] = ('', '')   # skill name, skill location


@dataclass
class Composition:
    role: Role
    harness: str
    module_names: List[str]


@dataclass
class Install:
    harness: str
    flag_text: str
    install_effect: str
    stratum: str
    note: str


@dataclass
class Index:
    models: List[Model]
    impersonations: List[Impersonation]
    modules: List[Module]
    compositions: List[Composition]
    installs: List[Install]


def _provenance(form) -> Provenance:
    vision_path, heading = dr.struct(form, 2, 'Provenance')
    return Provenance(dr.string(vision_path, 'VisionPath'), dr.string(heading, 'Heading'))


def _role(form) -> Role:
    v = dr.variant(form, ('Main', 'Sub', 'Psyche'), 'Role')
    allowed, label = {'Main': (LAYER, 'Layer'),
                      'Sub': (SUBFLOW_KIND, 'SubflowKind'),
                      'Psyche': (EFFORT, 'Effort')}[v.text]
    inner = dr.variant(v.payload, allowed, label)
    return Role(v.text, inner.text)


def _model(form) -> Model:
    items = dr.struct(form, 6, 'Model')
    return Model(
        dr.string(items[0], 'ModelId'),
        dr.string(items[1], 'ModelName'),
        dr.variant(items[2], HARNESS, 'Harness').text,
        dr.variant(items[3], TEMPERAMENT, 'Temperament').text,
        dr.variant(items[4], WINDOW, 'Window').text,
        _provenance(items[5]))


def _impersonation(form) -> Impersonation:
    items = dr.struct(form, 4, 'Impersonation')
    return Impersonation(_role(items[0]), dr.string(items[1], 'ModelId'),
                         dr.string(items[2], 'Note'), _provenance(items[3]))


def _module(form) -> Module:
    items = dr.struct(form, 4, 'Module')
    wrap = dr.variant(items[3], ('Bare', 'Source', 'Skill'), 'Wrap')
    module = Module(dr.string(items[0], 'ModuleName'), dr.string(items[1], 'ModulePath'),
                    dr.string(items[2], 'Sha256'), wrap.text)
    if wrap.text == 'Source':
        module.emitted_path = dr.string(wrap.payload, 'EmittedPath')
    elif wrap.text == 'Skill':
        name, location = dr.struct(wrap.payload, 2, 'Skill')
        module.skill = (dr.string(name, 'SkillName'), dr.string(location, 'SkillLocation'))
    return module


def _composition(form) -> Composition:
    items = dr.struct(form, 3, 'Composition')
    names = [dr.string(n, 'ModuleName') for n in dr.vector(items[2], 'ModuleNameVector')]
    return Composition(_role(items[0]),
                       dr.variant(items[1], HARNESS, 'Harness').text, names)


def _install(form) -> Install:
    items = dr.struct(form, 5, 'Install')
    return Install(dr.variant(items[0], HARNESS, 'Harness').text,
                   dr.string(items[1], 'FlagText'),
                   dr.variant(items[2], INSTALL_EFFECT, 'InstallEffect').text,
                   dr.variant(items[3], STRATUM, 'Stratum').text,
                   dr.string(items[4], 'Note'))


def read(text: str) -> Index:
    root = dr.parse(text)
    anatomy, modules, compositions, installs = dr.struct(root, 4, 'Index')
    model_vector, impersonation_vector = dr.struct(anatomy, 2, 'Anatomy')
    return Index(
        [_model(f) for f in dr.vector(model_vector, 'ModelVector')],
        [_impersonation(f) for f in dr.vector(impersonation_vector, 'ImpersonationVector')],
        [_module(f) for f in dr.vector(modules, 'ModuleVector')],
        [_composition(f) for f in dr.vector(compositions, 'CompositionVector')],
        [_install(f) for f in dr.vector(installs, 'InstallVector')])
