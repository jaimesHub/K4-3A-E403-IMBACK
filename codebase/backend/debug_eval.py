"""Debug script — xem LLM trả gì cho các case đang fail."""
import sys, json
sys.path.insert(0, 'codebase/backend')

from vlearn.transcript_index import TranscriptIndex
from vlearn import grader

index = TranscriptIndex.from_file('output/transcript/transcript-04-clean.md')
golden = json.loads(open('eval/golden_set.json', encoding='utf-8').read())

CHECK_IDS = ['GS-002', 'GS-004', 'GS-007', 'GS-008', 'GS-009',
             'GS-010', 'GS-015', 'GS-018', 'GS-019', 'GS-020', 'GS-025']
cases = {c['id']: c for c in golden['cases']}

for cid in CHECK_IDS:
    c = cases[cid]
    r = grader.grade_open_answer(c['input']['question'], c['input']['user_answer'], index)
    exp_v = c['expected_output']['verdict_label']
    got_v = r['verdict_label']
    codes_got = r.get('reference_code') or []
    codes_exp = c['expected_output'].get('reference_code', 'n/a')
    must_cover = c['expected_output'].get('explanation_must_cover', [])

    print(f"=== {cid} ===")
    print(f"  C1 verdict  : exp={exp_v} | got={got_v} | OK={exp_v==got_v}")
    print(f"  C4 ref_code : exp={codes_exp} | got={codes_got}")
    print(f"  Explanation : {r['explanation'][:300]}")
    print(f"  Must cover  : {must_cover}")
    print()
