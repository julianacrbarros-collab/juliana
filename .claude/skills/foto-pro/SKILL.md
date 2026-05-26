---
name: foto-pro
description: Generate photorealistic images using Gemini Pro. Prioritizes gemini-3-pro-image-preview with automatic fallback. Specializes in generating images of real people preserving all physical features using a subject photo reference and an optional style reference. Use when the user asks to generate, create, or edit photos — especially portraits, professional photos, or styled shots based on someone's appearance.
---

# Foto Pro — Geração Realista com Gemini

Gera imagens fotorrealistas priorizando o Gemini 3 Pro Image, com suporte a imagem de referência de pessoa (subject) e referência de estilo (style).

## Comando

```bash
uv run ~/.claude/skills/foto-pro/scripts/generate.py \
  --prompt "descrição detalhada" \
  --filename "YYYY-MM-DD-HH-MM-SS-nome.png" \
  [--subject-image "foto_da_pessoa.jpg"] \
  [--style-image "referencia_estilo.png"] \
  [--resolution 1K|2K|4K] \
  [--api-key KEY]
```

## Modelos (ordem de prioridade)

1. `gemini-3-pro-image-preview` — melhor qualidade e realismo
2. `gemini-2.5-flash-image` — fallback automático se Pro estiver sem cota

O script tenta o Pro primeiro e cai automaticamente para o próximo se houver erro de cota (429).

## Parâmetros de imagem

- `--subject-image` — foto da pessoa cujas características físicas devem ser preservadas (rosto, cabelo, pele, traços)
- `--style-image` — imagem de referência de estilo, composição e iluminação
- Podem ser usados juntos ou separados

## Resolução

- `1K` (padrão) — ~1024px
- `2K` — ~2048px
- `4K` — ~4096px, melhor para preservar detalhes faciais

## Geração de filename

Padrão: `YYYY-MM-DD-HH-MM-SS-nome-descritivo.png`

## Como construir o prompt para máximo realismo

### Quando tiver --subject-image + --style-image

Descreva no prompt:
1. Instrução clara de preservar o rosto da imagem de sujeito
2. Características físicas específicas (cabelo, olhos, pele, traços)
3. Pose, roupa e cena baseadas na referência de estilo
4. Sempre incluir: "photorealistic", "real photograph quality", "preserve face exactly"

**Exemplo:**
```
Generate a photorealistic portrait of THIS EXACT person from the subject image.
Her features: long straight dark black hair, olive warm skin, brown eyes, full lips.
Pose and style based on the style reference: standing, holding a MacBook under one arm,
coffee cup in other hand, black oversized blazer, white studio background, black and white.
The face MUST match the subject image exactly. Real photograph quality, editorial fashion.
```

### Quando tiver apenas --subject-image (edição)

Descreva o que mudar mantendo a pessoa:
```
Keep this exact person with all features preserved. Change only: [o que mudar].
Photorealistic result.
```

### Geração pura (sem imagem)

Descreva a cena completa com características físicas detalhadas.

## Lições aprendidas

- Usar `--subject-image` + `--style-image` juntos dá melhores resultados que só texto
- Descrever características físicas específicas no prompt reforça a preservação da face
- Resolução 4K preserva melhor detalhes sutis (cicatrizes, traços finos)
- Transformações muito grandes (mudar tudo de uma vez) geram resultados menos realistas
- Mudanças incrementais funcionam melhor

## Extração de imagem inline do chat

Quando o usuário enviar imagem inline (não como arquivo), extrair do histórico da sessão:

```python
import json, base64
fname = "/root/.claude/projects/-home-user-juliana/8358481b-903b-4e76-9270-cb2e9d12333d.jsonl"
with open(fname) as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    obj = json.loads(line)
    content = obj.get("message", obj).get("content", [])
    for j, block in enumerate(content):
        if isinstance(block, dict) and block.get("type") == "image":
            src = block.get("source", {})
            if src.get("type") == "base64":
                data = src["data"]
                ext = src["media_type"].split("/")[-1]
                with open(f"extracted_{i}_{j}.{ext}", "wb") as out:
                    out.write(base64.b64decode(data))
```

Pegar sempre a entrada mais recente do usuário (última linha com imagem).
