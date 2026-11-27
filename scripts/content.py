"""Content validation shared by build and the atomic issue importer."""
from datetime import date
from urllib.parse import urlparse
import re
REQUIRED = {'question', 'principle', 'progress', 'papers', 'applications', 'open', 'learning', 'practice'}
def validate(data):
    assert data['schemaVersion'] == 1, 'Unsupported schema'
    topics = [t['id'] for t in data['topics']]
    assert len(topics) == len(set(topics)) and 'ai-frontier' in topics
    ids, numbers = set(), set()
    assert data['issues'], 'At least one issue required'
    for issue in data['issues']:
        ident = issue['id']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', ident), 'Invalid issue id'
        assert ident not in ids, 'Duplicate issue id'
        ids.add(ident)
        assert issue['topic'] in topics, 'Unknown topic'
        for key in ('date', 'checkedAt'): date.fromisoformat(issue[key])
        assert issue['date'] <= date.today().isoformat(), 'Future issue cannot be published'
        for key in ('title','subtitle','summary','level'): assert isinstance(issue[key],str) and issue[key].strip(), key
        assert isinstance(issue['minutes'],int) and 1 <= issue['minutes'] <= 180
        assert isinstance(issue['number'],int) and issue['number'] > 0
        pair = (issue['topic'], issue['number'])
        assert pair not in numbers, 'Duplicate issue number'
        numbers.add(pair)
        assert isinstance(issue['tags'],list) and all(isinstance(t,str) for t in issue['tags'])
        source_ids = set()
        for s in issue['sources']:
            assert isinstance(s['id'],int) and s['id'] > 0 and s['id'] not in source_ids
            source_ids.add(s['id'])
            u = urlparse(s['url'])
            assert u.scheme == 'https' and u.hostname and not u.username and not u.password, 'Sources require HTTPS'
            date.fromisoformat(s['date'])
            for k in ('title','publisher','kind'): assert isinstance(s[k],str) and s[k]
        sections = [s['id'] for s in issue['sections']]
        assert len(sections) == len(set(sections)) and REQUIRED <= set(sections), 'Missing/duplicate sections'
        for s in issue['sections']:
            assert re.fullmatch(r'[a-z][a-z0-9-]*',s['id']) and s['title']
            assert s['id'] not in {'sources','interest'}, 'Reserved section id'
            assert s.get('paragraphs') or s.get('items'), 'Empty section'
            for k in ('paragraphs','items'):
                assert isinstance(s.get(k,[]),list) and all(isinstance(p,str) and p for p in s.get(k,[]))
            assert set(s['sources']) <= source_ids, 'Invalid citation'
            for text in s.get('paragraphs',[]) + s.get('items',[]):
                assert set(map(int,re.findall(r'\[(\d+)\]',text))) <= source_ids, 'Invalid inline citation'
