/* Registers JORAP_SHORTCODES from jorap-shortcodes.js with Sveltia CMS. */
(function () {
  if (typeof CMS === 'undefined') {
    console.error('editor-components.js: CMS not loaded');
    return;
  }
  if (!window.JORAP_SHORTCODES) {
    console.error('editor-components.js: load jorap-shortcodes.js first');
    return;
  }

  for (const definition of window.JORAP_SHORTCODES) {
    CMS.registerEditorComponent(definition);
  }
})();
