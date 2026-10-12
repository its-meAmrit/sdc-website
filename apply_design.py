#!/usr/bin/env python3
"""Idempotent editorial typography patch for SDC Website; preserves color classes."""
from pathlib import Path
import sys

root=Path.cwd()
files={
 'layout':'src/app/layout.tsx',
 'marketing':'src/app/(marketing)/layout.tsx',
 'hero':'src/components/home/hero.tsx',
 'about':'src/components/home/about-section.tsx',
 'css':'src/app/globals.css',
}
for key,rel in files.items():
 if not (root/rel).is_file():
  sys.exit(f'Missing {rel}. Run from repository root.')

changes=[]
def patch(key,old,new):
 p=root/files[key]
 s=p.read_text(encoding='utf-8')
 if new in s:
  print('Already applied:',files[key]);return
 if old not in s:
  sys.exit(f'Source mismatch in {files[key]}: {old!r}\nNo additional changes made after this point.')
 p.write_text(s.replace(old,new,1),encoding='utf-8')
 changes.append(files[key]);print('Updated:',files[key])

patch('layout','import { Geist, Geist_Mono } from "next/font/google";', 'import { Geist, Geist_Mono, Playfair_Display, Source_Sans_3 } from "next/font/google";')
patch('layout','const siteUrl = (', '''const editorialDisplay = Playfair_Display({
  variable: "--font-editorial-display",
  subsets: ["latin"],
  display: "swap",
});

const editorialBody = Source_Sans_3({
  variable: "--font-editorial-body",
  subsets: ["latin"],
  display: "swap",
});

const siteUrl = (''')
patch('layout','${geistSans.variable} ${geistMono.variable} h-full antialiased', '${geistSans.variable} ${geistMono.variable} ${editorialDisplay.variable} ${editorialBody.variable} h-full antialiased')
patch('marketing','className="flex-1"','className="editorial-site flex-1"')
patch('hero','relative grid items-center gap-12 py-16 md:grid-cols-2 md:py-24','relative grid items-center gap-14 py-20 sm:py-24 md:grid-cols-2 md:gap-16 md:py-32')
# In source the <div> and <p> are indented by 8/10 spaces, not 10/12.
patch('hero','        <div>\n          <p className="inline-flex','        <div className="max-w-2xl text-center md:text-left">\n          <p className="inline-flex')
patch('hero','mt-5 text-5xl font-extrabold leading-tight tracking-tight text-slate-900 md:text-6xl','mt-7 text-[clamp(2.8rem,5.8vw,5rem)] font-normal leading-[1.12] tracking-[-0.025em] text-slate-900')
patch('hero','mt-5 max-w-xl text-lg leading-relaxed text-slate-600','mx-auto mt-7 max-w-[38rem] text-lg leading-[1.8] tracking-[0.005em] text-slate-600 md:mx-0')
patch('hero','mt-8 flex flex-wrap items-center gap-3','mt-9 flex flex-wrap items-center justify-center gap-3 md:justify-start')
patch('about','bg-white py-16 sm:py-20','bg-white py-20 sm:py-28')
patch('about','grid gap-10 lg:grid-cols-2 lg:gap-16','grid items-start gap-12 lg:grid-cols-[1.15fr_0.85fr] lg:gap-20')
patch('about','text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl','text-4xl font-normal leading-[1.18] tracking-[-0.015em] text-slate-900 sm:text-5xl')
patch('about','mt-4 text-lg leading-relaxed text-slate-600','mt-6 max-w-[43rem] text-lg leading-[1.8] text-slate-600')
patch('about','rounded-xl border border-slate-200 bg-white p-6','rounded-xl border border-slate-200 bg-white p-7 sm:p-8')
patch('about','mt-4 font-semibold text-slate-900','mt-5 text-xl font-semibold leading-snug text-slate-900')
patch('about','mt-1 text-sm leading-relaxed text-slate-600','mt-3 text-sm leading-[1.8] text-slate-600')
css='''
/* SDC editorial typography; colors and brand styling intentionally unchanged. */
.editorial-site {
  font-family: var(--font-editorial-body), var(--font-geist-sans), sans-serif;
  letter-spacing: 0.005em;
}
.editorial-site :is(h1, h2, h3) {
  font-family: var(--font-editorial-display), Georgia, serif;
  text-wrap: balance;
}
.editorial-site h1 { font-weight: 400; line-height: 1.12; letter-spacing: -0.025em; }
.editorial-site h2 { font-weight: 400; line-height: 1.2; letter-spacing: -0.015em; }
.editorial-site h3 { line-height: 1.35; }
.editorial-site :is(p, li) { text-wrap: pretty; }
.editorial-site section :is(p, li) { overflow-wrap: break-word; }
.editorial-site :is(a, button, input, textarea, select) { font-family: var(--font-editorial-body), var(--font-geist-sans), sans-serif; }
.editorial-site :is(a, button):focus-visible { outline-offset: 3px; }
@media (max-width: 767px) {
  .editorial-site h1 { letter-spacing: -0.02em; }
  .editorial-site h2 { letter-spacing: -0.01em; }
}
@media (prefers-reduced-motion: reduce) {
  .editorial-site *, .editorial-site *::before, .editorial-site *::after {
    scroll-behavior: auto !important;
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
'''
p=root/files['css'];s=p.read_text(encoding='utf-8')
if '.editorial-site :is(h1, h2, h3)' not in s:
 p.write_text(s.rstrip()+'\n'+css,encoding='utf-8');print('Updated:',files['css'])
else: print('Already applied:',files['css'])
print('\nPatch complete. Run: npm run lint && npm run build && npm run dev')
