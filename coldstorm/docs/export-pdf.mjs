import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(__dirname, 'swissfox-deck-2026-03-03.html');
const pdfPath = path.join(__dirname, 'Coldstorm-AI-x-SwissFox-March-2026.pdf');

const browser = await puppeteer.launch({ headless: true });
const page = await browser.newPage();

await page.setViewport({ width: 1280, height: 720 });
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

await page.pdf({
  path: pdfPath,
  width: '1280px',
  height: '720px',
  printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
  preferCSSPageSize: false,
});

await browser.close();
console.log(`PDF saved to ${pdfPath}`);
