import json
import re

EMOJIS = {
    'root': '🌍', 'route': '🌍', 'travel': '🌍',
    'fix': '🤖', 'rag': '🤖', 'ai': '🤖',
    'rhythm': '🎵', 'music': '🎵',
    'menti': '🧠', 'mental': '🧠', 'health': '🧠',
    'medi': '🩺', 'medical': '🩺', 'healthcare': '🩺',
    'default': '📦'
}

def get_emoji(name, desc):
    text = (name + ' ' + (desc or '')).lower()
    for key, emoji in EMOJIS.items():
        if key in text:
            return emoji
    return EMOJIS['default']

try:
    with open('data.json') as f:
        data = json.load(f)
    
    repos = data['data']['user']['pinnedItems']['nodes']
    
    projects = []
    for repo in repos:
        name = repo['name']
        url = repo['url']
        desc = repo.get('description', 'No description')
        stars = repo.get('stargazerCount', 0)
        lang = repo.get('primaryLanguage', {})
        lang_name = lang.get('name', 'N/A') if lang else 'N/A'
        emoji = get_emoji(name, desc)
        
        projects.append(f"### {emoji} [{name}]({url})\n> {desc}\n- **Stack**: {lang_name}\n- **Stars**: ⭐ {stars}\n")
    
    projects_md = '\n'.join(projects)
    
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'(## 🏆 Featured Projects\s*\n\n)(.*?)(\n## )'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, rf'\1{projects_md}\n\3', content, flags=re.DOTALL)
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print('✅ README updated')
    else:
        print('⚠️ Featured Projects section not found')
except Exception as e:
    print(f'❌ Error: {e}')
