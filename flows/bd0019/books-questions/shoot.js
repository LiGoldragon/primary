// Phone-size render (390x844, mobile emulation) of every page, light and dark; reports horizontal overflow.
const { chromium } = require('/nix/store/cwcq27pd1q3hcaszl9ilalv3swcj9zdf-playwright-cli-0.1.13/lib/playwright-cli/node_modules/playwright-core');
const fs = require('fs');
const S = process.argv[2], D = '/home/li/primary/flows/bd0019/books-questions/';
(async () => {
  const b = await chromium.launch({ executablePath: '/home/li/.nix-profile/bin/google-chrome' });
  for (const theme of ['light', 'dark']) {
    const html = `<!doctype html><html data-theme="${theme}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0}</style></head><body>${fs.readFileSync(D + 'book.html', 'utf8')}</body></html>`;
    fs.writeFileSync(`${S}/pw-${theme}.html`, html);
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true, colorScheme: theme });
    const p = await ctx.newPage();
    await p.goto(`file://${S}/pw-${theme}.html`); await p.waitForTimeout(1500);
    const n = await p.$$eval('.page', e => e.length);
    for (let i = 1; i <= n; i++) {
      for (const where of ['start', 'end']) {
        const info = await p.evaluate(([i, where]) => { const el = document.getElementById('p' + i); el.scrollIntoView({ block: where });
          const over = [...el.querySelectorAll('.leaf *')].filter(e => e.getBoundingClientRect().right > innerWidth + 0.5).length;
          return { tall: el.scrollHeight > innerHeight + 1, over, docW: document.documentElement.scrollWidth, bookW: document.getElementById('book').scrollWidth, vw: innerWidth }; }, [i, where]);
        if (where === 'end' && !info.tall) continue;
        await p.waitForTimeout(150);
        await p.screenshot({ path: `${S}/${theme}-${i}${where === 'end' ? 'e' : ''}.png` });
        if (info.over || info.docW > info.vw || info.bookW > info.vw) console.log('OVERFLOW', theme, i, where, JSON.stringify(info));
      }
    }
    console.log(theme, 'pages', n, 'viewport', await p.evaluate(() => innerWidth + 'x' + innerHeight));
    await ctx.close();
  }
  await b.close();
})();
