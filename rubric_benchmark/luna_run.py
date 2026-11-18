"""Generate development rubrics using a tool-free Responses API request."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .smoke import build_smoke_prompt

ASSIGNMENTS = ('mario-more', 'cash', 'readability', 'dna')
API_URL = 'https://api.openai.com/v1/responses'
SYSTEM_INSTRUCTION = (
    'Generate a grading rubric using only the assignment text in the user message. '
    'Do not use external sources, tools, personal preferences, or prior conversation. '
    'Accept alternative implementations that satisfy the assignment requirements.'
)


def generate(prompt, api_key):
    """Send one stateless request with no tools or user configuration."""
    body = {
        'model': 'gpt-6-luna',
        'reasoning': {'effort': 'high'},
        'store': False,
        'input': [
            {'role': 'system', 'content': SYSTEM_INSTRUCTION},
            {'role': 'user', 'content': prompt},
        ],
        'tools': [],
    }
    request = Request(API_URL, data=json.dumps(body).encode('utf-8'), method='POST',
                      headers={'Authorization': 'Bearer ' + api_key,
                               'Content-Type': 'application/json'})
    with urlopen(request, timeout=300) as response:
        raw = response.read()
    result = json.loads(raw)
    if result.get('status') != 'completed':
        raise ValueError('Model response did not complete')
    output = result.get('output', [])
    if any(item.get('type') not in ('message', 'reasoning') for item in output):
        raise ValueError('Unexpected model output type')
    texts = [part['text'] for item in output if item.get('type') == 'message'
             for part in item.get('content', []) if part.get('type') == 'output_text']
    if len(texts) != 1 or not texts[0].strip():
        raise ValueError('Missing or ambiguous rubric')
    return body, raw, result, texts[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--assignments', type=Path, default=Path('data/assignments'))
    args = parser.parse_args()
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        parser.error('OPENAI_API_KEY is required for the isolated, tool-free API')
    # Validate all inputs before sending any request or creating output files.
    prompts = {name: build_smoke_prompt(args.assignments, name,
               include_reference=False, rubric_format='points') for name in ASSIGNMENTS}
    args.output.mkdir(parents=True, exist_ok=False)
    raw_dir = args.output / 'raw_data'
    raw_dir.mkdir()
    manifest = {'mode': 'development', 'requested_model': 'gpt-6-luna',
                'requested_reasoning_effort': 'high', 'transport': 'openai_responses',
                'tools': [], 'conditions': []}
    for name, prompt in prompts.items():
        case = raw_dir / name
        case.mkdir()
        (case / 'prompt.txt').write_text(prompt, encoding='utf-8')
        started = datetime.now(timezone.utc).isoformat()
        entry = {'assignment': name, 'started_utc': started,
                 'prompt_sha256': sha256(prompt.encode()).hexdigest()}
        try:
            body, raw, result, rubric = generate(prompt, key)
            (case / 'request.json').write_text(json.dumps(body, indent=2) + '\n', encoding='utf-8')
            (case / 'response.json').write_bytes(raw)
            (case / 'rubric.txt').write_text(rubric, encoding='utf-8')
            entry.update(status='success', resolved_model=result.get('model'),
                         response_id=result.get('id'),
                         response_sha256=sha256(raw).hexdigest(),
                         rubric_sha256=sha256(rubric.encode()).hexdigest())
        except HTTPError as exc:
            # Error bodies can echo credentials; do not persist them.
            entry.update(status='error', error=f'HTTP {exc.code}')
        except (URLError, TimeoutError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            entry.update(status='error', error=type(exc).__name__)
        entry['finished_utc'] = datetime.now(timezone.utc).isoformat()
        manifest['conditions'].append(entry)
        (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        print(f"{name}: {entry['status']}", flush=True)
    if any(item['status'] != 'success' for item in manifest['conditions']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
