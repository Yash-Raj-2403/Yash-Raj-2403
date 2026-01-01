const { execSync } = require('child_process');
const fs = require('fs');

const exec = (cmd) => execSync(cmd, { encoding: 'utf-8' });

try {
  const pinned = exec(`gh api graphql -f query='
    query {
      user(login: "Yash-Raj-2403") {
        pinnedItems(first: 6, types: REPOSITORY) {
          nodes {
            ... on Repository {
              name
              url
              description
              stargazerCount
              primaryLanguage { name }
            }
          }
        }
      }
    }'`);
  
  fs.writeFileSync('data.json', pinned);
  console.log('✅ Data extracted');
} catch (err) {
  console.error('❌ Error:', err.message);
  process.exit(1);
}
