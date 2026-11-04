import { getStore } from "@netlify/blobs";

const json = (d, s = 200) =>
  new Response(JSON.stringify(d), {
    status: s,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });
const clean = (s, n) =>
  String(s ?? "").replace(/[\u0000-\u001f<>]/g, " ").replace(/\s+/g, " ").trim().slice(0, n);
const pub = (r) => ({ name: r.name, zona: r.zona, stars: r.stars, text: r.text, ts: r.ts });

export default async (req) => {
  const store = getStore("reviews");

  if (req.method === "GET") {
    const { blobs } = await store.list({ prefix: "ok-" });
    const items = (await Promise.all(blobs.map((b) => store.get(b.key, { type: "json" }))))
      .filter(Boolean)
      .sort((a, b) => b.ts - a.ts)
      .slice(0, 50)
      .map(pub);
    return json(items);
  }

  if (req.method === "POST") {
    let b;
    try { b = await req.json(); } catch { return json({ error: "Datos no válidos" }, 400); }
    if (b.web) return json({ ok: true }); // campo trampa para bots
    const name = clean(b.name, 40);
    const zona = clean(b.zona, 40);
    const text = clean(b.text, 500);
    const stars = Number(b.stars);
    if (name.length < 2 || text.length < 10 || !(stars >= 1 && stars <= 5))
      return json({ error: "Rellena tu nombre y una opinión de al menos 10 caracteres." }, 400);
    const { blobs } = await store.list({ prefix: "pending-" });
    if (blobs.length >= 60) return json({ error: "Ahora mismo no podemos recibir más opiniones." }, 429);
    const ts = Date.now();
    const key = `pending-${ts}-${Math.random().toString(36).slice(2, 8)}`;
    await store.setJSON(key, { name, zona, stars: Math.round(stars), text, ts });
    return json({ ok: true });
  }

  return json({ error: "Método no permitido" }, 405);
};

export const config = { path: "/api/reviews" };
