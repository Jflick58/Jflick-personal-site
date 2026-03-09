/**
 * genimg – Cloudflare Worker that proxies image generation requests to the
 * Gemini API and returns WebP images.
 */

const STYLE_PROMPT = `## Style Requirements

- **Aesthetic**: Warm minimalist. Think: oak slats, white countertops, brass fixtures.
  Clean but not sterile. Handcrafted, not industrial.
- **Color palette**: Warm white (#f8f7f4) backgrounds, oak tones (#c49468),
  brass/gold accents (#b89048), near-black (#18171a) for contrast.
  NO cool blues, NO saturated primaries, NO neon.
- **Mood**: Contemplative, precise, quietly confident. Like a well-lit workspace
  at golden hour.
- **Composition**: Generous negative space. Off-center subjects. No clutter.
  The image should breathe.
- **Texture**: Subtle grain or warmth, like film photography or risograph.
  Not photorealistic, not cartoonish.

Aspects of the image composition that MUST be followed EXACTLY:
1. NO text, words, letters, numbers, or watermarks anywhere in the image
2. NO people or human figures
3. NO corporate/stock photo aesthetics
4. NO busy patterns or visual clutter
5. The image must work as a blog illustration at 740px wide

## Subject

`;

const GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta/models";

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== "POST") {
      return jsonError("Method not allowed", 405);
    }

    const url = new URL(request.url);
    if (url.pathname !== "/generate") {
      return jsonError("Not found", 404);
    }

    // Auth
    const auth = request.headers.get("Authorization") || "";
    const token = auth.startsWith("Bearer ") ? auth.slice(7) : "";
    if (!token || token !== env.API_KEY) {
      return jsonError("Unauthorized", 401);
    }

    // Parse body
    let body;
    try {
      body = await request.json();
    } catch {
      return jsonError("Invalid JSON body", 400);
    }

    const { prompt, aspect_ratio = "16:9", model = "gemini-2.0-flash-preview-image-generation" } = body;
    if (!prompt) {
      return jsonError("Missing required field: prompt", 400);
    }

    // Call Gemini
    const geminiUrl = `${GEMINI_BASE}/${model}:generateContent?key=${env.GEMINI_API_KEY}`;
    const geminiBody = {
      contents: [
        {
          parts: [{ text: STYLE_PROMPT + prompt }],
        },
      ],
      generationConfig: {
        responseModalities: ["IMAGE", "TEXT"],
        imageMimeType: "image/webp",
      },
    };

    let geminiRes;
    try {
      geminiRes = await fetch(geminiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(geminiBody),
      });
    } catch (err) {
      return jsonError(`Gemini API request failed: ${err.message}`, 502);
    }

    if (!geminiRes.ok) {
      const errText = await geminiRes.text();
      return jsonError(`Gemini API error (${geminiRes.status}): ${errText}`, 502);
    }

    const geminiData = await geminiRes.json();

    // Extract image from response
    const candidates = geminiData.candidates || [];
    for (const candidate of candidates) {
      const parts = candidate.content?.parts || [];
      for (const part of parts) {
        if (part.inlineData?.mimeType?.startsWith("image/")) {
          const imageBytes = base64ToBytes(part.inlineData.data);
          return new Response(imageBytes, {
            status: 200,
            headers: {
              "Content-Type": part.inlineData.mimeType,
              ...corsHeaders(),
            },
          });
        }
      }
    }

    return jsonError("No image returned by Gemini", 502);
  },
};

function base64ToBytes(b64) {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
  };
}

function jsonError(message, status) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { "Content-Type": "application/json", ...corsHeaders() },
  });
}
