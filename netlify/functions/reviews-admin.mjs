import { getStore } from "@netlify/blobs";

const json = (d, s = 200) =>
  new Response(JSON.stringify(d), {
    status: s,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
  });

export default async (req) => {
  const pass = Netlify.env.get("ADMIN_PASSWORD");
  const sent = req.headers.get("x-admin-key") || "";
  if (!pass || sent !== pass) {
    await new Promise((r) => setTimeout(r, 800));
    return json({ error: "Contraseña incorrecta" }, 401);
  }
  const store = getStore({ name: "reviews", consistency: "strong" });

  if (req.method === "GET") {
    const list = async (prefix) => {
      const { blobs } = await store.list({ prefix });
      const rows = await Promise.all(
        blobs.map(async (b) => {
          const v = await store.get(b.key, { type: "json", consistency: "strong" });
          return v ? { key: b.key, ...v } : null;
        })
      );
      return rows.filter(Boolean).sort((a, b) => b.ts - a.ts);
    };
    return json({ pending: await list("pending-"), approved: await list("ok-") });
  }

  if (req.method === "POST") {
    let b;
    try { b = await req.json(); } catch { return json({ error: "Datos no válidos" }, 400); }
    const key = String(b.key || "");
    if (!/^(pending|ok)-[\w-]+$/.test(key)) return json({ error: "Clave no válida" }, 400);
    if (b.action === "approve" && key.startsWith("pending-")) {
      const r = await store.get(key, { type: "json" });
      if (!r) return json({ error: "No existe" }, 404);
      await store.setJSON("ok-" + key.slice(8), r);
      await store.delete(key);
      return json({ ok: true });
    }
    if (b.action === "delete") {
      await store.delete(key);
      return json({ ok: true });
    }
    return json({ error: "Acción no válida" }, 400);
  }
  return json({ error: "Método no permitido" }, 405);
};

export const config = { path: "/api/reviews-admin" };
