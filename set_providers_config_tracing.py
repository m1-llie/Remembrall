# read "selected_providers.txt" and update "config.json" with the user_traces section
import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(current_dir, "info_providers", "selected_providers_v2.txt"), 'r') as f:
    providers = f.readlines()

user_traces = []
for i, provider in enumerate(providers, start=1):
    trace_name, provider_name = provider.strip().split('{', 1)
    user_trace = {
        'trace_name': f'{i:03}-{trace_name.rstrip()}',
        'provider_name': '{' + provider_name.lower(),
        'filters': {
            'none_of': {
                'activity_id_is': "{00000000-0000-0000-0000-000000000000}"
            }
        }
    }
    user_traces.append(user_trace)

with open(os.path.join(current_dir, "config.json"), 'r') as f:
    config = json.load(f)

config['user_traces'] = user_traces

with open(os.path.join(current_dir,"config.json"), 'w') as f:
    json.dump(config, f, indent=4)