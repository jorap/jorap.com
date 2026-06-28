/*
 * JoRap Hugo shortcodes → Sveltia editor components (jorap-* ids).
 *
 * Customize labels, fields, previews, and toBlock output here.
 * Keep static/admin/config.yml editor_components in sync with the ids below.
 *
 * Hugo template sources:
 *   layouts/shortcodes/card.html
 *   themes/jorap/layouts/shortcodes/{youtube,youtube_time,spotify,spotify_iframe_*}
 *   _vendor/.../images/layouts/shortcodes/image.html
 *   _vendor/.../shortcodes/{button,notice,mermaid}/layouts/shortcodes/*.html
 *   _vendor/.../{accordion,tab,modal,gallery-slider,videos,adsense,toc}/layouts/shortcodes/*.html
 */
(function (global) {
  const esc = (value) =>
    String(value ?? '')
      .replace(/\\/g, '\\\\')
      .replace(/"/g, '\\"');

  const parseAttrs = (raw) => {
    const attrs = {};
    if (!raw) return attrs;
    for (const match of raw.matchAll(/(\w+)="([^"]*)"/g)) attrs[match[1]] = match[2];
    return attrs;
  };

  const attrsToString = (attrs) =>
    Object.entries(attrs)
      .filter(([, value]) => value !== '' && value != null)
      .map(([key, value]) => `${key}="${esc(value)}"`)
      .join(' ');

  const noticeColors = {
    note: '#64748b',
    tip: '#22c55e',
    info: '#0ea5e9',
    warning: '#f59e0b',
    danger: '#ef4444',
    success: '#16a34a',
    question: '#8b5cf6',
  };

  const embedFrame = (src) =>
    `<div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;background:#000">
      <iframe src="${src}" title="Embed preview" loading="lazy" allowfullscreen
        style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe>
    </div>`;

  const placeholder = (label, detail = '') =>
    `<div style="padding:.75rem 1rem;border:1px dashed #cbd5e1;border-radius:8px;color:#64748b">
      <strong>${label}</strong>${detail ? `<div style="margin-top:.25rem;font-size:.875rem">${detail}</div>` : ''}
    </div>`;

  const parseTabsInner = (inner) => {
    const tabs = [];
    const re = /\{\{<\s*tab\s+"([^"]+)"\s*>\}\}([\s\S]*?)\{\{<\s*\/tab\s*>\}\}/g;
    let match;
    while ((match = re.exec(inner || ''))) {
      tabs.push({ name: match[1], content: match[2].trim() });
    }
    return tabs;
  };

  const serializeTabs = (tabs) => {
    const body = (tabs || [])
      .map(
        (tab) =>
          `{{< tab "${esc(tab.name || 'Tab')}" >}}\n${tab.content || ''}\n{{< /tab >}}`,
      )
      .join('\n');
    return `{{< tabs >}}\n${body}\n{{< /tabs >}}`;
  };

  /** @type {import('@sveltia/cms').EditorComponentDefinition[]} */
  global.JORAP_SHORTCODES = [
    // --- Media embeds ---
    {
      id: 'jorap-youtube',
      label: 'YouTube',
      icon: 'youtube_activity',
      fields: [{ name: 'id', label: 'Video ID' }],
      pattern: /^\{\{<\s*youtube\s+(?:id="(?<id>[^"]+)"|(?<posId>[^\s>]+))\s*>\}\}/m,
      fromBlock: ({ groups: { id, posId } = {} }) => ({ id: id || posId || '' }),
      toBlock: ({ id = '' }) => `{{< youtube ${id.trim()} >}}`,
      toPreview: ({ id = '' }) =>
        id.trim() ? embedFrame(`https://www.youtube-nocookie.com/embed/${id.trim()}`) : '',
    },
    {
      id: 'jorap-youtube-time',
      label: 'YouTube clip',
      icon: 'movie',
      fields: [
        { name: 'id', label: 'Video ID' },
        { name: 'start', label: 'Start (seconds)', default: '0' },
        { name: 'end', label: 'End (seconds)' },
      ],
      pattern:
        /^\{\{<\s*youtube_time\s+id="(?<id>[^"]+)"\s+start="(?<start>[^"]+)"\s+end="(?<end>[^"]+)"\s*>\}\}/m,
      toBlock: ({ id = '', start = '0', end = '' }) =>
        `{{< youtube_time id="${esc(id)}" start="${esc(start)}" end="${esc(end)}" >}}`,
      toPreview: ({ id = '', start = '0', end = '' }) => {
        if (!id.trim()) return '';
        const params = new URLSearchParams({ start: String(start || '0') });
        if (end) params.set('end', String(end));
        return embedFrame(
          `https://www.youtube-nocookie.com/embed/${id.trim()}?${params.toString()}`,
        );
      },
    },
    {
      id: 'jorap-youtube-lite',
      label: 'YouTube (lite)',
      icon: 'slow_motion_video',
      fields: [{ name: 'id', label: 'Video ID' }],
      pattern:
        /^\{\{<\s*youtube-lite\s+(?:id="(?<id>[^"]+)"|(?<posId>[^\s>]+))\s*>\}\}/m,
      fromBlock: ({ groups: { id, posId } = {} }) => ({ id: id || posId || '' }),
      toBlock: ({ id = '' }) => `{{< youtube-lite ${id.trim()} >}}`,
      toPreview: ({ id = '' }) =>
        id.trim() ? embedFrame(`https://www.youtube-nocookie.com/embed/${id.trim()}`) : '',
    },
    {
      id: 'jorap-vimeo-lite',
      label: 'Vimeo (lite)',
      icon: 'videocam',
      fields: [{ name: 'id', label: 'Vimeo video ID' }],
      pattern: /^\{\{<\s*vimeo-lite\s+(?:id="(?<id>[^"]+)"|(?<posId>[^\s>]+))\s*>\}\}/m,
      fromBlock: ({ groups: { id, posId } = {} }) => ({ id: id || posId || '' }),
      toBlock: ({ id = '' }) => `{{< vimeo-lite ${id.trim()} >}}`,
      toPreview: ({ id = '' }) =>
        id.trim() ? embedFrame(`https://player.vimeo.com/video/${id.trim()}`) : '',
    },
    {
      id: 'jorap-video',
      label: 'Video file',
      icon: 'movie_filter',
      fields: [
        { name: 'src', label: 'URL or assets path' },
        { name: 'width', label: 'Width', default: '100%', required: false },
        { name: 'height', label: 'Height', default: 'auto', required: false },
        { name: 'controls', label: 'Controls', widget: 'boolean', default: true, required: false },
        { name: 'autoplay', label: 'Autoplay', widget: 'boolean', default: false, required: false },
        { name: 'loop', label: 'Loop', widget: 'boolean', default: false, required: false },
        { name: 'muted', label: 'Muted', widget: 'boolean', default: false, required: false },
        { name: 'class', label: 'CSS class', default: 'rounded-lg', required: false },
      ],
      pattern: /^\{\{<\s*video\s+(?<attrs>[\s\S]+?)\s*>\}\}/m,
      fromBlock: ({ groups: { attrs } = {} }) => {
        const parsed = parseAttrs(attrs);
        return {
          src: parsed.src || '',
          width: parsed.width || '100%',
          height: parsed.height || 'auto',
          controls: parsed.controls !== 'false',
          autoplay: parsed.autoplay === 'true',
          loop: parsed.loop === 'true',
          muted: parsed.muted === 'true',
          class: parsed.class || 'rounded-lg',
        };
      },
      toBlock: (data) =>
        `{{< video ${attrsToString({
          src: data.src,
          width: data.width || '100%',
          height: data.height || 'auto',
          autoplay: data.autoplay ? 'true' : 'false',
          loop: data.loop ? 'true' : 'false',
          muted: data.muted ? 'true' : 'false',
          controls: data.controls !== false ? 'true' : 'false',
          class: data.class || 'rounded-lg',
        })} >}}`,
      toPreview: ({ src = '' }) =>
        src
          ? `<video src="${src}" controls style="max-width:100%;border-radius:8px"></video>`
          : placeholder('Video', 'Add a src URL or assets path'),
    },
    {
      id: 'jorap-spotify',
      label: 'Spotify embed',
      icon: 'library_music',
      fields: [
        {
          name: 'type',
          label: 'Type',
          widget: 'select',
          options: ['track', 'album', 'playlist', 'artist'],
          default: 'track',
        },
        { name: 'id', label: 'Spotify ID' },
      ],
      pattern:
        /^\{\{<\s*spotify\s+(?:(?<type1>track|album|playlist|artist)\s+(?<id1>[^\s>]+)|type="(?<type2>[^"]+)"\s+id="(?<id2>[^"]+)")\s*>\}\}/m,
      fromBlock: ({ groups = {} }) => ({
        type: groups.type1 || groups.type2 || 'track',
        id: groups.id1 || groups.id2 || '',
      }),
      toBlock: ({ type = 'track', id = '' }) => `{{< spotify ${type} ${id.trim()} >}}`,
      toPreview: ({ type = 'track', id = '' }) =>
        id.trim()
          ? `<iframe src="https://open.spotify.com/embed/${type}/${id.trim()}?utm_source=generator"
              width="100%" height="152" style="border:0;border-radius:12px" loading="lazy"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
          : '',
    },
    {
      id: 'jorap-spotify-track',
      label: 'Spotify track',
      icon: 'music_note',
      fields: [{ name: 'id', label: 'Track ID' }],
      pattern: /^\{\{<\s*spotify_iframe_track\s+(?:id="(?<id>[^"]+)"|(?<posId>[^\s>]+))\s*>\}\}/m,
      fromBlock: ({ groups: { id, posId } = {} }) => ({ id: id || posId || '' }),
      toBlock: ({ id = '' }) => `{{< spotify_iframe_track ${id.trim()} >}}`,
      toPreview: ({ id = '' }) =>
        id.trim()
          ? `<iframe src="https://open.spotify.com/embed/track/${id.trim()}?utm_source=generator"
              width="100%" height="152" style="border:0;border-radius:12px" loading="lazy"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
          : '',
    },
    {
      id: 'jorap-spotify-artist',
      label: 'Spotify artist',
      icon: 'person',
      fields: [{ name: 'id', label: 'Artist ID' }],
      pattern: /^\{\{<\s*spotify_iframe_artist\s+(?:id="(?<id>[^"]+)"|(?<posId>[^\s>]+))\s*>\}\}/m,
      fromBlock: ({ groups: { id, posId } = {} }) => ({ id: id || posId || '' }),
      toBlock: ({ id = '' }) => `{{< spotify_iframe_artist ${id.trim()} >}}`,
      toPreview: ({ id = '' }) =>
        id.trim()
          ? `<iframe src="https://open.spotify.com/embed/artist/${id.trim()}?utm_source=generator"
              width="100%" height="352" style="border:0;border-radius:12px" loading="lazy"
              allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>`
          : '',
    },

    // --- Images ---
    {
      id: 'jorap-image',
      label: 'Image',
      icon: 'image',
      fields: [
        { name: 'src', label: 'Image', widget: 'image' },
        { name: 'caption', label: 'Caption', required: false },
        { name: 'alt', label: 'Alt text', required: false },
        { name: 'title', label: 'Title', required: false },
        {
          name: 'position',
          label: 'Position',
          widget: 'select',
          required: false,
          options: ['center', 'left', 'right', 'float-left', 'float-right'],
          default: 'center',
        },
        { name: 'height', label: 'Height', required: false },
        { name: 'width', label: 'Width', required: false },
        {
          name: 'command',
          label: 'Resize command',
          widget: 'select',
          required: false,
          options: ['fit', 'fill', 'crop'],
          default: 'fit',
        },
        { name: 'option', label: 'Quality option', default: 'q75', required: false },
        { name: 'class', label: 'CSS class', default: 'img-fluid', required: false },
        { name: 'webp', label: 'WebP', widget: 'boolean', default: true, required: false },
        { name: 'zoomable', label: 'Zoomable', widget: 'boolean', default: false, required: false },
      ],
      pattern: /^\{\{<\s*image\s+(?<attrs>[\s\S]+?)\s*>\}\}/m,
      fromBlock: ({ groups: { attrs } = {} }) => {
        const parsed = parseAttrs(attrs);
        return {
          src: parsed.src || '',
          caption: parsed.caption || '',
          alt: parsed.alt || parsed.caption || '',
          title: parsed.title || '',
          position: parsed.position || 'center',
          height: parsed.height || '',
          width: parsed.width || '',
          command: parsed.command || 'fit',
          option: parsed.option || 'q75',
          class: parsed.class || 'img-fluid',
          webp: parsed.webp !== 'false',
          zoomable: parsed.zoomable === 'true',
        };
      },
      toBlock: (data) =>
        `{{< image ${attrsToString({
          src: data.src,
          caption: data.caption,
          alt: data.alt || data.caption,
          title: data.title,
          height: data.height,
          width: data.width,
          position: data.position || 'center',
          command: data.command || 'fit',
          option: data.option || 'q75',
          class: data.class || 'img-fluid',
          webp: data.webp !== false ? 'true' : 'false',
          zoomable: data.zoomable ? 'true' : 'false',
        })} >}}`,
      toPreview: ({ src = '', caption = '', alt = '' }) =>
        src
          ? `<figure style="margin:1rem 0;text-align:center">
              <img src="${src}" alt="${esc(alt || caption)}" style="max-width:100%;height:auto;border-radius:8px">
              ${caption ? `<figcaption style="margin-top:.5rem;color:#64748b;font-size:.875rem">${caption}</figcaption>` : ''}
            </figure>`
          : '',
    },
    {
      id: 'jorap-gallery',
      label: 'Gallery',
      icon: 'photo_library',
      fields: [
        { name: 'dir', label: 'Folder (under assets/)', default: 'images/gallery' },
        { name: 'class', label: 'CSS class', required: false },
        { name: 'height', label: 'Height', default: '400', required: false },
        { name: 'width', label: 'Width', default: '400', required: false },
        {
          name: 'command',
          label: 'Resize command',
          widget: 'select',
          options: ['Fit', 'fill', 'crop'],
          default: 'Fit',
          required: false,
        },
        { name: 'option', label: 'Quality option', required: false },
        { name: 'webp', label: 'WebP', widget: 'boolean', default: true, required: false },
        { name: 'zoomable', label: 'Zoomable', widget: 'boolean', default: true, required: false },
      ],
      pattern: /^\{\{<\s*gallery\s+(?<attrs>[\s\S]+?)\s*>\}\}/m,
      fromBlock: ({ groups: { attrs } = {} }) => {
        const parsed = parseAttrs(attrs);
        return {
          dir: parsed.dir || 'images/gallery',
          class: parsed.class || '',
          height: parsed.height || '400',
          width: parsed.width || '400',
          command: parsed.command || 'Fit',
          option: parsed.option || '',
          webp: parsed.webp !== 'false',
          zoomable: parsed.zoomable !== 'false',
        };
      },
      toBlock: (data) =>
        `{{< gallery ${attrsToString({
          dir: data.dir || 'images/gallery',
          class: data.class,
          height: data.height || '400',
          width: data.width || '400',
          webp: data.webp !== false ? 'true' : 'false',
          command: data.command || 'Fit',
          option: data.option,
          zoomable: data.zoomable !== false ? 'true' : 'false',
        })} >}}`,
      toPreview: ({ dir = '' }) => placeholder('Gallery', `Images from ${dir || 'images/gallery'}`),
    },
    {
      id: 'jorap-slider',
      label: 'Image slider',
      icon: 'view_carousel',
      fields: [
        { name: 'dir', label: 'Folder (under assets/)', default: 'images/gallery' },
        { name: 'class', label: 'CSS class', required: false },
        { name: 'height', label: 'Height', default: '400', required: false },
        { name: 'width', label: 'Width', default: '400', required: false },
        {
          name: 'command',
          label: 'Resize command',
          widget: 'select',
          options: ['Fit', 'fill', 'crop'],
          default: 'Fit',
          required: false,
        },
        { name: 'option', label: 'Quality option', required: false },
        { name: 'webp', label: 'WebP', widget: 'boolean', default: true, required: false },
        { name: 'zoomable', label: 'Zoomable', widget: 'boolean', default: true, required: false },
      ],
      pattern: /^\{\{<\s*slider\s+(?<attrs>[\s\S]+?)\s*>\}\}/m,
      fromBlock: ({ groups: { attrs } = {} }) => {
        const parsed = parseAttrs(attrs);
        return {
          dir: parsed.dir || 'images/gallery',
          class: parsed.class || '',
          height: parsed.height || '400',
          width: parsed.width || '400',
          command: parsed.command || 'Fit',
          option: parsed.option || '',
          webp: parsed.webp !== 'false',
          zoomable: parsed.zoomable !== 'false',
        };
      },
      toBlock: (data) =>
        `{{< slider ${attrsToString({
          dir: data.dir || 'images/gallery',
          class: data.class,
          height: data.height || '400',
          width: data.width || '400',
          webp: data.webp !== false ? 'true' : 'false',
          command: data.command || 'Fit',
          option: data.option,
          zoomable: data.zoomable !== false ? 'true' : 'false',
        })} >}}`,
      toPreview: ({ dir = '' }) => placeholder('Slider', `Slides from ${dir || 'images/gallery'}`),
    },

    // --- Typography & UI ---
    {
      id: 'jorap-notice',
      label: 'Notice',
      icon: 'campaign',
      fields: [
        {
          name: 'type',
          label: 'Type',
          widget: 'select',
          options: ['note', 'tip', 'info', 'warning', 'danger', 'success', 'question'],
          default: 'note',
        },
        { name: 'content', label: 'Content', widget: 'text' },
      ],
      pattern:
        /^\{\{<\s*notice\s+"(?<type>[^"]+)"\s*>\}\}(?<content>[\s\S]+?)\{\{<\s*\/notice\s*>\}\}/m,
      fromBlock: ({ groups: { type, content } = {} }) => ({
        type: type || 'note',
        content: (content || '').trim(),
      }),
      toBlock: ({ type = 'note', content = '' }) =>
        `{{< notice "${esc(type)}" >}}\n${content}\n{{< /notice >}}`,
      toPreview: ({ type = 'note', content = '' }) => {
        const color = noticeColors[type] || noticeColors.note;
        return `<div style="border-left:4px solid ${color};padding:.75rem 1rem;background:#f8fafc;border-radius:0 8px 8px 0">
          <strong style="display:block;text-transform:capitalize;margin-bottom:.25rem">${type}</strong>
          <div>${content.replace(/\n/g, '<br>')}</div>
        </div>`;
      },
    },
    {
      id: 'jorap-button',
      label: 'Button',
      icon: 'smart_button',
      mode: 'dialog',
      summary: '{{label}} → {{link}}',
      fields: [
        { name: 'label', label: 'Label' },
        { name: 'link', label: 'Link' },
        {
          name: 'style',
          label: 'Style',
          widget: 'select',
          options: ['solid', 'outline'],
          default: 'solid',
        },
      ],
      pattern:
        /^\{\{<\s*button\s+label="(?<label>[^"]+)"\s+link="(?<link>[^"]+)"(?:\s+style="(?<style>[^"]+)")?\s*>\}\}/m,
      toBlock: ({ label = '', link = '', style = 'solid' }) =>
        `{{< button label="${esc(label)}" link="${esc(link)}" style="${esc(style)}" >}}`,
      toPreview: ({ label = '', link = '', style = 'solid' }) => {
        const outline = style === 'outline';
        return `<a href="${link}" style="display:inline-block;padding:.5rem 1rem;border-radius:.375rem;text-decoration:none;${
          outline
            ? 'border:1px solid #2563eb;color:#2563eb;background:#fff'
            : 'background:#2563eb;color:#fff'
        }">${label || 'Button'}</a>`;
      },
    },
    {
      id: 'jorap-accordion',
      label: 'Accordion',
      icon: 'expand_more',
      fields: [
        { name: 'title', label: 'Header' },
        { name: 'content', label: 'Body', widget: 'text' },
      ],
      pattern:
        /^\{\{<\s*accordion\s+"(?<title>[^"]+)"\s*>\}\}(?<content>[\s\S]+?)\{\{<\s*\/accordion\s*>\}\}/m,
      fromBlock: ({ groups: { title, content } = {} }) => ({
        title: title || '',
        content: (content || '').trim(),
      }),
      toBlock: ({ title = '', content = '' }) =>
        `{{< accordion "${esc(title)}" >}}\n${content}\n{{< /accordion >}}`,
      toPreview: ({ title = '', content = '' }) =>
        `<details open style="border:1px solid #e2e8f0;border-radius:8px;padding:.75rem 1rem">
          <summary style="cursor:pointer;font-weight:600">${title || 'Accordion'}</summary>
          <div style="margin-top:.75rem;color:#334155">${content.replace(/\n/g, '<br>')}</div>
        </details>`,
    },
    {
      id: 'jorap-tabs',
      label: 'Tabs',
      icon: 'tab',
      fields: [
        {
          name: 'tabs',
          label: 'Tabs',
          widget: 'list',
          fields: [
            { name: 'name', label: 'Tab title' },
            { name: 'content', label: 'Content', widget: 'text' },
          ],
        },
      ],
      pattern: /^\{\{<\s*tabs\s*>\}\}(?<inner>[\s\S]+?)\{\{<\s*\/tabs\s*>\}\}/m,
      fromBlock: ({ groups: { inner } = {} }) => ({ tabs: parseTabsInner(inner) }),
      toBlock: ({ tabs = [] }) => serializeTabs(tabs),
      toPreview: ({ tabs = [] }) => {
        if (!tabs.length) return placeholder('Tabs', 'Add at least one tab');
        const labels = tabs.map((tab) => tab.name || 'Tab').join(' · ');
        return placeholder('Tabs', labels);
      },
    },
    {
      id: 'jorap-modal',
      label: 'Modal',
      icon: 'open_in_new',
      fields: [
        { name: 'btnLabel', label: 'Button label', default: 'Open' },
        { name: 'content', label: 'Modal body', widget: 'text' },
      ],
      pattern:
        /^\{\{<\s*modal\s+btn-label="(?<btnLabel>[^"]+)"\s*>\}\}(?<content>[\s\S]+?)\{\{<\s*\/modal\s*>\}\}/m,
      fromBlock: ({ groups: { btnLabel, content } = {} }) => ({
        btnLabel: btnLabel || 'Open',
        content: (content || '').trim(),
      }),
      toBlock: ({ btnLabel = 'Open', content = '' }) =>
        `{{< modal btn-label="${esc(btnLabel)}" >}}\n${content}\n{{< /modal >}}`,
      toPreview: ({ btnLabel = 'Open', content = '' }) =>
        `<div style="border:1px solid #e2e8f0;border-radius:8px;padding:1rem">
          <button type="button" style="padding:.5rem 1rem;border-radius:.375rem;border:0;background:#2563eb;color:#fff">${btnLabel}</button>
          <div style="margin-top:.75rem;color:#64748b;font-size:.875rem">${content.replace(/\n/g, '<br>')}</div>
        </div>`,
    },
    {
      id: 'jorap-toc',
      label: 'Table of contents',
      icon: 'list',
      fields: [],
      pattern: /^\{\{<\s*toc\s*>\}\}/m,
      toBlock: () => '{{< toc >}}',
      toPreview: () => placeholder('Table of contents', 'Hugo builds this from headings on publish'),
    },

    // --- Notes ---
    {
      id: 'jorap-card',
      label: 'Flashcard',
      icon: 'style',
      fields: [
        { name: 'front', label: 'Front (cue)', widget: 'text' },
        { name: 'back', label: 'Back (move)', widget: 'text' },
      ],
      pattern: /^\{\{<\s*card\s+front="(?<front>[^"]+)"\s+back="(?<back>[^"]+)"\s*>\}\}/m,
      toBlock: ({ front = '', back = '' }) =>
        `{{< card front="${esc(front)}" back="${esc(back)}" >}}`,
      toPreview: ({ front = '', back = '' }) =>
        `<div style="border:1px solid #cbd5e1;border-radius:12px;padding:1rem;background:#fff;max-width:32rem">
          <div style="font-size:.75rem;color:#64748b;margin-bottom:.5rem">Flashcard</div>
          <div style="font-weight:600;margin-bottom:.75rem">${front || 'Front'}</div>
          <div style="border-top:1px dashed #cbd5e1;padding-top:.75rem;color:#334155">${back || 'Back'}</div>
        </div>`,
    },

    // --- Diagrams & ads ---
    {
      id: 'jorap-mermaid',
      label: 'Mermaid diagram',
      icon: 'account_tree',
      fields: [{ name: 'content', label: 'Diagram source', widget: 'text' }],
      pattern: /^\{\{<\s*mermaid\s*>\}\}(?<content>[\s\S]+?)\{\{<\s*\/mermaid\s*>\}\}/m,
      fromBlock: ({ groups: { content } = {} }) => ({ content: (content || '').trim() }),
      toBlock: ({ content = '' }) => `{{< mermaid >}}\n${content}\n{{< /mermaid >}}`,
      toPreview: ({ content = '' }) =>
        `<pre style="background:#0f172a;color:#e2e8f0;padding:1rem;border-radius:8px;overflow:auto;font-size:.8125rem">${esc(content) || 'graph TD\n  A --> B'}</pre>`,
    },
    {
      id: 'jorap-adsense',
      label: 'AdSense',
      icon: 'ads_click',
      fields: [
        { name: 'slot', label: 'Ad slot ID' },
        {
          name: 'format',
          label: 'Format',
          widget: 'select',
          options: ['auto', 'rectangle', 'horizontal', 'vertical'],
          default: 'auto',
          required: false,
        },
      ],
      pattern: /^\{\{<\s*adsense\s+(?<attrs>[\s\S]+?)\s*>\}\}/m,
      fromBlock: ({ groups: { attrs } = {} }) => {
        const parsed = parseAttrs(attrs);
        return { slot: parsed.slot || '', format: parsed.format || 'auto' };
      },
      toBlock: ({ slot = '', format = 'auto' }) =>
        `{{< adsense ${attrsToString({ slot, format: format || 'auto' })} >}}`,
      toPreview: ({ slot = '' }) =>
        placeholder('AdSense', slot ? `Slot ${slot}` : 'Set ad slot ID'),
    },
  ];

  /** Id list for static/admin/config.yml editor_components — keep in sync. */
  global.JORAP_EDITOR_COMPONENT_IDS = ['code-block'].concat(
    global.JORAP_SHORTCODES.map((component) => component.id),
  );
})(window);
