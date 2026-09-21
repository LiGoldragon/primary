#!/usr/bin/env python3
"""The retired Herdr launch path must fail before sending input to a live pane."""
import importlib.util
import pathlib

source = pathlib.Path(__file__).with_name('claude-single-turn-start.py')
spec = importlib.util.spec_from_file_location('claude_single_turn_start', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
try:
    module.launch({}, 'fixture', 'w1:p1', 'fixture-agent', 'claude-sonnet-5', 'medium')
except RuntimeError as error:
    assert 'isolated job state' in str(error)
else:
    raise AssertionError('historical Claude launch was not blocked')
print('historical Claude launch guard passed')
