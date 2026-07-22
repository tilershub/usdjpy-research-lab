# TRADE90 unified platform migration

The target is one Django/Wagtail application on Render, backed by the dedicated TRADE90 Supabase PostgreSQL project and sharing the existing Python research engine.

## Safety rule

Cloudflare Pages and Streamlit remain production until staging reaches URL, design, content, tool and terminal parity. Domain cutover is a separate reviewed operation.

## Delivery stages

1. Platform foundation: Django, Wagtail, terminal API, database snapshots, Render Blueprint.
2. Content parity: import all Astro content with stable URLs and SEO metadata.
3. Design parity: header, footer, homepage, hubs, articles and mobile behavior.
4. Tool parity: calculators, journal, daily dashboard and plan builder.
5. Product layer: accounts, watchlists and alerts.
6. Staging verification and controlled domain cutover.

## Runtime boundaries

- Web requests render pages and read approved snapshots.
- Scheduled jobs fetch market data and publish snapshots.
- Training/recalibration runs separately and promotes a model only after validation.
- Streamlit remains a temporary advanced research fallback and is not the production host.
