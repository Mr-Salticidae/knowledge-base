#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

async function main() {
  const jobArg = process.argv[2];
  if (!jobArg) throw new Error('Usage: node prepare_icons.js <job.json>');
  const jobPath = path.resolve(jobArg);
  const job = JSON.parse(fs.readFileSync(jobPath, 'utf8'));
  const size = Number(job.size_px || 256);
  if (!Number.isInteger(size) || size < 32 || size > 2048) {
    throw new Error('size_px must be an integer between 32 and 2048');
  }
  if (!Array.isArray(job.icons) || job.icons.length === 0) {
    throw new Error('Icon job has no entries');
  }

  const planned = job.icons.map((icon) => {
    const source = path.resolve(icon.source);
    const output = path.resolve(icon.output);
    if (!fs.existsSync(source)) throw new Error(`Missing icon source: ${source}`);
    if (path.extname(output).toLowerCase() !== '.png') {
      throw new Error(`Icon output must be PNG: ${output}`);
    }
    if (fs.existsSync(output)) throw new Error(`Refusing to overwrite icon: ${output}`);
    return { name: icon.name, source, output };
  });

  const created = [];
  try {
    for (const icon of planned) {
      fs.mkdirSync(path.dirname(icon.output), { recursive: true });
      await sharp(icon.source, { density: 600 })
        .resize(size, size, {
          fit: 'contain',
          background: { r: 0, g: 0, b: 0, alpha: 0 },
        })
        .png({ compressionLevel: 9 })
        .toFile(icon.output);
      created.push(icon.output);
    }
  } catch (error) {
    for (const output of created) {
      if (fs.existsSync(output)) fs.unlinkSync(output);
    }
    throw error;
  }

  process.stdout.write(`${JSON.stringify({ size_px: size, created }, null, 2)}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.stack || error.message}\n`);
  process.exit(1);
});
