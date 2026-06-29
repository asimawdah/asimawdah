import fs from 'node:fs';
import process from 'node:process';

const readme = fs.readFileSync('README.md', 'utf8');

const requiredSections = [
  '# Asim Awdah',
  '## Featured projects',
  '## Current roadmap',
  '## Tech stack',
  '## What I build',
  '## Repository map',
  '## Profile maintenance',
];

const requiredLinks = [
  'https://github.com/asimawdah/maham-app',
  'https://github.com/asimawdah/maham-api',
  'https://github.com/asimawdah/MahamKit.app',
  'https://github.com/asimawdah/SkillMint',
  'https://github.com/asimawdah/DocSmith',
  'https://github.com/asimawdah/promptmint',
  'https://github.com/asimawdah/main_cluster',
];

const missingSections = requiredSections.filter((section) => !readme.includes(section));
const missingLinks = requiredLinks.filter((link) => !readme.includes(link));

if (missingSections.length > 0 || missingLinks.length > 0) {
  console.error('Profile README validation failed.');

  if (missingSections.length > 0) {
    console.error(`Missing sections: ${missingSections.join(', ')}`);
  }

  if (missingLinks.length > 0) {
    console.error(`Missing links: ${missingLinks.join(', ')}`);
  }

  process.exit(1);
}

console.log('Profile README validation passed.');
