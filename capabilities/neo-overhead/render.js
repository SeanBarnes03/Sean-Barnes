const { chromium } = require('playwright');
(async () => {
  const [,, html, pdf, pngdir] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1334, height: 750 }, deviceScaleFactor: 1 });
  await p.goto('file://' + html, { waitUntil: 'networkidle', timeout: 20000 }).catch(e => console.log('goto:', e.message));
  await p.evaluate(() => document.fonts.ready);
  console.log('DM Sans loaded:', await p.evaluate(() => document.fonts.check("16px 'DM Sans'")));
  await p.pdf({ path: pdf, width: '1334px', height: '750px', printBackground: true });
  const els = await p.$$('section.slide');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: `${pngdir}/s${String(i).padStart(2, '0')}.png` });
  const ov = await p.$$eval('section.slide', ss => ss.map((s, i) => {
    const top = s.getBoundingClientRect().top;
    const src = s.querySelector('.src');
    let maxB = 0;
    s.querySelectorAll('.card,.callout,table,.cards3').forEach(e => { if (!src.contains(e)) maxB = Math.max(maxB, e.getBoundingClientRect().bottom); });
    return [i, Math.round(maxB - top), Math.round(src.getBoundingClientRect().top - top)];
  }));
  console.log(JSON.stringify(ov));
  await b.close();
})();
