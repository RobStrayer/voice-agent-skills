"""Estimate the cost of a voice agent per call, per minute and per month.

Usage:
    python estimate.py assumptions.json
    python estimate.py --selftest

Prices are never built in. Put current prices from each provider's pricing page
in the JSON file (see ../references/example-assumptions.json), with the URL and
date you read them.
"""
import json
import math
import sys

# How many units of each kind one call consumes, given the call profile.
UNITS = {
    'per_call_minute': 'minutes of call time (billed per started minute if round_up is true)',
    'per_caller_audio_minute': 'minutes of audio streamed to speech-to-text',
    'per_agent_speech_minute': 'minutes of speech the agent produces',
    'per_tts_character': 'characters sent to text-to-speech',
    'per_llm_input_token': 'uncached language-model input tokens',
    'per_llm_cached_input_token': 'cached language-model input tokens',
    'per_llm_output_token': 'language-model output tokens',
    'per_call': 'calls',
    'per_month': 'fixed monthly fee (spread over all calls)',
}


def quantities(p):
    """Units consumed by one call. The LLM re-reads the whole history each turn,
    so input tokens grow with the square of the number of turns."""
    minutes = p['minutes_per_call']
    turns = max(1, round(p['turns_per_minute'] * minutes))
    history = p['history_tokens_per_turn'] * turns * (turns - 1) / 2
    llm_in = p['static_prompt_tokens'] * turns + history
    cached = llm_in * p.get('cached_input_share', 0.0)
    agent_minutes = minutes * p['agent_talk_share']
    return {
        'per_call_minute': minutes,
        'per_caller_audio_minute': minutes,  # streaming STT hears the whole call
        'per_agent_speech_minute': agent_minutes,
        'per_tts_character': agent_minutes * p.get('tts_characters_per_minute', 900),
        'per_llm_input_token': llm_in - cached,
        'per_llm_cached_input_token': cached,
        'per_llm_output_token': p['output_tokens_per_turn'] * turns,
        'per_call': 1,
        'per_month': 1 / p['calls_per_month'],
    }


def estimate(data):
    p = data['profile']
    q = quantities(p)
    rows = []
    for c in data['components']:
        unit = c['unit']
        if unit not in UNITS:
            raise ValueError(f"{c['name']}: unknown unit {unit!r}; use one of {sorted(UNITS)}")
        amount = q[unit]
        if unit == 'per_call_minute' and c.get('round_up', False):
            amount = math.ceil(amount)
        rows.append((c['name'], unit, amount, amount * c['price']))
    per_call = sum(r[3] for r in rows)
    return rows, per_call, per_call / p['minutes_per_call'], per_call * p['calls_per_month']


def report(data):
    rows, per_call, per_minute, monthly = estimate(data)
    width = max(len(r[0]) for r in rows)
    print(f"{'component'.ljust(width)}  {'units per call':>16}  {'$ per call':>10}  {'share':>6}")
    for name, unit, amount, cost in sorted(rows, key=lambda r: -r[3]):
        share = cost / per_call if per_call else 0
        print(f"{name.ljust(width)}  {amount:>16,.1f}  {cost:>10.4f}  {share:>6.0%}")
    print(f"\nPer call: ${per_call:.4f}   Per minute: ${per_minute:.4f}   "
          f"Per month ({data['profile']['calls_per_month']:,} calls): ${monthly:,.2f}")


def selftest():
    profile = {'minutes_per_call': 2, 'calls_per_month': 100, 'turns_per_minute': 2,
               'static_prompt_tokens': 1000, 'history_tokens_per_turn': 100,
               'output_tokens_per_turn': 50, 'agent_talk_share': 0.5, 'cached_input_share': 0.5}
    q = quantities(profile)
    assert q['per_llm_input_token'] + q['per_llm_cached_input_token'] == 4 * 1000 + 100 * 6
    assert q['per_llm_output_token'] == 200 and q['per_tts_character'] == 900
    data = {'profile': dict(profile, minutes_per_call=1.5), 'components': [
        {'name': 'phone', 'unit': 'per_call_minute', 'price': 0.01, 'round_up': True},
        {'name': 'number', 'unit': 'per_month', 'price': 100.0}]}
    _, per_call, _, monthly = estimate(data)
    assert math.isclose(per_call, 0.02 + 1.0) and math.isclose(monthly, 102.0)
    print('PASS: token growth, TTS characters, per-minute rounding and fixed fees.')


if __name__ == '__main__':
    if sys.argv[1:] == ['--selftest']:
        selftest()
    elif len(sys.argv) == 2:
        with open(sys.argv[1], encoding='utf-8') as f:
            report(json.load(f))
    else:
        sys.exit(__doc__)
