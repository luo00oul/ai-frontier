'use strict';

/** Render only display content. Textareas, saved notes and code are never rewritten. */
function renderMath(root = document.getElementById('main')) {
  if (!(root instanceof Element)) return false;

  const available = typeof window.renderMathInElement === 'function';
  root.querySelectorAll('.math-status').forEach(node => {
    node.hidden = available;
  });
  if (!available) return false;

  try {
    window.renderMathInElement(root, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false }
      ],
      throwOnError: false,
      trust: false,
      output: 'htmlAndMathml',
      maxSize: 20,
      maxExpand: 1000,
      errorColor: getComputedStyle(root).getPropertyValue('--text-muted').trim() || '#59665e',
      ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option'],
      ignoredClasses: ['katex', 'katex-display', 'katex-error', 'no-math', 'note-preview', 'lab-result']
    });
    return true;
  } catch (error) {
    root.querySelectorAll('.math-status').forEach(node => { node.hidden = false; });
    console.warn('Math rendering unavailable; keeping readable source.', error);
    return false;
  }
}
window.renderMath = renderMath;

// A late CDN load can upgrade the currently visible content without changing the route.
const autoRenderScript = document.querySelector('script[data-katex-auto]');
if (autoRenderScript) {
  autoRenderScript.addEventListener('load', () => {
    renderMath(document.getElementById('main'));
    if (typeof window.updateReadingProgress === 'function') {
      requestAnimationFrame(window.updateReadingProgress);
    }
  });
}
document.addEventListener('DOMContentLoaded', () => {
  renderMath(document.getElementById('main'));
}, { once: true });
