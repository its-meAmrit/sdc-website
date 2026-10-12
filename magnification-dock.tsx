"use client";

import { useRef, useState } from "react";
import Link from "next/link";
import {
  CalendarDays, Compass, GraduationCap, Info, Lightbulb, UsersRound,
  type LucideIcon,
} from "lucide-react";

export type DockLink = { href: string; label: string };

const ICONS: Record<string, LucideIcon> = {
  "/about": Info,
  "/team": UsersRound,
  "/initiatives": Lightbulb,
  "/events": CalendarDays,
  "/cotm": GraduationCap,
  "/resources": Compass,
};
const INFLUENCE_RADIUS = 110;

export function MagnificationDock({ links, pathname }: { links: DockLink[]; pathname: string }) {
  const itemRefs = useRef<(HTMLLIElement | null)[]>([]);
  const [scales, setScales] = useState<number[]>([]);
  const [hovered, setHovered] = useState<string | null>(null);

  const handlePointerMove = (x: number) => {
    setScales(links.map((_, index) => {
      const item = itemRefs.current[index];
      if (!item) return 1;
      const bounds = item.getBoundingClientRect();
      const distance = Math.abs(x - (bounds.left + bounds.width / 2));
      const t = Math.max(0, 1 - distance / INFLUENCE_RADIUS);
      return 1 + 0.2 * t * t * (3 - 2 * t);
    }));
  };

  return (
    <nav aria-label="Main navigation" className="sdc-dock-nav mx-2 hidden min-w-0 flex-1 lg:flex xl:mx-5">
      <ul
        className="sdc-dock flex w-full items-center justify-evenly gap-0.5 xl:gap-2"
        onPointerMove={(event) => {
          if (event.pointerType === "mouse" || event.pointerType === "pen") {
            handlePointerMove(event.clientX);
          }
        }}
        onPointerLeave={() => { setScales([]); setHovered(null); }}
      >
        {links.map((link, index) => {
          const Icon = ICONS[link.href] ?? Compass;
          const active = pathname === link.href || pathname.startsWith(`${link.href}/`);
          return (
            <li
              key={link.href}
              ref={(node) => { itemRefs.current[index] = node; }}
              className="sdc-dock-item relative min-w-0"
            >
              <Link
                href={link.href}
                aria-current={active ? "page" : undefined}
                onPointerEnter={() => setHovered(link.href)}
                onPointerLeave={() => setHovered(null)}
                onFocus={() => setHovered(link.href)}
                onBlur={() => setHovered(null)}
                className={`sdc-dock-link group relative inline-flex min-h-11 items-center justify-center gap-1.5 whitespace-nowrap rounded-xl px-1.5 py-2.5 text-[11px] font-medium leading-none outline-offset-2 focus-visible:outline-2 focus-visible:outline-brand-600 xl:gap-2 xl:px-3 xl:text-[13px] ${
                  active ? "bg-brand-50 text-brand-700" : "text-slate-700 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                <span
                  aria-hidden="true"
                  className="sdc-dock-icon inline-flex shrink-0 items-center justify-center"
                  style={{ transform: `scale(${scales[index] ?? 1})` }}
                >
                  <Icon className="h-[17px] w-[17px] xl:h-[19px] xl:w-[19px]" strokeWidth={1.85} />
                </span>
                <span className="sdc-dock-label whitespace-nowrap">{link.label}</span>
              </Link>
              <span
                role="tooltip"
                className={`sdc-dock-tooltip pointer-events-none absolute bottom-[calc(100%+8px)] left-1/2 z-50 -translate-x-1/2 whitespace-nowrap rounded-md bg-ink-900 px-2.5 py-1.5 text-xs font-medium text-white shadow-md ${hovered === link.href ? "sdc-dock-tooltip-visible" : ""}`}
              >
                {link.label}
              </span>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
